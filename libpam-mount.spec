%global srcname authselect
# Do not terminate build if language files are empty.
%define _empty_manifest_terminate_build 0

Name:           libpam-mount
Version:        1.5.0
Release:        0%{?dist}
Summary:        Extends authselect profile "local" to support pam_mount
URL:            https://github.com/authselect/authselect

License:        GPL-3.0-or-later
Source0:        %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz

%global makedir %{_builddir}/%{name}-%{version}

# Set the default profile
%{?fedora:%global default_profile xlocal with-silent-lastlog with-pam-mount}

# Patches
Requires: authselect-libs
Requires: pam_mount

%description
Wrapper for pam_mount: extends current authselect profile "local"
to include pam_mount.so support for PAM. 

%prep
%setup -q -n %{srcname}-%{version}

for p in %patches ; do
    %__patch -p1 -i $p
done

cp -a profiles/local profiles/xlocal

%build

%check

%install
install -d %{buildroot}/%{_datadir}/authselect/vendor/xlocal
install -D profiles/xlocal/* %{buildroot}/%{_datadir}/authselect/vendor/xlocal

# Find translations

# We want this file to contain only manual page translations

# Remove .la and .a files created by libtool

%files 
%dir %{_datadir}/authselect/vendor
%dir %{_datadir}/authselect/vendor/xlocal/
%{_datadir}/authselect/vendor/xlocal/dconf-db
%{_datadir}/authselect/vendor/xlocal/dconf-locks
%{_datadir}/authselect/vendor/xlocal/fingerprint-auth
%{_datadir}/authselect/vendor/xlocal/nsswitch.conf
%{_datadir}/authselect/vendor/xlocal/password-auth
%{_datadir}/authselect/vendor/xlocal/postlogin
%{_datadir}/authselect/vendor/xlocal/README
%{_datadir}/authselect/vendor/xlocal/REQUIREMENTS
%{_datadir}/authselect/vendor/xlocal/smartcard-auth
%{_datadir}/authselect/vendor/xlocal/system-auth
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
