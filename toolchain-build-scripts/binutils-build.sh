PREFIX="/home/kyle/programs/arm-none-eabi/"
SRC_DIR=$(dirname ${BASH_SOURCE})
cd $SRC_DIR && cd ../

if [[ ($1 -eq 0) || ("x${1}" == "x") ]]
then
    old_build_items=$(ls -1 | grep -v _keep | tr '\n' ' ')
    if [[ ! ("x${old_build_items}" == "x") ]]
    then
        rm -r ${old_build_items}
    fi

    # threads, initfini, libiberty
    ../binutils-2.32/configure \
        --prefix=$PREFIX \
        --target=arm-none-eabi \
        --with-lib-path="${PREFIX}lib/gcc/arm-none-eabi/11.0.0:${PREFIX}arm-none-eabi/lib:${PREFIX}lib" \
        --disable-nls


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
