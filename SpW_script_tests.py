spw_timing_report_list = []
path_number = 0
stb_flag = 0
dat_flag = 0
start = 0
path_data = []
line_one_space = []


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

try:
    f = open('spw_report.log', mode="rt")
    for line in f.readlines():
        if line.find("iSpwStbToCLK") != (-1):
            stb_flag = 1
            start = 1
            continue
        if line.find("iSpwDatToReg") != (-1):
            dat_flag = 1
            stb_flag = 0
            continue
        if start == 1:
            if line.find("Path") != (-1):
                 path_number += 1
                 path_data.append(path_number)
                 print "LICZBA PATHU"
            elif not line.strip():  # ignores empty line (whitespaces)
                print "PUSTA"
                continue
            else:
                print "DANE"
                line_one_space = " ".join(line.split())
                line_one_space = line_one_space.split(" ")
                print line_one_space[1]
                if line_one_space.find(":") != (-1):
                    line_one_space = line_one_space.replace(":", "")
                    if line_one_space.find(" (ns)") != (-1):
                        line_one_space = line_one_space.replace(" (ns)","(ns)")
                ##### TU DO ROBOTY
                path_data.append(line_one_space[2])
                print line_one_space[2]
            if len(path_data) == 7:
                if stb_flag == 1:
                    add_path_strobe(path_data[0], path_data[1], path_data[2], path_data[3], path_data[4], path_data[5], path_data[6])
                if dat_flag == 1:
                    add_path_data(path_data[0], path_data[1], path_data[2], path_data[3], path_data[4], path_data[5],
                                    path_data[6])
            if line.find("#") != (-1):
                start = 0
    f.close()
except Exception as error:
    print("Could not read file")
    print(error)
print path_data
print spw_timing_report_list
