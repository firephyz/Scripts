###############################################################################
# Build Makefile
###############################################################################
# TODO What rules require the .SECONDEXPANSION directive?

###############################################################################
# Defines
###############################################################################
arch               := x86_64
os_version         := fc32
rpm-release-suffix := $(os_version).$(arch)
packages           := newlib-3.2.0-1 \
                      gcc-bootstrap-10.1.0-1 \
											binutils-2.34-1

# package dep lists for each package
newlib-3.2.0-1-requires-list         := gcc-bootstrap-10.1.0-1 binutils-2.34-1
gcc-bootstrap-10.1.0-1-requires-list := binutils-2.34-1
binutils-2.34-1-requires-list        :=

rpm-db-dir	    := ./rpmdb
build-root	    := ./BUILDROOT
rpm-dir		    := ./RPMS/x86_64
srpm-dir	    := ./SRPMS
build-dir	    := ./BUILD

# select correct db to update when installing packages
rpml			:= rpm --dbpath=$(shell readlink -f $(rpm-db-dir))

###############################################################################
# Utilities
###############################################################################
# get full RPM path from pkg name
define rpm-path
	$(addprefix $(rpm-dir)/,$(call rpm-name,$(1)))
endef
# get full RPM name from pkg name
define rpm-name
	$(addsuffix .$(rpm-release-suffix).rpm, $(1))
endef
# get pkg-name from full RPM name
define pkg-name
	$(shell echo $(1) | sed "s/\.${rpm-release-suffix}\.rpm//")
endef
# get package full rpm name from package short name without version numbers
define short-name-to-rpm-path
	$(call rpm-path,$(shell echo $(packages) | tr ' ' '\n' | grep $(1)))
endef
# get package short name from package name
define pkg-name-to-short-name
    $(shell echo $(1) | sed -r "s/([-\.][0-9]+)+//")
endef
# turn make target pkg stem into pkg-name
define stem-to-pkg-name
	$(shell echo $(1) | sed "s/\.${rpm-release-suffix}//")
endef
# turn make target pkg stem into pkg-name
define stem-to-rpm-name
	$(call rpm-name,$(call stem-to-pkg-name,$(1)))
endef
# return path to spec file for given package name
define spec-path
	$(addsuffix .spec,$(addprefix SPECS/,$(1)))
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
all: build ;

build: $(rpm-targets);
###############################################################################
# Build each rpm package
###############################################################################
# Register <pkg>-requires target and spec files in dep list
define package-prereqs
	$(call spec-path,$(1)) |\
	$(addsuffix -requires,$(1))
endef

.SECONDEXPANSION:
RPMS/x86_64/%.rpm: $$(call package-prereqs,$$(call stem-to-pkg-name,$$*))
	@echo Building $(call stem-to-pkg-name,$*)...;
	@rpmbuild --define="install_prefix $(shell readlink -f $(build-root))" \
			 --define="num_cpus $(JFLAG)" --dbpath=$(shell readlink -f $(rpm-db-dir)) \
			 $(rpm-build-debuginfo) $(rpm-build-clean-after) \
			 -bb $(call spec-path,$(call stem-to-pkg-name,$*));

###############################################################################
# Manage dependencies between packages
###############################################################################
# Get paths to required packages for each rpm package target
define pkg-dep-list
	$(foreach dep,$(1),$(addsuffix -install,$(addprefix $(rpm-dir)/,$(call rpm-name,$(dep)))))
endef
#.SECONDEXPANSION:
%-requires: $$(call pkg-dep-list,$$($$*-requires-list)) ;


###############################################################################
# Install / Uninstall
###############################################################################
install: $(install-targets) ;

# TODO: Can $(rpm-dir) replace start of target?
# .SECONDEXPANSION:
RPMS/x86_64/%-install: $$(call rpm-path,$$(call pkg-name,$$*))
	@echo -n Checking for installation of $*:" "; \
	$(rpml) -qa | grep $(call pkg-name,$*);   \
	ret=$$?; \
	if [[ "$${ret}" == "1" ]]; then		 \
		echo -e ' No\n'Installing...;\
		$(rpml) --install $(addprefix $(rpm-dir)/,$*); \
	fi

# install targets for package short names (without version numbers)
# .SECONDEXPANSION:
%-install: $$(addsuffix -install,$$(call short-name-to-rpm-path,$$*)) ;

.PHONY: uninstall
uninstall: $$(foreach pkg,$$(packages),$$(addsuffix -uninstall,$$(call pkg-name-to-short-name,$$(pkg)))) ;

%-uninstall:
	@ $(rpml) -qa | grep $(call pkg-name,$*);   \
	ret=$$?; \
	if [[ "$${ret}" == "1" ]]; then \
		echo Package $* does not exist; \
	else \
		$(rpml) -ve $*; \
	fi

###############################################################################
# Cleanup
###############################################################################
.PHONY: clean
clean: clean_build_dir ;

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

.PHONY: distclean
distclean: clean clean_rpms uninstall
