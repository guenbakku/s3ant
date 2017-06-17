# coding: utf-8

#
# inout.py
#
# Utility functions for handling inout process
#
# @copyright  2017 NVB
# @license    MIT
#


def input(str=''):
    ''' Read input from stdin.
    This is made for compative with Python 2.x
    '''
    import sys
    sys.stdout.write(str)
    sys.stdout.flush()
    input = sys.stdin.readline()
    return input.rstrip()
