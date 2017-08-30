# coding: utf-8

#
# Utility functions
#
# @copyright  2017 guenbakku
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


def input(msg=''):
    ''' Read input from stdin.
    This is made for compative with Python 2.x
    '''
    import sys
    sys.stdout.write(msg)
    sys.stdout.flush()
    input = sys.stdin.readline()
    return input.rstrip('\n')
    
    
def error(msg=''):
    ''' Terminate script and write msg to stderr '''
    import sys
    sys.stderr.write(msg+'\n')
    sys.exit(1)
    

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
    return cmd.decode('utf-8')


def utc2epoch(dt):
    ''' Convert UTC datetime object to Epoch timestamp '''
    import calendar
    return calendar.timegm(dt.timetuple())


def random_str(length):
    ''' Return random string with provided length '''
    import string
    import random
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(length)])


def is_empty(check):
    ''' Check empty of various data type '''
    import six
    if check is None:
        return True
    if isinstance(check, list) and not list:
        return True
    if isinstance(check, six.string_types) and is_blank(check):
        return True
    return False

    
def is_blank(text):
    ''' Check text is blank '''
    return not (text and text.strip())
