#
# Conditional build
%bcond_without	popt	#
%bcond_without	xft	#
%bcond_without	gnome	#
%bcond_without	modules	#
%bcond_without	mmx	#
%bcond_without	libinkscape

Summary:	Inkscape - a vector illustrator program for GNOME environment
Summary(pl):	Inkscape - wektorowy program graficzny dla ¶rodowiska GNOME
Name:		inkscape
Version:	0.36
Release:	1
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
%{?with_popt:BuildRequires:	popt-devel}
%{?with_xft:BuildRequires:	xft-devel}
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
%configure \
	%{!?with_popt: --without-popt}\
	%{!?with_xft: --without-xft}\
	%{!?with_gnome: --without-gnome-print}\
	%{!?with_modules: --without-modules}\
	%{?with_libinkscape: --with-libinkscape} \
	%{!?with_mmx:--disable-mmx} 

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/inkscape
%{_datadir}/inkscape
%{_mandir}/man1/*
%{_pixmapsdir}/*.png
%{_desktopdir}/*.desktop
