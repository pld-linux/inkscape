#
# TODO: check why build requires libselinux-devel (because of some gnome* stuff)
#
# Conditional build
%bcond_without	xft		# Don't use xft scalable font database
%bcond_without	gnomevfs	# Don't use gnome vfs for loading files
%bcond_without	mmx		# Force building without MMX optimazation (Default: auto-detect)
%bcond_with	inkboard	# Enable inkboard support
%bcond_with	relocation	# Enable binary relocation support
#

# just set it nil when non-preview arrives
%define beta %{nil}

Summary:	Scalable vector graphics editor
Summary(pl.UTF-8):	Edytor skalowalnej grafiki wektorowej
Name:		inkscape
Version:	0.48.0
Release:	8
License:	GPL v2+, LGPL v2.1+
Group:		X11/Applications/Graphics
Source0:	http://downloads.sourceforge.net/inkscape/%{name}-%{version}%{beta}.tar.bz2
# Source0-md5:	fd8b17a3f06668603807176a77167bb9
# workaround for https://bugs.launchpad.net/inkscape/+bug/487038
Patch0:		%{name}-ldl.patch
URL:		http://www.inkscape.org/
BuildRequires:	ImageMagick-c++-devel
BuildRequires:	aspell-devel
BuildRequires:	autoconf >= 2.59-3
BuildRequires:	automake >= 1:1.9.4-2
BuildRequires:	boost-devel >= 1.35.0
BuildRequires:	cairo-devel >= 1.8.0
BuildRequires:	freetype-devel >= 2.0
BuildRequires:	gc-devel >= 6.4
BuildRequires:	gettext-devel
BuildRequires:	glibmm-devel >= 2.16.0
%{?with_gnomevfs:BuildRequires:	gnome-vfs2-devel >= 2.15.2}
BuildRequires:	gsl-devel
BuildRequires:	gtk+2-devel >= 2:2.14.0
BuildRequires:	gtkmm-devel >= 2.10.0
BuildRequires:	gtkspell-devel >= 2.0.11
BuildRequires:	intltool >= 0.35.0
BuildRequires:	lcms-devel >= 1.15
BuildRequires:	libpng-devel >= 1.2
BuildRequires:	libsigc++-devel >= 2.0.17
BuildRequires:	libstdc++-devel >= 6:4.2.2-2
BuildRequires:	libtool
BuildRequires:	libwpg-devel
BuildRequires:	libxml2-devel >= 1:2.6.26
BuildRequires:	libxslt-devel >= 1.1.17
%{?with_inkboard:BuildRequires:	loudmouth-devel >= 1.0.3}
BuildRequires:	pkgconfig
BuildRequires:	poppler-glib-devel >= 0.12.2
BuildRequires:	popt-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	sed >= 4.0
%{?with_xft:BuildRequires:	xorg-lib-libXft-devel}
BuildRequires:	zlib-devel
Requires(post,postun):	desktop-file-utils
Requires:	gc >= 6.4
%{?with_gnomevfs:Requires:	gnome-vfs2 >= 2.15.2}
Requires:	gtk+2 >= 2:2.14.0
Requires:	perl-XML-XQL
Suggests:	python-lxml
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
%setup -q -n %{name}-%{version}%{beta}
%patch0 -p1

rm -f po/en_US@piglatin.po
%{__sed} -i -e 's|en_US@piglatin||' configure.ac

mv po/te_IN.po po/te.po
%{__sed} -i -e 's|te_IN|te|' configure.ac

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
	%{!?with_gnomevfs:--without-gnome-vfs} \
	%{!?with_mmx:--disable-mmx} \
	%{?with_relocation:--enable-binreloc} \
	%{?with_inkboard:--enable-inkboard}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT


%post
%update_desktop_database_post

%postun
%update_desktop_database_postun

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TRANSLATORS doc/HACKING.txt
%lang(ca) %doc README.ca.txt
%lang(de) %doc README.de.txt
%lang(es) %doc README.es.txt
%lang(fr) %doc README.fr.txt
%lang(it) %doc README.it.txt
%lang(de) %doc doc/HACKING.de.txt
%lang(fr) %doc doc/HACKING.fr.txt
%lang(it) %doc doc/HACKING.it.txt
%attr(755,root,root) %{_bindir}/inkscape
%attr(755,root,root) %{_bindir}/inkview
%dir %{_datadir}/inkscape
%{_datadir}/inkscape/[!e]*
%{_datadir}/inkscape/examples
%dir %{_datadir}/inkscape/extensions
%{_datadir}/inkscape/extensions/Poly3DObjects/
%{_datadir}/inkscape/extensions/alphabet_soup/
%{_datadir}/inkscape/extensions/*.inx
%{_datadir}/inkscape/extensions/*.js
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
%{_mandir}/man1/*.1*
%lang(fr) %{_mandir}/fr/man1/*.1*
%{_iconsdir}/hicolor/*/apps/inkscape.png
%{_desktopdir}/inkscape.desktop
