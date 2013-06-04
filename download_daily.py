import os
import math
import time
import urllib2
import zipfile
import argparse
import datetime

__author__ = 'John Beieler, johnbeieler.org'
__email__ = 'jub270@psu.edu'


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
    now = datetime.date.today()-datetime.timedelta(days=1)
    year = now.year
    month = now.month
    day = now.day
    url = '%04d%02d%02d.export.CSV.zip' % (year, month, day)
    get_url = 'http://gdelt.utdallas.edu/data/dailyupdates/{}'.format(url)
    print 'Downloading {}'.format(url)
    written_file = _download_chunks(directory, get_url)
    if unzip:
        _unzip_file(directory, written_file)


def get_upload_daily_data(directory, bucket, folder_name):
    """
    Function to download the daily update file from the GDELT website.

    Parameters
    ----------

    directory: String.
               Directory to write the downloaded file.


    bucket: String.
            Name of the bucket on Amazon.

    folder_name: String.
                 Name of the folder within the bucket to which you want to
                 upload the file. This should be something like 'daily/' which
                 will create the key under 's3_bucket/daily/filename'. It is
                 important to note that Amazon S3 doesn't actually have a
                 concept of folders. This string is really just an extension
                 to the key.

    """
    now = datetime.date.today()-datetime.timedelta(days=1)
    year = now.year
    month = now.month
    day = now.day
    url = '%04d%02d%02d.export.CSV.zip' % (year, month, day)
    get_url = 'http://gdelt.utdallas.edu/data/dailyupdates/{}'.format(url)
    print 'Downloading {}'.format(url)
    written_file = _download_chunks(directory, get_url)
    final_file = _unzip_file(directory, written_file)
    s3_upload(final_file, url, bucket, folder_name)


def s3_upload(unzipped_file, filename, s3_bucket, folder=None):
    """"
    Function to upload downloaded GDELT daily files to Amazon S3. Requires
    the boto library for Python.

    Parameters
    ----------

    unzipped_file: String.
                   Filepath to the downloaded and unzipped daily update file.

    filename: String.
              Name of the file. This is used as the key to upload the file to
              Amazon.

    s3_bucket: String.
               Name of the bucket on Amazon.

    folder: String.
            Name of the folder within the bucket to which you want to upload
            the file. This should be something like 'daily/' which will create
            the key under 's3_bucket/daily/filename'. It is important to note
            that Amazon S3 doesn't actually have a concept of folders. This
            string is really just an extension to the key.

    """
    import boto
    from boto.s3.key import Key
    s3 = boto.connect_s3()
    bucket = s3.get_bucket(s3_bucket)
    k = Key(bucket)
    if folder:
        k.key = '{}/{}'.format(folder, filename)
    else:
        k.key = filename
    k.set_contents_from_filename(unzipped_file)


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

    return out_file


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

    fetch_upload_command = sub_parse.add_parser('fetch_upload', help="""Set the
                                                script to run on a daily basis 
                                                and upload the results to 
                                                Amazon S3. Unzips the files by
                                                default.""",
                                                description="""Set the
                                                script to run on a daily basis 
                                                and upload the results to 
                                                Amazon S3. Unzips the files by 
                                                default.""")
    fetch_upload_command.add_argument('-d', '--directory', help="""Path of 
                                      directory for file download""")
    fetch_upload_command.add_argument('--bucket', help="""Amazon S3 bucket
                                      to which files should be uploaded.
                                      Required.""", required=True)
    fetch_upload_command.add_argument('--folder', help="""Optional Argument
                                      indicating a sub-folder within the bucket
                                      to which to add files.""")

    schedule_command = sub_parse.add_parser('schedule', help="""Set the script
                                            to run on a daily basis.""",
                                            description="""Set the script
                                            to run on a daily basis.""")
    schedule_command.add_argument('-d', '--directory', help="""Path of
                                  directory for file download""")
    schedule_command.add_argument('-U', '--unzip', action='store_true',
                                  default=False, help="""Boolean flag
                                  indicating whether or not to unzip the
                                  downloaded files.""")

    upload_command = sub_parse.add_parser('schedule_upload', help="""Set the
                                          script to run on a daily basis and
                                          upload the results to Amazon S3.
                                          Unzips the files by default.""",
                                          description="""Set the
                                          script to run on a daily basis and
                                          upload the results to Amazon S3.
                                          Unzips the files by default.""")
    upload_command.add_argument('-d', '--directory', help="""Path of directory
                                  for file download""")
    upload_command.add_argument('--bucket', help="""Amazon S3 bucket
                                  to which files should be uploaded.
                                  Required.""",
                                  required=True)
    upload_command.add_argument('--folder', help="""Optional Argument
                                  indicating a sub-folder within the bucket
                                  to which to add files.""")

    args = aparse.parse_args()
    directory = args.directory

    if args.command_name == 'fetch':
        get_daily_data(directory, args.unzip)
    elif args.command_name == 'schedule_upload':
        import schedule
        schedule.every().day.at("10:00").do(get_upload_daily_data, directory,
                                            args.bucket, args.folder)
        while 1:
            schedule.run_pending()
            time.sleep(1)
    elif args.command_name == 'schedule':
        import schedule
        schedule.every().day.at("10:00").do(get_daily_data, directory, args.unzip)
        while 1:
            schedule.run_pending()
            time.sleep(1)
