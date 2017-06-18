# coding: utf-8

#
# compressor.py
#
# Object oriented interface for Linux' zip command
#
# @copyright  2017 NVB
# @license    MIT
#

import types
import subprocess
import core.utils as utils

class Compressor(object):
    ''' Simple interface for Linux' zip command '''
    
    def __init__(self):
        self.__config = {
            'paths': [],
            'options': ['symlinks'],
            'flags': ['r'],
            'exclude': [],
        }

        
    def configure(self, config):
        config = dict((k, v) for k, v in config.items() if k in self.__config)
        self.__config.update(config)


    def add(self, path):
        ''' Add path to zip '''
        if isinstance(path, types.StringTypes):
            path = [path]
        self.__config['paths'] += path


    def zip(self, zipfilepath):
        ''' Execute zip '''
        params = {}
        params['zipfilepath'] = zipfilepath
        params['paths'] = ' '.join(self.__config['paths'])
        params['options'] = ' '.join(['--'+v for v in self.__config['options']])
        params['flags'] = '-'+''.join(self.__config['flags'])
        params['exclude'] = ' '.join(['-x '+v for v in self.__config['exclude']])
        params['cmd'] = utils.which_cmd('zip')
        cmd = '%(cmd)s %(flags)s %(options)s %(zipfilepath)s %(paths)s %(exclude)s' % params
        exist_code = subprocess.call(cmd, shell=True)
        return exist_code
