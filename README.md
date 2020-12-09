# Hockey-Stats-Project-V4
## This is continuation of Hockey-Stats-Project-V3
### Improvements:
* Using Python instead of C
* Takes individual eventing data vs overall shots and opportunities per shift
* Outputs directly in Rmarkdown file instead of Latex tables
* Flexibility to add graphs directly with Rmarkdown instead of Latex
* Can use tags to change the play type (Even Strength, Powerplay, Penalty Kill) instead of keeping different files
* Can use tag to change period
* No longer have to use zeros when less than 5 players on ice

## Description:
This is a program used to analyze and automate the game report process for my role as Analyst for the Victoria Grizzlies.  There are two main features to this program, a rough expected goals model calculator and an analyzer that reads through game data and creates reports for each player.

## Data
The game data comes in the following format 
```
[Period index flag if needed] [change playtype flag if needed] [player1] [player2] [player i...] [event1] [event2] [event3]
```
Ex.
```
PERIOD ES 14 12 13 23 19 AHN FMN ALM
```

#### Flags:
'PERIOD': indexes period by one  
'ES': changes to Even Strength  
'PK': changes toPenalty Kill  
'PP': changes Powerplay  

#### Events:
[Team: {For: 'F', Against: 'A'}][Danger level: {High: 'H', Medium: 'M', Low: 'L'}][Result: {On net: 'N', Missed: 'M', Blocked: 'B', Goal: 'G'}]  
Ex: AMN, (A)gainst (M)edium danger on (N)et

## Running Programs 

#### Analyzer
```
python3 stats_analyzer.py [path to data] [Date as string for title] [Opponent] [output directory in players directory]
Ex.
python3 stats_analyzer.py data/oct31.txt "October 31" "Nanaimo Clippers" oct31
```

#### Expected Goals

```
python3 expect_goals.py
```
