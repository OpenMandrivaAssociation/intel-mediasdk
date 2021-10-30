%define major              1
%define mfxlibname         %mklibname mfx %{major}
%define mfxdevelname       %mklibname mfx -d

%define mfxtracerlibname   %mklibname mfxtracer %{major}
%define mfxtracerdevelname %mklibname mfxtracer -d

%define mfxhw64libname     %mklibname mfxhw64 %{major}
%define mfxhw64develname   %mklibname mfxhw64 -d

Name:           intel-mediasdk
Version:        21.1.3
Release:        %mkrel 1
Summary:        Hardware-accelerated video processing on Intel integrated GPUs Library
Group:          System/Kernel and hardware
License:        MIT
URL:            https://github.com/Intel-Media-SDK/MediaSDK
Source0:        %{url}/archive/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(igdgmm)
BuildRequires:  pkgconfig(libdrm_intel)
BuildRequires:  pkgconfig(pciaccess)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ocl-icd)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(libva)

# This package relies on igdgmm which relies on intel asm
ExclusiveArch:  x86_64

%description
Intel Media SDK provides a plain C API to access hardware-accelerated video
decode, encode and filtering on Intel Gen graphics hardware platforms.
Implementation written in C++ 11 with parts in C-for-Media (CM).

Supported video encoders: HEVC, AVC, MPEG-2, JPEG, VP9 Supported video decoders:
HEVC, AVC, VP8, VP9, MPEG-2, VC1, JPEG Supported video pre-processing filters:
Color Conversion, Deinterlace, Denoise, Resize, Rotate, Composition


##### mfx lib ###############################
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

##### mfxtracer lib ###############################
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

##### mfxhw64 lib ###############################
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


##### build  ###############################
%prep
%autosetup -p1 -n MediaSDK-intel-mediasdk-%{version}

%build
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

%cmake_build

%install
%cmake_install
find %{buildroot} -name '*.la' -delete
