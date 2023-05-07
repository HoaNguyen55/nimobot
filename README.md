# NimoTV bot

## 1. Description

I would like to show you a bot which is used in NimoTV website to help users enter any idol's room to advertise KC trading (Diamond trading). See how to use in next section.

## 2. How to use

It is very simple.

**Step 1**: Install the requirements by using command: pip3 install -r requirment.txt

**Step 2**: Open a terminal and use this command to show parameters that can be used: `python3 nimobot.py -h`

`usage: nimobot.py [-h] [--waitfirsttime WAITFIRSTTIME] [--waitlongtime WAITLONGTIME] [--waitshorttime WAITSHORTTIME] [--inittimeset INITTIMESET]\
                  [--opentabnum OPENTABNUM] [--username USERNAME] [--password PASSWORD] [--headless HEADLESS] [--nonlogin NONLOGIN] [--url URL]\
                  [--urlonlyset URLONLYSET] [--specificurl SPECIFICURL]`

`optional arguments:`

`-h, --help show this help message and exit`

`--waitfirsttime WAITFIRSTTIME 
                       Wait first time`

`--waitlongtime WAITLONGTIME
                       Wait long time`
                       
`--waitshorttime WAITSHORTTIME
                      Wait short time`
                      
`--inittimeset INITTIMESET
                      Force initialize time`
                      
`--opentabnum OPENTABNUM
                      Number of tabs to open`
                      
`--username USERNAME   User input`

`--password PASSWORD   Password input`

`--headless HEADLESS   Run Chrome in headless mode`

`--nonlogin NONLOGIN   Choose NOT to login account`

`--url URL             Website URL`

`--urlonlyset URLONLYSET
                      Use specific URL`
                      
`--specificurl SPECIFICURL
                      Specific URL`

**Example**:
- If use default, please remember put your account into `--username` and `--password` because they are the required \
`python3 nimobot.py --username=abcdef --pasword=12345 `

- If you'd like to change any parameters such as `opentabnum` (number of tab) on browser at a time \
`python3 nimobot.py --username=abcdef --pasword=12345 --opentabnum=10 `
