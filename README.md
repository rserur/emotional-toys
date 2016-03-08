BCH RAGE-Control Project
========================

This is the repository for the CALMS Study codebase, forked off of the the RAGE-Control Project. HRM contains code specific to heartrate monitors, ShakingTable contains code for running and communicating with the Shaky Table, and RAGE-Control contains code for the RAGE-Control computer game.

## RAGE-Control

### Prerequisites

- Python 2.7
- NumPy
- SciPy
- py2app (to create a redistribution)

### Instructions

To run the game via python script at the command line:
```
$ python game0.py
```

To build a redistributable version of the application:
```
$ python setup.py py2app --argv-emulation --graph
```

### Contributors
- Jason Khan (2013-)
- Rachael Serur (2016-)
- Marc Bucchieri (2013-2015)