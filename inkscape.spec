#
# Conditional build
%bcond_without	xft		# Don't use xft scalable font database
%bcond_without	gnome_print	# Don't use gnome print font database and spooler frontend
%bcond_without	mmx		# Force building without MMX optimazation (Default: auto-detect)
#
Summary:	Scalable vector graphics editor
Summary(pl):	Edytor skalowalnej grafiki wektorowej
Name:		inkscape
Version:	0.40
Release:	0.01
License:	GPL
Group:		Applications/Graphics
Source0:	http://dl.sourceforge.net/inkscape/%{name}-%{version}.tar.bz2
# Source0-md5:	5f53659eb47efce8593e39d30ebb1c77
URL:		http://www.inkscape.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	freetype-devel >= 2.0
BuildRequires:	gtk+2-devel >= 2:2.4.0
BuildRequires:	gtkmm-devel >= 2.4
BuildRequires:	gtkspell-devel
BuildRequires:	intltool
BuildRequires:	libart_lgpl-devel >= 2.3.10
%{?with_gnome_print:BuildRequires:	libgnomeprintui-devel >= 1.116.0}
BuildRequires:	libpng-devel
BuildRequires:	libsigc++-devel >= 2.0 
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.4.24
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
%{?with_xft:BuildRequires:	xft-devel}
Requires:	perl-XML-XQL
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Inkscape is a program for viewing, making, and editing two-dimensional
vector drawings.

%description -l pl
Inkscape jest programem do przeglądania, tworzenia i edycji
dwuwymiarowej grafiki wektorowej.

%prep
%setup -q

%build
cp -f /usr/share/automake/mkinstalldirs .
%{__libtoolize}
glib-gettextize --copy --force
intltoolize --copy --force --automake
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	%{!?with_xft: --without-xft}\
	%{!?with_gnome_print: --without-gnome-print}\
	%{?with_gnome_print: --with-gnome-print}\
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
%{_datadir}/inkscape
%{_mandir}/man1/*
%{_pixmapsdir}/*.png
%{_desktopdir}/*.desktop
