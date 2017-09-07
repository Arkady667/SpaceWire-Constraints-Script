# coding=utf-8
# python2
# Google naming style https://google.github.io/styleguide/pyguide.html

import sys
import subprocess
import os.path
import xlwt

# Constants (RT ProASIC3)
BIT_PERIOD = 20  # na
FF_SETUP = 0.4  # na
FF_HOLD = 0  # na

# xlwt
wb = xlwt.Workbook()

# xlwt styles
patternBackground = xlwt.Pattern()
patternBackground.pattern = patternBackground.SOLID_PATTERN
patternBackground.pattern = patternBackground.pattern_back_colour = 0x02

styleHeader = xlwt.XFStyle()
styleHeader.font.bold = True
styleHeader.font.height = 250

styleFormulaLeft = xlwt.XFStyle()
styleFormulaLeft.pattern = patternBackground
styleFormulaLeft.font.italic = True
styleFormulaLeft.font.height = 200
styleFormulaLeft.alignment.horz = styleFormulaLeft.alignment.HORZ_RIGHT
styleFormulaLeft.alignment.vert = styleFormulaLeft.alignment.VERT_CENTER

styleText = xlwt.XFStyle()
styleText.font.italic = True
styleText.font.height = 200
styleText.alignment.horz = styleText.alignment.HORZ_LEFT
styleText.alignment.vert = styleText.alignment.VERT_CENTER
styleText.alignment.wrap = styleText.alignment.WRAP_AT_RIGHT

styleFormulaRight = xlwt.XFStyle()
styleFormulaRight.pattern = patternBackground
styleFormulaRight.font.italic = True
styleFormulaRight.font.height = 200
styleFormulaRight.alignment.horz = styleFormulaRight.alignment.HORZ_LEFT
styleFormulaRight.alignment.vert = styleFormulaRight.alignment.VERT_CENTER

styleSign = xlwt.XFStyle()
styleSign.pattern = patternBackground
styleSign.font.bold = True
styleSign.font.height = 300
styleSign.alignment.horz = styleFormulaLeft.alignment.HORZ_CENTER
styleSign.alignment.vert = styleFormulaLeft.alignment.VERT_CENTER


styleBorder = xlwt.Borders()
styleBorder.left = xlwt.Borders.MEDIUM
styleBorder.right = xlwt.Borders.MEDIUM
styleBorder.bottom = xlwt.Borders.MEDIUM
styleBorder.top = xlwt.Borders.MEDIUM


# Data list
spw_timing_report_list = []

# tcl_script_path = r"C:\Users\aczuba\PycharmProjects\SpaceWire Constraints"
# stb_in_name = "iSpw0Stb"
# dat_in_name = "iSpw0Dat"
# reg_filter = r"*r.do*"
##


def get_width(num_char):
    return int((1 + num_char) * 256)


def tcl_script(tcl_script_path, stb_in_name, dat_in_name, reg_filter_rise, reg_filter_fall, error_flag):
    # line_one_space = []
    path_data = []
    path_number = 0
    stb_flag_r = 0
    dat_flag_r = 0
    stb_flag_f = 0
    dat_flag_f = 0
    start = 0

    # spw_timing_report_modtime = os.path.getmtime(tcl_script_path + r"\report_spw_timing.log")
    # Run TCL script report_spw_timing.tcl
    # cmd = subprocess.Popen(
    #     r'C:\Microsemi\Libero_SoC_v11.8\Designer\bin\designer.exe "SCRIPT:report_spw_timing.tcl {0} {1} {2} {3} {4}" "SCRIPT_DIR:{5}" "LOGFILE:report_spw_timing.log"'.format(
    #         stb_in_name, dat_in_name, reg_filter_rise, reg_filter_fall, error_flag, tcl_script_path), shell=True,
    #     cwd=r"C:\Microsemi\Libero_SoC_v11.8\Designer").wait()
    # # Simple cmd command error handling
    # if cmd == 0:
    #     print "report_spw_timing.log successfuly generated"
    # else:
    #     print "report_spw_timing.log generation failed"
    # # Check that report_spw_timing.tcl exist.
    # while not os.path.isfile(tcl_script_path+r"\report_spw_timing.log"):
    #     print "report_swp_timing.log not found"
    # spw_timing_report_modtime = os.path.getmtime(tcl_script_path + r"\report_spw_timing.log")
    # Reads report_spw_timing.log
    try:
        f = open('report_spw_timing.log', mode="rt")  # report_spw_timing.log
        for line in f.readlines():
            # Looking for particular string in file, and takes flag up to parse Strobe part
            if line.find("iSpwStbToCLK-RISE") != (-1):
                stb_flag_r = 1
                # Simple flag to chceck that proper lines are analysed, and avoid useless lines
                start = 1
                continue
            # Looking for particular string in file, and takes flag up to parse Data part
            if line.find("iSpwDatToReg-RISE") != (-1):
                dat_flag_r = 1
                stb_flag_r = 0
                path_number = 0
                continue
            if line.find("iSpwStbToCLK-FALL") != (-1):
                dat_flag_r = 0
                stb_flag_f = 1
                path_number = 0
                continue
            if line.find("iSpwDatToReg-FALL") != (-1):
                dat_flag_f = 1
                stb_flag_f = 0
                path_number = 0
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
                    if stb_flag_r == 1:
                        add_path_strobe("rise", path_data[0], path_data[1], path_data[2], path_data[3], path_data[4],
                                        path_data[5], path_data[6])
                        path_data[:] = []
                    # Adds data to main list - spw_timing_report_list
                    if dat_flag_r == 1:
                        add_path_data("rise", path_data[0], path_data[1], path_data[2], path_data[3], path_data[4],
                                      path_data[5],
                                      path_data[6])
                        path_data[:] = []
                    # Adds data to main list - spw_timing_report_list
                    if stb_flag_f == 1:
                        add_path_strobe("fall", path_data[0], path_data[1], path_data[2], path_data[3], path_data[4],
                                          path_data[5], path_data[6])
                        path_data[:] = []
                    # Adds data to main list - spw_timing_report_list
                    if dat_flag_f == 1:
                        add_path_data("fall", path_data[0], path_data[1], path_data[2], path_data[3], path_data[4],
                                          path_data[5], path_data[6])
                        path_data[:] = []
                # Searches for "#". "#" mean end of parsing
                if line.find("#") != (-1):
                    start = 0
        f.close()
    except Exception as error:
        print("Could not read file")
        print(error)
    # print spw_timing_report_list


def excel():



    excel_doc()
    excel_setup()
    setup = wb.add_sheet(('Setup Check'))
    hold = wb.add_sheet('Hold Check')
    pulsewidth = wb.add_sheet('Pulse Width Check')

    wb.save('SpW Constraints.xls')


def excel_doc():

    #Setup
    doc = wb.add_sheet('Formulas')
    doc.write(1, 1, "Hold Check Formula", style=styleHeader)

    col2 = doc.col(1)
    col2.width = 256 * 44
    doc.write(4, 1, "Longest ( Data to FF:D )", style=styleFormulaLeft)

    col3 = doc.col(2)
    col3.width = 256 * 5
    doc.write(4, 2, "<", style=styleSign)

    col4 = doc.col(3)
    col4.width = 256 * 68
    doc.write(4, 3, "Shortest ( Data to FF:CLK ) - FF Setup", style=styleFormulaRight)

    doc.write_merge(2, 3, 1, 3, "A setup check to ensure that a data event arrives on time to be captured by the clock edge generated with this same data event", style=styleText)

    # Hold
    doc.write(7, 1, "Setup Check Formula", style=styleHeader)

    doc.write(10, 1, "If External Data SKEW")
    doc.write(11, 1, "Bit_Period +  Data SKEW + Shortest( Data to FF:D )", style=styleFormulaLeft)
    doc.write(11, 2, ">", style=styleSign)
    doc.write(11, 3, "Longest( Strobe to FF:CK ) + Hold( FF )", style=styleFormulaRight)

    doc.write(12, 1, "If External Strobe SKEW")
    doc.write(13, 1, "Bit_Period + Strobe Skew + Shortest( Data to FF:D )", style=styleFormulaLeft)
    doc.write(13, 2, ">", style=styleSign)
    doc.write(13, 3, "Longest( Strobe to FF:CK ) + Hold( FF )", style=styleFormulaRight)
    doc.write_merge(8, 9, 1, 3, "A hold check to ensure that a Strobe event is not generating a clock edge capturing the wrong data:", style=styleText)

    # Pulse Width
    doc.write(16, 1, "Pulse Width Check Formula", style=styleHeader)

    doc.write(19, 1, "If External Data SKEW")
    doc.write(20, 1, "Bit_Period - Data Skew", style=styleFormulaLeft)
    doc.write(20, 2, ">", style=styleSign)
    doc.write(20, 3, "Longest( Data to FF:CK ) - Shortest( Strobe to FF:CK ) + Setup( FF ) + Hold( FF )", style=styleFormulaRight)

    doc.write(21, 1, "If External Strobe SKEW")
    doc.write(22, 1, "Bit_Period - Strobe Skew", style=styleFormulaLeft)
    doc.write(22, 2, ">", style=styleSign)
    doc.write(22, 3, "Longest( Strobe to FF:CK ) - Shortest( Data to FF:CK ) + Setup( FF ) + Hold( FF )", style=styleFormulaRight)
    doc.write_merge(17, 18, 1, 3, "A minimum pulse width on the Data-Strobe clock (XOR)", style=styleText)

def excel_setup():
    pass

# def excel_hold():
#     pass
#
#
# def excel_pulse():
#     pass
#
#
# def excel_exe():
#
#     excel_doc()
#     excel_setup()
#     excel_hold()
#     excel_pulse()


def add_path_strobe(fall_or_rise, number, ffrom, to, delay, slack, arrival, required):

    if fall_or_rise == "rise":
        edge = "rise"
    else:
        edge = "fall"

    path_strobe = {
        "clock": edge,
        "type": "Strobe",
        "number": number,
        "from": ffrom,
        "to": to,
        "delay": delay,
        "slack": slack,
        "arrival": arrival,
        "required": required
    }
    spw_timing_report_list.append(path_strobe)


def add_path_data(fall_or_rise, number, ffrom, to, delay, slack, arrival, required):

    if fall_or_rise == "rise":
        edge = "rise"
    else:
        edge = "fall"

    path_data = {
        "clock": edge,
        "type": "Data",
        "number": number,
        "from": ffrom,
        "to": to,
        "delay": delay,
        "slack": slack,
        "arrival": arrival,
        "required": required
    }
    spw_timing_report_list.append(path_data)


def data_to_ff_d(long_or_short, fall_or_rise):
    min_delay = []
    max_delay = []
    fmin = 0
    fmax = 0
    for path in spw_timing_report_list:
        if long_or_short == "shortest":
            if fall_or_rise == "rise":
                if path["type"] == "Data" and path["to"].find("[1]:D") != (-1) and path["clock"] == "rise":
                    min_delay.append(path["delay"])
                    fmin = 1
            elif fall_or_rise == "fall":
                if path["type"] == "Data" and (":D" in path["to"]) and (("nr.d:" in path["to"]) or ("nr.d_tmr" in path["to"])) and (path["clock"] == "fall"):
                    min_delay.append(path["delay"])
                    # if len(min_delay) == 3:
                    #     return min(min_delay)
                    fmin = 1
            else:
                print "WARNING (data_to_ff_d): Wrong second argument. Write 'rise' or 'fall'"
        elif long_or_short == "longest":
            if fall_or_rise == "rise":
                if path["type"] == "Data" and path["to"].find("[1]:D") != (-1) and path["clock"] == "rise":
                    max_delay.append(path["delay"])
                    fmax = 1
            elif fall_or_rise == "fall":
                if path["type"] == "Data" and (":D" in path["to"]) and (("nr.d:" in path["to"]) or ("nr.d_tmr" in path["to"])) and (path["clock"] == "fall"):
                    max_delay.append(path["delay"])
                    # if len(max_delay) == 3:
                    #     return max(max_delay)
                    fmax = 1
            else:
                print "WARNING (data_to_ff_d): Wrong second argument. Write 'rise' or 'fall'"
        else:
            print "WARNING (data_to_ff_d): Wrong first argument. Write 'longest' or 'shortest'"
    if fmax == 1:
        return max(max_delay)
    if fmin == 1:
        return min(min_delay)


def data_to_ff_clk(long_or_short, fall_or_rise):
    max_delay = []
    min_delay = []
    fmin = 0
    fmax = 0
    for path in spw_timing_report_list:
        if long_or_short == "longest":
            if fall_or_rise == "rise":
                if path["type"] == "Data" and path["to"].find("[1]:CLK") != (-1) and path["clock"] == "rise":
                    max_delay.append(path["delay"])
                    fmax = 1
            elif fall_or_rise == "fall":
                if path["type"] == "Data" and (":CLK" in path["to"]) and (path["clock"] == "fall") and (
                        path["to"].find("nr.d:CLK") != (-1) or (path["to"].find("nr.d_tmr") != (-1))):
                    max_delay.append(path["delay"])
                    fmax = 1
                    # if len(max_delay) == 3:
                    #     return max(max_delay)
            else:
                print "WARNING (data_to_ff_clk): Wrong second argument. Write 'rise' or 'fall'"
            # continue
        elif long_or_short == "shortest":
            if fall_or_rise == "rise":
                if path["type"] == "Data" and path["to"].find("[1]:CLK") != (-1) and path["clock"] == "rise":
                    min_delay.append(path["delay"])
                    fmin = 1
            elif fall_or_rise == "fall":
                if path["type"] == "Data" and (":CLK" in path["to"]) and (
                    ("nr.d:" in path["to"]) or ("nr.d_tmr" in path["to"])) and (path["clock"] == "fall") and (
                        path["to"].find("nr.d:CLK") != (-1) or (path["to"].find("nr.d_tmr") != (-1))):
                    min_delay.append(path["delay"])
                    # if len(min_delay) == 3:
                    #     return min(min_delay)
                    fmin = 1
            else:
                print "WARNING (data_to_ff_clk): Wrong second argument. Write 'rise' or 'fall'"
            # continue
        else:
            print "WARNING (data_to_ff_clk): Wrong first argument. Write 'longest' or 'shortest'"
    if fmax == 1:
        return max(max_delay)
    if fmin == 1:
        return min(min_delay)


def strobe_to_ff_clk(long_or_short, fall_or_rise):
    min_delay = []
    max_delay = []
    fmin = 0
    fmax = 0
    for path in spw_timing_report_list:
        if long_or_short == "shortest":
            if fall_or_rise == "rise":
                if path["type"] == "Strobe" and path["to"].find("[1]:CLK") != (-1) and path["clock"] == "rise":
                    min_delay.append(path["delay"])
                    fmin = 1
            elif fall_or_rise == "fall":
                if path["type"] == "Strobe" and (":CLK" in path["to"]) and (("nr.d:" in path["to"]) or ("nr.d_tmr" in path["to"])) and (path["clock"] == "fall"):
                    min_delay.append(path["delay"])
                    fmin = 1
            else:
                print "WARNING (strobe_to_ff_clk): Wrong second argument. Write 'rise' or 'fall'"
            continue
        elif long_or_short == "longest":
            if fall_or_rise == "rise":
                if path["type"] == "Strobe" and path["to"].find("[1]:CLK") != (-1) and path["clock"] == "rise":
                    max_delay.append(path["delay"])
                    fmax = 1
            elif fall_or_rise == "fall":
                if path["type"] == "Strobe" and (":CLK" in path["to"]) and (("nr.d:" in path["to"]) or ("nr.d_tmr" in path["to"])) and (path["clock"] == "fall"):
                    max_delay.append(path["delay"])
                    fmax = 1
            else:
                print "WARNING (strobe_to_ff_clk): Wrong second argument. Write 'rise' or 'fall'"
            continue
        else:
            print "WARNING (strobe_to_ff_clk): Wrong first argument. Write 'longest' or 'shortest'"
    if fmax == 1:
        return max(max_delay)
    if fmin == 1:
        return min(min_delay)




def main(tcl_script_path, stb_in_name, dat_in_name, reg_filter_rise,reg_filter_fall, error_flag):
    tcl_script(tcl_script_path, stb_in_name, dat_in_name, reg_filter_rise, reg_filter_fall, error_flag)
    excel()
    # print spw_timing_report_list
    # print "data_to_ff_d() :" + data_to_ff_d("longest", "rise")
    # print "data_to_ff_d() :" + data_to_ff_d("shortest", "rise")
    # print "data_to_ff_clk() :" + data_to_ff_clk("longest", "rise")
    # print "data_to_ff_clk() :" + data_to_ff_clk("shortest", "rise")
    # print "strobe_to_ff_clk() :" + strobe_to_ff_clk("shortest", "rise")
    # print "strobe_to_ff_clk() :" + strobe_to_ff_clk("longest", "rise")+"\n"
    #
    # print "data_to_ff_d() :" + data_to_ff_d("longest", "fall")
    # print "data_to_ff_d() :" + data_to_ff_d("shortest", "fall")
    # print "data_to_ff_clk() :" + data_to_ff_clk("longest", "fall")
    # print "data_to_ff_clk() :" + data_to_ff_clk("shortest", "fall")
    # print "strobe_to_ff_clk() :" + strobe_to_ff_clk("shortest", "fall")
    # print "strobe_to_ff_clk() :" + strobe_to_ff_clk("longest", "fall")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])