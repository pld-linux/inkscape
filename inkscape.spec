#
# Conditional build
%bcond_without	xft		# Don't use xft scalable font database
%bcond_without	gnome_print	# Don't use gnome print font database and spooler frontend
%bcond_without	mmx		# Force building without MMX optimazation (Default: auto-detect)
%bcond_with	relocation	# Enable binary relocation support
#
Summary:	Scalable vector graphics editor
Summary(pl):	Edytor skalowalnej grafiki wektorowej
Name:		inkscape
Version:	0.42.2
Release:	1
License:	GPL v2, LGPL v2.1
Group:		Applications/Graphics
Source0:	http://dl.sourceforge.net/inkscape/%{name}-%{version}.tar.bz2
# Source0-md5:	a27172087018e850e92e97e52b5dad08
URL:		http://www.inkscape.org/
BuildRequires:	autoconf >= 2.59-3
BuildRequires:	automake >= 1:1.9.4-2
BuildRequires:	freetype-devel >= 2.0
BuildRequires:	gc-devel >= 6.4
BuildRequires:	gcc-c++ >= 3.0
BuildRequires:	gtk+2-devel >= 2:2.4.0
BuildRequires:	gtkmm-devel >= 2.4
BuildRequires:	gtkspell-devel >= 2.0
BuildRequires:	intltool >= 0.22
BuildRequires:	libart_lgpl-devel >= 2.3.10
%{?with_gnome_print:BuildRequires:	libgnomeprintui-devel >= 1.116.0}
BuildRequires:	libpng-devel >= 1.2
BuildRequires:	libsigc++-devel >= 2.0.3
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 2.6.0
BuildRequires:	libxslt-devel >= 1.0.15
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
%{?with_xft:BuildRequires:	xft-devel}
BuildRequires:	zlib-devel
Requires(post,postun):	shared-mime-info
Requires:	gc >= 6.4
Requires:	gtk+2 >= 2:2.4.0
Requires:	perl-XML-XQL
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Inkscape is a program for viewing, making, and editing two-dimensional
vector drawings.

%description -l pl
Inkscape jest programem do przegl±dania, tworzenia i edycji
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
	%{!?with_mmx:--disable-mmx} \
	%{?with_relocation:--enable-binreloc} \
	--disable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
update-mime-database %{_datadir}/mime >/dev/null 2>&1 ||:
[ ! -x /usr/bin/update-desktop-database ] || /usr/bin/update-desktop-database >/dev/null 2>&1 ||:

%postun
umask 022
update-mime-database %{_datadir}/mime >/dev/null 2>&1
[ ! -x /usr/bin/update-desktop-database ] || /usr/bin/update-desktop-database >/dev/null 2>&1

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/inkscape
%{_datadir}/inkscape/[!e]*
%{_datadir}/inkscape/examples
%dir %{_datadir}/inkscape/extensions
%{_datadir}/inkscape/extensions/*.inx
%attr(755,root,root) %{_datadir}/inkscape/extensions/*.pl
%attr(755,root,root) %{_datadir}/inkscape/extensions/*.pm
%attr(755,root,root) %{_datadir}/inkscape/extensions/*.py
%attr(755,root,root) %{_datadir}/inkscape/extensions/*.sh
%attr(755,root,root) %{_datadir}/inkscape/extensions/svg_dropshadow
%{_mandir}/man1/*
%lang(fr) %{_mandir}/fr/man1/*
%{_pixmapsdir}/*.png
%{_desktopdir}/*.desktop
