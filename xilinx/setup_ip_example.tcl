puts {SETUP}
ipx::package_project -root_dir /home/kyle/dev/xilinx/test/output -vendor user.org -library user -taxonomy /UserIP -module test_core -import_files

puts {FILE GROUPS}
ipx::remove_file_group xilinx_anylanguagebehavioralsimulation [ipx::find_open_core user.org:user:test_core:1.0]

puts {PARAMETERS}
ipx::add_user_parameter SEED [ipx::find_open_core user.org:user:test_core:1.0]
set_property value_resolve_type user [ipx::get_user_parameters SEED -of_objects [ipx::find_open_core user.org:user:test_core:1.0]]
ipgui::add_param -name {SEED} -component [ipx::current_core]
set_property display_name {Seed} [ipgui::get_guiparamspec -name "SEED" -component [ipx::current_core] ]
set_property widget {hexEdit} [ipgui::get_guiparamspec -name "SEED" -component [ipx::current_core] ]
set_property value 0x1234 [ipx::get_user_parameters SEED -of_objects [ipx::find_open_core user.org:user:test_core:1.0]]
set_property value_bit_string_length 16 [ipx::get_user_parameters SEED -of_objects [ipx::find_open_core user.org:user:test_core:1.0]]
set_property value_format bitString [ipx::get_user_parameters SEED -of_objects [ipx::find_open_core user.org:user:test_core:1.0]]

ipx::add_user_parameter HAS_TEST [ipx::find_open_core user.org:user:test_core:1.0]
set_property value_resolve_type user [ipx::get_user_parameters HAS_TEST -of_objects [ipx::find_open_core user.org:user:test_core:1.0]]
ipgui::add_param -name {HAS_TEST} -component [ipx::current_core]
set_property display_name {Has Test} [ipgui::get_guiparamspec -name "HAS_TEST" -component [ipx::current_core] ]
set_property widget {checkBox} [ipgui::get_guiparamspec -name "HAS_TEST" -component [ipx::current_core] ]
set_property value false [ipx::get_user_parameters HAS_TEST -of_objects [ipx::find_open_core user.org:user:test_core:1.0]]
set_property value_format bool [ipx::get_user_parameters HAS_TEST -of_objects [ipx::find_open_core user.org:user:test_core:1.0]]

ipx::add_file_group -type utility {} [ipx::find_open_core user.org:user:test_core:1.0]

file copy /home/kyle/dev/xilinx/test/test.gen/sources_1/bd/test_core/hw_handoff/test_core_bd.tcl /home/kyle/dev/xilinx/test/output/src
ipx::add_file /home/kyle/dev/xilinx/test/output/src/test_core_bd.tcl [ipx::get_file_groups xilinx_utilityxitfiles -of_objects [ipx::find_open_core user.org:user:test_core:1.0]]
set_property type tclSource [ipx::get_files src/test_core_bd.tcl -of_objects [ipx::get_file_groups xilinx_utilityxitfiles -of_objects [ipx::find_open_core user.org:user:test_core:1.0]]]
file copy /home/kyle/dev/xilinx/test/setup_ip.tcl /home/kyle/dev/xilinx/test/output/src
ipx::add_file /home/kyle/dev/xilinx/test/output/src/setup_ip.tcl [ipx::get_file_groups xilinx_utilityxitfiles -of_objects [ipx::find_open_core user.org:user:test_core:1.0]]
set_property type tclSource [ipx::get_files src/setup_ip.tcl -of_objects [ipx::get_file_groups xilinx_utilityxitfiles -of_objects [ipx::find_open_core user.org:user:test_core:1.0]]]

puts {PORTS}
ipx::infer_bus_interface result xilinx.com:signal:data_rtl:1.0 [ipx::find_open_core user.org:user:test_core:1.0]
ipx::infer_bus_interface test xilinx.com:signal:data_rtl:1.0 [ipx::find_open_core user.org:user:test_core:1.0]
set_property enablement_dependency {$HAS_TEST = true} [ipx::get_bus_interfaces test -of_objects [ipx::find_open_core user.org:user:test_core:1.0]]

ipx::add_bus_parameter ASSOCIATED_BUSIF [ipx::get_bus_interfaces CLK.CLK -of_objects [ipx::find_open_core user.org:user:test_core:1.0]]

puts {MEMORY MAP}

puts {GUI}
ipgui::move_param -component [ipx::current_core] -order 0 [ipgui::get_guiparamspec -name "SEED" -component [ipx::current_core]] -parent [ipgui::get_pagespec -name "Page 0" -component [ipx::current_core]]
ipgui::move_param -component [ipx::current_core] -order 0 [ipgui::get_guiparamspec -name "HAS_TEST" -component [ipx::current_core]] -parent [ipgui::get_pagespec -name "Page 0" -component [ipx::current_core]]
ipgui::move_param -component [ipx::current_core] -order 1 [ipgui::get_guiparamspec -name "HAS_TEST" -component [ipx::current_core]] -parent [ipgui::get_pagespec -name "Page 0" -component [ipx::current_core]]

puts {}
