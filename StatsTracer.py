#!/usr/bin/env python3

import sys
import fileinput
import json
from json import JSONEncoder
from expect_goals_constants import *

acceptable_types = ["FHG", "FHN", "FHM","FMG", "FMN", "FMM","FLG", "FLN", "FLM","FLG", "AHG", "AHN", "AHM","AMG", "AMN", "AMM","ALG", "ALN", "ALM","ALG", "ALB", "AMB", "AHB", "FLB", "FMB", "FHB", "AEG", "FEG"]

roster = {
    12: "Braun",
    26: "Maia",
    22:"DiPaolo",
    13:"DeVries",
    21:"Eddy",
    17:"Hoekstraa",
    14:"Joseph",
    4:"Bateman",
    15:"Bandu",
    91:"Veilleux",
    44: "Attew",
    9: "Arthurs",
    19:"Monds",
    74:"Rickwood",
    25:"O'Hanisain",
    24:"Mount",
    71:"Turrin",
    86:"Pelletier",
    2:"Waram",
    6:"McInnis",
    7:"Amouse",
    88:"Yan"
}

prev_games = ["oct03", "oct16", "oct18", "oct23", "oct24", "oct31"]


class player:

    def __init__(self, number):
        self.gameTypes = {}
        self.number = number
        self.shifts = 0
        self.gameTypes["ES"] = {}
        self.gameTypes["PK"] = {}
        self.gameTypes["PP"] = {}

    def addPlay(self, gametype,statType,period):

        if self.gameTypes[gametype].get("TOTAL") == None:
            self.gameTypes[gametype]["TOTAL"] = dict()

        if self.gameTypes[gametype].get(period) == None:
            self.gameTypes[gametype][period] = dict()

        if statType in self.gameTypes[gametype][period]:
            self.gameTypes[gametype][period][statType] += 1
        else:
            self.gameTypes[gametype][period][statType] = 1

        if statType in self.gameTypes[gametype]["TOTAL"]:
            self.gameTypes[gametype]["TOTAL"][statType] += 1
        else:
            self.gameTypes[gametype]["TOTAL"][statType] = 1

    def addShift(self, gametype, period, addAll):
        if addAll == True:
            self.shifts += 1

        if self.gameTypes[gametype].get("TOTAL") == None:
            self.gameTypes[gametype]["TOTAL"] = dict()

        if self.gameTypes[gametype].get(period) == None:
            self.gameTypes[gametype][period] = dict()

        if "shifts" in self.gameTypes[gametype][period]:
            self.gameTypes[gametype][period]["shifts"] += 1
        else:
            self.gameTypes[gametype][period]["shifts"] = 1

        if "shifts" in self.gameTypes[gametype]["TOTAL"]:
            self.gameTypes[gametype]["TOTAL"]["shifts"] += 1
        else:
            self.gameTypes[gametype]["TOTAL"]["shifts"] = 1


    def toJSON(self):
        return json.dumps(self.__dict__ , cls = ComplexEncoder)



class team:
    def __init__(self):
        self.gameTypes = {}
        self.shifts = 0
        self.gameTypes["ES"] = {}
        self.gameTypes["PK"] = {}
        self.gameTypes["PP"] = {}
        self.gameTypes["GAMETOTAL"] = {}

    def addPlay(self, gametype,statType,period):

        if self.gameTypes[gametype].get("TOTAL") == None:
            self.gameTypes[gametype]["TOTAL"] = {}

        if self.gameTypes[gametype].get(period) == None:
            self.gameTypes[gametype][period] = dict()

        if statType in self.gameTypes[gametype][period]:
            self.gameTypes[gametype][period][statType] += 1
        else:
            self.gameTypes[gametype][period][statType] = 1

        if statType in self.gameTypes[gametype]["TOTAL"]:
            self.gameTypes[gametype]["TOTAL"][statType] += 1
        else:
            self.gameTypes[gametype]["TOTAL"][statType] = 1




        if self.gameTypes["GAMETOTAL"].get("TOTAL") == None:
            self.gameTypes["GAMETOTAL"]["TOTAL"] = dict()

        if self.gameTypes["GAMETOTAL"].get(period) == None:
            self.gameTypes["GAMETOTAL"][period] = dict()

        if statType in self.gameTypes["GAMETOTAL"][period]:
            self.gameTypes["GAMETOTAL"][period][statType] += 1
        else:
            self.gameTypes["GAMETOTAL"][period][statType] = 1

        if statType in self.gameTypes["GAMETOTAL"]["TOTAL"]:
            self.gameTypes["GAMETOTAL"]["TOTAL"][statType] += 1
        else:
            self.gameTypes["GAMETOTAL"]["TOTAL"][statType] = 1

def main():
    if len(sys.argv) < 5:
        print("Please enter file name and then Game Date and Opponent Name")
        sys.exit(0)



    input_file = sys.argv[1]
    game_date = sys.argv[2]
    opponent_name = sys.argv[3]
    path = sys.argv[4]
    
    input_lines = read_input(input_file)
    stats = read_lines(input_lines)
    
    print_team_to_latex(stats[1], stats[2], game_date, opponent_name, path)
    playerNums = [ int(key) for key in stats[0].keys()]
    playerNums.sort()
    for player in playerNums:
        print_player_to_latex(stats[0][player], stats[2], game_date, opponent_name, path)



def print_player_to_latex(playerObj, periods, game_date, opponent,path):
    with open('players/'+ path+ '/' +roster[playerObj.number]+  '.Rmd', 'w') as file:
        file.write("---\ntitle: "+ game_date + " vs. " + opponent + "\noutput: pdf_document\n---\n\n")
        file.write("""```{r setup, include=FALSE}\nknitr::opts_chunk$set(echo = TRUE)\n```\n\n""")
        types = ["ES","PP","PK"]
        typesFull = {"ES":"Even Strength", "PK": "Penalty Kill", "PP":"Powerplay"}
        file.write("# "+str(playerObj.number) + ": " + roster[playerObj.number]+ "  \n")
        for type in types:
            if playerObj.gameTypes[type].get("TOTAL") == None:
                playerObj.gameTypes[type]["TOTAL"] = dict()
            if playerObj.gameTypes[type]["TOTAL"].get("shifts") == None:
                playerObj.gameTypes[type]["TOTAL"]["shifts"] = 0
            for playType in acceptable_types:
                if playerObj.gameTypes[type]["TOTAL"].get(playType) == None:
                    playerObj.gameTypes[type]["TOTAL"][playType] = 0
                for period in range(1, periods+1):
                    if playerObj.gameTypes[type].get(period) == None:
                        playerObj.gameTypes[type][period] = dict()
                    if playerObj.gameTypes[type][period].get("shifts") == None:
                        playerObj.gameTypes[type][period]["shifts"] = 0
                    for playType in acceptable_types:
                        if playerObj.gameTypes[type][period].get(playType) == None:
                            playerObj.gameTypes[type][period][playType] = 0

        ForCorsi = playerObj.gameTypes["ES"]["TOTAL"]["FHN"] + playerObj.gameTypes["ES"]["TOTAL"]["FHB"] + playerObj.gameTypes["ES"]["TOTAL"]["FHM"] + playerObj.gameTypes["ES"]["TOTAL"]["FHG"] + playerObj.gameTypes["ES"]["TOTAL"]["FMN"] + playerObj.gameTypes["ES"]["TOTAL"]["FMB"] + playerObj.gameTypes["ES"]["TOTAL"]["FMM"] + playerObj.gameTypes["ES"]["TOTAL"]["FMG"] + playerObj.gameTypes["ES"]["TOTAL"]["FLN"] + playerObj.gameTypes["ES"]["TOTAL"]["FLB"] + playerObj.gameTypes["ES"]["TOTAL"]["FLM"] + playerObj.gameTypes["ES"]["TOTAL"]["FLG"]
        AgCorsi = playerObj.gameTypes["ES"]["TOTAL"]["AHN"] + playerObj.gameTypes["ES"]["TOTAL"]["AHB"] + playerObj.gameTypes["ES"]["TOTAL"]["AHM"] + playerObj.gameTypes["ES"]["TOTAL"]["AHG"] + playerObj.gameTypes["ES"]["TOTAL"]["AMN"] + playerObj.gameTypes["ES"]["TOTAL"]["AMB"] + playerObj.gameTypes["ES"]["TOTAL"]["AMM"] + playerObj.gameTypes["ES"]["TOTAL"]["AMG"] + playerObj.gameTypes["ES"]["TOTAL"]["ALN"] + playerObj.gameTypes["ES"]["TOTAL"]["ALB"] + playerObj.gameTypes["ES"]["TOTAL"]["ALM"] + playerObj.gameTypes["ES"]["TOTAL"]["ALG"]
        if ForCorsi + AgCorsi == 0:
            AgCorsi = 1
        file.write("### Corsi: "+ "{:.2f}".format((ForCorsi/(ForCorsi+AgCorsi))*100)  + "%  \n")
        ForFenwick = playerObj.gameTypes["ES"]["TOTAL"]["FHN"] + playerObj.gameTypes["ES"]["TOTAL"]["FHM"] + playerObj.gameTypes["ES"]["TOTAL"]["FHG"] + playerObj.gameTypes["ES"]["TOTAL"]["FMN"] + playerObj.gameTypes["ES"]["TOTAL"]["FMM"] + playerObj.gameTypes["ES"]["TOTAL"]["FMG"] + playerObj.gameTypes["ES"]["TOTAL"]["FLN"] + playerObj.gameTypes["ES"]["TOTAL"]["FLM"] + playerObj.gameTypes["ES"]["TOTAL"]["FLG"]
        AgFenwick = playerObj.gameTypes["ES"]["TOTAL"]["AHN"] + playerObj.gameTypes["ES"]["TOTAL"]["AHM"] + playerObj.gameTypes["ES"]["TOTAL"]["AHG"] + playerObj.gameTypes["ES"]["TOTAL"]["AMN"] + playerObj.gameTypes["ES"]["TOTAL"]["AMM"] + playerObj.gameTypes["ES"]["TOTAL"]["AMG"] + playerObj.gameTypes["ES"]["TOTAL"]["ALN"] + playerObj.gameTypes["ES"]["TOTAL"]["ALM"] + playerObj.gameTypes["ES"]["TOTAL"]["ALG"]
        if ForFenwick + AgFenwick == 0:
            AgFenwick = 1
        file.write("### Fenwick: "+ "{:.2f}".format((ForFenwick/(ForFenwick+AgFenwick))*100)  + "%  \n")

        xGF = FH_xG*(playerObj.gameTypes["ES"]["TOTAL"]["FHG"]+playerObj.gameTypes["ES"]["TOTAL"]["FHN"]+playerObj.gameTypes["ES"]["TOTAL"]["FHM"]) + FM_xG*(playerObj.gameTypes["ES"]["TOTAL"]["FMG"]+playerObj.gameTypes["ES"]["TOTAL"]["FMN"]+playerObj.gameTypes["ES"]["TOTAL"]["FMM"]) + FL_xG*(playerObj.gameTypes["ES"]["TOTAL"]["FLG"]+playerObj.gameTypes["ES"]["TOTAL"]["FLN"]+playerObj.gameTypes["ES"]["TOTAL"]["FLM"])
        xGA = AH_xG*(playerObj.gameTypes["ES"]["TOTAL"]["AHG"]+playerObj.gameTypes["ES"]["TOTAL"]["AHN"]+playerObj.gameTypes["ES"]["TOTAL"]["AHM"]) + AM_xG*(playerObj.gameTypes["ES"]["TOTAL"]["AMG"]+playerObj.gameTypes["ES"]["TOTAL"]["AMN"]+playerObj.gameTypes["ES"]["TOTAL"]["AMM"]) + FL_xG*(playerObj.gameTypes["ES"]["TOTAL"]["ALG"]+playerObj.gameTypes["ES"]["TOTAL"]["ALN"]+playerObj.gameTypes["ES"]["TOTAL"]["ALM"])
        if xGA + xGF == 0:
            file.write("### Even Strength Percent of expect Goals For: "+ "{:.2f}".format(0)  + "%  \n")
        else:
            file.write("### Even Strength Percent of expect Goals For: "+ "{:.2f}".format((xGF/(xGF+xGA))*100)  + "%  \n")
        file.write("### Even Strength Expected Goals For: "+ "{:.2f}".format(xGF)  + "  \n")
        file.write("### Even Strength Expected Goals Against: "+ "{:.2f}".format(xGA)  + "  \n")

        for type in types:
            if playerObj.gameTypes[type].get("TOTAL") == None:
                playerObj.gameTypes[type]["TOTAL"] = dict()
            if playerObj.gameTypes[type]["TOTAL"].get("shifts") == None:
                playerObj.gameTypes[type]["TOTAL"]["shifts"] = 0
            for playType in acceptable_types:
                if playerObj.gameTypes[type]["TOTAL"].get(playType) == None:
                    playerObj.gameTypes[type]["TOTAL"][playType] = 0


            file.write("## " + typesFull[type]+ "  \n")
            file.write("***\n")
            file.write("### Game Total:  \n")
            file.write("##### number of shifts: " + str(playerObj.gameTypes[type]["TOTAL"]["shifts"]) + "  \n")
            file.write("#### FOR  \n")
            file.write("  \n")
            file.write("\\begin{tabular}{ c || c | c | c || c}\n")
            file.write("& High & Medium & Low & Total\\\\\n")
            file.write("\hline\hline\n")
            file.write("Goal & " + str(playerObj.gameTypes[type]["TOTAL"]["FHG"]) + " & "  + str(playerObj.gameTypes[type]["TOTAL"]["FMG"]) + " & " + str(playerObj.gameTypes[type]["TOTAL"]["FLG"]) + " & " + str(playerObj.gameTypes[type]["TOTAL"]["FHG"] + playerObj.gameTypes[type]["TOTAL"]["FMG"] + playerObj.gameTypes[type]["TOTAL"]["FLG"]) + "\\\\\n")
            file.write("\hline\n")
            file.write("On Net & " + str(playerObj.gameTypes[type]["TOTAL"]["FHN"]) + " & "  + str(playerObj.gameTypes[type]["TOTAL"]["FMN"]) + " & " + str(playerObj.gameTypes[type]["TOTAL"]["FLN"]) + " & " + str(playerObj.gameTypes[type]["TOTAL"]["FHN"] + playerObj.gameTypes[type]["TOTAL"]["FMN"] + playerObj.gameTypes[type]["TOTAL"]["FLN"]) + "\\\\\n")
            file.write("\hline\n")
            file.write("Missed & " + str(playerObj.gameTypes[type]["TOTAL"]["FHM"]) + " & "  + str(playerObj.gameTypes[type]["TOTAL"]["FMM"]) + " & " + str(playerObj.gameTypes[type]["TOTAL"]["FLM"]) + " & " + str(playerObj.gameTypes[type]["TOTAL"]["FHM"] + playerObj.gameTypes[type]["TOTAL"]["FMM"] + playerObj.gameTypes[type]["TOTAL"]["FLM"]) + "\\\\\n")
            file.write("\hline\n")
            file.write("Blocked & " + str(playerObj.gameTypes[type]["TOTAL"]["FHB"]) + " & "  + str(playerObj.gameTypes[type]["TOTAL"]["FMB"]) + " & " + str(playerObj.gameTypes[type]["TOTAL"]["FLB"]) + " & " + str(playerObj.gameTypes[type]["TOTAL"]["FHB"] + playerObj.gameTypes[type]["TOTAL"]["FMB"] + playerObj.gameTypes[type]["TOTAL"]["FLB"]) + "\\\\\n")
            file.write("\hline\hline\n")
            file.write("Total & " + str(playerObj.gameTypes[type]["TOTAL"]["FHN"] + playerObj.gameTypes[type]["TOTAL"]["FHB"] + playerObj.gameTypes[type]["TOTAL"]["FHM"] + playerObj.gameTypes[type]["TOTAL"]["FHG"]) + " & "  + str(playerObj.gameTypes[type]["TOTAL"]["FMN"] + playerObj.gameTypes[type]["TOTAL"]["FMB"] + playerObj.gameTypes[type]["TOTAL"]["FMM"] + playerObj.gameTypes[type]["TOTAL"]["FMG"]) + " & " + str(playerObj.gameTypes[type]["TOTAL"]["FLN"] + playerObj.gameTypes[type]["TOTAL"]["FLB"] + playerObj.gameTypes[type]["TOTAL"]["FLM"] + playerObj.gameTypes[type]["TOTAL"]["FLG"]) + " & " + str(playerObj.gameTypes[type]["TOTAL"]["FHN"] + playerObj.gameTypes[type]["TOTAL"]["FHB"] + playerObj.gameTypes[type]["TOTAL"]["FHM"] + playerObj.gameTypes[type]["TOTAL"]["FHG"] + playerObj.gameTypes[type]["TOTAL"]["FMN"] + playerObj.gameTypes[type]["TOTAL"]["FMB"] + playerObj.gameTypes[type]["TOTAL"]["FMM"] + playerObj.gameTypes[type]["TOTAL"]["FMG"] + playerObj.gameTypes[type]["TOTAL"]["FLN"] + playerObj.gameTypes[type]["TOTAL"]["FLB"] + playerObj.gameTypes[type]["TOTAL"]["FLM"] + playerObj.gameTypes[type]["TOTAL"]["FLG"]) + "\\\\\n")
            file.write("\end{tabular}\n")
            file.write("\\vspace{5mm}  \n")
            file.write("#### AGAINST  \n")
            file.write("  \n")
            file.write("\\begin{tabular}{ c || c | c | c || c}\n")
            file.write("& High & Medium & Low & Total\\\\  \n")
            file.write("\hline\hline\n")
            file.write("Goal & " + str(playerObj.gameTypes[type]["TOTAL"]["AHG"]) + " & "  + str(playerObj.gameTypes[type]["TOTAL"]["AMG"]) + " & " + str(playerObj.gameTypes[type]["TOTAL"]["ALG"]) + " & " + str(playerObj.gameTypes[type]["TOTAL"]["AHG"] + playerObj.gameTypes[type]["TOTAL"]["AMG"] + playerObj.gameTypes[type]["TOTAL"]["ALG"]) + "\\\\\n")
            file.write("\hline\n")
            file.write("On Net & " + str(playerObj.gameTypes[type]["TOTAL"]["AHN"]) + " & "  + str(playerObj.gameTypes[type]["TOTAL"]["AMN"]) + " & " + str(playerObj.gameTypes[type]["TOTAL"]["ALN"]) + " & " + str(playerObj.gameTypes[type]["TOTAL"]["AHN"] + playerObj.gameTypes[type]["TOTAL"]["AMN"] + playerObj.gameTypes[type]["TOTAL"]["ALN"]) + "\\\\\n")
            file.write("\hline\n")
            file.write("Missed & " + str(playerObj.gameTypes[type]["TOTAL"]["AHM"]) + " & "  + str(playerObj.gameTypes[type]["TOTAL"]["AMM"]) + " & " + str(playerObj.gameTypes[type]["TOTAL"]["ALM"]) + " & " + str(playerObj.gameTypes[type]["TOTAL"]["AHM"] + playerObj.gameTypes[type]["TOTAL"]["AMM"] + playerObj.gameTypes[type]["TOTAL"]["ALM"]) + "\\\\\n")
            file.write("\hline\n")
            file.write("Blocked & " + str(playerObj.gameTypes[type]["TOTAL"]["AHB"]) + " & "  + str(playerObj.gameTypes[type]["TOTAL"]["AMB"]) + " & " + str(playerObj.gameTypes[type]["TOTAL"]["ALB"]) + " & " + str(playerObj.gameTypes[type]["TOTAL"]["AHB"] + playerObj.gameTypes[type]["TOTAL"]["AMB"] + playerObj.gameTypes[type]["TOTAL"]["ALB"]) + "\\\\\n")
            file.write("\hline\hline\n")
            file.write("Total & " + str(playerObj.gameTypes[type]["TOTAL"]["AHN"] + playerObj.gameTypes[type]["TOTAL"]["AHB"] + playerObj.gameTypes[type]["TOTAL"]["AHM"] + playerObj.gameTypes[type]["TOTAL"]["AHG"]) + " & "  + str(playerObj.gameTypes[type]["TOTAL"]["AMN"] + playerObj.gameTypes[type]["TOTAL"]["AMB"] + playerObj.gameTypes[type]["TOTAL"]["AMM"] + playerObj.gameTypes[type]["TOTAL"]["AMG"]) + " & " + str(playerObj.gameTypes[type]["TOTAL"]["ALN"] + playerObj.gameTypes[type]["TOTAL"]["ALB"] + playerObj.gameTypes[type]["TOTAL"]["ALM"] + playerObj.gameTypes[type]["TOTAL"]["ALG"]) + " & " + str(playerObj.gameTypes[type]["TOTAL"]["AHN"] + playerObj.gameTypes[type]["TOTAL"]["AHB"] + playerObj.gameTypes[type]["TOTAL"]["AHM"] + playerObj.gameTypes[type]["TOTAL"]["AHG"] + playerObj.gameTypes[type]["TOTAL"]["AMN"] + playerObj.gameTypes[type]["TOTAL"]["AMB"] + playerObj.gameTypes[type]["TOTAL"]["AMM"] + playerObj.gameTypes[type]["TOTAL"]["AMG"] + playerObj.gameTypes[type]["TOTAL"]["ALN"] + playerObj.gameTypes[type]["TOTAL"]["ALB"] + playerObj.gameTypes[type]["TOTAL"]["ALM"] + playerObj.gameTypes[type]["TOTAL"]["ALG"]) + "\\\\\n")
            file.write("\end{tabular}\n")
            file.write("  \n")

            for period in range(1, periods+1):
                if playerObj.gameTypes[type].get(period) == None:
                    playerObj.gameTypes[type][period] = dict()
                if playerObj.gameTypes[type][period].get("shifts") == None:
                    playerObj.gameTypes[type][period]["shifts"] = 0
                for playType in acceptable_types:
                    if playerObj.gameTypes[type][period].get(playType) == None:
                        playerObj.gameTypes[type][period][playType] = 0

                # file.write("### Period: "+ str(period) + "  \n")
                # file.write("##### number of shifts: " + str(playerObj.gameTypes[type][period]["shifts"]) + "  \n")
                # file.write("#### FOR  \n")
                # file.write("  \n")
                # file.write("\\begin{tabular}{ c || c | c | c || c}\n")
                # file.write("& High & Medium & Low & Total\\\\  \n")
                # file.write("\hline\hline\n")
                # file.write("Goal & " + str(playerObj.gameTypes[type][period]["FHG"]) + " & "  + str(playerObj.gameTypes[type][period]["FMG"]) + " & " + str(playerObj.gameTypes[type][period]["FLG"]) + " & " + str(playerObj.gameTypes[type][period]["FHG"] + playerObj.gameTypes[type][period]["FMG"] + playerObj.gameTypes[type][period]["FLG"]) + "\\\\\n")
                # file.write("\hline\n")
                # file.write("On Net & " + str(playerObj.gameTypes[type][period]["FHN"]) + " & "  + str(playerObj.gameTypes[type][period]["FMN"]) + " & " + str(playerObj.gameTypes[type][period]["FLN"]) + " & " + str(playerObj.gameTypes[type][period]["FHN"] + playerObj.gameTypes[type][period]["FMN"] + playerObj.gameTypes[type][period]["FLN"]) + "\\\\\n")
                # file.write("\hline\n")
                # file.write("Missed & " + str(playerObj.gameTypes[type][period]["FHM"]) + " & "  + str(playerObj.gameTypes[type][period]["FMM"]) + " & " + str(playerObj.gameTypes[type][period]["FLM"]) + " & " + str(playerObj.gameTypes[type][period]["FHM"] + playerObj.gameTypes[type][period]["FMM"] + playerObj.gameTypes[type][period]["FLM"]) + "\\\\\n")
                # file.write("\hline\n")
                # file.write("Blocked & " + str(playerObj.gameTypes[type][period]["FHB"]) + " & "  + str(playerObj.gameTypes[type][period]["FMB"]) + " & " + str(playerObj.gameTypes[type][period]["FLB"]) + " & " + str(playerObj.gameTypes[type][period]["FHB"] + playerObj.gameTypes[type][period]["FMB"] + playerObj.gameTypes[type][period]["FLB"]) + "\\\\\n")
                # file.write("\hline\hline\n")
                # file.write("Total & " + str(playerObj.gameTypes[type][period]["FHN"] + playerObj.gameTypes[type][period]["FHB"] + playerObj.gameTypes[type][period]["FHM"] + playerObj.gameTypes[type][period]["FHG"]) + " & "  + str(playerObj.gameTypes[type][period]["FMN"] + playerObj.gameTypes[type][period]["FMB"] + playerObj.gameTypes[type][period]["FMM"] + playerObj.gameTypes[type][period]["FMG"]) + " & " + str(playerObj.gameTypes[type][period]["FLN"] + playerObj.gameTypes[type][period]["FLB"] + playerObj.gameTypes[type][period]["FLM"] + playerObj.gameTypes[type][period]["FLG"]) + " & " + str(playerObj.gameTypes[type][period]["FHN"] + playerObj.gameTypes[type][period]["FHB"] + playerObj.gameTypes[type][period]["FHM"] + playerObj.gameTypes[type][period]["FHG"] + playerObj.gameTypes[type][period]["FMN"] + playerObj.gameTypes[type][period]["FMB"] + playerObj.gameTypes[type][period]["FMM"] + playerObj.gameTypes[type][period]["FMG"] + playerObj.gameTypes[type][period]["FLN"] + playerObj.gameTypes[type][period]["FLB"] + playerObj.gameTypes[type][period]["FLM"] + playerObj.gameTypes[type][period]["FLG"]) + "\\\\\n")
                # file.write("\end{tabular}\n")
                # file.write("\\vspace{5mm}  \n")
                # file.write("#### AGAINST  \n")
                # file.write("  \n")
                # file.write("\\begin{tabular}{ c || c | c | c || c}\n")
                # file.write("& High & Medium & Low & Total\\\\  \n")
                # file.write("\hline\hline\n")
                # file.write("Goal & " + str(playerObj.gameTypes[type][period]["AHG"]) + " & "  + str(playerObj.gameTypes[type][period]["AMG"]) + " & " + str(playerObj.gameTypes[type][period]["ALG"]) + " & " + str(playerObj.gameTypes[type][period]["AHG"] + playerObj.gameTypes[type][period]["AMG"] + playerObj.gameTypes[type][period]["ALG"]) + "\\\\\n")
                # file.write("\hline\n")
                # file.write("On Net & " + str(playerObj.gameTypes[type][period]["AHN"]) + " & "  + str(playerObj.gameTypes[type][period]["AMN"]) + " & " + str(playerObj.gameTypes[type][period]["ALN"]) + " & " + str(playerObj.gameTypes[type][period]["AHN"] + playerObj.gameTypes[type][period]["AMN"] + playerObj.gameTypes[type][period]["ALN"]) + "\\\\\n")
                # file.write("\hline\n")
                # file.write("Missed & " + str(playerObj.gameTypes[type][period]["AHM"]) + " & "  + str(playerObj.gameTypes[type][period]["AMM"]) + " & " + str(playerObj.gameTypes[type][period]["ALM"]) + " & " + str(playerObj.gameTypes[type][period]["AHM"] + playerObj.gameTypes[type][period]["AMM"] + playerObj.gameTypes[type][period]["ALM"]) + "\\\\\n")
                # file.write("\hline\n")
                # file.write("Blocked & " + str(playerObj.gameTypes[type][period]["AHB"]) + " & "  + str(playerObj.gameTypes[type][period]["AMB"]) + " & " + str(playerObj.gameTypes[type][period]["ALB"]) + " & " + str(playerObj.gameTypes[type][period]["AHB"] + playerObj.gameTypes[type][period]["AMB"] + playerObj.gameTypes[type][period]["ALB"]) + "\\\\\n")
                # file.write("\hline\hline\n")
                # file.write("Total & " + str(playerObj.gameTypes[type][period]["AHN"] + playerObj.gameTypes[type][period]["AHB"] + playerObj.gameTypes[type][period]["AHM"] + playerObj.gameTypes[type][period]["AHG"]) + " & "  + str(playerObj.gameTypes[type][period]["AMN"] + playerObj.gameTypes[type][period]["AMB"] + playerObj.gameTypes[type][period]["AMM"] + playerObj.gameTypes[type][period]["AMG"]) + " & " + str(playerObj.gameTypes[type][period]["ALN"] + playerObj.gameTypes[type][period]["ALB"] + playerObj.gameTypes[type][period]["ALM"] + playerObj.gameTypes[type][period]["ALG"]) + " & " + str(playerObj.gameTypes[type][period]["AHN"] + playerObj.gameTypes[type][period]["AHB"] + playerObj.gameTypes[type][period]["AHM"] + playerObj.gameTypes[type][period]["AHG"] + playerObj.gameTypes[type][period]["AMN"] + playerObj.gameTypes[type][period]["AMB"] + playerObj.gameTypes[type][period]["AMM"] + playerObj.gameTypes[type][period]["AMG"] + playerObj.gameTypes[type][period]["ALN"] + playerObj.gameTypes[type][period]["ALB"] + playerObj.gameTypes[type][period]["ALM"] + playerObj.gameTypes[type][period]["ALG"]) + "\\\\\n")
                # file.write("\end{tabular}\n")
                # file.write("  \n")
        file.write("### Fenwick: "+ "{:.2f}".format((ForFenwick/(ForFenwick+AgFenwick))*100)  + "%  \n")
        file.write("\pagebreak\n")
    file.close()

def print_team_to_latex(teamObj, periods, game_date, opponent, path):
    with open('players/'+ path+ '/team.Rmd', 'w') as file:
        file.write("---\ntitle: "+ game_date + " vs. " + opponent + "\noutput: pdf_document\n---\n\n")
        file.write("""```{r setup, include=FALSE}\nknitr::opts_chunk$set(echo = TRUE)\n```\n\n""")

        types = ["GAMETOTAL","ES","PP","PK"]
        typesFull = {"ES":"Even Strength", "PK": "Penalty Kill", "PP":"Powerplay", "GAMETOTAL":"Game/Period Summary"}
        file.write("# Team  \n")
        for type in types:
            if teamObj.gameTypes[type].get("TOTAL") == None:
                teamObj.gameTypes[type]["TOTAL"] = dict()
            if teamObj.gameTypes[type]["TOTAL"].get("shifts") == None:
                teamObj.gameTypes[type]["TOTAL"]["shifts"] = 0
            for playType in acceptable_types:
                if teamObj.gameTypes[type]["TOTAL"].get(playType) == None:
                    teamObj.gameTypes[type]["TOTAL"][playType] = 0
                for period in range(1,periods+1):
                    if teamObj.gameTypes[type].get(period) == None:
                        teamObj.gameTypes[type][period] = dict()
                    if teamObj.gameTypes[type][period].get("shifts") == None:
                        teamObj.gameTypes[type][period]["shifts"] = 0
                    for playType in acceptable_types:
                        if teamObj.gameTypes[type][period].get(playType) == None:
                            teamObj.gameTypes[type][period][playType] = 0
        ForCorsi = teamObj.gameTypes["ES"]["TOTAL"]["FHN"] + teamObj.gameTypes["ES"]["TOTAL"]["FHB"] + teamObj.gameTypes["ES"]["TOTAL"]["FHM"] + teamObj.gameTypes["ES"]["TOTAL"]["FHG"] + teamObj.gameTypes["ES"]["TOTAL"]["FMN"] + teamObj.gameTypes["ES"]["TOTAL"]["FMB"] + teamObj.gameTypes["ES"]["TOTAL"]["FMM"] + teamObj.gameTypes["ES"]["TOTAL"]["FMG"] + teamObj.gameTypes["ES"]["TOTAL"]["FLN"] + teamObj.gameTypes["ES"]["TOTAL"]["FLB"] + teamObj.gameTypes["ES"]["TOTAL"]["FLM"] + teamObj.gameTypes["ES"]["TOTAL"]["FLG"]
        AgCorsi = teamObj.gameTypes["ES"]["TOTAL"]["AHN"] + teamObj.gameTypes["ES"]["TOTAL"]["AHB"] + teamObj.gameTypes["ES"]["TOTAL"]["AHM"] + teamObj.gameTypes["ES"]["TOTAL"]["AHG"] + teamObj.gameTypes["ES"]["TOTAL"]["AMN"] + teamObj.gameTypes["ES"]["TOTAL"]["AMB"] + teamObj.gameTypes["ES"]["TOTAL"]["AMM"] + teamObj.gameTypes["ES"]["TOTAL"]["AMG"] + teamObj.gameTypes["ES"]["TOTAL"]["ALN"] + teamObj.gameTypes["ES"]["TOTAL"]["ALB"] + teamObj.gameTypes["ES"]["TOTAL"]["ALM"] + teamObj.gameTypes["ES"]["TOTAL"]["ALG"]
        if ForCorsi + AgCorsi == 0:
            AgCorsi = 1
        file.write("### Corsi: "+ "{:.2f}".format((ForCorsi/(ForCorsi+AgCorsi))*100)  + "%  \n")
        ForFenwick = teamObj.gameTypes["ES"]["TOTAL"]["FHN"] + teamObj.gameTypes["ES"]["TOTAL"]["FHM"] + teamObj.gameTypes["ES"]["TOTAL"]["FHG"] + teamObj.gameTypes["ES"]["TOTAL"]["FMN"] + teamObj.gameTypes["ES"]["TOTAL"]["FMM"] + teamObj.gameTypes["ES"]["TOTAL"]["FMG"] + teamObj.gameTypes["ES"]["TOTAL"]["FLN"] + teamObj.gameTypes["ES"]["TOTAL"]["FLM"] + teamObj.gameTypes["ES"]["TOTAL"]["FLG"]
        AgFenwick = teamObj.gameTypes["ES"]["TOTAL"]["AHN"] + teamObj.gameTypes["ES"]["TOTAL"]["AHM"] + teamObj.gameTypes["ES"]["TOTAL"]["AHG"] + teamObj.gameTypes["ES"]["TOTAL"]["AMN"] + teamObj.gameTypes["ES"]["TOTAL"]["AMM"] + teamObj.gameTypes["ES"]["TOTAL"]["AMG"] + teamObj.gameTypes["ES"]["TOTAL"]["ALN"] + teamObj.gameTypes["ES"]["TOTAL"]["ALM"] + teamObj.gameTypes["ES"]["TOTAL"]["ALG"]
        if ForFenwick + AgFenwick == 0:
            AgFenwick = 1
        file.write("### Fenwick: "+ "{:.2f}".format((ForFenwick/(ForFenwick+AgFenwick))*100)  + "%  \n")

        xGF = FH_xG*(teamObj.gameTypes["ES"]["TOTAL"]["FHG"]+teamObj.gameTypes["ES"]["TOTAL"]["FHN"]+teamObj.gameTypes["ES"]["TOTAL"]["FHM"]) + FM_xG*(teamObj.gameTypes["ES"]["TOTAL"]["FMG"]+teamObj.gameTypes["ES"]["TOTAL"]["FMN"]+teamObj.gameTypes["ES"]["TOTAL"]["FMM"]) + FL_xG*(teamObj.gameTypes["ES"]["TOTAL"]["FLG"]+teamObj.gameTypes["ES"]["TOTAL"]["FLN"]+teamObj.gameTypes["ES"]["TOTAL"]["FLM"])
        xGF += FH_xG*(teamObj.gameTypes["PP"]["TOTAL"]["FHG"]+teamObj.gameTypes["PP"]["TOTAL"]["FHN"]+teamObj.gameTypes["PP"]["TOTAL"]["FHM"]) + FM_xG*(teamObj.gameTypes["PP"]["TOTAL"]["FMG"]+teamObj.gameTypes["PP"]["TOTAL"]["FMN"]+teamObj.gameTypes["PP"]["TOTAL"]["FMM"]) + FL_xG*(teamObj.gameTypes["PP"]["TOTAL"]["FLG"]+teamObj.gameTypes["PP"]["TOTAL"]["FLN"]+teamObj.gameTypes["PP"]["TOTAL"]["FLM"])
        xGF += FH_xG*(teamObj.gameTypes["PK"]["TOTAL"]["FHG"]+teamObj.gameTypes["PK"]["TOTAL"]["FHN"]+teamObj.gameTypes["PK"]["TOTAL"]["FHM"]) + FM_xG*(teamObj.gameTypes["PK"]["TOTAL"]["FMG"]+teamObj.gameTypes["PK"]["TOTAL"]["FMN"]+teamObj.gameTypes["PK"]["TOTAL"]["FMM"]) + FL_xG*(teamObj.gameTypes["PK"]["TOTAL"]["FLG"]+teamObj.gameTypes["PK"]["TOTAL"]["FLN"]+teamObj.gameTypes["PK"]["TOTAL"]["FLM"])
        xGA = AH_xG*(teamObj.gameTypes["ES"]["TOTAL"]["AHG"]+teamObj.gameTypes["ES"]["TOTAL"]["AHN"]+teamObj.gameTypes["ES"]["TOTAL"]["AHM"]) + AM_xG*(teamObj.gameTypes["ES"]["TOTAL"]["AMG"]+teamObj.gameTypes["ES"]["TOTAL"]["AMN"]+teamObj.gameTypes["ES"]["TOTAL"]["AMM"]) + FL_xG*(teamObj.gameTypes["ES"]["TOTAL"]["ALG"]+teamObj.gameTypes["ES"]["TOTAL"]["ALN"]+teamObj.gameTypes["ES"]["TOTAL"]["ALM"])
        xGA += AH_xG*(teamObj.gameTypes["PP"]["TOTAL"]["AHG"]+teamObj.gameTypes["PP"]["TOTAL"]["AHN"]+teamObj.gameTypes["PP"]["TOTAL"]["AHM"]) + AM_xG*(teamObj.gameTypes["PP"]["TOTAL"]["AMG"]+teamObj.gameTypes["PP"]["TOTAL"]["AMN"]+teamObj.gameTypes["PP"]["TOTAL"]["AMM"]) + FL_xG*(teamObj.gameTypes["PP"]["TOTAL"]["ALG"]+teamObj.gameTypes["PP"]["TOTAL"]["ALN"]+teamObj.gameTypes["PP"]["TOTAL"]["ALM"])
        xGA += AH_xG*(teamObj.gameTypes["PK"]["TOTAL"]["AHG"]+teamObj.gameTypes["PK"]["TOTAL"]["AHN"]+teamObj.gameTypes["PK"]["TOTAL"]["AHM"]) + AM_xG*(teamObj.gameTypes["PK"]["TOTAL"]["AMG"]+teamObj.gameTypes["PK"]["TOTAL"]["AMN"]+teamObj.gameTypes["PK"]["TOTAL"]["AMM"]) + FL_xG*(teamObj.gameTypes["PK"]["TOTAL"]["ALG"]+teamObj.gameTypes["PK"]["TOTAL"]["ALN"]+teamObj.gameTypes["PK"]["TOTAL"]["ALM"])

        file.write("### Overall Percent of expect Goals For: "+ "{:.2f}".format((xGF/(xGF+xGA))*100)  + "%  \n")
        file.write("### Overall Expected Goals For: "+ "{:.2f}".format(xGF)  + "  \n")
        file.write("### Overall Expected Goals Against: "+ "{:.2f}".format(xGA)  + "  \n")

        xGF_ES = FH_xG*(teamObj.gameTypes["ES"]["TOTAL"]["FHG"]+teamObj.gameTypes["ES"]["TOTAL"]["FHN"]+teamObj.gameTypes["ES"]["TOTAL"]["FHM"]) + FM_xG*(teamObj.gameTypes["ES"]["TOTAL"]["FMG"]+teamObj.gameTypes["ES"]["TOTAL"]["FMN"]+teamObj.gameTypes["ES"]["TOTAL"]["FMM"]) + FL_xG*(teamObj.gameTypes["ES"]["TOTAL"]["FLG"]+teamObj.gameTypes["ES"]["TOTAL"]["FLN"]+teamObj.gameTypes["ES"]["TOTAL"]["FLM"])
        xGA_ES = AH_xG*(teamObj.gameTypes["ES"]["TOTAL"]["AHG"]+teamObj.gameTypes["ES"]["TOTAL"]["AHN"]+teamObj.gameTypes["ES"]["TOTAL"]["AHM"]) + AM_xG*(teamObj.gameTypes["ES"]["TOTAL"]["AMG"]+teamObj.gameTypes["ES"]["TOTAL"]["AMN"]+teamObj.gameTypes["ES"]["TOTAL"]["AMM"]) + FL_xG*(teamObj.gameTypes["ES"]["TOTAL"]["ALG"]+teamObj.gameTypes["ES"]["TOTAL"]["ALN"]+teamObj.gameTypes["ES"]["TOTAL"]["ALM"])

        file.write("### Even Strength Percent of expect Goals For: "+ "{:.2f}".format((xGF_ES/(xGF_ES+xGA_ES))*100)  + "%  \n")
        file.write("### Even Strength Expected Goals For: "+ "{:.2f}".format(xGF_ES)  + "  \n")
        file.write("### Even Strength Expected Goals Against: "+ "{:.2f}".format(xGA_ES)  + "  \n")

        for type in types:
            if teamObj.gameTypes[type].get("TOTAL") == None:
                teamObj.gameTypes[type]["TOTAL"] = dict()
            if teamObj.gameTypes[type]["TOTAL"].get("shifts") == None:
                teamObj.gameTypes[type]["TOTAL"]["shifts"] = 0
            for playType in acceptable_types:
                if teamObj.gameTypes[type]["TOTAL"].get(playType) == None:
                    teamObj.gameTypes[type]["TOTAL"][playType] = 0


            file.write("## " + typesFull[type] + "  \n")
            file.write("***\n")
            file.write("### Game Total:  \n")
            file.write("#### FOR  \n")
            file.write("  \n")
            file.write("\\begin{tabular}{ c || c | c | c || c}\n")
            file.write("& High & Medium & Low & Total\\\\  \n")
            file.write("\hline\hline\n")
            file.write("Goal & " + str(teamObj.gameTypes[type]["TOTAL"]["FHG"]) + " & "  + str(teamObj.gameTypes[type]["TOTAL"]["FMG"]) + " & " + str(teamObj.gameTypes[type]["TOTAL"]["FLG"]) + " & " + str(teamObj.gameTypes[type]["TOTAL"]["FHG"] + teamObj.gameTypes[type]["TOTAL"]["FMG"] + teamObj.gameTypes[type]["TOTAL"]["FLG"]) + "\\\\\n")
            file.write("\hline\n")
            file.write("On Net & " + str(teamObj.gameTypes[type]["TOTAL"]["FHN"]) + " & "  + str(teamObj.gameTypes[type]["TOTAL"]["FMN"]) + " & " + str(teamObj.gameTypes[type]["TOTAL"]["FLN"]) + " & " + str(teamObj.gameTypes[type]["TOTAL"]["FHN"] + teamObj.gameTypes[type]["TOTAL"]["FMN"] + teamObj.gameTypes[type]["TOTAL"]["FLN"]) + "\\\\\n")
            file.write("\hline\n")
            file.write("Missed & " + str(teamObj.gameTypes[type]["TOTAL"]["FHM"]) + " & "  + str(teamObj.gameTypes[type]["TOTAL"]["FMM"]) + " & " + str(teamObj.gameTypes[type]["TOTAL"]["FLM"]) + " & " + str(teamObj.gameTypes[type]["TOTAL"]["FHM"] + teamObj.gameTypes[type]["TOTAL"]["FMM"] + teamObj.gameTypes[type]["TOTAL"]["FLM"]) + "\\\\\n")
            file.write("\hline\n")
            file.write("Blocked & " + str(teamObj.gameTypes[type]["TOTAL"]["FHB"]) + " & "  + str(teamObj.gameTypes[type]["TOTAL"]["FMB"]) + " & " + str(teamObj.gameTypes[type]["TOTAL"]["FLB"]) + " & " + str(teamObj.gameTypes[type]["TOTAL"]["FHB"] + teamObj.gameTypes[type]["TOTAL"]["FMB"] + teamObj.gameTypes[type]["TOTAL"]["FLB"]) + "\\\\\n")
            file.write("\hline\hline\n")
            file.write("Total & " + str(teamObj.gameTypes[type]["TOTAL"]["FHN"] + teamObj.gameTypes[type]["TOTAL"]["FHB"] + teamObj.gameTypes[type]["TOTAL"]["FHM"] + teamObj.gameTypes[type]["TOTAL"]["FHG"]) + " & "  + str(teamObj.gameTypes[type]["TOTAL"]["FMN"] + teamObj.gameTypes[type]["TOTAL"]["FMB"] + teamObj.gameTypes[type]["TOTAL"]["FMM"] + teamObj.gameTypes[type]["TOTAL"]["FMG"]) + " & " + str(teamObj.gameTypes[type]["TOTAL"]["FLN"] + teamObj.gameTypes[type]["TOTAL"]["FLB"] + teamObj.gameTypes[type]["TOTAL"]["FLM"] + teamObj.gameTypes[type]["TOTAL"]["FLG"]) + " & " + str(teamObj.gameTypes[type]["TOTAL"]["FHN"] + teamObj.gameTypes[type]["TOTAL"]["FHB"] + teamObj.gameTypes[type]["TOTAL"]["FHM"] + teamObj.gameTypes[type]["TOTAL"]["FHG"] + teamObj.gameTypes[type]["TOTAL"]["FMN"] + teamObj.gameTypes[type]["TOTAL"]["FMB"] + teamObj.gameTypes[type]["TOTAL"]["FMM"] + teamObj.gameTypes[type]["TOTAL"]["FMG"] + teamObj.gameTypes[type]["TOTAL"]["FLN"] + teamObj.gameTypes[type]["TOTAL"]["FLB"] + teamObj.gameTypes[type]["TOTAL"]["FLM"] + teamObj.gameTypes[type]["TOTAL"]["FLG"]) + "  \n")
            file.write("\end{tabular}\n")
            file.write("\\vspace{5mm}  \n")
            file.write("#### AGAINST  \n")
            file.write("  \n")
            file.write("\\begin{tabular}{ c || c | c | c || c}\n")
            file.write("& High & Medium & Low & Total\\\\  \n")
            file.write("\hline\hline\n")
            file.write("Goal & " + str(teamObj.gameTypes[type]["TOTAL"]["AHG"]) + " & "  + str(teamObj.gameTypes[type]["TOTAL"]["AMG"]) + " & " + str(teamObj.gameTypes[type]["TOTAL"]["ALG"]) + " & " + str(teamObj.gameTypes[type]["TOTAL"]["AHG"] + teamObj.gameTypes[type]["TOTAL"]["AMG"] + teamObj.gameTypes[type]["TOTAL"]["ALG"]) + "\\\\\n")
            file.write("\hline\n")
            file.write("On Net & " + str(teamObj.gameTypes[type]["TOTAL"]["AHN"]) + " & "  + str(teamObj.gameTypes[type]["TOTAL"]["AMN"]) + " & " + str(teamObj.gameTypes[type]["TOTAL"]["ALN"]) + " & " + str(teamObj.gameTypes[type]["TOTAL"]["AHN"] + teamObj.gameTypes[type]["TOTAL"]["AMN"] + teamObj.gameTypes[type]["TOTAL"]["ALN"]) + "\\\\\n")
            file.write("\hline\n")
            file.write("Missed & " + str(teamObj.gameTypes[type]["TOTAL"]["AHM"]) + " & "  + str(teamObj.gameTypes[type]["TOTAL"]["AMM"]) + " & " + str(teamObj.gameTypes[type]["TOTAL"]["ALM"]) + " & " + str(teamObj.gameTypes[type]["TOTAL"]["AHM"] + teamObj.gameTypes[type]["TOTAL"]["AMM"] + teamObj.gameTypes[type]["TOTAL"]["ALM"]) + "\\\\\n")
            file.write("\hline\n")
            file.write("Blocked & " + str(teamObj.gameTypes[type]["TOTAL"]["AHB"]) + " & "  + str(teamObj.gameTypes[type]["TOTAL"]["AMB"]) + " & " + str(teamObj.gameTypes[type]["TOTAL"]["ALB"]) + " & " + str(teamObj.gameTypes[type]["TOTAL"]["AHB"] + teamObj.gameTypes[type]["TOTAL"]["AMB"] + teamObj.gameTypes[type]["TOTAL"]["ALB"]) + "\\\\\n")
            file.write("\hline\hline\n")
            file.write("Total & " + str(teamObj.gameTypes[type]["TOTAL"]["AHN"] + teamObj.gameTypes[type]["TOTAL"]["AHB"] + teamObj.gameTypes[type]["TOTAL"]["AHM"] + teamObj.gameTypes[type]["TOTAL"]["AHG"]) + " & "  + str(teamObj.gameTypes[type]["TOTAL"]["AMN"] + teamObj.gameTypes[type]["TOTAL"]["AMB"] + teamObj.gameTypes[type]["TOTAL"]["AMM"] + teamObj.gameTypes[type]["TOTAL"]["AMG"]) + " & " + str(teamObj.gameTypes[type]["TOTAL"]["ALN"] + teamObj.gameTypes[type]["TOTAL"]["ALB"] + teamObj.gameTypes[type]["TOTAL"]["ALM"] + teamObj.gameTypes[type]["TOTAL"]["ALG"]) + " & " + str(teamObj.gameTypes[type]["TOTAL"]["AHN"] + teamObj.gameTypes[type]["TOTAL"]["AHB"] + teamObj.gameTypes[type]["TOTAL"]["AHM"] + teamObj.gameTypes[type]["TOTAL"]["AHG"] + teamObj.gameTypes[type]["TOTAL"]["AMN"] + teamObj.gameTypes[type]["TOTAL"]["AMB"] + teamObj.gameTypes[type]["TOTAL"]["AMM"] + teamObj.gameTypes[type]["TOTAL"]["AMG"] + teamObj.gameTypes[type]["TOTAL"]["ALN"] + teamObj.gameTypes[type]["TOTAL"]["ALB"] + teamObj.gameTypes[type]["TOTAL"]["ALM"] + teamObj.gameTypes[type]["TOTAL"]["ALG"]) + "  \n")
            file.write("\end{tabular}\n")
            file.write("  \n")

            for period in range(1,periods+1):
                if teamObj.gameTypes[type].get(period) == None:
                    teamObj.gameTypes[type][period] = dict()
                if teamObj.gameTypes[type][period].get("shifts") == None:
                    teamObj.gameTypes[type][period]["shifts"] = 0
                for playType in acceptable_types:
                    if teamObj.gameTypes[type][period].get(playType) == None:
                        teamObj.gameTypes[type][period][playType] = 0




                # file.write("### Period: "+ str(period) + "  \n")
                # file.write("#### FOR  \n")
                # file.write("  \n")
                # file.write("\\begin{tabular}{ c || c | c | c || c}\n")
                # file.write("& High & Medium & Low & Total\\\\  \n")
                # file.write("\hline\hline\n")
                # file.write("Goal & " + str(teamObj.gameTypes[type][period]["FHG"]) + " & "  + str(teamObj.gameTypes[type][period]["FMG"]) + " & " + str(teamObj.gameTypes[type][period]["FLG"]) + " & " + str(teamObj.gameTypes[type][period]["FHG"] + teamObj.gameTypes[type][period]["FMG"] + teamObj.gameTypes[type][period]["FLG"]) + "\\\\\n")
                # file.write("\hline\n")
                # file.write("On Net & " + str(teamObj.gameTypes[type][period]["FHN"]) + " & "  + str(teamObj.gameTypes[type][period]["FMN"]) + " & " + str(teamObj.gameTypes[type][period]["FLN"]) + " & " + str(teamObj.gameTypes[type][period]["FHN"] + teamObj.gameTypes[type][period]["FMN"] + teamObj.gameTypes[type][period]["FLN"]) + "\\\\\n")
                # file.write("\hline\n")
                # file.write("Missed & " + str(teamObj.gameTypes[type][period]["FHM"]) + " & "  + str(teamObj.gameTypes[type][period]["FMM"]) + " & " + str(teamObj.gameTypes[type][period]["FLM"]) + " & " + str(teamObj.gameTypes[type][period]["FHM"] + teamObj.gameTypes[type][period]["FMM"] + teamObj.gameTypes[type][period]["FLM"]) + "\\\\\n")
                # file.write("\hline\n")
                # file.write("Blocked & " + str(teamObj.gameTypes[type][period]["FHB"]) + " & "  + str(teamObj.gameTypes[type][period]["FMB"]) + " & " + str(teamObj.gameTypes[type][period]["FLB"]) + " & " + str(teamObj.gameTypes[type][period]["FHB"] + teamObj.gameTypes[type][period]["FMB"] + teamObj.gameTypes[type][period]["FLB"]) + "\\\\\n")
                # file.write("\hline\hline\n")
                # file.write("Total & " + str(teamObj.gameTypes[type][period]["FHN"] + teamObj.gameTypes[type][period]["FHB"] + teamObj.gameTypes[type][period]["FHM"] + teamObj.gameTypes[type][period]["FHG"]) + " & "  + str(teamObj.gameTypes[type][period]["FMN"] + teamObj.gameTypes[type][period]["FMB"] + teamObj.gameTypes[type][period]["FMM"] + teamObj.gameTypes[type][period]["FMG"]) + " & " + str(teamObj.gameTypes[type][period]["FLN"] + teamObj.gameTypes[type][period]["FLB"] + teamObj.gameTypes[type][period]["FLM"] + teamObj.gameTypes[type][period]["FLG"]) + " & " + str(teamObj.gameTypes[type][period]["FHN"] + teamObj.gameTypes[type][period]["FHB"] + teamObj.gameTypes[type][period]["FHM"] + teamObj.gameTypes[type][period]["FHG"] + teamObj.gameTypes[type][period]["FMN"] + teamObj.gameTypes[type][period]["FMB"] + teamObj.gameTypes[type][period]["FMM"] + teamObj.gameTypes[type][period]["FMG"] + teamObj.gameTypes[type][period]["FLN"] + teamObj.gameTypes[type][period]["FLB"] + teamObj.gameTypes[type][period]["FLM"] + teamObj.gameTypes[type][period]["FLG"]) + "  \n")
                # file.write("\end{tabular}\n")
                # file.write("\\vspace{5mm}  \n")
                # file.write("#### AGAINST  \n")
                # file.write("  \n")
                # file.write("\\begin{tabular}{ c || c | c | c || c}\n")
                # file.write("& High & Medium & Low & Total\\\\  \n")
                # file.write("\hline\hline\n")
                # file.write("Goal & " + str(teamObj.gameTypes[type][period]["AHG"]) + " & "  + str(teamObj.gameTypes[type][period]["AMG"]) + " & " + str(teamObj.gameTypes[type][period]["ALG"]) + " & " + str(teamObj.gameTypes[type][period]["AHG"] + teamObj.gameTypes[type][period]["AMG"] + teamObj.gameTypes[type][period]["ALG"]) + "\\\\\n")
                # file.write("\hline\n")
                # file.write("On Net & " + str(teamObj.gameTypes[type][period]["AHN"]) + " & "  + str(teamObj.gameTypes[type][period]["AMN"]) + " & " + str(teamObj.gameTypes[type][period]["ALN"]) + " & " + str(teamObj.gameTypes[type][period]["AHN"] + teamObj.gameTypes[type][period]["AMN"] + teamObj.gameTypes[type][period]["ALN"]) + "\\\\\n")
                # file.write("\hline\n")
                # file.write("Missed & " + str(teamObj.gameTypes[type][period]["AHM"]) + " & "  + str(teamObj.gameTypes[type][period]["AMM"]) + " & " + str(teamObj.gameTypes[type][period]["ALM"]) + " & " + str(teamObj.gameTypes[type][period]["AHM"] + teamObj.gameTypes[type][period]["AMM"] + teamObj.gameTypes[type][period]["ALM"]) + "\\\\\n")
                # file.write("\hline\n")
                # file.write("Blocked & " + str(teamObj.gameTypes[type][period]["AHB"]) + " & "  + str(teamObj.gameTypes[type][period]["AMB"]) + " & " + str(teamObj.gameTypes[type][period]["ALB"]) + " & " + str(teamObj.gameTypes[type][period]["AHB"] + teamObj.gameTypes[type][period]["AMB"] + teamObj.gameTypes[type][period]["ALB"]) + "\\\\\n")
                # file.write("\hline\hline\n")
                # file.write("Total & " + str(teamObj.gameTypes[type][period]["AHN"] + teamObj.gameTypes[type][period]["AHB"] + teamObj.gameTypes[type][period]["AHM"] + teamObj.gameTypes[type][period]["AHG"]) + " & "  + str(teamObj.gameTypes[type][period]["AMN"] + teamObj.gameTypes[type][period]["AMB"] + teamObj.gameTypes[type][period]["AMM"] + teamObj.gameTypes[type][period]["AMG"]) + " & " + str(teamObj.gameTypes[type][period]["ALN"] + teamObj.gameTypes[type][period]["ALB"] + teamObj.gameTypes[type][period]["ALM"] + teamObj.gameTypes[type][period]["ALG"]) + " & " + str(teamObj.gameTypes[type][period]["AHN"] + teamObj.gameTypes[type][period]["AHB"] + teamObj.gameTypes[type][period]["AHM"] + teamObj.gameTypes[type][period]["AHG"] + teamObj.gameTypes[type][period]["AMN"] + teamObj.gameTypes[type][period]["AMB"] + teamObj.gameTypes[type][period]["AMM"] + teamObj.gameTypes[type][period]["AMG"] + teamObj.gameTypes[type][period]["ALN"] + teamObj.gameTypes[type][period]["ALB"] + teamObj.gameTypes[type][period]["ALM"] + teamObj.gameTypes[type][period]["ALG"]) + "  \n")
                # file.write("\end{tabular}\n")
                # file.write("  \n")


        file.write("\pagebreak\n")
    file.close()



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


def print_to_csv(period, gameType, players, playtype):
    output = [period]
    output.append(gameType)
    output = output + players
    output.append(playtype)
    for element in output[0:-1]:
        print(element, end = ",")
    print(output[-1])


def read_lines(input_lines):
    players = dict()
    team_stats = team()
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
                prev_shift_type = shift_type
                shift_type = line[0]
                line.pop(0)
            if not line[0].isnumeric:
                sys.exit("""incorrect type gametype change (ES, PP, PK) on line""" + str(i))

        j = 0
        curr_shift = []
        while line[j].isnumeric():
            if int(line[j]) in curr_shift:
                print("double in line: " + str(i))
            curr_shift.append(int(line[j]))
            if players.get(int(line[j])) == None:
                players[int(line[j])] = player(int(line[j]))
            if int(line[j]) in prev_shift:
                if shift_type != prev_shift_type:
                    players[int(line[j])].addShift(shift_type, period, False)
            else:
                players[int(line[j])].addShift(shift_type, period, True)
            j += 1
            if j == len(line):
                break

        while j < len(line):
            if line[j] not in acceptable_types:
                sys.exit("""incorrect play type """ + str(i) + line[j])
            for player_num in curr_shift:
                players[player_num].addPlay(shift_type, line[j], period)
            team_stats.addPlay(shift_type, line[j], period)
            j += 1
        prev_shift = curr_shift
        prev_shift_type = shift_type

    return (players, team_stats, period)

if __name__ == "__main__":
    main()
