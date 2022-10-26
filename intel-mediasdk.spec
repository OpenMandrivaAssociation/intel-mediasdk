# Crap, this can't be compiled with lld or gold
# https://github.com/Intel-Media-SDK/MediaSDK/issues/1844
%global optflags %{optflags} -fuse-ld=bfd

%define major              1
%define mfxlibname         %mklibname mfx %{major}
%define mfxdevelname       %mklibname mfx -d

%define mfxtracerlibname   %mklibname mfxtracer %{major}
%define mfxtracerdevelname %mklibname mfxtracer -d

%define mfxhw64libname     %mklibname mfxhw64 %{major}
%define mfxhw64develname   %mklibname mfxhw64 -d

Name:           intel-mediasdk
Version:        22.6.0
Release:        1
Summary:        Hardware-accelerated video processing on Intel integrated GPUs Library
Group:          System/Kernel and hardware
License:        MIT
URL:            https://github.com/Intel-Media-SDK/MediaSDK
Source0:        https://github.com/Intel-Media-SDK/MediaSDK/archive/%{version}/MediaSDK-intel-mediasdk-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(igdgmm)
BuildRequires:  pkgconfig(libdrm_intel)
BuildRequires:  pkgconfig(pciaccess)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ocl-icd)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(libva)

%description
Intel Media SDK provides a plain C API to access hardware-accelerated video
decode, encode and filtering on Intel Gen graphics hardware platforms.
Implementation written in C++ 11 with parts in C-for-Media (CM).

Supported video encoders: HEVC, AVC, MPEG-2, JPEG, VP9 Supported video decoders:
HEVC, AVC, VP8, VP9, MPEG-2, VC1, JPEG Supported video pre-processing filters:
Color Conversion, Deinterlace, Denoise, Resize, Rotate, Composition

%package -n     %{mfxlibname}
Summary:        Hardware-accelerated video processing on Intel integrated GPUs Library
Group:          System/Libraries
Provides:       %{name} = %{version}-%{release}

%description -n %{mfxlibname}
This package contains the library needed to run programs dynamically
linked with mfx library.

%package -n     %{mfxdevelname}
Summary:        SDK for hardware-accelerated video processing on Intel integrated GPUs
Group:          Development/C++
Requires:       %{mfxlibname} = %{version}
Provides:       %{name}-devel = %{version}-%{release}

%description -n %{mfxdevelname}
This package contains the headers that programmers will need to develop
applications which will use mfx library.

%files -n %{mfxlibname}
%{_libdir}/libmfx.so.%{major}{,.*}

%files -n %{mfxdevelname}
%dir %{_includedir}/mfx
%{_includedir}/mfx/mfx*.h
%{_libdir}/libmfx.so
%{_libdir}/pkgconfig/libmfx.pc
%{_libdir}/pkgconfig/mfx.pc


%package -n     %{mfxtracerlibname}
Summary:        Tracer for hardware-accelerated video processing on Intel integrated GPUs Library
Group:          System/Libraries
Provides:       %{name} = %{version}-%{release}

%description -n %{mfxtracerlibname}
This package contains the tracer for the mfx.

%package -n     %{mfxtracerdevelname}
Summary:        Tracer for hardware-accelerated video processing on Intel integrated GPUs
Group:          Development/C++
Requires:       %{mfxtracerlibname} = %{version}
Provides:       %{name}-devel = %{version}-%{release}

%description -n %{mfxtracerdevelname}
This package contains the tracer that programmers will need to develop
applications which will use mfx library.

%files -n %{mfxtracerlibname}
%{_bindir}/mfx-tracer-config
%{_libdir}/libmfx-tracer.so.%{major}{,.*}

%files -n %{mfxtracerdevelname}
%{_libdir}/libmfx-tracer.so


%package -n     %{mfxhw64libname}
Summary:        Hardware-accelerated video processing on Intel integrated GPUs Library
Group:          System/Libraries
Provides:       %{name} = %{version}-%{release}

%description -n %{mfxhw64libname}
This package contains the library needed to run programs dynamically
linked with mfxhw64 library.

%package -n     %{mfxhw64develname}
Summary:        SDK for hardware-accelerated video processing on Intel integrated GPUs
Group:          Development/C++
Requires:       %{mfxhw64libname} = %{version}
Provides:       %{name}-devel = %{version}-%{release}

%description -n %{mfxhw64develname}
This package contains the headers that programmers will need to develop
applications which will use mfxhw64 library.

%files -n %{mfxhw64libname}
%{_libdir}/libmfxhw64.so.%{major}{,.*}
%{_libdir}/mfx/libmfx_*_hw64.so
%{_datadir}/mfx/plugins.cfg
 
%files -n %{mfxhw64develname}
%{_libdir}/libmfxhw64.so
%{_libdir}/pkgconfig/libmfxhw64.pc


%prep
%autosetup -p1 -n MediaSDK-intel-mediasdk-%{version}

%build
# Compilation with Clang 13 failed.
# "/builddir/build/BUILD/MediaSDK-intel-mediasdk-21.3.5/tests/unit/suites/mfx_dispatch/linux/mfx_dispatch_test_main.cpp:48:12: 
# error: redefinition of a 'extern inline' function 'fgets' is not supported in C++"
export CC=gcc
export CXX=g++

%cmake \
    -DBUILD_DISPATCHER=ON \
    -DBUILD_SAMPLES=OFF \
    -DBUILD_TESTS=ON \
    -DBUILD_TOOLS=OFF \
    -DENABLE_OPENCL=ON \
    -DENABLE_WAYLAND=ON \
    -DENABLE_X11=ON \
    -DENABLE_X11_DRI3=ON \
    -DUSE_SYSTEM_GTEST=ON \
    -DCMAKE_BUILD_TYPE=Release

%make_build

%install
%make_install -C build
find %{buildroot} -name '*.la' -delete
