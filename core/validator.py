# coding: utf-8

#
# validator.py
#
# Utility functions for handling validator
#
# @copyright  2017 NVB
# @license    MIT
#

import socket

def hostname(path=''):
    ''' Return internal hostname of current machine '''
    return socket.gethostbyaddr(socket.gethostname())[0]
