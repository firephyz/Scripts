Name:           binutils
Version:        2.34
Release:        1%{?dist}
Summary:        GNU Binutils
License:        FIXME
Source0:        %{name}-%{version}.tar.xz
Source1:        %{name}-build.sh
Nosource:       0
Nosource:       1
BuildArch:      x86_64

# BuildRequires:
# Requires:

# Make sure unknown built files terminate build
%define _unpackaged_files_terminate_build 1

%global build_script_name %(echo %{S:1} | sed 's/.*\\///')
%global build_script %{_sourcedir}/scripts/arm-xgcc-scripts/%{build_script_name}
%global sourcedir %{_builddir}/%{name}-%{version}
%global builddir %{_builddir}/%{name}-%{version}-build

%description
  Packaged binutils.


%prep
%setup -q
echo "hi"
mkdir -p %{builddir}
cd %{builddir}
cp -v %build_script .

%build
cd %{builddir}
bash %{build_script_name} -sourcedir %{sourcedir} -prefix %{_prefix} -action configure


%make_build %{_smp_mflags}


%install
cd %{builddir}
rm -rf %{buildroot}
%make_install


%check


%clean
rm -rf %{buildroot}
rm -rf %{builddir}
rm -rf %{sourcedir}


%files
  %defattr(0777,-,users)
  %ghost /%{build_script_name}

  /usr/arm-none-eabi
  /usr/bin
  /usr/lib
  /usr/share
  /usr/src/debug/%{name}-%{version}-%{release}.%{_arch}
  # -f <file list file>
  #%%verify
  #%%attr
  #%%license add-license-file-here
  #%%doc add-docs-here
  #%%config
  #%%dir


%changelog
* Tue Oct 13 2020 Kyle Burge <kyle.burge7196@gmail.com>
- Created package
