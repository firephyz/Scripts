###############################################################################
# GNU Binutils for arm-none-eabi targets.
###############################################################################
Name:           binutils
Version:        2.34
Release:        1%{?dist}
Summary:        GNU Binutils
License:        FIXME
BuildArch:      x86_64
AutoReq:        no

%undefine       _disable_source_fetch
Source0:        https://ftp.gnu.org/gnu/binutils/%{name}-%{version}.tar.xz
Source1:        https://ftp.gnu.org/gnu/binutils/%{name}-%{version}.tar.xz.sig
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

%global sourcedir %{_builddir}/%{name}-%{version}
%global builddir %{_builddir}/%{name}-%{version}-build
%global install_prefix %{?install_prefix}%{!?install_prefix: %{_prefix}}


###############################################################################
# Description
###############################################################################
%description
  Packaged binutils.


###############################################################################
# Prep
###############################################################################
%prep
gpg --keyring %{gnu_keyring} --verify %{_sourcedir}/%{name}-%{version}.tar.xz.sig
%setup -q
mkdir -p %{builddir}


###############################################################################
# Build
###############################################################################
%build
cd %{builddir}
#%%global LD_LIB_PATHS "%{_prefix}/lib/gcc/arm-none-eabi/11.0.0:%{_prefix}/arm-none-eabi/lib"
%global LD_LIB_PATHS ""
%{sourcedir}/configure \
    --prefix=%{install_prefix} \
    --target=arm-none-eabi \
    --with-lib-path=%{LD_LIB_PATHS} \
    --disable-nls


%make_build %{_smp_mflags}


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
%{!?keep_buildroot: rm -rf %{buildroot}}
rm -rf %{builddir}
rm -rf %{sourcedir}


###############################################################################
# Files
###############################################################################
%files
  %defattr(0777,-,users)

  %{install_prefix}/arm-none-eabi
  %{install_prefix}/bin

  %exclude %{install_prefix}/arm-none-eabi/lib/ldscripts
  %exclude %{install_prefix}/share
  %exclude %{install_prefix}/src


###############################################################################
# Changelog
###############################################################################
%changelog
* Tue Oct 13 2020 Kyle Burge <kyle.burge7196@gmail.com>
- Created package
