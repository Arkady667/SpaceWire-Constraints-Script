#! /bin/env tclsh

################# TCL TEST  ##############################
# new_design -name "prepi" -family "ProASIC3E"
# save_design {prepi.adb}
# puts {TEST}
# close_design 
######################################################
# running from cmd (without error handling option)
# >designer "SCRIPT:spw.tcl iSpw0Stb iSpw0Dat *r.do*" "SCRIPT_DIR:<script path>" "LOGFILE:<log file name.log"
# *iSpw0* - name of SpW inputs pins filter\
# *r.do* - filter to input registers - rising edge
# *nr.d* - filter to input registers - falling edge
# argv3 - error handling option:
#					  [int] 1 - ON
#	 			OTHER or NONE - OFF
# running from cmd (with error handling option)
# <path to>designer.exe "SCRIPT:spw.tcl iSpw0Stb iSpw0Dat *r.do* 1" "SCRIPT_DIR:C:\Users\aczuba\TCL\spw_script" "LOGFILE:spw_report.log"
# v.2 # <path to>designer.exe "SCRIPT:report_spw_timing.tcl *iSpw0* *r.do* *nr.d* 1" "SCRIPT_DIR:C:\Users\aczuba\PycharmProjects\SpaceWire-Constraints" "LOGFILE:spw_report_timing.log"
# <path to>C:\Microsemi\Libero_SoC_v11.8\Designer\bin\designer.exe
# C:\Microsemi\Libero_SoC_v11.8\Designer\bin\designer.exe "SCRIPT:report_spw_timing.tcl *iSpw0* *r.do* *nr.d* 1" "SCRIPT_DIR:C:\Users\aczuba\PycharmProjects\SpaceWire-Constraints" "LOGFILE:spw_report_timing.log"
######################################################
# Assign global argv variables to new variables
set argv0 [lindex $::argv 0]
set argv1 [lindex $::argv 1]
set argv2 [lindex $::argv 2]
set argv3 [lindex $::argv 3]
set argv4 [lindex $::argv 4]

# Variables which contain names of sets
set setNameDatR {iSpwDatToRegRise}
set setNameStbR {iSpwStbToClkRise}
set setNameDatF {iSpwDatToRegFall}
set setNameStbF {iSpwStbToClkFall}

## Replaced by argv
# set setSourceStb { iSpw0Stb } 
# set setSourceDat { iSpw0Dat } 
# set setSink { *r.do* }

# Print argv list values to check correctness of argv content
puts "$argv0 is argv0"
puts "$argv1 is argv1"
puts "$argv2 is argv2"
puts "$argv3 is argv3"
puts "$argv4 is argv4"

# Variable which contain path to existing Designer design (.adb)
set designFileTest {C:\Users\aczuba\PycharmProjects\SpaceWire-Constraints\P3_DPU.adb} 
set designFile {C:\DPU FPGA repo v2\alllib\designs\P3CCB_RT\P3_DPU.adb}
puts $designFile


proc add_set_rise {from to errorFlag} {
if {0} {\
	Procedure adds new custom set of paths to SmartTime User Sets with rising edge clock capture \

	Args:\
		from - name of SpW inputs pins filter\
		to - input registers filter name \
		errorFlag - error handlingflag value\

	return: None
}

	st_create_set -name $::setNameStbR -source  $from -sink  $to
	st_create_set -name $::setNameDatR -source $from -sink  $to
	puts "##########\nSETS ADDED\n##########"
	if {$errorFlag == 1} {
		if  { [catch {st_create_set -name  $::setNameStb -source  $fromStb -sink  $to }] || [catch {st_create_set -name $setNameDat -source $fromDat -sink  $to }]} {
			puts "Failed to set paths \n $::errorInfo \n"
			# Handle Failure 
		} 
	}
	st_commit
}

proc add_set_fall {from to errorFlag} {
if {0} {\
	Procedure adds new custom set of paths to SmartTime User Sets with falling edge clock capture \

	Args:\
		from - name of SpW inputs pins filter\
		to - input registers filter name \
		errorFlag - error handlingflag value\

	return: None
}

	st_create_set -name $::setNameStbF -source  $from -sink  $to
	st_create_set -name $::setNameDatF -source $from -sink  $to
	puts "##########\nSETS ADDED\n##########"
	if {$errorFlag == 1} {
		if  { [catch {st_create_set -name  $::setNameStbF -source  $from -sink  $to }] || [catch {st_create_set -name $setNameDatF -source $from -sink  $to }]} {
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
	puts "\n------------\niSpwStbToCLK-RISE\n------------"
	st_list_paths -set $::setNameStbR
	puts "\n------------\niSpwDatToReg-RISE\n------------"
	st_list_paths -set $::setNameDatR
	puts "\n------------\niSpwStbToCLK-FALL\n------------"
	st_list_paths -set $::setNameStbF
	puts "\n------------\niSpwDatToReg-FALL\n------------"
	st_list_paths -set $::setNameDatF  
	puts "###############\nPATH LIST - END\n###############"
	if {$errorFlag == 1} {
		if  { [catch st_list_paths -set $::setNameStbR] || [catch st_list_paths -set $::setNameDatR] || [catch st_list_paths -set $::setNameStbF] || [catch st_list_paths -set $::setNameDatF]} {
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

	st_remove_set -name $::setNameStbR
	st_remove_set -name $::setNameStbF
	st_remove_set -name $::setNameDatR
	st_remove_set -name $::setNameDatF
	puts "############\nSETS DELETED\n############"
	if {$errorFlag == 1} {
		if  { [catch st_list_paths -set $::setNameStbR] || [catch st_list_paths -set $::setNameDatR] || [catch st_list_paths -set $::setNameStbF] || [catch st_list_paths -set $::setNameDatF]}  {
			puts "Path sets $::setNameStb or $::setNameDat doesn't exist. Will be created new path\n $::errorInfo \n"
			# Handle Failure 
		} 
	}
	st_commit
}

proc main_exec {from toR toF errorFlag} {
if {0} {\
	Main procedure. Controls procedure flow\

	Args:\
		from - name of SpW inputs pins filter\
		toR - input registers filter name - rising edge\
		toF - input registers filter name - falling edge\
		errorFlag - error handlingflag value\

	return: None
}	
	add_set_rise $from $toR $errorFlag
	add_set_fall $from $toF $errorFlag
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

main_exec $argv1 $argv2 $argv3 $argv4
st_commit
save_design {P3_DPU.adb}
close_design