"""

Usage:
  cli_audiorecorder.py <url> [--filename=<name>] [--duration=<time>] [--blocksize=<size>]
  cli_audiorecorder.py -h | --help

Options:
  -h --help             Show this screen.
  --filename=<name>     Name of recording [default: myRadio].
  --duration=<time>     Duration of recording in seconds [default: 30].
  --blocksize=<size>    Block size for read/write in bytes [default: 64].

"""
from os.path import join

from docopt import docopt
from pydub import AudioSegment
import os
import datetime
import urllib.request
import sys

__author__ = "Aslan Pourmoslemi"
__version__ = "0.0.5"


# Converting a string to an integer with a try-and-except block
def cast_int(var):
    try:
        return int(var)
    except ValueError:
        print('')
        print('Error: ' + var + ' is wrong input')
        sys.exit(1)


# Request the URL of the streaming source with exception handling
def request_url(audio_src):
    try:
        return urllib.request.urlopen(audio_src)
    except Exception as e:
        print('')
        print(e)
        sys.exit(1)


class AudioRecorder(object):
    """
    a class to record mp3 streams from the Internet.
    """

    def __init__(self, page_url, file_name, duration_time, block_size):
        """
        :param page_url: Streaming-Quelle URL
        :param file_name: Name of the mp3 file to be saved at the end.
        :param duration_time: Duration of recording in seconds
        :param block_size: Buffer size for read/write in bytes

        """
        self.audio_src = request_url(page_url)
        self.filename = file_name
        self.duration = cast_int(duration_time)
        self.size = cast_int(block_size)

    # to cut and save the recorded audio file into exactly the desired recording time.
    def audio_cut(self):
        starttime = 0
        endtime = self.duration * 1000
        file_path = os.path.dirname(os.path.abspath(__file__))
        print('Processing mp3-file ...')
        song = AudioSegment.from_mp3(join(file_path, self.filename + '.mp3'))
        extract = song[starttime:endtime]
        extract.export(filename + '.mp3', format="mp3")
        print('\n''Audio is successfully saved!')
    
    #mainmethod for recording
    def main(self):
        print('\n''Recording in progress ...\n')
        start_time = datetime.datetime.now()
        with open(self.filename + '.mp3', 'wb') as audio_dst:
            while (datetime.datetime.now() - start_time).seconds < self.duration:
                audio_dst.write(self.audio_src.read(self.size))
        self.audio_cut()


if __name__ == '__main__':
    args = docopt(__doc__)
    print('')
    print(args)
    url = args['<url>']
    filename = args['--filename']
    duration = args['--duration']
    size = args['--blocksize']

    record = AudioRecorder(url, filename, duration, size)
    record.main()
