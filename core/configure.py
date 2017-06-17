# coding: utf-8

import os
import json
import core.path as path
import core.hash as hash
import core.inout as io
import core.validator as vld
from collections import OrderedDict

class Configure(object):
    ''' Handle configure '''
    
    config_filepath = path.abspath('config.json')
    
    __config = OrderedDict([
        ('access_key_id', None),
        ('secret_access_key', None),
        ('region', None),
        
        ('bucket', None),
        ('basepath', None),
        
        ('keep_days', 7),
        ('timezone', 'Asia1/Tokyo'),
        
        ('hostname', None),
    ])
    
    # List of keys of config that not allowed for user input
    __reserved_config_keys = [
        'hostname'
    ]
    

    @classmethod
    def set(cls, config):
        ''' Update config in memory'''
        cls.__config.update(config)


    @classmethod
    def get(cls, path):
        ''' Return config from provided path '''
        return hash.get(cls.__config, path)
    
    
    @classmethod
    def initialize(cls):
        ''' Initialize config file '''
        cls.user_input()
        cls.sys_input()
        cls.write_to_file()
    

    @classmethod
    def user_input(cls):
        ''' Prompt user input for config '''
        cls.read_from_file()
        config = {}
        for key, val in cls.__config.items():
            if key in cls.__reserved_config_keys:
                continue
            config[key] = io.input(' %s [%s]: ' % (key, val))
            if not config[key]:
                config[key] = val
        cls.set(config)


    @classmethod
    def sys_input(cls):
        ''' Set system config '''
        config = {
            'hostname': vld.hostname(),
        }
        cls.set(config)
        

    @classmethod
    def write_to_file(cls):
        ''' Write config to file '''
        with open(cls.config_filepath, 'w') as f:
            json.dump(cls.__config, f, indent=4)


    @classmethod
    def read_from_file(cls):
        ''' Read config from file '''
        config = {}
        if (os.path.isfile(cls.config_filepath)):
            with open(cls.config_filepath, 'r') as f:
                config = json.load(f)
        cls.set(config)


# Initialize
Configure.read_from_file()