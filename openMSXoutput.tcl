# OpenMSX Tcl script to send the MSX text responses to stderr

debug set_bp 0x18 {[pc_in_slot 0 0]} {output::char}
debug set_bp 0xa2 {[pc_in_slot 0 0]} {output::char}

namespace eval output {
  proc char {} {
		puts -nonewline stderr [format %c [reg A]]
  }
}