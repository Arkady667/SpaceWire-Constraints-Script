#! /bin/env tclsh

################# TCL TEST  ##############################
# new_design -name "prepi" -family "ProASIC3E"
# save_design {prepi.adb}
# puts {TEST}
# close_design 
######################################################
# running from cmd (without error handling option)
# >designer "SCRIPT:spw.tcl iSpw0Stb iSpw0Dat *r.do*" "SCRIPT_DIR:<script path>" "LOGFILE:<log file name.log"
# iSpw0Stb - Strobe input pin
# iSpw0Dat - Data input pin
# *r.do* - filter to input registers 
# argv3 - error handling option:
#					  [int] 1 - ON
#	 			OTHER or NONE - OFF
# running from cmd (with error handling option)
# designer "SCRIPT:spw.tcl iSpw0Stb iSpw0Dat *r.do* 1" "SCRIPT_DIR:C:\Users\aczuba\TCL\spw_script" "LOGFILE:spw_report.log"
######################################################
# Assign global argv variables to new variables
set argv0 [lindex $::argv 0]
set argv1 [lindex $::argv 1]
set argv2 [lindex $::argv 2]
set argv3 [lindex $::argv 3]

# Variables which contain names of sets
set setNameStb {iSpwDatToReg}
set setNameDat {iSpwStbToCLK}

## Replaced by argv
# set setSourceStb { iSpw0Stb } 
# set setSourceDat { iSpw0Dat } 
# set setSink { *r.do* }

# Print argv list values to check correctness of argv content
puts "$argv0 is argv0"
puts "$argv1 is argv1"
puts "$argv2 is argv2"
puts "$argv3 is argv3"

# Variable which contain path to existing Designer design (.adb)
set designFileTest {C:\Users\aczuba\TCL\spw_script\P3_DPU.adb} 
set designFile {C:\DPU FPGA repo v2\alllib\designs\P3CCB_RT\P3_DPU.adb}
puts $designFile


proc add_set {fromStb fromDat to errorFlag} {
if {0} {\
	Procedure adds new custom set of paths to SmartTime User Sets \

	Args:\
		fromStb - name of SpW Strobe input pin\
		fromDat - name of SpW Data input pin\
		to - input registers filter name \
		errorFlag - error handlingflag value\

	return: None
}

	st_create_set -name $::setNameStb -source  $fromStb -sink  $to
	st_create_set -name $::setNameDat -source $fromDat -sink  $to
	puts "##########\nSETS ADDED\n##########"
	if {$errorFlag == 1} {
		if  { [catch {st_create_set -name  $::setNameStb -source  $fromStb -sink  $to }] || [catch {st_create_set -name $setNameDat -source $fromDat -sink  $to }]} {
			puts "Failed to set paths \n $::errorInfo \n"
			# Handle Failure 
		} 
	}
	st_commit
}


proc list_set {errorFlag} {
if {0} {\
	Procedure write to log file new sets timings\

	Args:\
		errorFlag - error handlingflag value\

	return: None
}

	puts "#################\nPATH LIST - START\n#################"
	puts "\n------------\niSpwStbToCLK\n------------"
	st_list_paths -set $::setNameStb
	puts "\n------------\niSpwDatToReg\n------------"
	st_list_paths -set $::setNameDat 
	puts "###############\nPATH LIST - END\n###############"
	if {$errorFlag == 1} {
		if  { [catch st_list_paths -set $::setNameStb] || [catch st_list_paths -set $::setNameDat]} {
			puts "Failed to read sets \n $::errorInfo \n"
			# Handle Failure 
		}
	}
	
	st_commit
}


proc clear_set {errorFlag} {
if {0} {\
	Procedure clears added new sets of paths from SmartTime User Sets \

	Args:\
		errorFlag - error handlingflag value\

	return: None
}

	st_remove_set -name $::setNameStb
	st_remove_set -name $::setNameDat
	puts "############\nSETS DELETED\n############"
	if {$errorFlag == 1} {
		if {[catch {st_remove_set -name $::setNameStb}] || [catch {st_remove_set -name $::setNameDat}]} {
			puts "Path sets $::setNameStb or $::setNameDat doesn't exist. Will be created new path\n $::errorInfo \n"
			# Handle Failure 
		} 
	}
	st_commit
}

proc main_exec {fromStb fromDat to errorFlag} {
if {0} {\
	Main procedure. Controls procedure flow\

	Args:\
		fromStb - name of SpW Strobe input pin\
		fromDat - name of SpW Data input pin\
		to - input registers filter name \
		errorFlag - error handlingflag value\

	return: None
}	
	add_set $fromStb $fromDat $to $errorFlag
	list_set $errorFlag
	clear_set $errorFlag
	# gen_report 

}

open_design $designFileTest
	if  { [catch { open_design $designFileTest }]} { 
		puts "Failed to open design \n $::errorInfo \n"
		# Handle Failure 
	} else { 
		puts "##########################\nDESIGN OPENED SUCCESSFULLY\n##########################"
		# Proceed to further preocssing 
	} 

main_exec $argv0 $argv1 $argv2 $argv3
st_commit
save_design {P3_DPU.adb}
close_design