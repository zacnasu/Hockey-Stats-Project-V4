#!/usr/bin/env python3

acceptable_types = ["FHG", "FHN", "FHM","FMG", "FMN", "FMM","FLG", "FLN", "FLM","FLG", "AHG", "AHN", "AHM","AMG", "AMN", "AMM","ALG", "ALN", "ALM","ALG", "ALB", "AMB", "AHB", "FLB", "FMB", "FHB", "AEG", "FEG"]

def main():
    games = ["oct03.txt", "oct16.txt", "oct18.txt", "oct23.txt", "oct24.txt", "oct31.txt", "nov07.txt", "nov13.txt"]
    stats = {}
    for game in games:
        input_lines = read_input(game)
        stats = read_lines(input_lines, stats)
    with open('expect_goals_constants.py', 'w') as file:
        file.write("FH_xG = "+ str(stats["FHG"]/(stats["FHG"]+stats["FHN"]+stats["FHM"])) +"\n")
        file.write("FM_xG = "+ str(stats["FMG"]/(stats["FMG"]+stats["FMN"]+stats["FMM"])) +"\n")
        file.write("FL_xG = "+ str(stats["FLG"]/(stats["FLG"]+stats["FLN"]+stats["FLM"])) +"\n")
        file.write("AH_xG = "+ str(stats["AHG"]/(stats["AHG"]+stats["AHN"]+stats["AHM"])) +"\n")
        file.write("AM_xG = "+ str(stats["AMG"]/(stats["AMG"]+stats["AMN"]+stats["AMM"])) +"\n")
        file.write("AL_xG = "+ str(stats["ALG"]/(stats["ALG"]+stats["ALN"]+stats["ALM"])) +"\n")

def read_input(input_file_name):
    try:
        fileptr = open(input_file_name, 'r')
    except FileNotFoundError:
        print("Invalid Input File")
        sys.exit(1)
    #goes through file line by line and takes out newline
    input_list = [line.strip() for line in fileptr]
    fileptr.close()
    return input_list

def read_lines(input_lines, stats):
    shift_type = "ES"
    prev_shift_type = "ES"
    prev_shift = []
    period = 1
    for i in range(0,len(input_lines)):
        line = input_lines[i].split()
        if not line[0].isnumeric():
            if line[0] == "PERIOD":
                period += 1
                line.pop(0)
            if line[0] == "ES" or line[0] == "PP" or line[0] == "PK":
                shift_type = line[0]
                line.pop(0)
            if not line[0].isnumeric:
                sys.exit("""incorrect type gametype change (ES, PP, PK) on line""" + str(i))

        j = 0
        while line[j].isnumeric():
            j += 1
            if j == len(line):
                break

        while j < len(line):
            # print(line[j] + " play type")
            if line[j] not in acceptable_types:
                sys.exit("""incorrect play type """ + str(i) + line[j])

            if line[j] not in stats.keys():
                stats[line[j]] = 1
            else:
                stats[line[j]] += 1
            j += 1

    return stats

if __name__ == "__main__":
    main()
