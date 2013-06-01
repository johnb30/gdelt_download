import os
import math
import time
import urllib2
import zipfile
import argparse
import datetime

#Author: John Beieler, jub270@psu.edu
#johnbeieler.org


def get_daily_data(directory, unzip=False):
    """
    Function to download the daily update file from the GDELT website.

    Parameters
    ----------

    directory: String.
               Directory to write the downloaded file.

    unzip: Boolean.
           Argument that indicates whether or not to unzip the downloaded
           file. Defaults to False.

    """
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    url = '%04d%02d%02d' % (year, month, day)
    print 'Processing {}'.format(url)
    written_file = _download_chunks(directory, url)
    if unzip:
        _unzip_file(directory, written_file)

def _unzip_file(directory, zipped_file):
    """
    Private function to unzip a zipped file that was downloaded.

    Parameters
    ----------

    directory: String.
               Directory to write the unzipped file.

    zipped_file: String.
                 Filepath of the zipped file to unzip.

    """
    print 'Unzipping {}'.format(zipped_file)
    z = zipfile.ZipFile(zipped_file)
    for name in z.namelist():
        f = z.open(name)
        out_path = os.path.join(directory, f)
        with open(out_path, 'w') as out_file:
            out_file.write(f.read())


def _download_chunks(directory, url):
#Thanks to https://gist.github.com/gourneau/1430932
    """
    Private function to download a zipped file in chunks.

    Parameters
    ----------

    directory: String.
               Directory to write the downloaded file.

    url: String.
         URL of the file to download.

    """

    base_file = os.path.basename(url)

    temp_path = directory
    try:
        file = os.path.join(temp_path, base_file)

        req = urllib2.urlopen(url)
        total_size = int(req.info().getheader('Content-Length').strip())
        downloaded = 0
        CHUNK = 256 * 10240
        with open(file, 'wb') as fp:
            while True:
                chunk = req.read(CHUNK)
                downloaded += len(chunk)
                prog = math.floor((downloaded / total_size) * 100)
                if prog == 0.0:
                    pass
                else:
                    print prog
                if not chunk:
                    break
                fp.write(chunk)
    except urllib2.HTTPError, e:
        print "HTTP Error:", e.code, url
        return False
    except urllib2.URLError, e:
        print "URL Error:", e.reason, url
        return False

    return file

if __name__ == '__main__':
    print 'Running...'
    aparse = argparse.ArgumentParser()

    sub_parse = aparse.add_subparsers(dest='command_name')

    fetch_command = sub_parse.add_parser('fetch', help="""Download only the
                                         daily update for today's date.""",
                                         description="""Download only the
                                         daily update for today's date.""")
    fetch_command.add_argument('-d', '--directory', help="""Path of directory
                               for file download""")
    fetch_command.add_argument('-U', '--unzip', action='store_true',
                               default=False, help="""Boolean flag indicating
                               whether or not to unzip the downloaded
                               files.""")

    schedule_command = sub_parse.add_parser('schedule', help="""Set the script
                                          to run on a daily basis.""",
                                          description="""Set the script
                                          to run on a daily basis.""")
    schedule_command.add_argument('-d', '--directory', help="""Path of directory
                                for file download""")
    schedule_command.add_argument('-U', '--unzip', action='store_true',
                                default=False, help="""Boolean flag indicating
                                whether or not to unzip the downloaded
                                files.""")


    args = aparse.parse_args()
    directory = args.directory

    if args.command_name == 'fetch':
        get_daily_data(directory, args.unzip)
    elif args.command_name == 'schedule':
        import schedule
        schedule.every().day.at("10:00").do(get_daily_data(directory,
                                                           args.unzip))
        while 1:
            schedule.run_pending()
            time.sleep(1)
