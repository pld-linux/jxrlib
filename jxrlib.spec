Summary:	Library for reading JPEG XR images
Summary(pl.UTF-8):	Biblioteka do odczytu obrazów JPEG XR
Name:		jxrlib
Version:	1.1
%define	gitref	2019.10.9
%define	rel	1
Release:	0.%{gitref}.%{rel}
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/4creators/jxrlib/tags
Source0:	https://github.com/4creators/jxrlib/archive/v%{gitref}/%{name}-%{gitref}.tar.gz
# Source0-md5:	33d686fdf81e235cd8581c653dafffd6
Source1:	%{name}-CMakeLists.txt
Patch0:		%{name}-warnings.patch
# originally https://jxrlib.codeplex.com/ but no longer available
URL:		https://github.com/4creators/jxrlib
BuildRequires:	cmake >= 2.8
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This device porting kit (DPK) supports the JPEG XR still image format,
based on technology originally developed by Mirosoft under the name HD
Photo (formerly Windows Media Photo).

%description -l pl.UTF-8
Ten pakiet oprogramowania obsługuje format statycznego obrazu JPEG XR,
oparty na technologii oryginalnie rozwijanej przez Microsoft pod nazwą
HD Photo (dawniej Windows Media Photo).

%package devel
Summary:	Header files for JXR library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki JXR
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for JXR library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki JXR.

%prep
%setup -q -n %{name}-%{gitref}
%patch -P0 -p1

cp -p %{SOURCE1} CMakeLists.txt

%{__sed} \
	-e 's,%%(DIR_INSTALL)s,%{_prefix},' \
	-e '/^libdir=/ s,/lib,/%{_lib},' \
	-e 's,%%(JXR_VERSION)s,%{version},' \
	-e 's,%%(JXR_ENDIAN)s,,' \
	-e '/^Cflags: / s,: .*,: -I${includedir}/libjxr -D__ANSI__,' \
	libjxr.pc.in > libjxr.pc

%build
install -d build
cd build
%cmake ..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -Dp libjxr.pc $RPM_BUILD_ROOT%{_pkgconfigdir}/libjxr.pc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md doc/readme.txt
%attr(755,root,root) %{_bindir}/JxrDecApp
%attr(755,root,root) %{_bindir}/JxrEncApp
%attr(755,root,root) %{_libdir}/libjpegxr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjpegxr.so.0
%attr(755,root,root) %{_libdir}/libjxrglue.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjxrglue.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjpegxr.so
%attr(755,root,root) %{_libdir}/libjxrglue.so
%{_includedir}/jxrlib
%{_pkgconfigdir}/libjxr.pc
