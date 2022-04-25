#!/usr/bin/python
# ‐*‐ encoding: utf‐8 ‐*‐

import datetime
import urllib.request
import urllib.error
from docopt import docopt
import os

__doc__ = \
    """AudioRecorder.

    Usage:
      cli_audiorecorder.py <url> [--filename=<name>] [--duration=<time>] [--blocksize=<size>]
      cli_audiorecorder.py -h | --help
      cli_audiorecorder.py -l | --listrecordings
    
    Options:
      -h --help             Show this screen.
      --filename=<name>     Name of recording [default: myRadio.mp3].
      --duration=<time>     Duration of recording in seconds [default: 5].
      --blocksize=<size>    Block size for read/write in bytes [default: 64].
      
    """


def record_stream(url, filename, duration, blocksize):
    try:
        audio_src = urllib.request.urlopen(url)
        start_time = datetime.datetime.now()

        # with open -> Datei wird nach dem Block automatisch geschlossen
        with open(filename, 'wb') as audio_dst:
            while (datetime.datetime.now() - start_time).seconds < int(duration):
                audio_dst.write(audio_src.read(int(blocksize)))
                # Puffergröße sorgt für längere Aufnahme, Streams mit möglichst großem Puffer um mangelnde Bandbreite abzufedern

    except urllib.error.URLError as e:
        print("Die URL konnte nicht gefunden werden:", e)
    except TypeError as e:
        print("Error:", e)
    except Exception as e:  # any other Exception
        print("Error:", e)
    except PermissionError:
        print("Exception: No permission to write" + filename)
    else:  # no exception occured
        print("No exception occured.")


def print_recordings():
    print("Previous Recordings: ")
    print([f for f in os.listdir(os.getcwd()) if f.endswith('.mp3')])


if __name__ == '__main__':
    args = docopt(__doc__, version='AudioRecorder 1.0')

    # for pair in args.items():
    # print(pair)

    if args['--listrecordings'] or args['-l']:
        print_recordings()

    elif args['<url>'] is not None:
        if args['--filename'][-4:] != ".mp3":
            args['--filename'] += ".mp3"

        record_stream(args['<url>'], args['--filename'], args['--duration'], args['--blocksize'])
    else:
        print("command not found")
