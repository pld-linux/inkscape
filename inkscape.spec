Summary:	Inkscape - a vector illustrator program for GNOME environment
Summary(pl):	Inkscape - wektorowy program graficzny dla ¶rodowiska GNOME
Name:		inkscape
Version:	0.36
Release:	0.1
License:	GPL
Group:		Graphics
Source0:	http://dl.sourceforge.net/inkscape/%{name}-%{version}.tar.gz
# Source0-md5:	3bd8581afee27b00dd7fdce0e7d8f6fa
URL:		http://www.inkscape.org/
BuildRequires:	freetype-devel >= 2.0
BuildRequires:	gtk+-devel >= 2.0.0
BuildRequires:	libart_lgpl-devel >= 2.3.10
BuildRequires:	libgnomeprintui-devel >= 2.2
BuildRequires:	libpng-devel
BuildRequires:	libxml2-devel >= 2.4.24
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	xft-devel
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Inkscape is (or at least should be) a vector illustrator program for
the GNOME environment. It is currently in active development and
approaching general usability.

%description -l pl
Inkscape jest (a przynajmniej powinien byæ) wektorowym programem
graficznym dla ¶rodowiska GNOME. Aktualnie jest aktywnie rozwijany i
osi±ga ogóln± u¿ywalno¶æ.

%prep
%setup -q

%build
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc
