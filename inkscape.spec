#
# TODO: check why build requires libselinux-devel (because of some gnome* stuff)
#
# Conditional build
%bcond_without	xft		# Don't use xft scalable font database
%bcond_without	gnomeprint	# Don't use gnome print font database and spooler frontend
%bcond_without	gnomevfs	# Don't use gnome vfs for loading files
%bcond_without	mmx		# Force building without MMX optimazation (Default: auto-detect)
%bcond_with	inkboard	# Enable inkboard support
%bcond_with	relocation	# Enable binary relocation support
#
Summary:	Scalable vector graphics editor
Summary(pl.UTF-8):	Edytor skalowalnej grafiki wektorowej
Name:		inkscape
Version:	0.46
Release:	1
License:	GPL v2, LGPL v2.1
Group:		Applications/Graphics
Source0:	http://dl.sourceforge.net/inkscape/%{name}-%{version}.tar.gz
# Source0-md5:	3bae9034047379012127e52f9b138d32
Patch1:		%{name}-desktop.patch
URL:		http://www.inkscape.org/
BuildRequires:	autoconf >= 2.59-3
BuildRequires:	automake >= 1:1.9.4-2
BuildRequires:	boost-any-devel
BuildRequires:	boost-bind-devel
BuildRequires:	freetype-devel >= 2.0
BuildRequires:	gcc-c++ >= 6:4.2.2-2
BuildRequires:	gc-devel >= 6.4
BuildRequires:	gettext-devel
%{?with_gnomevfs:BuildRequires:	gnome-vfs2-devel >= 2.15.2}
BuildRequires:	gtk+2-devel >= 2:2.9.4
BuildRequires:	gtkmm-devel >= 2.4
BuildRequires:	gtkspell-devel >= 2.0.11
BuildRequires:	intltool >= 0.35.0
BuildRequires:	lcms-devel >= 1.15
BuildRequires:	libart_lgpl-devel >= 2.3.10
%{?with_gnomeprint:BuildRequires:	libgnomeprintui-devel >= 2.12.1}
BuildRequires:	libpng-devel >= 1.2
BuildRequires:	libsigc++-devel >= 2.0.17
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6.26
BuildRequires:	libxslt-devel >= 1.1.17
%{?with_inkboard:BuildRequires:	loudmouth-devel >= 1.0.3}
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	rpm-pythonprov
%{?with_xft:BuildRequires:	xorg-lib-libXft-devel}
BuildRequires:	zlib-devel
Requires(post,postun):	shared-mime-info
Requires:	gc >= 6.4
%{?with_gnomevfs:Requires:	gnome-vfs2 >= 2.15.2}
Requires:	gtk+2 >= 2:2.9.4
Requires:	perl-XML-XQL
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Inkscape is a program for viewing, making, and editing two-dimensional
vector drawings.

%description -l pl.UTF-8
Inkscape jest programem do przeglądania, tworzenia i edycji
dwuwymiarowej grafiki wektorowej.

%prep
%setup -q
%patch1 -p1
rm -f po/en_US@piglatin.po
sed -i -e 's|en_US@piglatin||' configure.ac

%build
%{__libtoolize}
%{__glib_gettextize}
%{__intltoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	%{!?with_xft: --without-xft} \
	%{!?with_gnomeprint:--without-gnome-print} \
	%{?with_gnomeprint:--with-gnome-print} \
	%{!?with_gnomevfs:--without-gnome-vfs} \
	%{!?with_mmx:--disable-mmx} \
	%{?with_relocation:--enable-binreloc} \
	%{?with_inkboard:--enable-inkboard} \
	--disable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

[ -d $RPM_BUILD_ROOT%{_datadir}/locale/sr@latin ] || \
	mv -f $RPM_BUILD_ROOT%{_datadir}/locale/sr@{Latn,latin}
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
%doc AUTHORS ChangeLog HACKING.txt NEWS README TRANSLATORS
%lang(ca) %doc README.ca.txt
%lang(de) %doc README.de.txt
%lang(es) %doc README.es.txt
%lang(fr) %doc README.fr.txt
%lang(it) %doc README.it.txt
%lang(de) %doc HACKING.de.txt
%lang(fr) %doc HACKING.fr.txt
%lang(it) %doc HACKING.it.txt
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/inkscape
%{_datadir}/inkscape/[!e]*
%{_datadir}/inkscape/examples
%dir %{_datadir}/inkscape/extensions
%{_datadir}/inkscape/extensions/*.cmd
%{_datadir}/inkscape/extensions/*.inx
%{_datadir}/inkscape/extensions/*.txt
%{_datadir}/inkscape/extensions/*.xml
%{_datadir}/inkscape/extensions/*.xsl
%{_datadir}/inkscape/extensions/*.xslt
%attr(755,root,root) %{_datadir}/inkscape/extensions/*.pl
%attr(755,root,root) %{_datadir}/inkscape/extensions/*.pm
%attr(755,root,root) %{_datadir}/inkscape/extensions/*.py
%attr(755,root,root) %{_datadir}/inkscape/extensions/*.rb
%attr(755,root,root) %{_datadir}/inkscape/extensions/*.sh
%dir %{_datadir}/inkscape/extensions/Barcode
%attr(755,root,root) %{_datadir}/inkscape/extensions/Barcode/*.py
%dir %{_datadir}/inkscape/extensions/xaml2svg
%{_datadir}/inkscape/extensions/xaml2svg/*.xsl
%{_mandir}/man1/*
%lang(fr) %{_mandir}/fr/man1/*
%{_pixmapsdir}/*.png
%{_desktopdir}/*.desktop
