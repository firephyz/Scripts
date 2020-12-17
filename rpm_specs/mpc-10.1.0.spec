###############################################################################
# GNU GCC bootstrapping compiler for arm-none-eabi targets.
###############################################################################
Name:           mpc
Version:        10.1.0
Release:        1%{?dist}
Summary:        GNU GCC
License:        FIXME
BuildArch:      x86_64
AutoReq:        no
BuildRequires:  mpfr == 10.1.0, gmp == 10.1.0
Requires:       mpfr == 10.1.0, gmp == 10.1.0

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
  Packaged gcc prerequisite mpc.


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

%{sourcedir}/mpc/configure \
    --srcdir=%{sourcedir}/mpc \
    --cache-file=./config.cache \
    --prefix=%{install_prefix} \
    --enable-multilib \
    --without-headers \
    --disable-libssp \
    --with-multilib-list=@armv7-a-profile \
    --enable-languages=c,lto \
    '--program-transform-name=s&^&arm-none-eabi-&' \
    --disable-option-checking \
    --build=x86_64-pc-linux-gnu \
    --host=x86_64-pc-linux-gnu \
    --target=arm-none-eabi \
    --disable-shared \
    --with-gmp-include=%{install_prefix}/include \
    --with-gmp-lib=%{install_prefix}/lib \
    --with-mpfr-include=%{install_prefix}/include \
    --with-mpfr-lib=%{install_prefix}/lib \
    --disable-maintainer-mode


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
