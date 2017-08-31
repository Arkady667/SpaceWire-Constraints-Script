# coding=utf-8
# python2
# Google naming style https://google.github.io/styleguide/pyguide.html

import sys
import subprocess
import time
import os.path
import datetime

start_time = datetime.datetime


spw_timing_report = []
script_path = r"C:\Users\aczuba\TCL\spw_script"
stb_in_name = "iSpw0Stb"
dat_in_name = "iSpw0Dat"
reg_filter = r"*r.do*"


def tcl_script(script_path, stb_in_name, dat_in_name, reg_filter, error_flag):

    spw_timing_report_modtime = os.path.getmtime(script_path + r"\report_spw_timing.log")
    # Run TCL script report_spw_timing.tcl
    subprocess.call('designer "SCRIPT:report_spw_timing.tcl {0} {1} {2} {3}" "SCRIPT_DIR:{4}" "LOGFILE:report_spw_timing.log"'.format(stb_in_name, dat_in_name, reg_filter, error_flag, script_path), shell=False)
    # Check that report_spw_timing.tcl exist. If not wait until TCL generate log (only if script is launched first time)
    while not os.path.isfile(script_path+r"\report_spw_timing.log"):
        time.sleep(1)
    # Waits until report_spw_timing.log modification time will be later than script execution time.
    # Makes sure that proper log file will be read (not previous)
    while start_time >= spw_timing_report_modtime:
        time.sleep(1)
    # Reads report_spw_timing.log
    try:
        f = open('report_spw_timing.log', mode="rt")
        for line in f.readlines():
            if line =="iSpwStbToCLK":
                while line != "iSpwDatToReg":
                    if line.find("Path") == (-1):

                    # Deletes large number of spaces and replace with one space and assign data to pin_one_space.
                    line_two_space = "  ".join(line.split())
                    # Separates pin parameters and save each one of them as one list element (pin_data).
                    line_data = line_two_space.split(" ")
                    add_path_strobe()

                add_path_data()
                pin_one_space = " ".join(pin.split())
                pin_data = pin_one_space.split(" ")
                continue
        f.close()
    except Exception as error:
        print("Could not read file")
        print(error)


def add_path_strobe(name, ffrom, to, delay, slack, arrival, required):


def add_path_data(name, ffrom, to, delay, slack, arrival, required):


def main(cript_path, stb_in_name, dat_in_name, reg_filter, error_flag):


if __name__ == "__main__":
    main(sys.argv[1])