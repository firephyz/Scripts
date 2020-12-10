################################################################################
# Pin mapping
################################################################################
set PIN_MAP_ARRAY {
  { PIN_SYS_CLK          M6    }
  { PIN_SRST             SRST  }
  { PIN_PS_ERR_OUT       P17   }
  { PIN_PS_ERR_STAT      M20   }
  { PIN_PS_DONE          M21   }
  { PIN_STATUS           AA13  }
  { PIN_ARSTN            R17   }
  { PIN_TMS              N21   }
  { PIN_TCK              R19   }
  { PIN_TDI              R18   }
  { PIN_TDO              T21   }
  { PIN_UART0_RXD        AH10  }
  { PIN_UART0_TXD        AB10  }
  { PIN_DEBUG_UART_RXD   L17   }
  { PIN_DEBUG_UART_TXD   H17   }
}

set PIN_MAP [dict create {*}[concat {*}$PIN_MAP_ARRAY]]

################################################################################
# Create new project
################################################################################
set TARGET_PART xazu3eg-sfvc784-1-i

proc new_proj {proj_name path} {
    global TARGET_PART
    if {$path == ""} {
	set path /home/kyle/dev/xilinx/$proj_name
    }
    create_project $proj_name $path -part $TARGET_PART
}

################################################################################
# IP management
################################################################################
set IP_DIR /home/kyle/dev/xilinx/ip/

proc install_ip {ipname} {
    global IP_DIR
    set NULL {}
    # Setup variables
    set ip_core [ipx::find_open_core [append NULL user.org:user: $ipname :1.0]]
    set NULL {}
    set ip_core_dir [append NULL [get_property ROOT_DIRECTORY $ip_core] /]
    puts $ip_core_dir

    # Clean core ip directory
    puts [format "Cleaning IP directory %s" $ip_core_dir]
    set files {}
    catch {global files; set files [glob -directory $ip_core_dir *]}
    foreach f $files {
    	file delete -force $f
    }

    # Package ip core
    puts [format "Packing IP '%s'..." $ipname]
    set ip_rev [get_property CORE_REVISION $ip_core]
    set_property core_revision [expr $ip_rev + 1] $ip_core
    ipx::create_xgui_files $ip_core
    ipx::update_checksums $ip_core
    ipx::check_integrity $ip_core
    ipx::save_core $ip_core
    update_ip_catalog -rebuild -repo_path $ip_core_dir

    # Create archive
    puts "Creating IP archive..."
    set NULL {}; set NULL1 {}
    set zip_path [append NULL1 $ip_core_dir [append NULL $ipname _ $ip_rev .zip]]
    ipx::check_integrity -quiet $ip_core
    ipx::archive_core $zip_path $ip_core

    # Installing IP
    set NULL {}
    set install_dir [append NULL $IP_DIR $ipname /]
    if {[file exists $install_dir]} {
    	file delete -force $install_dir
    }
    exec unzip -d $install_dir $zip_path
}







# set PIN_SYS_CLK             M6
# set PIN_SRST                N19
#
# set PIN_PS_ERR_OUT          P17
#
# set PIN_PS_ERR_STAT         M20
#
# set PIN_PS_DONE             M21
#
# set PIN_STATUS              AA13
#
# set PIN_ARSTN               R17
#
# set PIN_TMS                 N21
# set PIN_TCK                 R19
# set PIN_TDI                 R18
# set PIN_TDO                 T21
#
# set PIN_UART0_RXD           AH10
# set PIN_UART0_TXD           AB10
# set PIN_DEBUG_UART_RXD      L17
# set PIN_DEBUG_UART_TXD      H17

# set PIN_MAP_ARRAY {
#   { PIN_SYS_CLK          M6    }
#   { PIN_SRST             SRST  }
#   { COMMENT # PS_ERROR_OUT, hardware error? }
#   { PIN_PS_ERR_OUT       P17   }
#   { COMMENT # PS_ERROR_STATUS, software error? }
#   { PIN_PS_ERR_STAT      M20   }
#   { COMMENT # PS_DONE }
#   { PIN_PS_DONE          M21   }
#   { COMMENT # System_status_indicator, OK# System_status_indicator, OK }
#   { PIN_STATUS           AA13  }
#   { PIN_ARSTN            R17   }
#   { PIN_TMS              N21   }
#   { PIN_TCK              R19   }
#   { PIN_TDI              R18   }
#   { PIN_TDO              T21   }
#   { PIN_UART0_RXD        AH10  }
#   { PIN_UART0_TXD        AB10  }
#   { PIN_DEBUG_UART_RXD   L17   }
#   { PIN_DEBUG_UART_TXD   H17   }
# }
