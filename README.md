poor-mans-time-machine
======================

A simple tool for performing local incremental backups.


Usage
-----

    Usage: poor-mans-time-machine [-c NAME] [-e PATH]... [-l LIMIT] [-p PREFIX] [-r PATH] SRC DEST

      -h --help           Show this help
      -c --canary NAME    Name of a file stored in the rotated backup directory to
                          signify a successful run [default: .poor-mans-time-machine-ok]
      -e --exclude PATH   Exclude paths [default: /dev /media /mnt /proc /sys]
      -l --limit LIMIT    Number of rotated backup directories to keep
      -p --prefix PREFIX  Name prefix of the rotated backup directory [default: backup]
      -r --rsync PATH     Path to rsync command [default: rsync]


Example
-------

    poor-mans-time-machine / /media/usbdisk

The above will:

1. rename `/media/usbdisk/backup` to `/media/usbdisk/backup.1`,
2. create `/media/usbdisk/backup`
3. synchronize `/` to `/media/usbdisk/backup` using rsync.

The synchronization uses `--link-dest=/media/usbdisk/backup.1` to copy only the
files that were modified or added since the previous run.

Each successful backup is marked with a "canary" file. No directory rotation is
performed if the file is missing from the latest backup directory. This allows
to resume interrupted backups and guards against removal of older backups after
a failed run (when `--limit` is applied).


Installation
------------

    apt install rsync
    pip install git+https://github.com/neuroid/poor-mans-time-machine.git
