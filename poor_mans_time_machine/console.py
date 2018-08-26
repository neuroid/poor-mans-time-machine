#!/usr/bin/env python
"""Usage: poor-mans-time-machine [-c NAME] [-e PATH]... [-l LIMIT] [-p PREFIX] [-r PATH] SRC DEST

  -h --help           Show this help
  -c --canary NAME    Name of a file stored in the rotated backup directory to
                      signify a successful run [default: .poor-mans-time-machine-ok]
  -e --exclude PATH   Exclude paths [default: /dev /media /mnt /proc /run /sys /tmp]
  -l --limit LIMIT    Number of rotated backup directories to keep
  -p --prefix PREFIX  Name prefix of the rotated backup directory [default: backup]
  -r --rsync PATH     Path to rsync command [default: rsync]
"""
import os
import subprocess
import sys

from docopt import docopt

from . import backups
from . import delete
from . import rotate
from . import sync
from . import touch


def main():
    args = docopt(__doc__)

    source = os.path.abspath(args['SRC'])
    destination = os.path.abspath(args['DEST'])
    canary = os.path.basename(args['--canary'])
    exclude = args['--exclude']
    limit = int(args['--limit'] or 0)
    prefix = args['--prefix']
    rsync = args['--rsync']

    if not os.path.isdir(destination):
        sys.exit('Destination {} is not a valid directory'.format(destination))

    if not os.path.exists(source):
        sys.exit('Source {} does not exist'.format(source))

    paths = backups(destination, prefix)
    destination = os.path.join(destination, prefix)

    if paths:
        if os.path.exists(os.path.join(paths[0], canary)):
            rotate(paths)
    else:
        paths.insert(0, None)  # Dummy link_dest

    exclude.append('/' + canary)

    # Exit values (rsync):
    # 0 -- Success
    # 24 -- Partial transfer due to vanished source files
    try:
        sync(rsync, source, destination, link_dest=paths[0], exclude=exclude)
    except subprocess.CalledProcessError as error:
        if error.returncode != 24:
            raise

    touch(os.path.join(destination, canary))

    if limit and paths[0]:   # Remove only if rotated
        for path in paths[limit:]:
            delete(rsync, path)


if __name__ == '__main__':
    main()
