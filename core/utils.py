# coding: utf-8

#
# utils.py
#
# Utility functions
#
# @copyright  2017 NVB
# @license    MIT
#

def abspath(path=''):
    ''' Return absolute path of provided item
    If provided item is an absolute path, just return it.
    If provided item is a relative path, add absolute to front 
    main.py to before it to make a completely absolute path.
    '''
    import os
    return os.path.join(basepath(), path)


def basepath():
    ''' Return base path to front main.py file '''
    import os
    back_level = 2
    base_path = os.path.abspath(__file__)
    for count in range(back_level):
        base_path = os.path.dirname(base_path)
    return base_path + os.sep


def hostname(path=''):
    ''' Return internal hostname of current machine '''
    import socket
    return socket.gethostbyaddr(socket.gethostname())[0]


def input(str=''):
    ''' Read input from stdin.
    This is made for compative with Python 2.x
    '''
    import sys
    sys.stdout.write(str)
    sys.stdout.flush()
    input = sys.stdin.readline()
    return input.rstrip()


def which_cmd(name):
    ''' Return fullpath to executation of provided command '''
    import subprocess
    cmd = subprocess.Popen(
        "which %s 2>/dev/null" % name, 
        shell=True, 
        stdout=subprocess.PIPE
    ).stdout.read()
    cmd = cmd.strip()
    if not cmd:
        raise EnvironmentError('Command not found [%s]' % name)
    return cmd