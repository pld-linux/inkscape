#
# Conditional build
%bcond_with	dbus		# DBus interface
%bcond_with	gtk3		# GTK+ 3 interface [experimental]
%bcond_without	gnomevfs	# Don't use gnome vfs for loading files
%bcond_with	relocation	# Enable binary relocation support
#

Summary:	Scalable vector graphics editor
Summary(pl.UTF-8):	Edytor skalowalnej grafiki wektorowej
Name:		inkscape
Version:	0.92.3
Release:	1
License:	GPL v2+, LGPL v2.1+
Group:		X11/Applications/Graphics
Source0:	https://media.inkscape.org/dl/resources/file/%{name}-%{version}.tar.bz2
# Source0-md5:	4ef7171cc1de9e1608d8c49b77fed99e
Patch0:		%{name}-man.patch
Patch1:		%{name}-gtk3.patch
Patch2:		%{name}-poppler.patch
URL:		http://www.inkscape.org/
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
%{?with_gnomevfs:BuildRequires:	gnome-vfs2-devel >= 2.15.2}
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
%if %{with gtk3}
BuildRequires:	gdl-devel >= 3.6
BuildRequires:	gtk+3-devel >= 3.8
BuildRequires:	gtkmm3-devel >= 3.10
BuildRequires:	gtkspell3-devel >= 3.0
%else
BuildRequires:	gtk+2-devel >= 2:2.24
BuildRequires:	gtkmm-devel >= 2.24
BuildRequires:	gtkspell-devel >= 2.0.11
%endif
Requires(post,postun):	desktop-file-utils
Requires:	cairo >= 1.10
Requires:	cairomm >= 1.9.8
Requires:	gc >= 7.2
Requires:	glib2 >= 1:2.28
Requires:	glibmm >= 2.28
%{?with_gnomevfs:Requires:	gnome-vfs2 >= 2.15.2}
Requires:	libsigc++ >= 2.0.17
Requires:	libxml2 >= 1:2.6.26
Requires:	libxslt >= 1.1.17
Requires:	pango >= 1:1.24
Requires:	perl-XML-XQL
Requires:	poppler-glib >= 0.29.0
%if %{with gtk3}
Requires:	gdl >= 3.6
Requires:	gtk+3 >= 3.8
Requires:	gtkmm3 >= 3.10
%else
Requires:	gtk+2 >= 2:2.24
Requires:	gtkmm >= 2.24
Requires:	gtkspell >= 2.0.11
%endif
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
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%{__sed} -i -e 's,po/Makefile.in,,' configure.ac

%build
%{__libtoolize}
%{__gettextize}
%{__intltoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_relocation:--enable-binreloc} \
	%{?with_dbus:--enable-dbusapi} \
	%{?with_gtk3:--enable-gtk3-experimental} \
	--disable-silent-rules \
	%{!?with_gnomevfs:--without-gnome-vfs}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# localized manuals cleanup
for manlang in de el fr ja sk zh_TW ; do
	%{__mv} $RPM_BUILD_ROOT%{_mandir}/${manlang}/man1/{inkscape.${manlang}.1,inkscape.1}
	%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/inkscape.${manlang}.1
done

# unify locale name, overwrite outdated bn
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{bn_BD,bn}/LC_MESSAGES/inkscape.mo
# joke language, unsupported
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/en_US@piglatin
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
%doc AUTHORS ChangeLog NEWS README TRANSLATORS doc/HACKING.txt
%lang(ca) %doc README.ca.txt
%lang(de) %doc README.de.txt doc/HACKING.de.txt
%lang(es) %doc README.es.txt
%lang(fr) %doc README.fr.txt doc/HACKING.fr.txt
%lang(it) %doc README.it.txt doc/HACKING.it.txt
%lang(pt_BR) %doc README.pt_BR.txt doc/HACKING.pt_BR.txt
%lang(sk) %doc README.sk.txt
%lang(sr) %doc README.sr.txt
%attr(755,root,root) %{_bindir}/inkscape
%attr(755,root,root) %{_bindir}/inkview
%dir %{_datadir}/inkscape
%{_datadir}/inkscape/[!e]*
%{_datadir}/inkscape/examples
%dir %{_datadir}/inkscape/extensions
%dir %{_datadir}/inkscape/extensions/Barcode
%attr(755,root,root) %{_datadir}/inkscape/extensions/Barcode/*.py
%{_datadir}/inkscape/extensions/Poly3DObjects
%{_datadir}/inkscape/extensions/alphabet_soup
%dir %{_datadir}/inkscape/extensions/ink2canvas
%attr(755,root,root) %{_datadir}/inkscape/extensions/ink2canvas/*.py
%{_datadir}/inkscape/extensions/test
%{_datadir}/inkscape/extensions/xaml2svg
%attr(755,root,root) %{_datadir}/inkscape/extensions/*.pl
%attr(755,root,root) %{_datadir}/inkscape/extensions/*.py
%attr(755,root,root) %{_datadir}/inkscape/extensions/*.rb
%attr(755,root,root) %{_datadir}/inkscape/extensions/*.sh
%{_datadir}/inkscape/extensions/*.inx
%{_datadir}/inkscape/extensions/*.js
%{_datadir}/inkscape/extensions/*.svg
%{_datadir}/inkscape/extensions/*.xml
%{_datadir}/inkscape/extensions/*.xsl
%{_datadir}/inkscape/extensions/*.xslt
%{_datadir}/inkscape/extensions/fontfix.conf
%{_datadir}/inkscape/extensions/inkscape.extension.rng
%{_datadir}/appdata/inkscape.appdata.xml
%{_iconsdir}/hicolor/*/apps/inkscape.png
%{_desktopdir}/inkscape.desktop
%{_mandir}/man1/inkscape.1*
%{_mandir}/man1/inkview.1*
%lang(de) %{_mandir}/de/man1/inkscape.1*
%lang(el) %{_mandir}/el/man1/inkscape.1*
%lang(fr) %{_mandir}/fr/man1/inkscape.1*
%lang(ja) %{_mandir}/ja/man1/inkscape.1*
%lang(sk) %{_mandir}/sk/man1/inkscape.1*
%lang(zh_TW) %{_mandir}/zh_TW/man1/inkscape.1*
