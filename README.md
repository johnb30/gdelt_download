##GDELT Download

The GDELT data is spread across multiple files, with a new file added each day.
Downloading each and every file is not a fun endeavor. These scripts were 
written in order to aid in the download of the GDELT data. The first script 
`download_historical.py` is aimed at downloading the historical data, and the 
previous daily updated. The second script, `download_daily.py`, is aimed
at downloading the new files that are uploaded to the GDELT website each day.
This script enables the user to either call the script each day to fetch the
newest upload, or to run the process in the background to download the new 
updates, i.e., the events for the previous day, each day at 10:00am. 

Each script implements a 30 second delay where appropriate in order to 
avoid swamping the server.

All of the commands have been tested and run as expected. I haven't had a chance
to let the daily `schedule` command run for a day, so if it ends up breaking
please let me know.

##`download_historical` Usage

The script has three modes: `daily`, `single`, and `range`.

*Note*: If you wish to use the `daily` mode, the `requests` and `lxml` libaries
are necessary. You can install both using `pip install library_name`. The script 
also makes use of `argparse`, which is included in the standard libary from
Python 2.7+. If you are using an older version, it is necessary to install 
`argparse` using `pip` or `easy_install`. 

###Daily:

The daily mode downloads the daily updates that are currently uploaded to the
GDELT website.  

####Usage:

`python download_historical.py daily -d ~/gdelt/ -U` 

Where `-d` is the flag for the directory to which the files should be written,
and `-U` is the optional flag indicating whether each downloaded file should
be unzipped.

###Single:

The single mode downloads the updates for a single year.

####Usage:

`python download_historical.py single -y 1979 -d ~/gdelt/ -U` 

Where `-y` is the flag that indicates which year should be downloaded, `-d` 
is the flag for the directory to which the files should be written, and `-U` 
is the optional flag indicating whether each downloaded file should be unzipped.

###Range:

The range mode downloads the updates for a range of years.

####Usage:

`python download_historical.py range -y 1979-2012 -d ~/gdelt/ -U` 

Where `-y` is the flag that indicates which years should be downloaded, `-d` 
is the flag for the directory to which the files should be written, and `-U` 
is the optional flag indicating whether each downloaded file should be unzipped.

##`download_daily` Usage

The script has two modes: `fetch`, and `schedule`.

*Note*: If you wish to use the `schedule` mode, the `schedule` library
is necessary. You can install using `pip install schedule`. 

###Fetch:

The fetch mode downloads only the current date's update. 

####Usage:

`python download_daily.py fetch -d ~/gdelt/ -U` 

Where `-d` is the flag for the directory to which the files should be written,
and `-U` is the optional flag indicating whether each downloaded file should
be unzipped.

###Schedule:

The schedule mode sets the script to run in the background and request 
each day at 10:00am that date's upload from the server. In order to work, the 
script must be left running in a terminal tab. The use of a utility such as 
`screen` or `tmux` is recommended in order to allow the program to run
unmonitored in the background.

####Usage:

`python download_daily.py schedule -d ~/gdelt/ -U` 

Where `-d` is the flag for the directory to which the files should be written,
and `-U` is the optional flag indicating whether each downloaded file should
be unzipped.
