# testing with-multi-lib on phase 1
# testing disable-multilib on phase 1
# building phase 2, enable-multilib

#PATH=/home/kyle/programs/arm-none-eabi/bin:$PATH
#echo $PATH
# CFLAGS="$CFLAGS -mcpu=cortex-a8 -mfloat-abi=hard -mfpu=neon"
# ../gcc/configure --prefix=/home/kyle/programs/arm-none-eabi-hard \
    # 		 --target=arm-none-eabihf \
    #          --with-cpu=cortex-a8 --with-fpu=neon\
    # 		 --enable-languages=c,c++ \
    # 		 --disable-hosted-libstdcxx \
    # 		 --with-newlib \
    #          --disable-multilib \

    # phase 1, libssp

SRC_DIR=$(dirname ${BASH_SOURCE})
cd $SRC_DIR && cd ../

if [[ ($1 -eq 0) || ("x${1}" == "x") ]]
then
    old_build_items=$(ls -1 | grep -v _keep | tr '\n' ' ')
    if [[ ! ("x${old_build_items}" == "x") ]]
    then
        rm -r ${old_build_items}
    fi

    if [[ ($2 -eq 0) ]]
    then
        ../gcc/configure \
            --prefix=/home/kyle/programs/arm-none-eabi-hard \
            --target=arm-none-eabihf \
            --enable-languages=c \
            --enable-multilib \
            --with-multilib-list=@profile \
            --without-headers \
            --disable-libssp
    elif [[ ($2 -eq 1) ]]
    then
        ../gcc/configure \
            --prefix=/home/kyle/programs/arm-none-eabi-hard \
            --target=arm-none-eabihf \
            --enable-languages=c,c++ \
            --enable-multilib \
            --with-multilib-list=@profile \
            --enable-lto \
            --with-newlib \
            --disable-hosted-libstdcxx \
            --disable-libssp \
            --disable-tm-clone-registry
    fi
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

#make -j9
# 		 --disable-libquadmath \
    # 		 --disable-libada \
    # 		 --disable-hosted-libstdcxx \
    # 		 --disable-liboffloadmic \
    # 		 --disable-libstdcxx \

    # 		 --with-newlib \
    # 		 --disable-hosted-libstdcxx \


    # ../gcc/configure --prefix=/home/kyle/programs/arm-none-eabi \
    # 		     --target=arm-none-eabi \
    # 		     --enable-languages=c \
    # 		     --with-build-time-tools=/home/kyle/programs/arm-none-eabi/arm-none-eabi/bin \
    # 		 --disable-libquadmath \
    # 		 --disable-libssp \

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

    # ../gcc/configure --prefix=/home/kyle/programs/arm-none-eabi \
    # 		 --target=arm-none-eabi \
    # 		 --enable-languages=c \
    # 		 --with-build-sysroot=/home/kyle/programs/arm-none-eabi \
    # 		 --disable-libssp \
    # 		 --disable-libquadmath \
    # 		 --disable-libada \
    # 		 --disable-hosted-libstdcxx \
    # 		 --disable-liboffloadmic \
    # 		 --disable-libstdcxx \
