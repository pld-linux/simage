#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_with	qt		# load/save images using Qt
%bcond_with	qt4		# Qt4 instead of Qt5
#
Summary:	Library with image format loaders and front-ends to common import libraries
Summary(pl.UTF-8):	Biblioteka z wczytywaniem formatów obrazów oraz frontendami do popularnych bibliotek importujących
Name:		simage
Version:	1.8.0
Release:	1
License:	MIT, MPEG
Group:		Libraries
#Source0Download: https://github.com/coin3d/simage/releases
Source0:	https://github.com/coin3d/simage/releases/download/simage-%{version}/%{name}-%{version}-src.tar.gz
# Source0-md5:	a1810e0c2a1c9c7a6c191198bd8465bc
Patch0:		%{name}-gifutil.patch
Patch1:		%{name}-doxygen.patch
Patch2:		%{name}-link.patch
URL:		https://github.com/coin3d/simage
%if %{with qt}
%if %{with qt4}
BuildRequires:	QtCore-devel >= 4
BuildRequires:	QtGui-devel >= 4
%else
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5Gui-devel >= 5
%endif
%endif
BuildRequires:	cmake >= 3.0
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	giflib-devel >= 5.2.1-2
BuildRequires:	jasper-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libogg-devel
BuildRequires:	libpng-devel
BuildRequires:	libsndfile-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	libvorbis-devel
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	zlib-devel
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
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
install -d builddir
cd builddir
%cmake .. \
	%{?with_apidocs:-DSIMAGE_BUILD_DOCUMENTATION=ON} \
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
# bogus location
%{__rm} -r $RPM_BUILD_ROOT%{_infodir}/simage1

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
%attr(755,root,root) %{_libdir}/libsimage.so
%{_includedir}/simage.h
%{_pkgconfigdir}/simage.pc
%{_libdir}/cmake/simage-%{version}

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc builddir/html/*
%endif
