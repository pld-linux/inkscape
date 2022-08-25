#
# Conditional build
%bcond_with	dbus		# DBus interface
%bcond_with	relocation	# Enable binary relocation support
%bcond_with	imagick		# ImageMagick 6.x instead of GraphicsMagick
#

Summary:	Scalable vector graphics editor
Summary(pl.UTF-8):	Edytor skalowalnej grafiki wektorowej
Name:		inkscape
Version:	1.2
Release:	1
License:	GPL v2+, LGPL v2.1+
Group:		X11/Applications/Graphics
# download: follow https://inkscape.org/release/
Source0:	https://media.inkscape.org/dl/resources/file/%{name}-%{version}.tar.xz
# Source0-md5:	fb40ac4635b9ea5608e1706584cd0665
URL:		https://inkscape.org/
%{!?with_imagick:BuildRequires:	GraphicsMagick-c++-devel}
%{?with_imagick:BuildRequires:	ImageMagick6-c++-devel < 7}
BuildRequires:	aspell-devel
BuildRequires:	boost-devel >= 1.36
BuildRequires:	cairo-devel >= 1.10
BuildRequires:	cairomm-devel >= 1.9.8
BuildRequires:	cmake >= 3.1.0
%if %{with dbus}
BuildRequires:	dbus-devel
BuildRequires:	dbus-glib-devel
%endif
BuildRequires:	double-conversion-devel
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel >= 2.0
BuildRequires:	gc-devel >= 7.2
BuildRequires:	gdl-devel >= 3.6
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	glib2-devel >= 1:2.28
BuildRequires:	glibmm-devel >= 2.28
BuildRequires:	gsl-devel
BuildRequires:	gspell-devel >= 1.0
BuildRequires:	gtk+3-devel >= 3.22
BuildRequires:	gtkmm3-devel >= 3.22
BuildRequires:	harfbuzz-devel
BuildRequires:	lcms2-devel >= 2
BuildRequires:	lib2geom-devel >= 1.1
BuildRequires:	libcdr-devel >= 0.1
BuildRequires:	libexif-devel
BuildRequires:	libgomp-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel >= 1.2
BuildRequires:	librevenge-devel
BuildRequires:	libsigc++-devel >= 2.0.17
BuildRequires:	libsoup-devel >= 2.42
BuildRequires:	libstdc++-devel >= 6:4.7
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
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	zlib-devel
Requires(post,postun):	desktop-file-utils
Requires:	cairo >= 1.10
Requires:	cairomm >= 1.9.8
Requires:	gc >= 7.2
Requires:	gdl >= 3.6
Requires:	glib2 >= 1:2.28
Requires:	glibmm >= 2.28
Requires:	gtk+3 >= 3.22
Requires:	gtkmm3 >= 3.22
Requires:	libsigc++ >= 2.0.17
Requires:	libxml2 >= 1:2.6.26
Requires:	libxslt >= 1.1.17
Requires:	pango >= 1:1.24
Requires:	perl-XML-XQL
Requires:	poppler-glib >= 0.29.0
Suggests:	python-lxml
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Inkscape is a program for viewing, making, and editing two-dimensional
vector drawings.

%description -l pl.UTF-8
Inkscape jest programem do przeglądania, tworzenia i edycji
dwuwymiarowej grafiki wektorowej.

%package -n bash-completion-inkscape
Summary:	Bash completion for inkscape arguments
Summary(pl.UTF-8):	Bashowe dopełnianie argumentów programu inkscape
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
BuildArch:	noarch

%description -n bash-completion-inkscape
Bash completion for inkscape arguments.

%description -n bash-completion-inkscape -l pl.UTF-8
Bashowe dopełnianie argumentów programu inkscape.

%prep
%setup -q -n %{name}-%{version}_2022-05-15_dc2aedaf03

# python3-only
%{__sed} -i -e '1s,/usr/bin/env python3,%{__python3},' \
	CMakeScripts/cmake_consistency_check.py \
	buildtools/check_license_headers.py \
	share/extensions/*.py \
	share/extensions/tests/add_pylint.py \
	share/*/i18n.py

# look python2/3 compatible
%{__sed} -i -e '1s,/usr/bin/env python$,%{__python3},' \
	buildtools/msys2checkdeps.py \
	share/extensions/*.py \
	share/extensions/inkex/tester/inx.py \
	share/extensions/tests/test_*.py \

# python2-only
%{__sed} -i -e '1s,/usr/bin/python$,%{__python},' \
	packaging/scripts/lp-mark-bugs-released

%{__sed} -i -e '1s,/usr/bin/env perl$,%{__perl},' \
	share/attributes/genMapDataCSS.pl \
	share/attributes/genMapDataSVG.pl

%build
mkdir -p build
cd build

%cmake .. \
	-DBUILD_SHARED_LIBS:BOOL=OFF \
	%{cmake_on_off relocation ENABLE_BINRELOC} \
	%{cmake_on_off dbus WITH_DBUS} \
	%{cmake_on_off imagick WITH_IMAGE_MAGICK}

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

%{__rm} $RPM_BUILD_ROOT%{_datadir}/inkscape/extensions/{.darglint,.pre-commit-config.yaml,.pylintrc,CONTRIBUTING.md,LICENSE.txt,MANIFEST.in,README.md,TESTING.md,doxygen-main.dox,poetry.lock,pyproject.toml,tox.ini}
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/inkscape/extensions/docs

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
%{_datadir}/inkscape/extensions/inkman
%{_datadir}/inkscape/extensions/other
%{_datadir}/inkscape/extensions/svg_fonts
%{_datadir}/inkscape/extensions/tools
%{_datadir}/inkscape/extensions/xaml2svg
%attr(755,root,root) %{_datadir}/inkscape/extensions/*.py
%attr(755,root,root) %{_datadir}/inkscape/extensions/*.sh
%{_datadir}/inkscape/extensions/dxf14_*.txt
%{_datadir}/inkscape/extensions/*.inx
%{_datadir}/inkscape/extensions/*.js
%{_datadir}/inkscape/extensions/*.svg
%{_datadir}/inkscape/extensions/*.xml
%{_datadir}/inkscape/extensions/*.xsl
%{_datadir}/inkscape/extensions/*.xslt
%{_datadir}/inkscape/extensions/fontfix.conf
%{_datadir}/inkscape/extensions/inkscape.extension.rng
%{_datadir}/inkscape/extensions/inkscape.extension.schema
%{_datadir}/metainfo/org.inkscape.Inkscape.appdata.xml
%{_iconsdir}/hicolor/*/apps/org.inkscape.Inkscape.png
%{_iconsdir}/hicolor/scalable/apps/org.inkscape.Inkscape.svg
%{_iconsdir}/hicolor/symbolic/apps/org.inkscape.Inkscape-symbolic.svg
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

%files -n bash-completion-inkscape
%defattr(644,root,root,755)
%{bash_compdir}/inkscape
