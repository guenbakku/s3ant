# coding: utf-8

#
# path.py
#
# Utility functions for handling path
#
# @copyright  2017 NVB
# @license    MIT
#

import os

def abspath(path=''):
    ''' Return absolute path of provided item
    If provided item is an absolute path, just return it.
    If provided item is a relative path, add absolute to front 
    main.py to before it to make a completely absolute path.
    '''
    base_path = base()
    return os.path.join(base_path, path)


def base():
    ''' Return base path to front main.py file '''
    back_level = 2
    base_path = os.path.abspath(__file__)
    for count in range(back_level):
        base_path = os.path.dirname(base_path)
    return base_path + os.sep