# Simple argument parser for small bash scripts.
# Handles '-<flag>', '--<flag>', '<option>' forms.
# Flags are set as [_flag_<flag-ident>=value].
# Options are set as [_flag_<option-ident>=]

_debug=1

gather_args() {
    flags=
    args=
    _flags_rest=

    curflag=
    echo $@
    echo "$@"
    for arg in $(echo $(printf "%q " "$@"))
    do
	    if [[ ("x${curflag}" == "x") ]]
	    then
                if [[ ("${arg::1}" == "-") ]]
                then
                    if [[ ! -z $_debug ]]; then
                        echo $(printf "FLAG: %s" $arg)
                    fi
                    # Register flag in flag list
		            flag=$(echo $arg | sed 's/-[-]\{0,1\}\(.*\)/\1/')
		            flags="${flag} ${flags}"
                    # set curflag for storing flag's value
		            curflag=$flag
                else
                    if [[ ! -z $_debug ]]; then
                        echo $(printf "Opt: %s" $arg)
                    fi
                    # Store option
		            _flags_rest="${arg} ${_flags_rest}"
                fi
	    else
            if [[ ! -z $_debug ]]; then
                echo $(printf "ARG <%s>: %s" $curflag $arg)
            fi
            # Set flag ident to flag value
	        eval $curflag=$arg
	        curflag=
	    fi
    done

    # Export all flag, value pairs
    for f in $flags
    do
	    eval export _flag_$f=${!f}
    done

    # Export option flags
    for r in $_flags_rest
    do
	    eval export _flag_$r=
    done
}
