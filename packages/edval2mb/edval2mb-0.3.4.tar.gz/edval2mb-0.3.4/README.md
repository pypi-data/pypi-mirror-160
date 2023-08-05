# edval2mb

Convert edval export of schedule to ManageBac CSV. Can be used as csv timetable upload

## Install

Please install python version 3.9 or above. On Mac, you can use [brew](https://brew.sh), and on Windows, you can use the Microsoft Store.

Best practice with Python is to create virtual environments to install tools. It is recommended. The most straight-forward way to create and use a virtual environment is the follwing:

```
python3 -m venv venv
```

That sets up the virtual environment. Then, to activate the virtual environment:

```
source venv/bin/activate  # Mac/Unix
./venv/Bin/Activate  # Windows
```

Once the virtual environment is activated, install:

```
pip install edval2mb
```

You will now have the command line tool "edval2mb" available in the terminal.

## To use

This tool takes as input the csv export, and will save the result into a file that is output when complete.

```
edval2mb path/to/exported/csv.csv to_mb
```

Output:

```
Saved csv of 1365 rows (including header) and 5 columns to /path/to/managebac_timetable.csv
```

## Options

To view the options available on the `to_mb` command, please see the output to this command:

```
edval2mb path/to/exported/csv.csv 
```

Output:

```
Options:
  --academic-year TEXT          The value passed here will be output to each
                                row of the output
  --day-start-index INTEGER     Some schools ManageBac timetable starts from
                                day 0.  In this case, you can pass 0 to this
                                option.
  --period-start-index INTEGER  Some schools have their timetable start with
                                0.  In this case, you can pass 0 to this
                                option.
  --day TEXT                    If the exported csv uses days of week other
                                than Mon, Tue, Wed Thu Friday, you can specify
                                these by passing multiple --day Lundi --day
                                Marchi etc in sequential order
  --output-path TEXT            The path (including file name) of the output
                                file
  --help                        Show this message and exit.
```

