# testing
###############################################################################
# Build Makefile
###############################################################################
# TODO What rules require the .SECONDEXPANSION directive?

###############################################################################
# Defines
###############################################################################
arch               := x86_64
os_version         := fc32
rpm-release-suffix := $(arch)
packages           := newlib-3.2.0-1 \
                      libgcc-bootstrap-10.1.0 \
                      gcc-bootstrap-10.1.0 \
											gcc-prerequisites-10.1.0 \
											gmp-10.1.0 \
											mpfr-10.1.0 \
											mpc-10.1.0 \
                      binutils-2.34

# package dep lists for each package
newlib-3.2.0-1-requires-list            := gcc-bootstrap-10.1.0 libgcc-bootstrap-10.1.0 binutils-2.34
gcc-bootstrap-10.1.0-1-requires-list    := gmp-10.1.0 mpfr-10.1.0 mpc-10.1.0
libgcc-bootstrap-10.1.0-1-requires-list := gcc-bootstrap-10.1.0 binutils-2.34
gcc-prerequisites-1.0-1-requires-list   := gmp-10.1.0 mpfr-10.1.0 mpc-10.1.0
gmp-10.1.0-1-requires-list              :=
mpfr-10.1.0-1-requires-list             := gmp-10.1.0
mpc-10.1.0-1-requires-list              := mpfr-10.1.0 gmp-10.1.0
binutils-2.34-1-requires-list           :=

rpm-db-dir	    := rpmdb
build-root	    := BUILDROOT
rpm-dir		      := RPMS/x86_64
srpm-dir	      := SRPMS
build-dir	      := BUILD
source-dir      := SOURCES

# select correct db to update when installing packages
rpml			:= rpm --dbpath=$(shell readlink -f $(rpm-db-dir))

###############################################################################
# Utilities
###############################################################################
# get full RPM path from pkg name
# define rpm-path
# 	$(addprefix $(rpm-dir)/,$(call rpm-name,$(1)))
# endef
# # get full RPM name from pkg name
# define rpm-name
# 	$(addsuffix .$(rpm-release-suffix).rpm, $(1))
# endef
define rpm-path
	$(addprefix $(rpm-dir)/,$(call rpm-name,$(1)))
endef
# get full RPM name from pkg name
define rpm-name
	$(addsuffix .rpm, $(1))
endef
# get pkg-name from full RPM name
define pkg-name
	$(shell echo $(1) | sed "s/\.rpm//")
endef
# get package full rpm name from package short name without version numbers
define short-name-to-rpm-path
	$(call rpm-path,$(shell echo $(packages) | tr ' ' '\n' | grep $(1)))
endef
# get package short name from package name
define pkg-name-to-short-name
    $(shell echo $(1) | sed -r "s/([-\.][0-9]+)+//")
endef
# # turn make target pkg stem into pkg-name
# define stem-to-pkg-name
# 	$(shell echo $(1) | sed "s/\.fc[0-9]*\.${arch}//")
# endef
# # turn make target pkg stem into pkg-name
# define stem-to-rpm-name
# 	$(call rpm-name,$(call stem-to-pkg-name,$(1)))
# endef
define stem-to-pkg-name
	$(shell echo $(1))
endef
# turn make target pkg stem into pkg-name
define stem-to-rpm-name
	$(call rpm-name,$(1))
endef
# turn a long stem including os version and cpu type into package name
define long-stem-to-pkg-name
	$(eval sed_string=s/$(shell echo $(call get-os-release-version) | sed 's/\./\\\\./g')//)
	$(shell echo $(1) | sed $(sed_string))
endef
# return path to spec file for given package name
define spec-path
	$(addsuffix .spec,$(addprefix SPECS/,$(1)))
endef
define get-package-buildroot-dir
	$(addsuffix $(shell rpm --eval "%{dist}.%{_host_cpu}"),$(1))
endef
define get-os-release-version
	$(shell rpm --eval "%{dist}.%{_host_cpu}")
endef
# remove large directories without too much output
define remove-large-dir
	@if [[ 1 -eq 1 ]]; then					 \
		dir=$$(readlink -f $(1));			   \
		for f in $$(ls $$dir); do			   \
			if [[ -d $$dir/$$f ]]; then		 \
				rm -fr $$dir/$$f/*;			 \
				rm -frv $$dir/$$f;			  \
			else								\
				rm -fv $$dir/$$f;			   \
			fi								  \
		done									\
	fi
endef

###############################################################################
# More defines
###############################################################################
JFLAG := $(shell [[ -z "${JFLAG}" ]] && echo 9 || echo "${JFLAG}")
rpms := $(foreach package,$(packages),$(call rpm-name,$(package)))
rpm-targets := $(foreach target,$(rpms),$(addprefix $(rpm-dir)/,$(target)))
install-targets := $(foreach target,$(rpms),$(addsuffix -install,$(addprefix $(rpm-dir)/,$(target))))
rpm-build-debuginfo := $(shell [[ "x$$RPM_BUILD_DEBUGINFO" == "x1" ]] && echo '' || echo '--nodebuginfo')
rpm-build-clean-after := $(shell [[ "x$$RPM_BUILD_CLEAN_AFTER" == "x" ]] && echo '' || echo '--noclean')


###############################################################################
# Recipes
###############################################################################
.SECONDEXPANSION:
all: build ;

build: $(rpm-targets);
###############################################################################
# Build each rpm package
###############################################################################
# Register <pkg>-requires target and spec files in dep list
define package-prereqs
	| $(addsuffix -requires,$(1)) \
	$(addsuffix -setup,$(1)) \
	$(call spec-path,$(1))
endef

%-setup: ;#$$(addprefix $$(source-dir)/,$$(addsuffix -setup.sh,$$*))
	#exec bash $(addprefix $(source-dir)/,$(addsuffix -setup.sh,$*))


BUILDROOT/%: $$(call package-prereqs,$$(call long-stem-to-pkg-name,$$*))
	@echo Building $(call stem-to-pkg-name,$*)...;
	@rm -rf $(addprefix $(rpm-dir)/,$(addsuffix .rpm,$*))
	@rpmbuild --define="install_prefix $(shell readlink -f $(build-root))" \
			 --define="num_cpus $(JFLAG)" --dbpath=$(shell readlink -f $(rpm-db-dir)) \
			 $(rpm-build-debuginfo) $(rpm-build-clean-after) \
			 -bb $(call spec-path,$(shell echo $* | sed 's/\.fc[0-9]*\.x86_64//'));

RPMS/x86_64/%.rpm: $(addprefix $(build-root)/,$(call get-package-buildroot-dir, $$*))
	$(eval pkg_name=$(shell echo $(call stem-to-pkg-name,$*)))
	$(eval pkg_path=$(addsuffix .rpm,$(addprefix $(rpm-dir)/,$(pkg_name))))
	$(eval rpm_path=$(shell find $(rpm-dir) -regex ".*$(pkg_name).*"))
	if [[ "$(rpm_path)" == "" ]]; then \
	  echo Could not find target RPM file.; \
	  exit 1; \
	fi
	mv -v $(rpm_path) $(pkg_path)

%: $$(call short-name-to-rpm-path,$$*);


###############################################################################
# Manage dependencies between packages
###############################################################################
# Get paths to required packages for each rpm package target
define pkg-dep-list
	$(foreach dep,$(1),$(addsuffix -install,$(addprefix $(rpm-dir)/,$(call rpm-name,$(dep)))))
endef

%-requires: $$(call pkg-dep-list,$$($$*-requires-list)) ;


###############################################################################
# Install
###############################################################################
install: $(install-targets) ;

# TODO: Can $(rpm-dir) replace start of target?
RPMS/x86_64/%-install: $$(call rpm-path,$$(call pkg-name,$$*));
	@echo -n Checking for installation of $*:" "; \
	$(rpml) -qa | grep $(call pkg-name,$*);   \
	ret=$$?; \
	if [[ "$${ret}" == "1" ]]; then		 \
		echo -e ' No\n'Installing $(addprefix $(rpm-dir)/,$*)...;\
		$(rpml) -v --install $(addprefix $(rpm-dir)/,$*); \
	fi

# install targets for package short names (without version numbers)
%-install: $$(addsuffix -install,$$(call short-name-to-rpm-path,$$*)) ;

###############################################################################
# Uninstall
###############################################################################
.PHONY: uninstall
uninstall: uninstall_init $$(foreach pkg,$$(packages),$$(addsuffix -uninstall,$$(call pkg-name-to-short-name,$$(pkg))))
	@echo -e "Done\n"

.PHONY: uninstall_init
uninstall_init:
	@echo "Uninstalling packages..."

%-uninstall:
	@ $(rpml) -qa | grep $(call pkg-name,$*);   \
	ret=$$?; \
	if [[ "$${ret}" == "1" ]]; then \
		echo Package $* does not exist; \
	else \
		$(rpml) --nodeps -ve $*; \
	fi

###############################################################################
# Cleanup
###############################################################################
.PHONY: clean
clean: clean_build_dir clean_build_root;

.PHONY: clean_rpms
clean_rpms:
	@echo Removing RPMs...
	@rm -fv $(rpm-dir)/*
	@rm -fv $(srpm-dir)/*
	@echo -e Done'\n'

.PHONY: clean_build_dir
clean_build_dir:
	@echo Cleaning build directory...
	$(call remove-large-dir,$(build-dir))
	@echo -e Done'\n'

.PHONY: clean_build_root
clean_build_root:
	@echo Cleaning build root...
	$(call remove-large-dir,$(build-root))
	@echo -e Done'\n'

.PHONY: distclean
distclean: uninstall clean clean_rpms


###############################################################################
# Help Text
###############################################################################
help:
	@echo "*"
	@echo "* GCC toolchain builder and RPM packager"
	@echo "*"
	@echo ""
	@echo "Include packages:"
	@echo "  newlib, gcc-bootstrap, libgcc-bootstrap, binutils, mpc, mpfr, gmp"
	@echo ""
	@echo "Targets: "
	@echo "  all - Build and install all packages."
	@echo "  <package> - Build a specific package."
	@echo "  <package>-install - Build and install a specific package to the rpm database."
	@echo "  <package>-uninstall - Uninstall a specific package from rpm database."
	@echo "  uninstall - Uninstall all packages from rpm database."
	@echo "  clean - Clean build directory and buildroot directory."
	@echo "  distclean - Same as clean but also remove generated RPMs and uninstall"
	@echo "              all packages from the rpm database."
	@echo ""
