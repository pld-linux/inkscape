Summary:	Inkscape -
Summary(pl):	Inkscape -
Name:		inkscape
Version:	0.36
Release:	0.1
License:	GPL
Group:		Graphics
Source0:	http://dl.sourceforge.net/inkscape/%{name}-%{version}.tar.gz
#Source0-md5:	3bd8581afee27b00dd7fdce0e7d8f6fa
#BuildRequires:
#Requires:
URL:		http://www.inkscape.org/
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
- -- empty --

%description -l pl
- -- pusty --

%prep
%setup -q

#%patch

%build
./configure --prefix=%{_prefix}
%{__make} RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} prefix=$RPM_BUILD_ROOT%{_prefix} install

%post
%postun

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc
