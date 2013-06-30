poor-mans-time-machine
======================

A simple tool for performing local incremental backups.


Usage
-----

    Usage: poor-mans-time-machine [-e PATH]... [-p PREFIX] [-r PATH] SRC DEST

      -h --help           Show this help
      -e --exclude PATH   Exclude paths [default: /dev /media /mnt /proc /sys]
      -p --prefix PREFIX  Name prefix of the rotated backup directory [default: backup]
      -r --rsync PATH     Path to rsync command [default: rsync]


Example
-------

    ./poor-mans-time-machine / /media/usbdisk

The above will:

1. rename `/media/usbdisk/backup` to `/media/usbdisk/backup.1`,
2. create `/media/usbdisk/backup`
3. synchronize `/` to `/media/usbdisk/backup` using rsync.

The synchronization uses `--link-dest=/media/usbdisk/backup.1` to copy only the
files that were modified/added since the previous run.


Requirements
------------

    aptitude install rsync
    pip install docopt
