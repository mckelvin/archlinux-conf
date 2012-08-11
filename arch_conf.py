#!/usr/bin/env python
# -*- coding:UTF-8 -*-
import os
import sys
import subprocess
#from distutils.file_util import copy_file

CONST_BUNDLE_DIR = 'bundle'
CONST_FILE_LIST = 'filelist.txt'
CONST_CP_OK = 'cp %s %s'
CONST_CP_EXCEPT = '''WARN: except happened when copy from `%s` to `%s`,ignored.\n\t%s'''
CONST_BACKUP_DONE = 'DONE: all file in file_list.txt have been backed up in ./bundle'
CONST_RESTORE_DONE = 'DONE: all file in file_list.txt have been restored from ./bundle'

#TODO: true log
def log(msg):
    sys.stdout.write(msg)
    sys.stdout.flush()

class ArchConf:
    def __init__(self, BUNDLE_DIR=CONST_BUNDLE_DIR):
        """make sure an exists bundle dir"""
        self.repo = os.path.dirname(os.path.realpath(__file__))
        self.root = os.path.join(self.repo, BUNDLE_DIR)
        try:
            if not os.path.isdir(self.root):
                os.mkdir(self.root)
        except:
            pass
        finally:
            os.chdir(self.root)
    
    def copy_file(self, from_path, to_path):
        assert self.root == os.path.abspath(os.curdir)
        process = subprocess.Popen(['cp', '--parent',from_path, to_path], stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print output

    def copy(self, from_path, to_path):
        try:
            self.copy_file(from_path, to_path)
        except Exception, err:
            log(CONST_CP_EXCEPT % (from_path, to_path, err))
        else:
            log(CONST_CP_OK % (from_path, to_path))

    def backup(self, FILE_LIST=CONST_FILE_LIST):
        file_list = open(os.path.join(self.repo,FILE_LIST))
        for f in file_list:
            f = f.strip()
            if f and not f.startswith('#'):
                self.copy(f, self.root)#hack trick
    
    def restore(self, FILE_LIST=CONST_FILE_LIST):
        file_list = open(os.path.join(self.repo,FILE_LIST))
        for f in file_list:
            f = f.strip()
            if f and not f.startswith('#'):
                self.copy(f[1:], '/')#hack trick
        

def main(argv):
    ab = ArchConf()
    if len(argv) == 2:
        if '-b' in argv[1] or '--backup' in argv[1]:
            ab.backup()
        elif '-r' in argv[1] or '--restore' in argv[1]:
            ab.restore()
    else:
        print ''
        print 'usage:'
        print ''
        print '    backup via: python', argv[0], '-b' 
        print '    restore via: python', argv[0], '-r' 
    return 0

if __name__ == '__main__':
    sys.exit(main(['foo','-b']))
    #sys.exit(main(sys.argv))
