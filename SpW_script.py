# coding=utf-8
# python2
# Google naming style https://google.github.io/styleguide/pyguide.html
# example> python SpW_script.py C:\Users\aczuba\PycharmProjects\SpaceWire-Constraints iSpw0Stb iSpw0Dat *r.do* *nr.d* 0 0.5 0.5
"""

argv1: Path to TCL script (~/report_spw_timing.log)
argv2: SpaceWire Strobe input pin name
argv3: SpaceWire Data input pin name
argv4: String use to filter input registers - reg with rising edge clock
argv5: String use to filter input registers - reg with falling edge clock
argv6: TCL script arg - if 1 error handling ON, if anything else OFF
argv7: Data Skew value (output skew GR712RC - 0.5 ns)
argv8: Strobe Skew value (output skew GR712RC - 0.5 ns)

"""
import sys
import subprocess
import os.path
import xlwt

# Constants (RT ProASIC3)
BIT_PERIOD = 20  # na
FF_SETUP = 0.4  # na
FF_HOLD = 0  # na
D_SKEW = float(sys.argv[7])  # ns
S_SKEW = float(sys.argv[8])  # ns

# Variables
shortest = "shortest"
longest = "longest"
rise = "rise"
fall = "fall"
data = "data"
strobe = "strobe"

# xlwt
wb = xlwt.Workbook()

# xlwt styles
patternBackground = xlwt.Pattern()
patternBackground.pattern = patternBackground.SOLID_PATTERN
patternBackground.pattern = patternBackground.pattern_back_colour = 0x02  # red

patternBackgroundGood = xlwt.Pattern()
patternBackgroundGood.pattern = patternBackgroundGood.SOLID_PATTERN
patternBackgroundGood.pattern = patternBackgroundGood.pattern_back_colour = 0x03

styleHeader = xlwt.XFStyle()
styleHeader.font.bold = True
styleHeader.font.height = 250

styleLowHeader = xlwt.XFStyle()
styleLowHeader.font.bold = True
styleLowHeader.font.height = 200
styleLowHeader.alignment.horz = styleLowHeader.alignment.HORZ_LEFT

styleResult = xlwt.XFStyle()
styleResult.pattern = patternBackground
styleResult.font.bold = True

styleResultBad = xlwt.XFStyle()
styleResultBad.pattern = patternBackground
styleResultBad.font.bold = True
styleResultBad.font.height = 200
styleResultBad.alignment.horz = styleResultBad.alignment.HORZ_CENTER

styleResultGood = xlwt.XFStyle()
styleResultGood.pattern = patternBackgroundGood
styleResultGood.font.bold = True
styleResultGood.font.height = 200
styleResultGood.alignment.horz = styleResultGood.alignment.HORZ_CENTER

styleFormulaLeft = xlwt.XFStyle()
styleFormulaLeft.pattern = patternBackground
styleFormulaLeft.font.italic = True
styleFormulaLeft.font.height = 200
styleFormulaLeft.alignment.horz = styleFormulaLeft.alignment.HORZ_RIGHT
styleFormulaLeft.alignment.vert = styleFormulaLeft.alignment.VERT_CENTER

styleText = xlwt.XFStyle()
styleText.font.italic = True
styleText.font.height = 200
styleText.alignment.horz = styleText.alignment.HORZ_CENTER
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

# Main list with data
spw_timing_report_list = []


# # Helpful during tests without argv and shell commands
# tcl_script_path = r"C:\Users\aczuba\PycharmProjects\SpaceWire Constraints"
# stb_in_name = "iSpw0Stb"
# dat_in_name = "iSpw0Dat"
# reg_filter = r"*r.do*"


def tcl_script(tcl_script_path, stb_in_name, dat_in_name, reg_filter_rise, reg_filter_fall, error_flag):
    """Function which invoke TCL script report_spw_timing.tcl to generate SpaceWire inputs timing report and save data
       in particular structures.

    :param tcl_script_path: Full path to dir with TCL script
    :param stb_in_name: SpaceWire Strobe input pin name
    :param dat_in_name: SpaceWire Data input pin name
    :param reg_filter_rise: String use to filter input registers - reg with rising edge clock
    :param reg_filter_fall: String use to filter input registers - reg with falling edge clock
    :param error_flag: TCL script arg - if 1 error handling ON, if anything else OFF
    :return: None
    """
    path_data = []

    # TCL Command string
    cmd_string = r'C:\Microsemi\Libero_SoC_v11.8\Designer\bin\designer.exe "SCRIPT:report_spw_timing.tcl {0} {1} {2} {3} {4}" "SCRIPT_DIR:{5}" "LOGFILE:report_spw_timing.log"'.format(
        stb_in_name, dat_in_name, reg_filter_rise, reg_filter_fall, error_flag, tcl_script_path)

    # Flag initialization
    path_number = 0
    stb_flag_r = 0
    dat_flag_r = 0
    stb_flag_f = 0
    dat_flag_f = 0
    start = 0

    # Run TCL script report_spw_timing.tcl
    print "TCL script report_spw_timing.tcl is running..."
    try:
        cmd = subprocess.Popen(cmd_string, shell=True, cwd=r"C:\Microsemi\Libero_SoC_v11.8\Designer").wait()
        if cmd == 0:
            print "report_spw_timing.log successfully generated"
            # Simple cmd command error handling
    except Exception as error:
        print "report_spw_timing.log generation failed"
        print error
    # Check that report_spw_timing.tcl exist.
    while not os.path.isfile(tcl_script_path + r"\report_spw_timing.log"):
        print "report_swp_timing.log not found"
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
            # Looking for particular string in file, and takes flag up to parse
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
            # Flag which start parsing
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
                        # After adding data, path_data list has to be empty and ready for next data
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


def add_path_strobe(fall_or_rise, number, ffrom, to, delay, slack, arrival, required):
    """ Function, which adds 'Strobe path' raw data to structure fields to keep data sorted and ordered ready for use. Adds containing path to main list

    :param fall_or_rise: Specify that register is fall or rise clock
    :param number: Path number
    :param ffrom: Input pin name
    :param to: Input register full path
    :param delay: Delay (ns)
    :param slack: Slack (ns)
    :param arrival: Arrival(ns)
    :param required: Required (ns)
    :return: None
    """
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
    """ Function, which adds 'Data path' raw data to structure fields to keep data sorted and ordered ready for use. Adds containing path to main list

    :param fall_or_rise: Specify that register is fall or rise clock
    :param number: Path number
    :param ffrom: Input pin name
    :param to: Input register full path
    :param delay: Delay (ns)
    :param slack: Slack (ns)
    :param arrival: Arrival(ns)
    :param required: Required (ns)
    :return: None
    """
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
    """Function which searches main list looks for paths form input data pin to input register D input

    :param long_or_short: Determine that path will be longest or shortest
    :param fall_or_rise: Determine that register has falling or rising edge clock input
    :return: Longest or shortest path (delay value)
    """
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
                if path["type"] == "Data" and (":D" in path["to"]) and (
                            ("nr.d:" in path["to"]) or ("nr.d_tmr" in path["to"])) and (path["clock"] == "fall"):
                    min_delay.append(path["delay"])
                    fmin = 1
            else:
                print "WARNING (data_to_ff_d): Wrong second argument. Write 'rise' or 'fall'"
        elif long_or_short == "longest":
            if fall_or_rise == "rise":
                if path["type"] == "Data" and path["to"].find("[1]:D") != (-1) and path["clock"] == "rise":
                    max_delay.append(path["delay"])
                    fmax = 1
            elif fall_or_rise == "fall":
                if path["type"] == "Data" and (":D" in path["to"]) and (
                            ("nr.d:" in path["to"]) or ("nr.d_tmr" in path["to"])) and (path["clock"] == "fall"):
                    max_delay.append(path["delay"])
                    fmax = 1
            else:
                print "WARNING (data_to_ff_d): Wrong second argument. Write 'rise' or 'fall'"
        else:
            print "WARNING (data_to_ff_d): Wrong first argument. Write 'longest' or 'shortest'"
    if fmax == 1:
        return float(max(max_delay))
    if fmin == 1:
        return float(min(min_delay))


def data_to_ff_clk(long_or_short, fall_or_rise):
    """Function which searches main list looks for paths form input data pin to input register CLK input

    :param long_or_short: Determine that path will be longest or shortest
    :param fall_or_rise: Determine that register has falling or rising edge clock input
    :return: Longest or shortest path (delay value)
    """
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
                    fmin = 1
            else:
                print "WARNING (data_to_ff_clk): Wrong second argument. Write 'rise' or 'fall'"
                # continue
        else:
            print "WARNING (data_to_ff_clk): Wrong first argument. Write 'longest' or 'shortest'"
    if fmax == 1:
        return float(max(max_delay))
    if fmin == 1:
        return float(min(min_delay))


def strobe_to_ff_clk(long_or_short, fall_or_rise):
    """Function which searches main list looks for paths form input strobe pin to input register CLK input

    :param long_or_short: Determine that path will be longest or shortest
    :param fall_or_rise: Determine that register has falling or rising edge clock input
    :return: Longest or shortest path (delay value)
    """
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
                if path["type"] == "Strobe" and (":CLK" in path["to"]) and (
                            ("nr.d:" in path["to"]) or ("nr.d_tmr" in path["to"])) and (path["clock"] == "fall"):
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
                if path["type"] == "Strobe" and (":CLK" in path["to"]) and (
                            ("nr.d:" in path["to"]) or ("nr.d_tmr" in path["to"])) and (path["clock"] == "fall"):
                    max_delay.append(path["delay"])
                    fmax = 1
            else:
                print "WARNING (strobe_to_ff_clk): Wrong second argument. Write 'rise' or 'fall'"
            continue
        else:
            print "WARNING (strobe_to_ff_clk): Wrong first argument. Write 'longest' or 'shortest'"
    if fmax == 1:
        return float(max(max_delay))
    if fmin == 1:
        return float(min(min_delay))


def setup_check(edge1, edge2):
    """Function, which calculate setup check value according to Actel SpaceWire Clock Recovery Implementation doc formula
    https://www.microsemi.com/document-portal/doc_view/130012-ac305-implementation-of-the-spacewire-clock-recovery-logic-in-actel-rtax-s-devices-app-note

    :param edge1: Clock edge (Rise or Fall) for first path from formula
    :param edge2: Clock edge (Rise or Fall) for second path from formula
    :return: Setup check value
    """
    return data_to_ff_clk(shortest, edge1) - data_to_ff_d(longest, edge2) - FF_SETUP


def hold_check(edge1, edge2, data_or_strobe):
    """Function, which calculate hold check value according to Actel SpaceWire Clock Recovery Implementation doc formula
    https://www.microsemi.com/document-portal/doc_view/130012-ac305-implementation-of-the-spacewire-clock-recovery-logic-in-actel-rtax-s-devices-app-note

    :param edge1: Clock edge (Rise or Fall) for first path from formula
    :param edge2: Clock edge (Rise or Fall) for second path from formula
    :param data_or_strobe: Data or Strobe Skew formula
    :return: Hold check value
    """
    if data_or_strobe == "data":
        return BIT_PERIOD + D_SKEW + data_to_ff_d(shortest, edge1) - strobe_to_ff_clk(longest, edge2) - FF_HOLD
    if data_or_strobe == "strobe":
        return BIT_PERIOD - S_SKEW + data_to_ff_d(shortest, edge1) - strobe_to_ff_clk(longest, edge2) - FF_HOLD


def pulse_check(edge1, edge2, data_or_strobe):
    """Function, which calculate pulse width check value according to Actel SpaceWire Clock Recovery Implementation doc formula
    https://www.microsemi.com/document-portal/doc_view/130012-ac305-implementation-of-the-spacewire-clock-recovery-logic-in-actel-rtax-s-devices-app-note

    :param edge1: Clock edge (Rise or Fall) for first path from formula
    :param edge2: Clock edge (Rise or Fall) for second path from formula
    :param data_or_strobe: ata or Strobe Skew formula
    :return: Pulse Width value
    """
    if data_or_strobe == "data":
        return BIT_PERIOD - D_SKEW - data_to_ff_clk(longest, edge1) + strobe_to_ff_clk(shortest, edge2) - FF_SETUP - FF_HOLD
    if data_or_strobe == "strobe":
        return BIT_PERIOD - S_SKEW - strobe_to_ff_clk(longest, edge1) + data_to_ff_clk(shortest, edge2) - FF_SETUP - FF_HOLD


def excel():
    """Control function, which executes each spreadsheet generation function and saves excel ss

    :return: None
    """
    excel_doc()
    excel_setup()
    excel_hold()
    excel_pulse()

    try:
        wb.save('SpW Timing Verification.xls')
        print "Excel spreadsheet 'SpW Timing Verification.xls' successfully created"
    except Exception as error:
        print("WARNING: Close excel spreadsheet 'SpW Timing Verification.xls' before running the script. XLS file not save")
        print(error)


def excel_doc():
    """Excel function, which generate and formats 'Formulas' sheet

    :return: None
    """
    doc = wb.add_sheet('Formulas')

    # Setup
    doc.write(1, 1, "Setup Check Formula", style=styleHeader)

    col2 = doc.col(1)
    col2.width = 256 * 44
    doc.write(4, 1, "Longest ( Data to FF:D )", style=styleFormulaLeft)

    col3 = doc.col(2)
    col3.width = 256 * 5
    doc.write(4, 2, "<", style=styleSign)

    col4 = doc.col(3)
    col4.width = 256 * 68
    doc.write(4, 3, "Shortest ( Data to FF:CLK ) - FF Setup", style=styleFormulaRight)

    doc.write_merge(2, 3, 1, 3,
                    "A setup check to ensure that a data event arrives on time to be captured by the clock edge generated with this same data event",
                    style=styleText)

    # Hold
    doc.write(7, 1, "Hold Check Formula", style=styleHeader)

    doc.write(10, 1, "If External Data SKEW")
    doc.write(11, 1, "Bit_Period +  Data SKEW + Shortest( Data to FF:D )", style=styleFormulaLeft)
    doc.write(11, 2, ">", style=styleSign)
    doc.write(11, 3, "Longest( Strobe to FF:CK ) + Hold( FF )", style=styleFormulaRight)

    doc.write(12, 1, "If External Strobe SKEW")
    doc.write(13, 1, "Bit_Period + Strobe Skew + Shortest( Data to FF:D )", style=styleFormulaLeft)
    doc.write(13, 2, ">", style=styleSign)
    doc.write(13, 3, "Longest( Strobe to FF:CK ) + Hold( FF )", style=styleFormulaRight)
    doc.write_merge(8, 9, 1, 3,
                    "A hold check to ensure that a Strobe event is not generating a clock edge capturing the wrong data:",
                    style=styleText)

    # Pulse Width
    doc.write(16, 1, "Pulse Width Check Formula", style=styleHeader)

    doc.write(19, 1, "If External Data SKEW")
    doc.write(20, 1, "Bit_Period - Data Skew", style=styleFormulaLeft)
    doc.write(20, 2, ">", style=styleSign)
    doc.write(20, 3, "Longest( Data to FF:CK ) - Shortest( Strobe to FF:CK ) + Setup( FF ) + Hold( FF )",
              style=styleFormulaRight)

    doc.write(21, 1, "If External Strobe SKEW")
    doc.write(22, 1, "Bit_Period - Strobe Skew", style=styleFormulaLeft)
    doc.write(22, 2, ">", style=styleSign)
    doc.write(22, 3, "Longest( Strobe to FF:CK ) - Shortest( Data to FF:CK ) + Setup( FF ) + Hold( FF )",
              style=styleFormulaRight)
    doc.write_merge(17, 18, 1, 3, "A minimum pulse width on the Data-Strobe clock (XOR)", style=styleText)


def excel_setup():
    """Excel function, which generate and formats 'Setup Check' sheet

    :return: None
    """
    setup = wb.add_sheet('Setup Check')

    setup.write(1, 1, "Setup Timing Check", style=styleHeader)
    setup.write_merge(2, 2, 1, 6,
                      "Shortest[Data to FF:CLK (Rise/Fall)] - Longest[Data to FF:D (Rise/Fall)] - Setup FF ",
                      style=styleFormulaRight)

    setup.write_merge(6, 6, 1, 6, "Shortest[Data to FF:CLK (Rise)] - Longest[Data to FF:D (Rise)] - Setup FF ",
                      style=styleLowHeader)
    setup.write(6, 7, "Setup Check", style=styleLowHeader)
    setup.write(7, 1, "{0}".format(data_to_ff_clk(shortest, rise)), style=styleText)
    setup.write(7, 2, "-", styleText)
    setup.write(7, 3, "{0}".format(data_to_ff_d(longest, rise), style=styleText))
    setup.write(7, 4, "-", style=styleText)
    setup.write(7, 5, "{0}".format(FF_SETUP), style=styleText)
    if setup_check(rise, rise) > 0:
        setup.write(7, 7, "{0}".format(setup_check(rise, rise)), style=styleResultGood)
    else:
        setup.write(7, 7, "{0}".format(setup_check(rise, rise)), style=styleResultBad)

    setup.write_merge(8, 8, 1, 6, "Shortest[Data to FF:CLK (Rise)] - Longest[Data to FF:D (Fall)] - Setup FF ",
                      style=styleLowHeader)
    setup.write(8, 7, "Setup Check", style=styleLowHeader)
    setup.write(9, 1, "{0}".format(data_to_ff_clk(shortest, rise)), style=styleText)
    setup.write(9, 2, "-", styleText)
    setup.write(9, 3, "{0}".format(data_to_ff_d(longest, fall), style=styleText))
    setup.write(9, 4, "-", style=styleText)
    setup.write(9, 5, "{0}".format(FF_SETUP), style=styleText)
    if setup_check(rise, rise) > 0:
        setup.write(9, 7, "{0}".format(setup_check(rise, fall)), style=styleResultGood)
    else:
        setup.write(9, 7, "{0}".format(setup_check(rise, fall)), style=styleResultBad)

    setup.write_merge(10, 10, 1, 6, "Shortest[Data to FF:CLK (Fall)] - Longest[Data to FF:D (Rise)] - Setup FF ", style=styleLowHeader)
    setup.write(10, 7, "Setup Check", style=styleLowHeader)
    setup.write(11, 1, "{0}".format(data_to_ff_clk(shortest, fall)), style=styleText)
    setup.write(11, 2, "-", styleText)
    setup.write(11, 3, "{0}".format(data_to_ff_d(longest, rise), style=styleText))
    setup.write(11, 4, "-", style=styleText)
    setup.write(11, 5, "{0}".format(FF_SETUP), style=styleText)
    if setup_check(rise, rise) > 0:
        setup.write(11, 7, "{0}".format(setup_check(fall, rise)), style=styleResultGood)
    else:
        setup.write(11, 7, "{0}".format(setup_check(fall, rise)), style=styleResultBad)

    setup.write_merge(12, 12, 1, 6, "Shortest[Data to FF:CLK (Fall)] - Longest[Data to FF:D (Fall)] - Setup FF ",
                      style=styleLowHeader)
    setup.write(12, 7, "Setup Check", style=styleLowHeader)
    setup.write(13, 1, "{0}".format(data_to_ff_clk(shortest, fall)), style=styleText)
    setup.write(13, 2, "-", styleText)
    setup.write(13, 3, "{0}".format(data_to_ff_d(longest, fall), style=styleText))
    setup.write(13, 4, "-", style=styleText)
    setup.write(13, 5, "{0}".format(FF_SETUP), style=styleText)
    if setup_check(rise, rise) > 0:
        setup.write(13, 7, "{0}".format(setup_check(fall, fall)), style=styleResultGood)
    else:
        setup.write(13, 7, "{0}".format(setup_check(fall, fall)), style=styleResultBad)


def excel_hold():
    """Excel function, which generate and formats 'Hold Check' sheet

    :return: None
    """
    hold = wb.add_sheet('Hold Check')

    hold.write(1, 1, "Hold Timing Check", style=styleHeader)
    hold.write(2, 1, "If Data Skew", style=styleText)
    hold.write_merge(3, 3, 1, 8,
                     "BIT_PERIOD + D_SKEW + Shortest[Data to FF:D(Rise/Fall)] - Longest[Strobe to FF:CLK(Rise/Fall)] - Hold FF ",
                     style=styleFormulaRight)
    hold.write(4, 1, "If Data Skew", style=styleText)
    hold.write_merge(5, 5, 1, 8,
                     "BIT_PERIOD - S_SKEW + Shortest[Data to FF:D(Rise/Fall)] - Longest[Strobe to FD:CLK(Rise/Fall)] - Hold FF ",
                     style=styleFormulaRight)
    hold.write_merge(8, 8, 1, 4, "If Data Skew (D_SKEW = 2 ns - default value)", style=styleText)
    hold.write_merge(18, 18, 1, 4, "If Strobe Skew (S_SKEW = 2 ns - default value)", style=styleText)

    # Data Skew
    hold.write_merge(9, 9, 1, 9,
                     "BIT_PERIOD + D_SKEW + Shortest[Data to FF:D(Rise)] - Longest[Strobe to FF:CLK(Rise)] - Hold FF ",
                     style=styleLowHeader)
    hold.write(9, 10, "Hold Check", style=styleLowHeader)
    hold.write(10, 1, "{0}".format(BIT_PERIOD), style=styleText)
    hold.write(10, 2, "+", styleText)
    hold.write(10, 3, "{0}".format(D_SKEW), style=styleText)
    hold.write(10, 4, "+", styleText)
    hold.write(10, 5, "{0}".format(data_to_ff_d(shortest, rise)), style=styleText)
    hold.write(10, 6, "-", styleText)
    hold.write(10, 7, "{0}".format(strobe_to_ff_clk(longest, rise), style=styleText))
    hold.write(10, 8, "-", style=styleText)
    hold.write(10, 9, "{0}".format(FF_HOLD), style=styleText)
    if setup_check(rise, rise) > 0:
        hold.write(10, 10, "{0}".format(hold_check(rise, rise, data)), style=styleResultGood)
    else:
        hold.write(10, 10, "{0}".format(hold_check(rise, rise, data)), style=styleResultBad)

    hold.write_merge(11, 11, 1, 9,
                     "BIT_PERIOD + D_SKEW + Shortest[Data to FF:D(Rise)] - Longest[Strobe to FF:CLK(Fall)] - Hold FF ",
                     style=styleLowHeader)
    hold.write(11, 10, "Hold Check", style=styleLowHeader)
    hold.write(12, 1, "{0}".format(BIT_PERIOD), style=styleText)
    hold.write(12, 2, "+", styleText)
    hold.write(12, 3, "{0}".format(D_SKEW), style=styleText)
    hold.write(12, 4, "+", styleText)
    hold.write(12, 5, "{0}".format(data_to_ff_d(shortest, rise)), style=styleText)
    hold.write(12, 6, "-", styleText)
    hold.write(12, 7, "{0}".format(strobe_to_ff_clk(longest, fall), style=styleText))
    hold.write(12, 8, "-", style=styleText)
    hold.write(12, 9, "{0}".format(FF_HOLD), style=styleText)
    if hold_check(rise, fall, data) > 0:
        hold.write(12, 10, "{0}".format(hold_check(rise, fall, data)), style=styleResultGood)
    else:
        hold.write(12, 10, "{0}".format(hold_check(rise, fall, data)), style=styleResultBad)

    hold.write_merge(13, 13, 1, 9,
                     "BIT_PERIOD + D_SKEW + Shortest[Data to FF:D(Fall)] - Longest[Strobe to FF:CLK(Rise)] - Hold FF ",
                     style=styleLowHeader)
    hold.write(13, 10, "Hold Check", style=styleLowHeader)
    hold.write(14, 1, "{0}".format(BIT_PERIOD), style=styleText)
    hold.write(14, 2, "+", styleText)
    hold.write(14, 3, "{0}".format(D_SKEW), style=styleText)
    hold.write(14, 4, "+", styleText)
    hold.write(14, 5, "{0}".format(data_to_ff_d(shortest, fall)), style=styleText)
    hold.write(14, 6, "-", styleText)
    hold.write(14, 7, "{0}".format(strobe_to_ff_clk(longest, rise), style=styleText))
    hold.write(14, 8, "-", style=styleText)
    hold.write(14, 9, "{0}".format(FF_HOLD), style=styleText)
    if hold_check(fall, rise, data) > 0:
        hold.write(14, 10, "{0}".format(hold_check(fall, rise, data)), style=styleResultGood)
    else:
        hold.write(14, 10, "{0}".format(hold_check(fall, rise, data)), style=styleResultBad)

    hold.write_merge(15, 15, 1, 9,
                     "BIT_PERIOD + D_SKEW + Shortest[Data to FF:D(Fall)] - Longest[Strobe to FF:CLK(Fall)] - Hold FF ",
                     style=styleLowHeader)
    hold.write(15, 10, "Hold Check", style=styleLowHeader)
    hold.write(16, 1, "{0}".format(BIT_PERIOD), style=styleText)
    hold.write(16, 2, "+", styleText)
    hold.write(16, 3, "{0}".format(D_SKEW), style=styleText)
    hold.write(16, 4, "+", styleText)
    hold.write(16, 5, "{0}".format(data_to_ff_d(shortest, fall)), style=styleText)
    hold.write(16, 6, "-", styleText)
    hold.write(16, 7, "{0}".format(strobe_to_ff_clk(longest, fall), style=styleText))
    hold.write(16, 8, "-", style=styleText)
    hold.write(16, 9, "{0}".format(FF_HOLD), style=styleText)
    if hold_check(fall, fall, data) > 0:
        hold.write(16, 10, "{0}".format(hold_check(fall, fall, data)), style=styleResultGood)
    else:
        hold.write(16, 10, "{0}".format(hold_check(fall, fall, data)), style=styleResultBad)

    # Strobe Skew
    hold.write_merge(19, 19, 1, 9,
                     "BIT_PERIOD - S_SKEW + Shortest[Data to FF:D(Rise)] - Longest[Strobe to FF:CLK(Rise)] - Hold FF ",
                     style=styleLowHeader)
    hold.write(19, 10, "Hold Check", style=styleLowHeader)
    hold.write(20, 1, "{0}".format(BIT_PERIOD), style=styleText)
    hold.write(20, 2, "-", styleText)
    hold.write(20, 3, "{0}".format(S_SKEW), style=styleText)
    hold.write(20, 4, "+", styleText)
    hold.write(20, 5, "{0}".format(data_to_ff_d(shortest, rise)), style=styleText)
    hold.write(20, 6, "-", styleText)
    hold.write(20, 7, "{0}".format(strobe_to_ff_clk(longest, rise), style=styleText))
    hold.write(20, 8, "-", style=styleText)
    hold.write(20, 9, "{0}".format(FF_HOLD), style=styleText)
    if hold_check(rise, rise, strobe) > 0:
        hold.write(20, 10, "{0}".format(hold_check(rise, rise, strobe)), style=styleResultGood)
    else:
        hold.write(20, 10, "{0}".format(hold_check(rise, rise, strobe)), style=styleResultBad)

    hold.write_merge(21, 21, 1, 9,
                     "BIT_PERIOD - S_SKEW + Shortest[Data to FF:D(Rise)] - Longest[Strobe to FF:CLK(Fall)] - Hold FF ",
                     style=styleLowHeader)
    hold.write(21, 10, "Hold Check", style=styleLowHeader)
    hold.write(22, 1, "{0}".format(BIT_PERIOD), style=styleText)
    hold.write(22, 2, "-", styleText)
    hold.write(22, 3, "{0}".format(S_SKEW), style=styleText)
    hold.write(22, 4, "+", styleText)
    hold.write(22, 5, "{0}".format(data_to_ff_d(shortest, rise)), style=styleText)
    hold.write(22, 6, "-", styleText)
    hold.write(22, 7, "{0}".format(strobe_to_ff_clk(longest, fall), style=styleText))
    hold.write(22, 8, "-", style=styleText)
    hold.write(22, 9, "{0}".format(FF_HOLD), style=styleText)
    if hold_check(rise, fall, strobe) > 0:
        hold.write(22, 10, "{0}".format(hold_check(rise, fall, strobe)), style=styleResultGood)
    else:
        hold.write(22, 10, "{0}".format(hold_check(rise, fall, strobe)), style=styleResultBad)

    hold.write_merge(23, 23, 1, 9,
                     "BIT_PERIOD - S_SKEW + Shortest[Data to FF:D(Fall)] - Longest[Strobe to FF:CLK(Rise)] - Hold FF ",
                     style=styleLowHeader)
    hold.write(23, 10, "Hold Check", style=styleLowHeader)
    hold.write(24, 1, "{0}".format(BIT_PERIOD), style=styleText)
    hold.write(24, 2, "-", styleText)
    hold.write(24, 3, "{0}".format(S_SKEW), style=styleText)
    hold.write(24, 4, "+", styleText)
    hold.write(24, 5, "{0}".format(data_to_ff_d(shortest, fall)), style=styleText)
    hold.write(24, 6, "-", styleText)
    hold.write(24, 7, "{0}".format(strobe_to_ff_clk(longest, rise), style=styleText))
    hold.write(24, 8, "-", style=styleText)
    hold.write(24, 9, "{0}".format(FF_HOLD), style=styleText)
    if hold_check(fall, rise, strobe) > 0:
        hold.write(24, 10, "{0}".format(hold_check(fall, rise, strobe)), style=styleResultGood)
    else:
        hold.write(24, 10, "{0}".format(hold_check(fall, rise, strobe)), style=styleResultBad)

    hold.write_merge(25, 25, 1, 9,
                     "BIT_PERIOD - S_SKEW + Shortest[Data to FF:D(Fall)] - Longest[Strobe to FF:CLK(Fall)] - Hold FF ",
                     style=styleLowHeader)
    hold.write(25, 10, "Hold Check", style=styleLowHeader)
    hold.write(26, 1, "{0}".format(BIT_PERIOD), style=styleText)
    hold.write(26, 2, "-", styleText)
    hold.write(26, 3, "{0}".format(S_SKEW), style=styleText)
    hold.write(26, 4, "+", styleText)
    hold.write(26, 5, "{0}".format(data_to_ff_d(shortest, fall)), style=styleText)
    hold.write(26, 6, "-", styleText)
    hold.write(26, 7, "{0}".format(strobe_to_ff_clk(longest, fall), style=styleText))
    hold.write(26, 8, "-", style=styleText)
    hold.write(26, 9, "{0}".format(FF_HOLD), style=styleText)
    if hold_check(fall, fall, strobe) > 0:
        hold.write(26, 10, "{0}".format(hold_check(fall, fall, strobe)), style=styleResultGood)
    else:
        hold.write(26, 10, "{0}".format(hold_check(fall, fall, strobe)), style=styleResultBad)


def excel_pulse():
    """Excel function, which generate and formats 'Pulse Width Check' sheet

    :return: None
    """
    pulse = wb.add_sheet('Pulse Width Check')

    col13 = pulse.col(12)
    col13.width = 256 * 18

    pulse.write(1, 1, "Pulse Width Timing Check", style=styleHeader)
    pulse.write(2, 1, "If Data Skew", style=styleText)
    pulse.write_merge(3, 3, 1, 9,
                      "BIT_PERIOD - D_SKEW - Longest[Data to FF:CLK(Rise/Fall)] + Shortest[Strobe to FF:CLK(Rise/Fall)] - Setup FF - Hold FF ",
                      style=styleFormulaRight)
    pulse.write(4, 1, "If Data Skew", style=styleText)
    pulse.write_merge(5, 5, 1, 9,
                      "BIT_PERIOD - S_SKEW - Longest[Strobe to FF:CLK(Rise/Fall)] + Shortest[Data to FF:CLK(Rise/Fall)] - Setup FF - Hold FF ",
                      style=styleFormulaRight)
    pulse.write_merge(8, 8, 1, 4, "If Data Skew (D_SKEW = 2 ns - default value)", style=styleText)
    pulse.write_merge(18, 18, 1, 4, "If Strobe Skew (S_SKEW = 2 ns - default value)", style=styleText)

    # Data Skew
    pulse.write_merge(9, 9, 1, 9,
                      "BIT_PERIOD - D_SKEW - Longest[Data to FF:CLK(Rise)] + Shortest[Strobe to FF:CLK(Rise)] - Setup FF - Hold FF ",
                      style=styleLowHeader)
    pulse.write(9, 12, "Pulse Width Check", style=styleLowHeader)
    pulse.write(10, 1, "{0}".format(BIT_PERIOD), style=styleText)
    pulse.write(10, 2, "-", styleText)
    pulse.write(10, 3, "{0}".format(D_SKEW), style=styleText)
    pulse.write(10, 4, "-", styleText)
    pulse.write(10, 5, "{0}".format(data_to_ff_clk(longest, rise)), style=styleText)
    pulse.write(10, 6, "+", styleText)
    pulse.write(10, 7, "{0}".format(strobe_to_ff_clk(shortest, rise)), style=styleText)
    pulse.write(10, 8, "-", style=styleText)
    pulse.write(10, 9, "{0}".format(FF_SETUP), style=styleText)
    pulse.write(10, 10, "-", style=styleText)
    pulse.write(10, 11, "{0}".format(FF_HOLD), style=styleText)
    if pulse_check(rise, rise, data) > 0:
        pulse.write(10, 12, "{0}".format(pulse_check(rise, rise, data)), style=styleResultGood)
    else:
        pulse.write(10, 12, "{0}".format(pulse_check(rise, rise, data)), style=styleResultBad)

    pulse.write_merge(11, 11, 1, 9,
                      "BIT_PERIOD - D_SKEW - Longest[Data to FF:CLK(Rise)] + Shortest[Strobe to FF:CLK(Fall)] - Setup FF - Hold FF ",
                      style=styleLowHeader)
    pulse.write(11, 12, "Pulse Width Check", style=styleLowHeader)
    pulse.write(12, 1, "{0}".format(BIT_PERIOD), style=styleText)
    pulse.write(12, 2, "-", styleText)
    pulse.write(12, 3, "{0}".format(D_SKEW), style=styleText)
    pulse.write(12, 4, "-", styleText)
    pulse.write(12, 5, "{0}".format(data_to_ff_clk(longest, rise)), style=styleText)
    pulse.write(12, 6, "+", styleText)
    pulse.write(12, 7, "{0}".format(strobe_to_ff_clk(shortest, fall)), style=styleText)
    pulse.write(12, 8, "-", style=styleText)
    pulse.write(12, 9, "{0}".format(FF_SETUP), style=styleText)
    pulse.write(12, 10, "-", style=styleText)
    pulse.write(12, 11, "{0}".format(FF_HOLD), style=styleText)
    if pulse_check(rise, fall, data) > 0:
        pulse.write(12, 12, "{0}".format(pulse_check(rise, fall, data)), style=styleResultGood)
    else:
        pulse.write(12, 12, "{0}".format(pulse_check(rise, fall, data)), style=styleResultBad)

    pulse.write_merge(13, 13, 1, 9,
                      "BIT_PERIOD - D_SKEW - Longest[Data to FF:CLK(Fall)] + Shortest[Strobe to FF:CLK(Rise)] - Setup FF - Hold FF ",
                      style=styleLowHeader)
    pulse.write(13, 12, "Pulse Width Check", style=styleLowHeader)
    pulse.write(14, 1, "{0}".format(BIT_PERIOD), style=styleText)
    pulse.write(14, 2, "-", styleText)
    pulse.write(14, 3, "{0}".format(D_SKEW), style=styleText)
    pulse.write(14, 4, "-", styleText)
    pulse.write(14, 5, "{0}".format(data_to_ff_clk(longest, fall)), style=styleText)
    pulse.write(14, 6, "+", styleText)
    pulse.write(14, 7, "{0}".format(strobe_to_ff_clk(shortest, rise)), style=styleText)
    pulse.write(14, 8, "-", style=styleText)
    pulse.write(14, 9, "{0}".format(FF_SETUP), style=styleText)
    pulse.write(14, 10, "-", style=styleText)
    pulse.write(14, 11, "{0}".format(FF_HOLD), style=styleText)
    if pulse_check(fall, rise, data) > 0:
        pulse.write(14, 12, "{0}".format(pulse_check(fall, rise, data)), style=styleResultGood)
    else:
        pulse.write(14, 12, "{0}".format(pulse_check(fall, rise, data)), style=styleResultBad)

    pulse.write_merge(15, 15, 1, 9,
                      "BIT_PERIOD - D_SKEW - Longest[Data to FF:CLK(Fall)] + Shortest[Strobe to FF:CLK(Fall)] - Setup FF - Hold FF ",
                      style=styleLowHeader)
    pulse.write(15, 12, "Pulse Width Check", style=styleLowHeader)
    pulse.write(16, 1, "{0}".format(BIT_PERIOD), style=styleText)
    pulse.write(16, 2, "-", styleText)
    pulse.write(16, 3, "{0}".format(D_SKEW), style=styleText)
    pulse.write(16, 4, "-", styleText)
    pulse.write(16, 5, "{0}".format(data_to_ff_clk(longest, fall)), style=styleText)
    pulse.write(16, 6, "+", styleText)
    pulse.write(16, 7, "{0}".format(strobe_to_ff_clk(shortest, fall)), style=styleText)
    pulse.write(16, 8, "-", style=styleText)
    pulse.write(16, 9, "{0}".format(FF_SETUP), style=styleText)
    pulse.write(16, 10, "-", style=styleText)
    pulse.write(16, 11, "{0}".format(FF_HOLD), style=styleText)
    if pulse_check(fall, fall, data) > 0:
        pulse.write(16, 12, "{0}".format(pulse_check(fall, fall, data)), style=styleResultGood)
    else:
        pulse.write(16, 12, "{0}".format(pulse_check(fall, fall, data)), style=styleResultBad)

    # Strobe Skew
    pulse.write_merge(19, 19, 1, 9,
                      "BIT_PERIOD - S_SKEW - Longest[Strobe to FF:CLK(Rise)] + Shortest[Data to FF:CLK(Rise)] - Setup FF - Hold FF ",
                      style=styleLowHeader)
    pulse.write(19, 12, "Pulse Width Check", style=styleLowHeader)
    pulse.write(20, 1, "{0}".format(BIT_PERIOD), style=styleText)
    pulse.write(20, 2, "-", styleText)
    pulse.write(20, 3, "{0}".format(S_SKEW), style=styleText)
    pulse.write(20, 4, "-", styleText)
    pulse.write(20, 5, "{0}".format(strobe_to_ff_clk(longest, rise)), style=styleText)
    pulse.write(20, 6, "+", styleText)
    pulse.write(20, 7, "{0}".format(data_to_ff_clk(shortest, rise)), style=styleText)
    pulse.write(20, 8, "-", style=styleText)
    pulse.write(20, 9, "{0}".format(FF_SETUP), style=styleText)
    pulse.write(20, 10, "-", style=styleText)
    pulse.write(20, 11, "{0}".format(FF_HOLD), style=styleText)
    if pulse_check(rise, rise, strobe) > 0:
        pulse.write(20, 12, "{0}".format(pulse_check(rise, rise, strobe)), style=styleResultGood)
    else:
        pulse.write(20, 12, "{0}".format(pulse_check(rise, rise, strobe)), style=styleResultBad)

    pulse.write_merge(21, 21, 1, 9,
                      "BIT_PERIOD - S_SKEW - Longest[Strobe to FF:CLK(Rise)] + Shortest[Data to FF:CLK(Fall)] - Setup FF - Hold FF ",
                      style=styleLowHeader)
    pulse.write(21, 12, "Pulse Width Check", style=styleLowHeader)
    pulse.write(22, 1, "{0}".format(BIT_PERIOD), style=styleText)
    pulse.write(22, 2, "-", styleText)
    pulse.write(22, 3, "{0}".format(S_SKEW), style=styleText)
    pulse.write(22, 4, "-", styleText)
    pulse.write(22, 5, "{0}".format(strobe_to_ff_clk(longest, rise)), style=styleText)
    pulse.write(22, 6, "+", styleText)
    pulse.write(22, 7, "{0}".format(data_to_ff_clk(shortest, fall)), style=styleText)
    pulse.write(22, 8, "-", style=styleText)
    pulse.write(22, 9, "{0}".format(FF_SETUP), style=styleText)
    pulse.write(22, 10, "-", style=styleText)
    pulse.write(22, 11, "{0}".format(FF_HOLD), style=styleText)
    if pulse_check(rise, fall, strobe) > 0:
        pulse.write(22, 12, "{0}".format(pulse_check(rise, fall, strobe)), style=styleResultGood)
    else:
        pulse.write(22, 12, "{0}".format(pulse_check(rise, fall, strobe)), style=styleResultBad)

    pulse.write_merge(23, 23, 1, 9,
                      "BIT_PERIOD - S_SKEW - Longest[Strobe to FF:CLK(Fall)] + Shortest[Data to FF:CLK(Rise)] - Setup FF - Hold FF ",
                      style=styleLowHeader)
    pulse.write(23, 12, "Pulse Width Check", style=styleLowHeader)
    pulse.write(24, 1, "{0}".format(BIT_PERIOD), style=styleText)
    pulse.write(24, 2, "-", styleText)
    pulse.write(24, 3, "{0}".format(S_SKEW), style=styleText)
    pulse.write(24, 4, "-", styleText)
    pulse.write(24, 5, "{0}".format(strobe_to_ff_clk(longest, fall)), style=styleText)
    pulse.write(24, 6, "+", styleText)
    pulse.write(24, 7, "{0}".format(data_to_ff_clk(shortest, rise)), style=styleText)
    pulse.write(24, 8, "-", style=styleText)
    pulse.write(24, 9, "{0}".format(FF_SETUP), style=styleText)
    pulse.write(24, 10, "-", style=styleText)
    pulse.write(24, 11, "{0}".format(FF_HOLD), style=styleText)
    if pulse_check(fall, rise, strobe) > 0:
        pulse.write(24, 12, "{0}".format(pulse_check(fall, rise, strobe)), style=styleResultGood)
    else:
        pulse.write(24, 12, "{0}".format(pulse_check(fall, rise, strobe)), style=styleResultBad)

    pulse.write_merge(25, 25, 1, 9,
                      "BIT_PERIOD - S_SKEW - Longest[Strobe to FF:CLK(Fall)] + Shortest[Data to FF:CLK(Fall)] - Setup FF - Hold FF ",
                      style=styleLowHeader)
    pulse.write(25, 12, "Pulse Width Check", style=styleLowHeader)
    pulse.write(26, 1, "{0}".format(BIT_PERIOD), style=styleText)
    pulse.write(26, 2, "-", styleText)
    pulse.write(26, 3, "{0}".format(S_SKEW), style=styleText)
    pulse.write(26, 4, "-", styleText)
    pulse.write(26, 5, "{0}".format(strobe_to_ff_clk(longest, fall)), style=styleText)
    pulse.write(26, 6, "+", styleText)
    pulse.write(26, 7, "{0}".format(data_to_ff_clk(shortest, fall)), style=styleText)
    pulse.write(26, 8, "-", style=styleText)
    pulse.write(26, 9, "{0}".format(FF_SETUP), style=styleText)
    pulse.write(26, 10, "-", style=styleText)
    pulse.write(26, 11, "{0}".format(FF_HOLD), style=styleText)
    if pulse_check(fall, fall, strobe) > 0:
        pulse.write(26, 12, "{0}".format(pulse_check(fall, fall, strobe)), style=styleResultGood)
    else:
        pulse.write(26, 12, "{0}".format(pulse_check(fall, fall, strobe)), style=styleResultBad)


def main(tcl_script_path, stb_in_name, dat_in_name, reg_filter_rise, reg_filter_fall, error_flag):
    """Main function, which executes others, to maintain order

    :param tcl_script_path: Full path to dir with TCL script
    :param stb_in_name: SpaceWire Strobe input pin name
    :param dat_in_name: SpaceWire Data input pin name
    :param reg_filter_rise: String to filter input registers - reg with rising edge clock
    :param reg_filter_fall: String to filter input registers - reg with falling edge clock
    :param error_flag: TCL script arg - if 1 error handling ON, if anything else OFF
    :return: None
    """
    tcl_script(tcl_script_path, stb_in_name, dat_in_name, reg_filter_rise, reg_filter_fall, error_flag)
    excel()
    # print spw_timing_report_list


if __name__ == "__main__":
    """Main function execution and argv usage
    """
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
