#!/bin/bash

###############################################################################
# Parse Arguments
###############################################################################
source /etc/profile.d/profile_script.sh
gather_args $@

###############################################################################
# Cleanup functions
###############################################################################
function remove_packages {
    packages=$($rpml -qa)
    for pack in $packages
    do
        $rpml -ve $pack
    done
}

function remove_rpms {
    rm -fvr ${rpmdir}/*
}

function remove_large_dir {
    if [[ "x$1" == "x" ]]; then exit; fi
    dir=$(readlink -f $1)
    for f in $(ls $dir)
    do
        if [[ -d $dir/$f ]]
        then
            rm -fr $dir/${f}/*
            rm -frv $dir/$f
        else
            rm -fv $dir/$f
        fi
    done
}

###############################################################################
# Defines
###############################################################################
rpmdbdir=/home/builder/rpmbuild/rpmdb
buildroot=/home/builder/rpmbuild/BUILDROOT
rpmdir=/home/builder/rpmbuild/RPMS/x86_64
srpmdir=/home/builder/rpmbuild/SRPMS
builddir=/home/builder/rpmbuild/BUILD

rpml="rpm --dbpath=$rpmdbdir"

###############################################################################
# Handle --reset option
###############################################################################
if [[ ("x$_flag_reset" == "xall") ]]
then
    remove_packages
    remove_rpms
    exit;
elif [[ ("x$_flag_reset" == "xdb") ]]
then
    remove_packages
    exit;
elif [[ ("x$_flag_reset" == "xrpms") ]]
then
    remove_rpms
    exit;
elif [[ "x$_flag_reset" != "x" ]]
then
    echo "reset <all, db, rpms>"
    exit
fi

###############################################################################
# Handle clean flag
###############################################################################
if [[ "x$_flag_clean" == "xtrue" ]]
then
    rm -frv $srpmdir/*
    rm -frv $rpmdir/*
    remove_large_dir $buildroot
    remove_large_dir $builddir
    exit
elif [[ ! -z "${_flag_clean+x}" ]]
then
    echo "clean isn't an option, its a flag"
    exit
fi

###############################################################################
# Build and install binutils
###############################################################################
binutils_source=$(ls ${rpmdir} | grep binutils)
if [[ "x$binutils_source" == "x" ]]
then
    rpmbuild --define="install_prefix ${buildroot}" \
        --nodebuginfo -bb \
        SPECS/binutils.spec
fi

$rpml -q binutils > /dev/null
if [[ "$?" == "1" ]]
then
    echo "Installing binutils..."
    $rpml --install --nodeps ${rpmdir}/binutils*
fi

###############################################################################
# Build and install gcc-bootstrap
###############################################################################
gcc_source=$(ls ${rpmdir} | grep gcc)
if [[ "x$gcc_source" == "x" ]]
then
    rpmbuild --define="install_prefix ${buildroot}" \
        --nodebuginfo -ba \
        SPECS/gcc-bootstrap.spec
fi

$rpml -q gcc_bootstrap > /dev/null
if [[ "$?" == "1" ]]
then
    echo "Installing gcc_bootstrap..."
    $rpml --install --nodeps ${rpmdir}/gcc-bootstrap*
fi
