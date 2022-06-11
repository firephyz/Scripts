#PREFIX="/home/kyle/programs/arm-none-eabi/"
#SRC_DIR=$(dirname ${BASH_SOURCE})
#cd $SRC_DIR && cd ../
# ${prefix}lib

prefix=
sourcedir=
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

${sourcedir}/configure \
    --prefix=${prefix} \
    --target=arm-none-eabi \
    --with-lib-path="${prefix}lib/gcc/arm-none-eabi/11.0.0:${prefix}arm-none-eabi/lib" \
    --disable-nls
