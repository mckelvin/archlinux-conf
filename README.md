# ArchlinuxConf

This tool is used to backup and restore archlinux in a convenient way.

it maintains:
- pip packages
- pacman and packages
- misc conf like files

DO **NOT** ADD ANY PRIVATE FILE INTO THE REPO, UNLESS YOU REALLY KNOW WHAT ARE YOU DOING.

## HOWTO

INIT

    $ git clone git://github.com/mckelvin/archlinux-conf.git archlinux-conf
    $ cd archlinux-conf
    $ make init

BACKUP

    $ make backup

RESTORE

    $ cd archlinux
    $ make restore

## MISC

.
├── arch_conf.py *a python script used to copy (file(s),directory(s),..)*
├── bundle **
├── filelist_sudo.txt *list of maintained files which need root privilege*
├── filelist.txt *list of maintained files which don't need root privilege*
├── Makefile *a lot of scripts,RTFC*
├── pacman.txt *list of pacman packages*
├── pip-requirements_sudo.txt *list of python packages installed globally*
├── pip-requirements.txt *list of python packages installed in your home*
├── README.md *current file*
└── yaourt.txt *list of yaourt packages*

only `filelist_sudo.txt` and `filelist.txt` need to be maintained manually,other \*.txt can be gen automaticly after `make backup`
