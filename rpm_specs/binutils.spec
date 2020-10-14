###############################################################################
# GNU Binutils for arm-none-eabi targets.
###############################################################################
Name:           binutils
Version:        2.34
Release:        1%{?dist}
Summary:        GNU Binutils
License:        FIXME
Source0:        %{name}-%{version}.tar.xz
Nosource:       0
BuildArch:      x86_64

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

###############################################################################
# Description
###############################################################################
%description
  Packaged binutils.


###############################################################################
# Prep
###############################################################################
%prep
%setup -q
mkdir -p %{builddir}


###############################################################################
# Build
###############################################################################
%build
cd %{builddir}
%{sourcedir}/configure \
    --prefix=%{_prefix} \
    --target=arm-none-eabi \
    --with-lib-path="%{_prefix}lib/gcc/arm-none-eabi/11.0.0:%{_prefix}arm-none-eabi/lib" \
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
rm -rf %{buildroot}
rm -rf %{builddir}
rm -rf %{sourcedir}


###############################################################################
# Files
###############################################################################
%files
  %defattr(0777,-,users)

  /usr/arm-none-eabi
  /usr/bin
  %exclude /usr/arm-none-eabi/lib/ldscripts
  %exclude /usr/share
  %exclude /usr/src


###############################################################################
# Changelog
###############################################################################
%changelog
* Tue Oct 13 2020 Kyle Burge <kyle.burge7196@gmail.com>
- Created package
