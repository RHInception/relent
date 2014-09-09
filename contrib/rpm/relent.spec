%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%global _pkg_name relent

Name: relent
Summary: Linter for Release Engine Playbooks
Version: 0.0.1
Release: 1%{?dist}

Group: Applications/System
License: AGPLv3
Source0: %{_pkg_name}-%{version}.tar.gz
Url: https://github.com/rhinception/relent

BuildArch: noarch
BuildRequires: python2-devel
BuildRequires: python-setuptools
Requires: python-setuptools
Requires: python-argparse
Requires: python-jsonschema
# BuildRequires: python-nose
# %{?el6:BuildRequires: python-unittest2}

%description
Linter for Release Engine playbooks.


%prep
%setup -q -n %{_pkg_name}-%{version}

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --root=$RPM_BUILD_ROOT --record=relent-files.txt

%files -f relent-files.txt
%defattr(-, root, root)
%dir %{python2_sitelib}/%{_pkg_name}
%doc README.md LICENSE AUTHORS


%changelog
* Tue Sep  9 2014 Steve Milner <stevem@gnulinux.net> - 0.0.1-1
- Initial package.
