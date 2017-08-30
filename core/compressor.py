# coding: utf-8

#
# Object oriented interface of Linux' zip command
#
# @copyright  2017 guenbakku
# @license    MIT
#

import subprocess
import core.utils as utils

class CompressErrorException(Exception):
    pass

class Compressor(object):
    ''' Simple interface of Linux' zip command '''
    
    def __init__(self):
        self.__config = {
            'paths': [],
            'exclude': [],
            'options': [],
            'flags': ['r'],
        }

        
    def configure(self, config):
        ''' Setup configuration '''
        config = dict((k, v) for k, v in config.items() if k in self.__config)
        self.__config.update(config)


    def add(self, path):
        ''' Add path to zip '''
        if isinstance(path, str):
            path = [path]
        self.__config['paths'] += path
        
    
    def exclude(self, path):
        ''' Add exclude path to zip '''
        if isinstance(path, str):
            path = [path]
        self.__config['exclude'] += path


    def zip(self, zipfilepath):
        ''' Execute zip '''
        params = {}
        params['zipfilepath'] = zipfilepath
        params['paths'] = ' '.join(self.__config['paths'])
        params['options'] = ' '.join(['--'+v for v in self.__config['options']])
        params['flags'] = ' '.join(['-'+v for v in self.__config['flags']])
        params['exclude'] = ' '.join(['-x '+v for v in self.__config['exclude']])
        params['cmd'] = utils.which_cmd('zip')
        cmd = '%(cmd)s %(flags)s %(options)s %(zipfilepath)s %(paths)s %(exclude)s' % params
        exist_code = subprocess.call(cmd, shell=True)
        if int(exist_code) != 0:
            raise CompressErrorException('Something went wrong when compress files')
