#
# Conditional build
%bcond_with	dbus		# DBus interface
%bcond_with	relocation	# Enable binary relocation support
#

Summary:	Scalable vector graphics editor
Summary(pl.UTF-8):	Edytor skalowalnej grafiki wektorowej
Name:		inkscape
Version:	1.0
Release:	1
License:	GPL v2+, LGPL v2.1+
Group:		X11/Applications/Graphics
# download: follow https://inkscape.org/release/
Source0:	https://media.inkscape.org/dl/resources/file/%{name}-%{version}.tar.xz
# Source0-md5:	e5f1ee6b32ac0a94bdd5d99190e7bb9e
URL:		https://inkscape.org/
BuildRequires:	GraphicsMagick-c++-devel
BuildRequires:	ImageMagick-c++-devel
BuildRequires:	aspell-devel
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.9.4-2
BuildRequires:	boost-devel >= 1.36
BuildRequires:	cairo-devel >= 1.10
BuildRequires:	cairomm-devel >= 1.9.8
%{?with_dbus:BuildRequires:	dbus-glib-devel}
BuildRequires:	freetype-devel >= 2.0
BuildRequires:	gc-devel >= 7.2
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	glib2-devel >= 1:2.28
BuildRequires:	glibmm-devel >= 2.28
BuildRequires:	gsl-devel
BuildRequires:	intltool >= 0.40.0
BuildRequires:	lcms2-devel >= 2
BuildRequires:	libcdr-devel >= 0.1
BuildRequires:	libexif-devel
BuildRequires:	libgomp-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel >= 1.2
BuildRequires:	librevenge-devel
BuildRequires:	libsigc++-devel >= 2.0.17
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libvisio-devel >= 0.1
BuildRequires:	libwpd-devel >= 0.9
BuildRequires:	libwpg-devel >= 0.3
BuildRequires:	libxml2-devel >= 1:2.6.26
BuildRequires:	libxslt-devel >= 1.1.17
BuildRequires:	pango-devel >= 1:1.24
BuildRequires:	pkgconfig
BuildRequires:	poppler-glib-devel >= 0.29.0
BuildRequires:	popt-devel
BuildRequires:	potrace-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
BuildRequires:	gdl-devel >= 3.6
BuildRequires:	gtk+3-devel >= 3.8
BuildRequires:	gtkmm3-devel >= 3.10
BuildRequires:	gtkspell3-devel >= 3.0
Requires(post,postun):	desktop-file-utils
Requires:	cairo >= 1.10
Requires:	cairomm >= 1.9.8
Requires:	gc >= 7.2
Requires:	glib2 >= 1:2.28
Requires:	glibmm >= 2.28
Requires:	libsigc++ >= 2.0.17
Requires:	libxml2 >= 1:2.6.26
Requires:	libxslt >= 1.1.17
Requires:	pango >= 1:1.24
Requires:	perl-XML-XQL
Requires:	poppler-glib >= 0.29.0
Requires:	gdl >= 3.6
Requires:	gtk+3 >= 3.8
Requires:	gtkmm3 >= 3.10
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
%setup -q -n %{name}-%{version}_2020-05-01_4035a4fb49

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+python2(\s|$),#!%{__python}\1,' -e '1s,#!\s*/usr/bin/env\s+python(\s|$),#!%{__python}\1,' -e '1s,#!\s*/usr/bin/python(\s|$),#!%{__python}\1,' \
      CMakeScripts/cmake_consistency_check.py \
      buildtools/msys2checkdeps.py \
      packaging/scripts/lp-mark-bugs-released \
      packaging/wix/*.py \
      share/extensions/*.py \
      share/extensions/*/*.py \
      share/*/i18n.py

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+perl(\s|$),#!%{__perl}\1,' \
      share/attributes/genMapDataCSS.pl \
      share/attributes/genMapDataSVG.pl

%build
mkdir -p build
cd build

%cmake ../ \
	-DBUILD_SHARED_LIBS:BOOL=OFF \
	%{cmake_on_off relocation ENABLE_BINRELOC} \
	%{cmake_on_off dbus WITH_DBUS}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# unify locale name, overwrite outdated bn
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{bn_BD,bn}/LC_MESSAGES/inkscape.mo
# unify names
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{ks@aran,ks}
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{ks@deva,ks@devanagari}
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{sd@deva,sd@devanagari}
# unsupported variants
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{kok@latin,mni@beng,sat@deva}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post

%postun
%update_desktop_database_postun

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS CONTRIBUTING.md NEWS.md README.md
%attr(755,root,root) %{_bindir}/inkscape
%attr(755,root,root) %{_bindir}/inkview
%dir %{_datadir}/inkscape
%{_datadir}/inkscape/[!e]*
%{_datadir}/inkscape/examples
%dir %{_datadir}/inkscape/extensions
%{_datadir}/inkscape/extensions/Poly3DObjects
%{_datadir}/inkscape/extensions/alphabet_soup
%{_datadir}/inkscape/extensions/barcode
%{_datadir}/inkscape/extensions/ink2canvas_lib
%{_datadir}/inkscape/extensions/inkex
%{_datadir}/inkscape/extensions/svg_fonts
%{_datadir}/inkscape/extensions/tools
%{_datadir}/inkscape/extensions/xaml2svg
%attr(755,root,root) %{_datadir}/inkscape/extensions/*.py
%attr(755,root,root) %{_datadir}/inkscape/extensions/*.sh
%{_datadir}/inkscape/extensions/*.inx
%{_datadir}/inkscape/extensions/*.js
%{_datadir}/inkscape/extensions/*.svg
%{_datadir}/inkscape/extensions/*.xml
%{_datadir}/inkscape/extensions/*.xsl
%{_datadir}/inkscape/extensions/*.xslt
%{_datadir}/inkscape/extensions/fontfix.conf
%{_datadir}/inkscape/extensions/setup.cfg
%{_datadir}/inkscape/extensions/inkscape.extension.rng
%{_datadir}/metainfo/org.inkscape.Inkscape.appdata.xml
%{_iconsdir}/hicolor/*/apps/org.inkscape.Inkscape.png
%{_desktopdir}/org.inkscape.Inkscape.desktop
%{_mandir}/man1/inkscape.1*
%{_mandir}/man1/inkview.1*
%lang(de) %{_mandir}/de/man1/inkscape.1*
%lang(fr) %{_mandir}/fr/man1/inkscape.1*
%lang(hr) %{_mandir}/hr/man1/inkscape.1*
%lang(hu) %{_mandir}/hu/man1/inkscape.1*
%lang(de) %{_mandir}/de/man1/inkview.1*
%lang(es) %{_mandir}/es/man1/inkview.1*
%lang(fr) %{_mandir}/fr/man1/inkview.1*
%lang(hr) %{_mandir}/hr/man1/inkview.1*
%lang(hu) %{_mandir}/hu/man1/inkview.1*
%lang(pt_BR) %{_mandir}/pt_BR/man1/inkview.1*
