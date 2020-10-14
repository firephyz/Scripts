#!/bin/bash

PREFIX="/home/kyle/programs/arm-none-eabi-hard/"
PATH="${PREFIX}bin:$PATH"

SRC_DIR=$(dirname ${BASH_SOURCE})
cd $SRC_DIR && cd ../

if [[ ($1 -eq 0) || ("x${1}" == "x") ]]
then
    rm -r `ls -1 | grep -v _keep`

    REG_FINI=--enable-newlib-register-fini
    #MB_SUPPORT=--enable-newlib-mb
    ATEXIT_DYN_ALLOC=--disable-newlib-atexit-dynamic-alloc # is already disabled if no syscalls?
    GLOBAL_STDIO=--enable-newlib-global-stdio-streams
    GLOBAL_ATEXIT=--enable-newlib-global-atexit
    NANO_MALLOC=--enable-newlib-nano-malloc
    OPT_SPACE=--enable-target-optspace
    NO_SYSCALLS=--disable-newlib-supplied-syscalls

    FLAGS=$REG_FINI $ATEXIT_DYN_ALLOC $GLOBAL_STDIO $GLOBAL_ATEXIT $NANO_MALLOC \
      $OPT_SPACE $NO_SYSCALLS


    ../newlib/configure \
        --prefix=$PREFIX \
        --target=arm-none-eabihf \
        --enable-multilib \
        $FLAGS


        #        --with-arch=armv7-a/armv7-a+fp/armv7-a+fp.sp --with-fpu=neon \
elif [[ ($1 -eq 1) ]]
then
    num_threads=9
    if [[ ! ("x${2}" == "x") ]]
    then
        num_threads=$2
    fi
    make -j${num_threads}
elif [[ ($1 -eq 2) ]]
then
    make install
fi
#		    --with-build-time-tools=/home/kyle/programs/arm-none-eabi/bin

# --disable-hosted-libstdcxx \
    # --disable-libstdcxx \

    # --prefix=/home/kyle/programs/arm-none-eabi \
    #     --target=arm-none-eabi \
    #     --with-newlib \
    #     --enable-languages=c \
    #     --with-build-sysroot=/home/kyle/programs/arm-none-eabi \
    #     --disable-libssp \
    #     --disable-libquadmath \
    #     --disable-libada \
    #     --disable-libstdcxx \
    #     --without-libbacktrace \

    # --enable-host-shared \
    # --enable-stage1-languages=c,c++ \
    # --enable-ld \
    # --enable-lto \
    # --disable-bootstrap \
    # --disable-objc-gc \
    # --disable-vtable-verify \
    # --disable-multilib \
    # --disable-hosted-libstdcxx \
    # --disable-as-accelerator \
    # --disable-gold \
    # --disable-compressed-debug-sections \
    # --disable-libquadmath \
    # --disable-libada \
    # --disable-libssp \
    # --disable-liboffloadmic \
    # --disable-libstdcxx \
    # --disable-libbacktrace \
    # --with-newlib \
    # --without-libatomic \
    # --without-libbacktrace \
    # --with-build-sysroot=/usr/arm-none-eabi
# --enable-static \
    # --disable-shared \
