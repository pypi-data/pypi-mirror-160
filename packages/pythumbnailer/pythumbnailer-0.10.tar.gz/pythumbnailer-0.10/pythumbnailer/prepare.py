#!/usr/bin/env python
from pathlib import Path
import os
import argparse
import logging
import subprocess
import gzip

from . import pypublish
from . import utils

logger = logging.getLogger(__name__)


SUFFIXES = {
    '.JPG': '.jpg',
    '.PNG': '.png',
}
# TODO: Use `convert` (ImageMagick) to convert some images to JPEG
# See https://github.com/python-pillow/Pillow/issues/2806
SUFFIX_IMAGES = [
    '.heic',  # HEIF
]
SUFFIX_VIDEO_ARGS = {
    '.mov': ['-movflags', 'use_metadata_tags'],
    '.mpg': [],
}
SUFFIX_TRACKS = '.gpx'
LSUFFIX_GZIP = [
    ['.gpx', '.gz'],
]
assert all(len(lst) >= 2 for lst in LSUFFIX_GZIP)


def __main__():
    parser = argparse.ArgumentParser(description='Remove "pypublish" creations')

    parser.add_argument('--basedir',
                        type=pypublish.Directory, default=Path('.'),
                        help='Base directory to process. Defaults to `%(default)s`')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Show debug messages')
    # TODO: Support fixing old MP4 videos:
    # - Move metadata to start of file
    # for v in *.mp4; do ffmpeg -i "$v"  -c copy -map 0 -movflags +faststart "fast-$v" && mv -vf "fast-$v" "$v"; done
    # - Audio volume normalization (very slow)
    #   Must be 2 passes: https://peterforgacs.github.io/2018/05/20/Audio-normalization-with-ffmpeg/
    # ffmpeg -i INPUT.mp4 -vf copy -af loudnorm OUTPUT.mp4

    args = parser.parse_args()

    utils.setup_logging(args.verbose)

    for p in args.basedir.iterdir():
        if p.is_file():
            # Remove executable bits from files
            # TODO: No need to use subprocess for this
            subprocess.run(['chmod', '-x', str(p)])
            if p.suffix in SUFFIXES:
                new_name = p.with_suffix(SUFFIXES[p.suffix])
                if not new_name.exists():
                    logger.debug(f'Suffix: Rename "{p}" -> "{new_name}"')
                    p.rename(new_name)
                else:
                    new_name = None
            elif p.suffix.lower() in SUFFIX_VIDEO_ARGS:
                new_name = p.with_suffix('.mp4')
                if not new_name.exists():
                    loglevel = ['-v', 'quiet']
                    if args.verbose:
                        loglevel = []
                    convert_command = [
                        'ffmpeg',
                        *loglevel,
                        '-i', p,
                        *SUFFIX_VIDEO_ARGS[p.suffix.lower()],
                        '-movflags', '+faststart',  # Move the metadata to the top of the file
                        new_name,
                        '-map_metadata', '0',
                    ]
                    logger.debug(f'{p.suffix.upper()[1:]}: Convert "{p}" -> "{new_name}"')
                    convert_ret = subprocess.call(convert_command)
                    if convert_ret == 0:
                        logger.debug('- Success!')
                        old_stat = p.stat()
                        old_times = (old_stat.st_atime, old_stat.st_mtime)
                        os.utime(new_name, times=old_times)  # touch --reference=
                        p.unlink()
                    else:
                        logger.error('- Error!')
                else:
                    new_name = None  # Skip
            elif p.suffixes in LSUFFIX_GZIP:
                # Remove the last suffix
                new_name = p.with_suffix(''.join(p.suffixes[:-2]))
                if not new_name.exists():
                    logger.debug(f'Suffix: Decompress "{p}" -> "{new_name}"')
                    try:
                        old = gzip.open(p, mode='rb')
                        with new_name.open(mode='wb') as new:
                            while True:
                                chunk = old.read(1024)  # Chunked read
                                if not chunk:
                                    break
                                new.write(chunk)
                        old.close()
                        logger.debug('- Success!')
                        p.unlink()
                    except gzip.BadGzipFile:
                        logger.error('- Error!')
                        new_name.unlink()
                else:
                    new_name = None
            elif p.suffix.lower() == SUFFIX_TRACKS:
                # TODO: Split inner `<trk>` into separate files: /gpx/trk
                pass


if __name__ == '__main__':
    import sys
    sys.exit(__main__())
