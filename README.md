###GDELT Download

The GDELT data is spread across multiple files, with a new file added each day.
Downloading each and every file is not a fun endeavor. These scripts were 
written in order to aid in the download of the GDELT data. The first script 
`download_historical.py` is aimed at downloading the historical data, and the 
previous daily updated. 

A second script will soon be added. This script, `download_daily.py`, is aimed
at downloading the new files that are uploaded to the GDELT website each day. 

Each script implements a 30 second delay between each download in order to 
avoid swamping the server.

###`download_historical` Usage

The script has three modes: `daily`, `single`, and `range`.

*Note*: If you wish to use the `daily` mode, the `requests` and `lxml` libaries
are necessary. You can install both using `pip install library_name`. The script 
also makes use of `argparse`, which is included in the standard libary from
Python 2.7+. If you are using an older version, it is necessary to install 
`argparse` using `pip` or `easy_install`. 

####Daily:

The daily mode downloads the daily updates that are currently uploaded to the
GDELT website.  

#####Usage:

`python download_historical.py daily -d ~/gdelt/ -U` 

Where `-d` is the flag for the directory to which the files should be written,
and `-U` is the optional flag indicating whether each downloaded file should
be unzipped.

####Single:

The single mode downloads the updates for a single year.

#####Usage:

`python download_historical.py single -y 1979 -d ~/gdelt/ -U` 

Where `-y` is the flag that indicates which year should be downloaded, `-d` 
is the flag for the directory to which the files should be written, and `-U` 
is the optional flag indicating whether each downloaded file should be unzipped.

####Range:

The range mode downloads the updates for a range years.

#####Usage:

`python download_historical.py range -y 1979-2012 -d ~/gdelt/ -U` 

Where `-y` is the flag that indicates which years should be downloaded, `-d` 
is the flag for the directory to which the files should be written, and `-U` 
is the optional flag indicating whether each downloaded file should be unzipped.

