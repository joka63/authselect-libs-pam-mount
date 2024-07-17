%global srcname authselect
# Do not terminate build if language files are empty.
%define _empty_manifest_terminate_build 0
%define debug_package %{nil}

Name:           authselect-libs-pam-mount
Version:        1.5.0
Release:        1%{?dist}
Summary:        Extends authselect profile "local" to support pam_mount
URL:            https://github.com/authselect/authselect

License:        GPL-3.0-or-later
Source0:        %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildArch: noarch

%global makedir %{_builddir}/%{name}-%{version}

# Patches
Patch0012: 0012-local-with-pam-mount-feature.patch


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

%build

cp -a profiles/local profiles/xlocal

%check

%install
install -d %{buildroot}/%{_datadir}/authselect/default/xlocal
install -D profiles/xlocal/* %{buildroot}/%{_datadir}/authselect/default/xlocal

# Find translations

# We want this file to contain only manual page translations

# Remove .la and .a files created by libtool

%files 
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
    CurProfile=$(%{_bindir/authselect} current -r | awk '{print $1}')
    CurProfileName=$(echo $CurProfile | awk '{print $1}')
    if [ "$OldProfileName" == xlocal ] ; then
        %{_bindir}/authselect disable-feature with-pam-mount -q
        OldProfile=$(%{_bindir/authselect} current -r | %__sed 's/xlocal/local/')
        %{_bindir}/authselect select $OldProfile --force --nobackup &> /dev/null
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

# If this is a new installation and local profile is current, replace it by xlocal
if [ $1 == 1 ] ; then
    OldProfile=$(%{_bindir/authselect} current -r | awk '{print $1}')
    OldProfileName=$(echo $OldProfile | awk '{print $1}')
    if [ "$OldProfileName" == local ] && ! grep -q 'pam_mount.so' %{_datadir}/pam.d/* ; then
        %{_bindir}/authselect select x$OldProfile with-pam-mount --force --nobackup &> /dev/null
    fi
    exit 0
fi

# Apply any changes to profiles (validates configuration first internally)
%{_bindir}/authselect apply-changes &> /dev/null

exit 0

%changelog
* Wed Jul 17 2024 joka63 <JoKatzer@gmx.de> 1.5.0-1
- new package built with tito

