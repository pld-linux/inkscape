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
Version:	0.91
Release:	13
License:	GPL v2+, LGPL v2.1+
Group:		X11/Applications/Graphics
#Source0:	http://downloads.sourceforge.net/inkscape/%{name}-%{version}%{beta}.tar.bz2
Source0:	https://inkscape.org/en/gallery/item/3860/%{name}-%{version}%{beta}.tar.bz2
# Source0-md5:	278dfa4514adcde23546370ec2c84581
# workaround for https://bugs.launchpad.net/inkscape/+bug/487038
Patch0:		%{name}-ldl.patch
Patch1:		%{name}-0.48.2-types.patch
Patch2:		%{name}-0.91-drop-wait-for-targets.patch
URL:		http://www.inkscape.org/
BuildRequires:	ImageMagick-c++-devel
BuildRequires:	aspell-devel
BuildRequires:	autoconf >= 2.59-3
BuildRequires:	automake >= 1:1.9.4-2
BuildRequires:	boost-devel >= 1.36
BuildRequires:	cairo-devel >= 1.8.0
BuildRequires:	freetype-devel >= 2.0
BuildRequires:	gc-devel >= 6.4
BuildRequires:	gettext-tools
BuildRequires:	glibmm-devel >= 2.16.0
%{?with_gnomevfs:BuildRequires:	gnome-vfs2-devel >= 2.15.2}
BuildRequires:	gsl-devel
BuildRequires:	gtk+2-devel >= 2:2.14.0
BuildRequires:	gtkmm-devel >= 2.10.0
BuildRequires:	gtkspell-devel >= 2.0.11
BuildRequires:	intltool >= 0.35.0
BuildRequires:	lcms2-devel >= 2
BuildRequires:	libgomp-devel
BuildRequires:	libpng-devel >= 1.2
BuildRequires:	libsigc++-devel >= 2.0.17
BuildRequires:	libstdc++-devel >= 6:4.2.2-2
BuildRequires:	libtool
BuildRequires:	libwpd-devel >= 0.9
BuildRequires:	libwpg-devel >= 0.2
BuildRequires:	libxml2-devel >= 1:2.6.26
BuildRequires:	libxslt-devel >= 1.1.17
%{?with_inkboard:BuildRequires:	loudmouth-devel >= 1.0.3}
BuildRequires:	pkgconfig
BuildRequires:	poppler-glib-devel >= 0.20.0
BuildRequires:	popt-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	sed >= 4.0
%{?with_xft:BuildRequires:	xorg-lib-libXft-devel}
BuildRequires:	zlib-devel
Requires(post,postun):	desktop-file-utils
Requires:	cairo >= 1.8.0
Requires:	gc >= 6.4
Requires:	glibmm >= 2.16.0
%{?with_gnomevfs:Requires:	gnome-vfs2 >= 2.15.2}
Requires:	gtk+2 >= 2:2.14.0
Requires:	gtkmm >= 2.24.0
Requires:	gtkspell >= 2.0.11
Requires:	libsigc++ >= 2.0.17
Requires:	libxml2 >= 1:2.6.26
Requires:	libxslt >= 1.1.17
Requires:	perl-XML-XQL
Requires:	poppler-glib >= 0.20.0
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
%patch1 -p1
%patch2 -p0

%build
%{__libtoolize}
%{__glib_gettextize}
%{__intltoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
CXXFLAGS="%{rpmcxxflags} -std=c++11"
%configure \
	--disable-silent-rules \
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

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{bn_BD,en_US@piglatin}

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
%lang(pt_BR) %doc README.it.txt
%lang(sk) %doc README.it.txt
%lang(sr) %doc README.it.txt
%lang(de) %doc doc/HACKING.de.txt
%lang(fr) %doc doc/HACKING.fr.txt
%lang(it) %doc doc/HACKING.it.txt
%lang(pt_BR) %doc doc/HACKING.it.txt
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
%attr(755,root,root) %{_datadir}/inkscape/extensions/*.py
%attr(755,root,root) %{_datadir}/inkscape/extensions/*.rb
%attr(755,root,root) %{_datadir}/inkscape/extensions/*.sh
%dir %{_datadir}/inkscape/extensions/ink2canvas
%attr(755,root,root) %{_datadir}/inkscape/extensions/ink2canvas/*.py
%dir %{_datadir}/inkscape/extensions/Barcode
%attr(755,root,root) %{_datadir}/inkscape/extensions/Barcode/*.py
%dir %{_datadir}/inkscape/extensions/xaml2svg
%{_datadir}/inkscape/extensions/xaml2svg/*.xsl
%{_datadir}/inkscape/extensions/fontfix.conf
%{_datadir}/inkscape/extensions/inkscape.extension.rng
%{_datadir}/inkscape/extensions/jessyInk_video.svg
%{_mandir}/man1/*.1*
%lang(el) %{_mandir}/el/man1/*.1*
%lang(fr) %{_mandir}/fr/man1/*.1*
%lang(ja) %{_mandir}/ja/man1/*.1*
%lang(sk) %{_mandir}/sk/man1/*.1*
%lang(zh_TW) %{_mandir}/zh_TW/man1/*.1*
%{_iconsdir}/hicolor/*/apps/inkscape.png
%{_desktopdir}/inkscape.desktop
