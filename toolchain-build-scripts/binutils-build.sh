#PREFIX="/home/kyle/programs/arm-none-eabi/"
#SRC_DIR=$(dirname ${BASH_SOURCE})
#cd $SRC_DIR && cd ../
# ${prefix}lib

prefix=
sourcedir=
action=
rest=

curflag=
for arg in $@
do
    if [[ ("x${curflag}" == "x") ]]
    then
        if [[ ("${arg::1}" == "-") ]]
        then
            curflag=${arg/-/}
        else
            rest="${rest} ${arg}"
        fi
    else
        declare -n curflag
        curflag=$arg
        declare +n curflag
        curflag=
    fi
done

prefix=$(readlink -f $prefix)
sourcedir=$(readlink -f $sourcedir)

if [[ ("${action}" == "configure") ]]
then
    ${sourcedir}/configure \
        --prefix=${prefix} \
        --target=arm-none-eabi \
        --with-lib-path="${prefix}lib/gcc/arm-none-eabi/11.0.0:${prefix}arm-none-eabi/lib" \
        --disable-nls

elif [[ ("${action}" == "build") ]]
then
    num_threads=9
    if [[ ! ("x${rest}" == "x") ]]
    then
        num_threads=${action}
    fi
    make -j${num_threads}

elif [[ (${action} -eq "install") ]]
then
    make install
fi
