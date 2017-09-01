
import sys
import subprocess
import time
import os.path
import datetime

start_time = datetime.datetime

spw_timing_report_list = []
path_number = 0
stb_flag = 0
dat_flag = 0
start = 0
path_data = []
line_one_space = []

tcl_script_path = r"C:\Users\aczuba\PycharmProjects\SpaceWire-Constraints"
# tcl_script_path = r"C:\Microsemi\Libero_SoC_v11.8\Designer\scripts"
stb_in_name = "iSpw0Stb"
dat_in_name = "iSpw0Dat"
reg_filter = r"*r.do*"
error_flag = "0"


def tcl_control(tcl_script_path, stb_in_name, dat_in_name, reg_filter, error_flag):


    cmd = subprocess.Popen(r'C:\Microsemi\Libero_SoC_v11.8\Designer\bin\designer.exe "SCRIPT:report_spw_timing.tcl {0} {1} {2} {3}" "SCRIPT_DIR:{4}" "LOGFILE:report_spw_timingXD.log"'.format(stb_in_name, dat_in_name, reg_filter, error_flag, tcl_script_path), shell=True, cwd=r"C:\Microsemi\Libero_SoC_v11.8\Designer").wait()
    # cmd = os.system('"SCRIPT:report_spw_timing.tcl {0} {1} {2} {3}" "SCRIPT_DIR:{4}" "LOGFILE:report_spw_timingXD.log"'.format(stb_in_name, dat_in_name, reg_filter, error_flag, tcl_script_path))
    print cmd
    # Makes sure that script will be parsing proper log. After subprocess termination, overwritting log file takes some time
    time.sleep(5)
    now = (time.time())
    print now

    spw_timing_report_modtime = os.path.getmtime(tcl_script_path + r"\report_spw_timingXD.log")
    print spw_timing_report_modtime
    # Check that report_spw_timing.tcl exist. If not wait until TCL generate log (only if script is launched first time)
    while not os.path.isfile(tcl_script_path + r"\report_spw_timingXD.log"):
        time.sleep(1)
    # spw_timing_report_modtime = time.gmtime(os.path.getmtime(tcl_script_path + r"\report_spw_timing.log"))
    # Waits until report_spw_timing.log modification time will be later than script execution time.
    # Makes sure that proper log file will be read (not previous)
    while start_time >= spw_timing_report_modtime:
        time.sleep(1)
        # Reads report_spw_timing.log

    print "EZZZZ"

tcl_control(tcl_script_path, stb_in_name, dat_in_name, reg_filter, error_flag)

# def add_path_strobe(number, ffrom, to, delay, slack, arrival, required):
#
#     path_strobe_dic = {
#         "type": "Strobe",
#         "number": number,
#         "from": ffrom,
#         "to": to,
#         "delay": delay,
#         "slack": slack,
#         "arrival": arrival,
#         "required": required
#     }
#     spw_timing_report_list.append(path_strobe_dic)
#
#
# def add_path_data(number, ffrom, to, delay, slack, arrival, required):
#
#     path_data_dic = {
#         "type": "Data",
#         "number": number,
#         "from": ffrom,
#         "to": to,
#         "delay": delay,
#         "slack": slack,
#         "arrival": arrival,
#         "required": required
#     }
#     spw_timing_report_list.append(path_data_dic)
#
# try:
#     f = open('spw_report.log', mode="rt")
#     for line in f.readlines():
#         if line.find("iSpwStbToCLK") != (-1):
#             stb_flag = 1
#             start = 1
#             continue
#         if line.find("iSpwDatToReg") != (-1):
#             dat_flag = 1
#             stb_flag = 0
#             continue
#         if start == 1:
#             if line.find("Path") != (-1):
#                  path_number += 1
#                  path_data.append(path_number)
#             elif not line.strip():  # ignores empty line (whitespaces)
#                 continue
#             else:
#                 line_one_space = " ".join(line.split())
#                 line_one_space = line_one_space.split(" ")
#                 if any("(ns):" in i for i in line_one_space):
#                     line_one_space.remove("(ns):")
#                 if len(line_one_space) == 1:
#                     line_one_space.append("-")
#                 path_data.append(line_one_space[1])
#             if len(path_data) == 7:
#                 if stb_flag == 1:
#                     add_path_strobe(path_data[0], path_data[1], path_data[2], path_data[3], path_data[4], path_data[5], path_data[6])
#                     path_data[:] = []
#                     if path_number == 6:
#                         path_number = 0
#                 if dat_flag == 1:
#                     add_path_data(path_data[0], path_data[1], path_data[2], path_data[3], path_data[4], path_data[5],
#                                     path_data[6])
#                     path_data[:] = []
#             if line.find("#") != (-1):
#                 start = 0
#     f.close()
# except Exception as error:
#     print("Could not read file")
#     print(error)
# print spw_timing_report_list
