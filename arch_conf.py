#!/usr/bin/env python
# -*- coding:UTF-8 -*-
import os
import sys
import subprocess
import glob
#from distutils.file_util import copy_file

CONST_BUNDLE_DIR = 'bundle'
CONST_FILE_LIST = 'filelist.txt'
CONST_CP_OK = '%s'
CONST_CP_EXCEPT = '''WARN: except happened when copy from `%s` to `%s`,ignored.\n\treason:%s'''
CONST_BACKUP_DONE = 'DONE: all file in file_list.txt have been backed up in ./bundle'
CONST_RESTORE_DONE = 'DONE: all file in file_list.txt have been restored from ./bundle'

#TODO: true log
def log(msg):
    sys.stdout.write(msg + '\n')
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
        if from_path.startswith('~'):
            from_path = from_path.replace('~', os.environ['HOME'], 1)
        if to_path.startswith('~'):
            to_path = to_path.replace('~', os.environ['HOME'], 1)
        from_path_checked = glob.glob(from_path)
        command = ''
        response = ''
        if len(from_path_checked) == 0:
            response = '[the from path does not exists]'
        else:
            command = ['cp', '--parent', '-t', to_path] + from_path_checked
            if len(from_path_checked) == 1 and os.path.isdir(from_path_checked[0]):
                command.insert(1, '-r')
            process = subprocess.Popen(command,stdout=subprocess.PIPE)
            response = process.communicate()[0]
        return (' '.join(command or []), response or '')

    def copy(self, from_path, to_path):
        cmd, err = self.copy_file(from_path, to_path)
        if err:
            log(CONST_CP_EXCEPT % (from_path, to_path, err))
        else:
            log(CONST_CP_OK % cmd)

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
