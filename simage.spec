#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_with	qt		# load/save images using Qt
%bcond_with	qt4		# Qt4 instead of Qt5
%bcond_with	qt6		# Qt6 instead of Qt5
#
Summary:	Library with image format loaders and front-ends to common import libraries
Summary(pl.UTF-8):	Biblioteka z wczytywaniem formatów obrazów oraz frontendami do popularnych bibliotek importujących
Name:		simage
Version:	1.8.3
Release:	2
License:	MIT, MPEG
Group:		Libraries
#Source0Download: https://github.com/coin3d/simage/releases
Source0:	https://github.com/coin3d/simage/releases/download/v%{version}/%{name}-%{version}-src.tar.gz
# Source0-md5:	af4faec8a7881937cc6b4440e45405bf
Patch0:		%{name}-doxygen.patch
URL:		https://github.com/coin3d/simage
%if %{with qt}
%if %{with qt4}
BuildRequires:	QtCore-devel >= 4
BuildRequires:	QtGui-devel >= 4
%else
%if %{with qt6}
BuildRequires:	Qt6Core-devel >= 6
BuildRequires:	Qt6Gui-devel >= 6
%else
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5Gui-devel >= 5
%endif
%endif
%endif
BuildRequires:	cmake >= 3.0
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	flac-devel
BuildRequires:	giflib-devel >= 5.2.1-2
BuildRequires:	jasper-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libogg-devel
BuildRequires:	libpng-devel
BuildRequires:	libsndfile-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	libvorbis-devel
BuildRequires:	opus-devel
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
BuildRequires:	zstd-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is simage, a library with image format loaders and front-ends to
common import libraries. simage is meant for use with applications
which reads image files as textures.

%description -l pl.UTF-8
Ten pakiet zawiera bibliotekę simage, obsługującą wczytywanie różnych
formatów obrazów oraz frontendy do popularnych bibliotek
importujących. Biblioteka jest przeznaczona do użycia w aplikacjach
czytających pliki obrazów jako tekstury.

%package devel
Summary:	Header files for simage library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki simage
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	flac-devel
Requires:	jasper-devel
Requires:	libjpeg-devel
Requires:	libogg-devel
Requires:	libpng-devel
Requires:	libsndfile-devel
Requires:	libtiff-devel
Requires:	libvorbis-devel
Requires:	opus-devel
Requires:	xz-devel
Requires:	zlib-devel
Requires:	zstd-devel

%description devel
Header files for simage library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki simage.

%package apidocs
Summary:	API documentation for simage library
Summary(pl.UTF-8):	Dokumentacja API biblioteki simage
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for simage library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki simage.

%prep
%setup -q -n %{name}
%patch -P0 -p1

%build
install -d builddir
cd builddir
%cmake .. \
	%{?with_apidocs:-DSIMAGE_BUILD_DOCUMENTATION=ON} \
	-DSIMAGE_LIBJASPER_SUPPORT=ON \
	%{?with_qt:-DSIMAGE_USE_QIMAGE=ON} \
	%{?with_qt4:-DSIMAGE_USE_QT5=OFF} \
	-DSIMAGE_XWD_SUPPORT=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C builddir install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/html

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog LICENSE LICENSE.mpeg2enc NEWS README
%attr(755,root,root) %{_libdir}/libsimage.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsimage.so.20

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/simage-config
%attr(755,root,root) %{_libdir}/libsimage.so
%{_includedir}/simage.h
%{_pkgconfigdir}/simage.pc
%{_libdir}/cmake/simage-%{version}
%dir %{_datadir}/Coin
%dir %{_datadir}/Coin/conf
%{_datadir}/Coin/conf/simage-default.cfg

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc builddir/html/*
%endif
