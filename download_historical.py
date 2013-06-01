import os
import math
import time
import urllib2
import argparse
import zipfile

#Author: John Beieler, jub270@psu.edu
#johnbeieler.org


def get_historical_data(directory, year, unzip=False):
    """
    Function to download the historical files from the GDELT website.

    Parameters
    ----------

    directory: String.
               Directory to write the downloaded file.

    year: String or int.
          Year of files to download.

    unzip: Boolean.
           Argument that indicates whether or not to unzip the downloaded
           file. Defaults to False.

    """
    if int(year) < 2006:
            to_get = '{}'.format(year)
            print 'Downloading {}'.format(to_get)
            url = 'http://gdelt.utdallas.edu/data/backfiles/{}.zip'.format(to_get)
            written_file = _download_chunks(directory, url)
            if unzip:
                _unzip_file(directory, written_file)
    elif int(year) >= 2006:
        year = int(year)
        for i in range(1, 13):
            to_get = '%4d%02d' % (year, i)
            print 'Downloading {}'.format(to_get)
            url = 'http://gdelt.utdallas.edu/data/backfiles/{}.zip'.format(to_get)
            written_file = _download_chunks(directory, url)
            print 'Pausing 15 seconds...'
            time.sleep(15)
            if unzip:
                _unzip_file(directory, written_file)
    else:
        print "That's not a valid year!"
    time.sleep(30)


def get_historical_daily(directory, unzip=False):
    """
    Function to download the daily update files from the GDELT website.

    Parameters
    ----------

    directory: String.
               Directory to write the downloaded file.

    unzip: Boolean.
           Argument that indicates whether or not to unzip the downloaded
           file. Defaults to False.

    """
    urls = _get_links()
    for url in urls:
        #http://gdelt.utdallas.edu/data/dailyupdates/20130531.export.CSV.zip
        print 'Downloading {}'.format(url)
        get_url = 'http://gdelt.utdallas.edu/data/dailyupdates/{}'.format(url)
        written_file = _download_chunks(directory, get_url)
        if unzip:
            _unzip_file(directory, written_file)
        print 'Pausing 30 seconds...'
        time.sleep(30)


def _get_links():
    """
    Private function to obtain the links for the daily update files from
    the GDELT website. Requires requests and lxmlself.
    """
    import requests
    import lxml.html as lh
    url = 'http://gdelt.utdallas.edu/data/dailyupdates/?O=D'
    page = requests.get(url)
    text = lh.fromstring(page.content)
    urls = text.xpath('//a/@href')
    urls = [url for url in urls if '.zip' in url]

    return urls


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
        out_path = os.path.join(directory, name)
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
#        total_size = int(req.info().getheader('Content-Length').strip())
        downloaded = 0
        CHUNK = 256 * 10240
        with open(file, 'wb') as fp:
            while True:
                chunk = req.read(CHUNK)
                downloaded += len(chunk)
#                prog = math.floor((downloaded / total_size) * 100)
#                if prog == 0.0:
#                    pass
#                else:
#                    print prog
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

    daily_command = sub_parse.add_parser('daily', help="""Download the old
                                         daily update files.""",
                                         description="""Download the old
                                         daily update files.""")
    daily_command.add_argument('-d', '--directory', help="""Path of directory
                               for file download""")
    daily_command.add_argument('-U', '--unzip', action='store_true',
                               default=False, help="""Boolean flag indicating
                               whether or not to unzip the downloaded
                               files.""")

    single_command = sub_parse.add_parser('single', help="""Download a single
                                          year.""",
                                          description="""Download a single
                                          year.""")
    single_command.add_argument('-y', '--year', help='Year to download')
    single_command.add_argument('-d', '--directory', help="""Path of directory
                                for file download""")
    single_command.add_argument('-U', '--unzip', action='store_true',
                                default=False, help="""Boolean flag indicating
                                whether or not to unzip the downloaded
                                files.""")

    range_command = sub_parse.add_parser('range', help="""Download a range
                                         of years.""",
                                         description="""Download a range
                                         of years.""")
    range_command.add_argument('-y', '--year', help="""Years to download, e.g.
                               1979-1981""")
    range_command.add_argument('-d', '--directory', help="""Path of directory
                               for file download""")
    range_command.add_argument('-U', '--unzip', action='store_true',
                               default=False, help="""Boolean flag indicating
                               whether or not to unzip the downloaded
                               files.""")

    args = aparse.parse_args()
    directory = args.directory

    if args.command_name == 'daily':
        get_historical_daily(directory, args.unzip)
    elif args.command_name == 'single':
        get_historical_data(directory, args.year, args.unzip)
    elif args.command_name == 'range':
        try:
            begin, end = args.year.split('-')
        except Exception, e:
            print 'Error {}. Please enter a valid range, e.g. 1979-1980'.format(e)
        try:
            begin = int(begin)
            end = int(end)
        except Exception, e:
            print 'Error {}. Please enter a valid range, e.g. 1979-1980.'.format(e)
        for y in range(begin, end+1):
            get_historical_data(directory, y, args.unzip)
            print 'Pausing 30 seconds...'
            time.sleep(30)
