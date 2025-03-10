# TODO:
# Split examplest to separate module
#
# Conditional build:
%bcond_with	doc		# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	nagiosplugin
Summary:	Python class library which helps writing Nagios (or Icinga) compatible plugins easily in Python
Summary(pl.UTF-8):	Biblioteka klas Pythona pomagająca łatwo pisać wtyczki dla Nagiosa (lub Icingi) w Pythonie
Name:		python-%{module}
Version:	1.3.3
Release:	2
License:	ZPL 2.1
Group:		Libraries/Python
Source0:	https://pypi.debian.net/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	7539bf58002fb1285706d91e94dd4e26
URL:		nagiosplugin
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:  python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:  python3-pytest
%endif
%endif
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
nagiosplugin is a Python class library which helps writing Nagios (or
Icinga) compatible plugins easily in Python. It cares for much of the
boilerplate code and default logic commonly found in Nagios checks

%description -l pl.UTF-8
nagiosplugin jest biblioteką klas Pythona pomagającą łatwo pisać
wtyczki dla Nagiosa (lub Icingi) w Pythonie. Dostarcza większość
typowego kodu i domyślna logikę zawartą w testach Nagiosa.

%package -n python3-%{module}
Summary:	Python class library which helps writing Nagios (or Icinga) compatible plugins easily in Python
Summary(pl.UTF-8):	Biblioteka klas Pythona pomagająca łatwo pisać wtyczki dla Nagiosa (lub Icingi) w Pythonie
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
nagiosplugin is a Python class library which helps writing Nagios (or
Icinga) compatible plugins easily in Python. It cares for much of the
boilerplate code and default logic commonly found in Nagios checks

%description -n python3-%{module} -l pl.UTF-8
nagiosplugin jest biblioteką klas Pythona pomagającą łatwo pisać
wtyczki dla Nagiosa (lub Icingi) w Pythonie. Dostarcza większość
typowego kodu i domyślna logikę zawartą w testach Nagiosa.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}

install -d examples
cp -p nagiosplugin/examples/check_*.py examples

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/%{module}/examples
%py_postclean

install -d $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/%{module}/examples

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc HACKING.txt CONTRIBUTORS.txt HISTORY.txt README.txt
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%{_examplesdir}/python-%{module}-%{version}
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc HACKING.txt CONTRIBUTORS.txt HISTORY.txt README.txt
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%{_examplesdir}/python3-%{module}-%{version}
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
