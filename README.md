**Note: 02/17/14**

I am no longer associated with the GDELT project as noted
[here](http://blog.gdelt.org/2014/01/20/gdelt-suspension/), so I will
not continue to update this package. There is a fork of this project
[here](https://github.com/00krishna/gdelt_download) that has some updates
available.

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
avoid swamping the server. Additionally, all of the functions in
`download_historical.py` check to see whether the file already exists in the 
directory before downloading.

###Dependencies

As of September 20, 2013 the `requests` library is required for all functions.
This requirement was to help ease the transition from Python 2 to Python 3.
The library is easy to install using `pip` or `easy_install`.

##`download_historical` Usage

The script has three modes: `daily`, `single`, and `range`.

*Note*: If you wish to use the `daily` mode, the `lxml` library
is necessary. You can install the library using `pip install lxml`. The script 
also makes use of `argparse`, which is included in the standard library from
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

The script has four modes: `fetch`, `schedule`, `fetch_upload`, and `schedule_upload`.

*Note*: If you wish to use the `schedule` mode, the `schedule` library
is necessary. You can install using `pip install schedule`. Additionally, 
the `upload` commands require the `boto` library and a boto config file located
in `~/.boto`. 

*Note: Due to the use of `boto`, the `upload` commands are not compatible with 
Python 3. There is the `botocore` project, which is compatible with Python 3,
but it doesn't seem stable enough for me to use currently. Feel free to change
my mind, though.*

###Fetch:

The fetch mode downloads only the current date's update. 

####Usage:

`python download_daily.py fetch -d ~/gdelt/ -U` 

Where `-d` is the flag for the directory to which the files should be written,
and `-U` is the optional flag indicating whether each downloaded file should
be unzipped.

###Schedule:

The schedule mode sets the script to run in the background and request 
each day at 10:00am the previous date's upload from the server. In order to work, the 
script must be left running in a terminal tab. The use of a utility such as 
`screen` or `tmux` is recommended in order to allow the program to run
unmonitored in the background.

####Usage:

`python download_daily.py schedule -d ~/gdelt/ -U` 

Where `-d` is the flag for the directory to which the files should be written,
and `-U` is the optional flag indicating whether each downloaded file should
be unzipped.

###Schedule_upload:

The schedule_upload mode sets the script to run in the background and request 
each day at 10:00am the previous date's upload from the server. This new
download is then uploaded to the indicated Amazon S3 bucket. This helps
facilitate work using Amazon's Elastic Cloud Compute or Elastic MapReduce 
environments. Also, due to the uploads to S3, each file is unzipped by default
and no option to change this is provided. If one wishes, however, it would be
trivial to change this within the `get_upload_daily_data` function within the
script. Finally, in order to work, the script must be left running in a terminal
tab. The use of a utility such as `screen` or `tmux` is recommended in order 
to allow the program to run unmonitored in the background.

####Usage:

`python download_daily.py schedule_upload -d ~/gdelt/ --bucket gdelt --folder daily/` 

Where `-d` is the flag for the directory to which the files should be written,
`--bucket` indicates the name of the S3 bucket, and `--folder` is the optional
argument indicating a folder within the bucket. 


###Fetch_upload:

Does the same thing as `schedule_upload` but has to be called every day.
