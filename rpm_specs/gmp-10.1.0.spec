###############################################################################
# GNU GCC bootstrapping compiler for arm-none-eabi targets.
###############################################################################
Name:           gmp
Version:        10.1.0
Release:        1%{?dist}
Summary:        GNU GCC
License:        FIXME
BuildArch:      x86_64
AutoReq:        no

%undefine       _disable_source_fetch
Source0:        https://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.xz
Source1:        https://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.xz.sig
Nosource:       0
Nosource:       1


###############################################################################
# Defines
###############################################################################
%define _unpackaged_files_terminate_build 1
# separate, compat, so binaries are shipped with build-ids
%define _build_id_links none
# so source and debug are combined
%define _debugsource_packages 0

%global sourcedir %{_builddir}/gcc-%{version}
%global builddir %{_builddir}/%{name}-%{version}-build
%global install_prefix %{?install_prefix}%{!?install_prefix: %{_prefix}}
%global num_cpus %{?num_cpus}%{!?num_cpus: %{_smp_mflags}}


###############################################################################
# Description
###############################################################################
%description
  Packaged gcc prerequisite gmp.


###############################################################################
# Prep
###############################################################################
%prep
gpg --keyring %{gnu_keyring} --verify %{_sourcedir}/gcc-%{version}.tar.xz.sig

%setup -q -n gcc-%{version}
mkdir -p %{builddir}
%{sourcedir}/contrib/download_prerequisites


###############################################################################
# Build
###############################################################################
%build
cd %{builddir}

%{sourcedir}/gmp/configure \
    --enable-bootstrap \
    --enable-languages=c,c++,fortran,objc,obj-c++,ada,go,d,lto \
    --prefix=%{install_prefix} \
    --enable-shared \
    --enable-threads=posix \
    --enable-checking=release \
    --enable-multilib \
    --with-system-zlib \
    --enable-__cxa_atexit \
    --disable-libunwind-exceptions \
    --enable-gnu-unique-object \
    --enable-linker-build-id \
    --with-gcc-major-version-only \
    --with-linker-hash-style=gnu \
    --enable-plugin \
    --enable-initfini-array \
    --with-isl \
    --enable-offload-targets=nvptx-none \
    --without-cuda-driver \
    --enable-gnu-indirect-function \
    --enable-cet \
    --with-tune=generic \
    --with-arch_32=i686 \
    --build=x86_64-redhat-linux

# %{sourcedir}/configure \
#     --prefix=%{install_prefix} \
#     --target=arm-none-eabi \
#     --enable-languages=c \
#     --enable-multilib \
#     --without-headers \
#     --disable-libssp \
#     --with-multilib-list=@armv7-a-profile

%make_build -j%{num_cpus}


###############################################################################
# Install
###############################################################################
%install
cd %{builddir}
%make_install



###############################################################################
# Check
###############################################################################
%check



###############################################################################
# Clean
###############################################################################
%clean
cd %{_builddir}
# %{!?keep_buildroot: rm -rf %{buildroot}}
# rm -rf %{builddir}
#rm -rf %{sourcedir}


###############################################################################
# Files
###############################################################################
%files
  %defattr(0777,-,users)

  %{install_prefix}/lib
  %{install_prefix}/include

  %exclude %{install_prefix}/share


###############################################################################
# Changelog
###############################################################################
%changelog
* Tue Oct 13 2020 Kyle Burge <kyle.burge7196@gmail.com>
- Created package
