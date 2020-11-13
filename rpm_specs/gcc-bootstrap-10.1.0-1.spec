###############################################################################
# GNU GCC bootstrapping compiler for arm-none-eabi targets.
###############################################################################
Name:           gcc-bootstrap
Version:        10.1.0
Release:        1%{?dist}
Summary:        GNU GCC
License:        FIXME
BuildArch:      x86_64
AutoReq:        no
BuildRequires:  binutils == 2.34
Requires:       binutils == 2.34

%undefine       _disable_source_fetch
Source0:        https://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.xz
Source1:        https://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.xz.sig
Source2:        armv7-a-profile
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
%global builddir %{_builddir}/gcc-%{version}-build
%global install_prefix %{?install_prefix}%{!?install_prefix: %{_prefix}}
%global num_cpus %{?num_cpus}%{!?num_cpus: %{_smp_mflags}}


###############################################################################
# Description
###############################################################################
%description
  Packaged bootstrap gcc.


###############################################################################
# Prep
###############################################################################
%prep
gpg --keyring %{gnu_keyring} --verify %{_sourcedir}/gcc-%{version}.tar.xz.sig

%setup -q -n gcc-%{version}
mkdir -p %{builddir}
cp -v %{S:2} %{sourcedir}/gcc/config/arm/
%{sourcedir}/contrib/download_prerequisites


###############################################################################
# Build
###############################################################################
%build
cd %{builddir}
%{sourcedir}/configure \
    --prefix=%{install_prefix} \
    --target=arm-none-eabi \
    --enable-languages=c \
    --enable-multilib \
    --with-multilib-list=@armv7-a-profile \
    --without-headers \
    --disable-libssp

%make_build -j%{num_cpus}


###############################################################################
# Install
###############################################################################
%install
cd %{builddir}
rm -rf %{buildroot}
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
rm -rf %{sourcedir}


###############################################################################
# Files
###############################################################################
%files
  %defattr(0777,-,users)

  %{install_prefix}/bin
  %{install_prefix}/lib
  %{install_prefix}/lib64
  %{install_prefix}/libexec

  %exclude %{install_prefix}/lib/gcc/arm-none-eabi/%{version}/crt*
  %exclude %{install_prefix}/lib/gcc/arm-none-eabi/%{version}/lib*
  %exclude %{install_prefix}/lib/gcc/arm-none-eabi/%{version}/thumb/crt*
  %exclude %{install_prefix}/lib/gcc/arm-none-eabi/%{version}/thumb/lib*
  %exclude %{install_prefix}/lib/gcc/arm-none-eabi/%{version}/include-fixed
  %exclude %{install_prefix}/lib/gcc/arm-none-eabi/%{version}/install-tools
  %exclude %{install_prefix}/lib/gcc/arm-none-eabi/%{version}/plugin
  %exclude %{install_prefix}/libexec/gcc/arm-none-eabi/%{version}/install-tools
  %exclude %{install_prefix}/libexec/gcc/arm-none-eabi/%{version}/liblto_plugin*
  %exclude %{install_prefix}/libexec/gcc/arm-none-eabi/%{version}/plugin
  %exclude %{install_prefix}/share

  # %ghost %{install_prefix}/armv7-a-profile


###############################################################################
# Changelog
###############################################################################
%changelog
* Tue Oct 13 2020 Kyle Burge <kyle.burge7196@gmail.com>
- Created package
