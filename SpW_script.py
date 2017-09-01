# coding=utf-8
# python2
# Google naming style https://google.github.io/styleguide/pyguide.html

import sys
import subprocess
import time
import os.path
import datetime

start_time = datetime.datetime

spw_timing_report_list = []

# tcl_script_path = r"C:\Users\aczuba\PycharmProjects\SpaceWire Constraints"
# stb_in_name = "iSpw0Stb"
# dat_in_name = "iSpw0Dat"
# reg_filter = r"*r.do*"
##
print sys.argv[2]


def tcl_script(tcl_script_path, stb_in_name, dat_in_name, reg_filter, error_flag):
    # line_one_space = []
    path_data = []
    path_number = 0
    stb_flag = 0
    dat_flag = 0
    start = 0

    # spw_timing_report_modtime = os.path.getmtime(tcl_script_path + r"\report_spw_timing.log")
    # Run TCL script report_spw_timing.tcl
    cmd = subprocess.Popen(
        r'C:\Microsemi\Libero_SoC_v11.8\Designer\bin\designer.exe "SCRIPT:report_spw_timing.tcl {0} {1} {2} {3}" "SCRIPT_DIR:{4}" "LOGFILE:report_spw_timing.log"'.format(
            stb_in_name, dat_in_name, reg_filter, error_flag, tcl_script_path), shell=True,
        cwd=r"C:\Microsemi\Libero_SoC_v11.8\Designer").wait()
    # Simple cmd command error handling
    if cmd == 0:
        print "report_spw_timing.log successfuly generated"
    else:
        print "report_spw_timing.log generation failed"
    # Check that report_spw_timing.tcl exist.
    while not os.path.isfile(tcl_script_path+r"\report_spw_timing.log"):
        print "report_swp_timing.log not found"
    # spw_timing_report_modtime = os.path.getmtime(tcl_script_path + r"\report_spw_timing.log")
    # Reads report_spw_timing.log
    try:
        f = open('spw_report.log', mode="rt")
        for line in f.readlines():
            # Looking for particular string in file, and takes flag up to parse Strobe part
            if line.find("iSpwStbToCLK") != (-1):
                stb_flag = 1
                # Simple flag to chceck that proper lines are analysed, and avoid useless lines
                start = 1
                continue
            # Looking for particular string in file, and takes flag up to parse Data part
            if line.find("iSpwDatToReg") != (-1):
                dat_flag = 1
                stb_flag = 0
                continue
            if start == 1:
                # Looking for "Path" in log. When finds, append path number to path_data
                if line.find("Path") != (-1):
                    path_number += 1
                    path_data.append(path_number)
                # if finds empty line - continue
                elif not line.strip():  # ignores empty line (whitespaces)
                    continue
                # Main parsing process
                else:
                    # Deletes large number of spaces and replace with one space and assign data to line_one_space.
                    line_one_space = " ".join(line.split())
                    # Separates pin parameters and save each one of them as one list element.
                    line_one_space = line_one_space.split(" ")
                    # Deletes "(ns):" from list
                    if any("(ns):" in i for i in line_one_space):
                        line_one_space.remove("(ns):")
                    # If line don't have any value, add "-" to make sure that line_one_space has two elements
                    if len(line_one_space) == 1:
                        line_one_space.append("-")
                    # Adds data from line to path list (order is maintain)
                    path_data.append(line_one_space[1])
                # Checks length of path list. One path has 7 parameters
                if len(path_data) == 7:
                    # Adds data to main list - spw_timing_report_list
                    if stb_flag == 1:
                        add_path_strobe(path_data[0], path_data[1], path_data[2], path_data[3], path_data[4],
                                        path_data[5], path_data[6])
                        path_data[:] = []
                        if path_number == 6:
                            path_number = 0
                    # Adds data to main list - spw_timing_report_list
                    if dat_flag == 1:
                        add_path_data(path_data[0], path_data[1], path_data[2], path_data[3], path_data[4],
                                      path_data[5],
                                      path_data[6])
                        path_data[:] = []
                # Searches for "#". "#" mean end of parsing
                if line.find("#") != (-1):
                    start = 0
        f.close()
    except Exception as error:
        print("Could not read file")
        print(error)
    print spw_timing_report_list


def add_path_strobe(number, ffrom, to, delay, slack, arrival, required):

    path_strobe_dic = {
        "type": "Strobe",
        "number": number,
        "from": ffrom,
        "to": to,
        "delay": delay,
        "slack": slack,
        "arrival": arrival,
        "required": required
    }
    spw_timing_report_list.append(path_strobe_dic)


def add_path_data(number, ffrom, to, delay, slack, arrival, required):

    path_data_dic = {
        "type": "Data",
        "number": number,
        "from": ffrom,
        "to": to,
        "delay": delay,
        "slack": slack,
        "arrival": arrival,
        "required": required
    }
    spw_timing_report_list.append(path_data_dic)


def shortest_data_to_ff_d ():
    print ""


def longest_data_to_ff_d():
    max_delay = []
    for path in spw_timing_report_list:
        if path["type"] == "Data" and path["to"].find(":D") != (-1):
            max_delay.append(path["delay"])
    print max_delay
    return max(max_delay)


def shortest_strobe_to_ff_clk():
    print ""


def longest_strobe_to_ff_clk():
    print ""


def longest_data_to_ff_clk():
    print ""


def main(tcl_script_path, stb_in_name, dat_in_name, reg_filter, error_flag):
    tcl_script(tcl_script_path, stb_in_name, dat_in_name, reg_filter, error_flag)
    longest_data_to_ff_d()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])