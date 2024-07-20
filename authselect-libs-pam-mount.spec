%global srcname authselect-libs-pam-mount

Name:           authselect-libs-pam-mount
Version:        1.5.0
Release:        3%{?dist}
Summary:        Provides extended local authselect profile to support pam_mount
Url:            https://github.com/joka63/%{srcname}
Source0:        %{name}-%{version}-%{release}.tar.gz
License:        GPL-3.0-or-later

BuildArch: noarch

%global makedir %{_builddir}/%{name}-%{version}-%{release}


Requires: authselect-libs >= 1.5.0
Requires: pam_mount

%description
Wrapper for pam_mount: 
proivdes an extended version "xlocal" of authselect standard profile "local"
to include pam_mount.so support for PAM. 

%prep
%setup -q -n %{srcname}-%{version}-%{release}

%build

%check

%install
install -d %{buildroot}/%{_datadir}/%{srcname}/default/xlocal
install -D profiles/xlocal/* %{buildroot}/%{_datadir}/%{srcname}/default/xlocal


%files
%dir %{_datadir}/%{srcname}/default
%dir %{_datadir}/%{srcname}/default/xlocal/
%{_datadir}/%{srcname}/default/xlocal/README
%{_datadir}/%{srcname}/default/xlocal/REQUIREMENTS
%{_datadir}/%{srcname}/default/xlocal/password-auth
%license COPYING
%doc README.md

%preun
if [ $1 == 0 ] ; then
    # Switch back to standard local profile, if profile xlocal is still selected.
    CurProfileName=$(%{_bindir/authselect} current -r | awk '{print $1}')
    if [ "$CurProfileName" == xlocal ] ; then
        %{_bindir}/authselect disable-feature with-pam-mount -q
        OldProfile=$(%{_bindir/authselect} current -r | %__sed 's/xlocal/local/')
        %{_bindir}/authselect select $OldProfile --force --nobackup &> /dev/null
    fi
fi

%posttrans
# If this is a new installation, create xlocal profile from local profile
if [ $1 == 1 ] ; then
    %{_bindir}/authselect create-profile xlocal --vendor --base-on local --symlink-dconf --symlink-nsswitch -s=system-auth -s=postlogin  &> /dev/null
    %{_bindir}/cp -a %{_datadir}/%{srcname}/default/xlocal/* %{_datadir}/authselect/vendor/xlocal
    exit 0
fi

# Apply any changes to xlocal profile,
CurProfileName=$(echo $CurProfile | awk '{print $1}')
if [ "$CurProfileName" == xlocal ] ; then
  %{_bindir}/authselect apply-changes &> /dev/null
fi

exit 0

%changelog
* Sat Jul 20 2024 joka63 <JoKatzer@gmx.de> 1.5.0-3
- Initial commit: provide new vendor profile "xlocal" with pam_mount support

* Thu Jul 18 2024 joka63 <JoKatzer@gmx.de> 1.5.0-2
- fix: wrong vendor profile on rpm-ostree systems (JoKatzer@gmx.de)

* Wed Jul 17 2024 joka63 <JoKatzer@gmx.de> 1.5.0-1
- new package built with tito

