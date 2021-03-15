###############################################################################
# GNU GCC bootstrapping compiler for arm-none-eabi targets.
###############################################################################
%{!?skip_download:%undefine _disable_source_fetch}
%define _unpackaged_files_terminate_build 1
%define _debugsource_packages 0
# separate, compat, so binaries are shipped with build-ids
%define _build_id_links none
%define _color_output auto


###############################################################################
# Package
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

Source0:        https://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.xz
Source1:        https://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.xz.sig
Nosource:       0
Nosource:       1


###############################################################################
# Defines
###############################################################################
%global package_extract_dir_name gcc-%{version}
%global package_extract_dir %{_builddir}/%{package_extract_dir_name}
%global package_build_dir %{package_extract_dir}-build
%global package_install_prefix %{_buildrootdir}/tools
%global package_sysroot %{_buildrootdir}


###############################################################################
# Description
###############################################################################
%description
  Packaged gcc prerequisite mpc.


###############################################################################
# Download source if necessary. Prep.
###############################################################################
%prep
rm -rf %{package_build_dir}
mkdir -p %{package_build_dir}
mkdir -p %{package_build_dir}/rpmlogs


###############################################################################
# Check source signature, unpack and move into source directory.
###############################################################################
#gpg --keyring %{gnu_keyring} --verify %{_sourcedir}/gcc-%{version}.tar.xz.sig
if [[ ! -e %{package_extract_dir} ]]; then
%setup -q -n %{package_extract_dir_name}
cd %{package_extract_dir}
%{package_extract_dir}/contrib/download_prerequisites
fi


###############################################################################
# Start build phase. Setup build dir, configure and build
###############################################################################
%build
cd %{package_build_dir}

F_BUILD_HOST_TARGET="\
    --build=x86_64-pc-linux-gnu \
    --host=x86_64-pc-linux-gnu \
    --target=arm-none-eabi"
F_WITH_WITHOUT="\
    --with-system-zlib \
    --with-gcc-major-version-only \
    --with-linker-hash-style=gnu \
    --with-isl \
    --without-cuda-driver \
    --with-tune=generic \
    --with-arch_32=i686 \
    --with-gmp-include=%{package_install_prefix}/include \
    --with-gmp-lib=%{package_install_prefix}/lib \
    --with-mpfr-include=%{package_install_prefix}/include \
    --with-mpfr-lib=%{package_install_prefix}/lib"
F_ENABLE_DISABLE="\
    --disable-libssp \
    --disable-option-checking \
    --disable-maintainer-mode"
F_STANDARD="\
    --prefix=%{package_install_prefix} \
    --enable-multilib \
    --without-headers \
    --with-multilib-list=@armv7-a-profile
    --enable-languages=c,lto \
    --disable-shared"
F_OTHER="\
    --srcdir=%{sourcedir}/mpc \
    --cache-file=./config.cache \
    '--program-transform-name=s&^&arm-none-eabi-&'"
F_ALL="\
    ${F_STANDARD} \
    ${F_BUILD_HOST_TARGET} \
    ${F_WITH_WITHOUT} \
    ${F_ENABLE_DISABLE} \
    ${F_OTHER}"

%{package_extract_dir}/mpc/configure ${F_ALL} 2>&1 | tee %{package_build_dir}/rpmlogs/configure.log > /dev/null

# #%{sourcedir}/mpc/configure \
#     --srcdir=%{sourcedir}/mpc \
#     --cache-file=./config.cache \
#     --prefix=%{package_install_prefix} \
#     --enable-multilib \
#     --without-headers \
#     --disable-libssp \
#     --with-multilib-list=@armv7-a-profile \
#     --enable-languages=c,lto \
#     '--program-transform-name=s&^&arm-none-eabi-&' \
#     --disable-option-checking \
#     --build=x86_64-pc-linux-gnu \
#     --host=x86_64-pc-linux-gnu \
#     --target=arm-none-eabi \
#     --disable-shared \
#     --with-gmp-include=%{package_install_prefix}/include \
#     --with-gmp-lib=%{package_install_prefix}/lib \
#     --with-mpfr-include=%{package_install_prefix}/include \
#     --with-mpfr-lib=%{package_install_prefix}/lib \
#     --disable-maintainer-mode


# %{sourcedir}/configure \
#     --prefix=%{package_install_prefix} \
#     --target=arm-none-eabi \
#     --enable-languages=c \
#     --enable-multilib \
#     --without-headers \
#     --disable-libssp \
#     --with-multilib-list=@armv7-a-profile

make %{_smp_mflags} 2>&1 | tee %{package_build_dir}/rpmlogs/make.log > /dev/null


###############################################################################
# Start install phase, change to build dir and install files
###############################################################################
%install

cd %{package_build_dir}
DESTDIR=%{buildroot} \
INSTALL="/usr/bin/install -p" \
make install | tee %{package_build_dir}/rpmlogs/install.log > /dev/null



###############################################################################
# Check
###############################################################################
%check



###############################################################################
# Clean
###############################################################################
%clean


###############################################################################
# Files
###############################################################################
%files
  %defattr(0777,-,users)

  %{package_install_prefix}/lib
  %{package_install_prefix}/include

  %exclude %{package_install_prefix}/share


###############################################################################
# Changelog
###############################################################################
%changelog
* Tue Oct 13 2020 Kyle Burge <kyle.burge7196@gmail.com>
- Created package
