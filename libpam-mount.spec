# Do not terminate build if language files are empty.
%define _empty_manifest_terminate_build 0

Name:           libpam-mount
Version:        1.5.0
Release:        0%{?dist}
Summary:        Extends authselect profile "local" to support pam_mount
URL:            https://github.com/authselect/authselect

License:        GPL-3.0-or-later
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

%global makedir %{_builddir}/%{name}-%{version}

# Disable NIS profile on RHEL
%if 0%{?rhel}
%global with_nis_profile 0
%else
%global with_nis_profile 1
%endif

# Set the default profile
%{?fedora:%global default_profile xlocal with-silent-lastlog with-pam-mount}

# Patches
Requires: authselect-libs
Requires: pam_mount

%description
Wrapper for pam_mount: extends current authselect profile "local"
to include pam_mount.so support for PAM. 

%prep
%setup -q

for p in %patches ; do
    %__patch -p1 -i $p
done

%build

%make_build

%check
%make_build check

%install
%make_install

# Find translations

# We want this file to contain only manual page translations

# Remove .la and .a files created by libtool

%files 
%dir %{_sysconfdir}/authselect
%dir %{_localstatedir}/lib/authselect
%ghost %attr(0755,root,root) %{_localstatedir}/lib/authselect/backups/
%dir %{_datadir}/authselect
%dir %{_datadir}/authselect/vendor
%dir %{_datadir}/authselect/default
%dir %{_datadir}/authselect/default/xlocal/
%{_datadir}/authselect/default/xlocal/dconf-db
%{_datadir}/authselect/default/xlocal/dconf-locks
%{_datadir}/authselect/default/xlocal/fingerprint-auth
%{_datadir}/authselect/default/xlocal/nsswitch.conf
%{_datadir}/authselect/default/xlocal/password-auth
%{_datadir}/authselect/default/xlocal/postlogin
%{_datadir}/authselect/default/xlocal/README
%{_datadir}/authselect/default/xlocal/REQUIREMENTS
%{_datadir}/authselect/default/xlocal/smartcard-auth
%{_datadir}/authselect/default/xlocal/system-auth
%license COPYING
%doc README.md

%preun
if [ $1 == 0 ] ; then
    # Switch back to standard local profile, if profile xlocal is still selected.
    if [ $(%{_bindir/authselect} current -r | awk '{print $1}') == xlocal ] ; then
        %{_bindir}/authselect local
    fi
fi

%posttrans 
# Keep nss-altfiles for all rpm-ostree based systems.
# See https://github.com/authselect/authselect/issues/48
if test -e /run/ostree-booted; then
    for PROFILE in `ls %{_datadir}/authselect/default/xlocal`; do
        %{_bindir}/authselect create-profile $PROFILE --vendor --base-on $PROFILE --symlink-pam --symlink-dconf --symlink=REQUIREMENTS --symlink=README &> /dev/null
        %__sed -i -e 's/{if "with-altfiles":\([^}]\+\)}/\1/g' %{_datadir}/authselect/vendor/$PROFILE/nsswitch.conf &> /dev/null
    done
fi

# If this is a new installation select the default configuration.
if [ $1 == 1 ] ; then
    if [ $(%{_bindir/authselect} current -r | awk '{print $1}') == local ] ; then
      %{_bindir}/authselect select %{default_profile} --force --nobackup &> /dev/null
    exit 0
fi

# Minimal profile was removed. Switch to local during upgrade.
%__sed -i '1 s/^local$/xlocal/'  %{_sysconfdir}/authselect/authselect.conf

# Apply any changes to profiles (validates configuration first internally)
%{_bindir}/authselect apply-changes &> /dev/null

exit 0

%changelog
