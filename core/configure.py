# coding: utf-8

#
# Manage configuration centrally
#
# @copyright  2017 guenbakku
# @license    MIT
#

import os
import json
import six # For compatibility in Python 2 and 3
import core.utils as utils
import core.hash as hash
from collections import OrderedDict


class Configure(object):
    ''' Handle configure '''
    
    CS = ' '    # Command's arguments seperator
    SS = '/'    # S3 path seperator
    
    config_filepath = utils.abspath('config.json')
    
    # User input config
    __user_config = OrderedDict([
        ('aws_access_key_id', ''),
        ('aws_secret_access_key', ''),
        ('region_name', ''),
        
        ('bucket', ''),
        ('bucket_basepath', ''),
        ('backup_paths', []),
        ('backup_exclude_paths', []),
        
        ('keep_days', 7),
        ('retry', 3),
    ])
    
    # User input config but not executed via CLI
    __opt_config = OrderedDict([
        ('timezone', 'Asia/Tokyo'),
        ('zip_options', []),
        ('zip_flags', ['r']),
    ])
    
    # System config
    __sys_config = OrderedDict([
        ('hostname', None),
    ])
    
    # Full config
    __config = OrderedDict()


    @classmethod
    def set(cls, config):
        ''' Update config in memory '''
        config = dict((k, v) for k, v in config.items() if k in cls.__config)
        cls.standadize(config)
        cls.__config.update(config)


    @classmethod
    def standadize(cls, config):
        ''' Standardize config to correct data type which were declared '''
        raw_config = {}
        raw_config.update(cls.__user_config)
        raw_config.update(cls.__opt_config)
        raw_config.update(cls.__sys_config)
        for key, val in config.items():
            if key not in raw_config:
                continue
            raw_val = raw_config[key]
            if isinstance(val, six.string_types):
                config[key] = val.strip()
            if isinstance(raw_val, list):
                if isinstance(config[key], six.string_types):
                    config[key] = config[key].split(cls.CS)
                config[key] = [v for v in config[key] if not utils.is_empty(v)]
            if isinstance(raw_val, six.integer_types):
                if isinstance(config[key], six.string_types):
                    config[key] = int(config[key])


    @classmethod
    def get(cls, path=None):
        ''' Return config from provided path '''
        if path is None:
            return cls.__config
        else:
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
        for key in cls.__user_config:
            if (isinstance(cls.__user_config[key], list)):
                default_val = cls.CS.join(cls.__config[key])
            else:
                default_val = cls.__config[key]
            config[key] = utils.input(' %s [%s]:\n -> ' % (key, default_val))
            if config[key] == '':
                config[key] = default_val
        cls.set(config)


    @classmethod
    def sys_input(cls):
        ''' Set system config '''
        config = {
            'hostname': utils.hostname(),
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
        cls.__config.update(cls.__user_config)
        cls.__config.update(cls.__opt_config)
        cls.__config.update(cls.__sys_config)
        config = {}
        if (os.path.isfile(cls.config_filepath)):
            with open(cls.config_filepath, 'r') as f:
                config = json.load(f)
        cls.set(config)
    
    
    @classmethod
    def validate(cls):
        # Check current machine can run this backup process or not.
        # We compare hostname in config.json with runtime hostname,
        # if they are equal, current machine has privilege to run this script.
        if utils.hostname() != Configure.get('hostname'):
            utils.error(
                'Error: Hostname not match. \n'
                + 'Run command [configure] to redump hostname and try again.')
                
        # Validate required input
        required_keys = [
            'aws_access_key_id', 
            'aws_secret_access_key', 
            'region_name', 
            'bucket', 
            'backup_paths',
            'keep_days',
            'retry',
        ]
        for key in required_keys:
            if utils.is_empty(cls.__config[key]):
                utils.error('Error: Config item [%s] is empty' % key)


# Initialize
Configure.read_from_file()
