# coding: utf-8

#
# Backup data to AWS S3 bucket
#
# @copyright  2017 guenbakku
# @license    MIT
#

import os
import time
from datetime import datetime
from core import utils
from core.configure import Configure
from core.compressor import Compressor
from core.backup import Backup

NAME = 's3ant'
VERSION = '0.1.1'
CREDITS = '%s (v%s)' % (NAME, VERSION)
DESCRIPTION = '%s - Backup data to AWS S3 bucket like an ant.' % NAME

def backup(dry_run=False, delete=True):
    ''' Execute backup to S3 and retry if error '''
    retry = Configure.get('retry')
    count = 0
    success = False
    while True:
        count+=1
        try:
            backup_single(dry_run, delete)
            success = True
        except Exception as ex:
            print('\nFAILED: %s' % str(ex))
        
        if success == True:
            print('\nOK')
            break
        if count > retry:
            break
        if dry_run:
            break
            
        print('\nRetrying... [%d]\n' % count)
        time.sleep(3)
        
    if dry_run:
        print('=====DRY RUN=====')

def backup_single(dry_run=False, delete=True):
    ''' Execute backup to S3 '''
    Configure.validate()
    try:
        timezone = Configure.get('timezone')
        if timezone:
            os.environ['TZ'] = timezone
        
        zip_config = {
            'paths': Configure.get('backup_paths'),
            'exclude': Configure.get('backup_exclude_paths'),
            'options': Configure.get('zip_options'),
            'flags': Configure.get('zip_flags'),
        }
        zip_target = utils.abspath('_'.join([
            Configure.get('hostname'),
            datetime.now().strftime('%Y%m%d-%H%M%S'),
            utils.random_str(6)
        ]) + '.zip')
        
        print('Create zip file:')
        cp = Compressor()
        cp.configure(zip_config)
        cp.zip(zip_target)
        
        print('\nBackup to S3:')
        bk = Backup()
        bk.dry_run = dry_run
        bk.delete = delete
        bk.credentials(Configure.get())
        bk.bucket(Configure.get())
        bk.backup(zip_target)
    finally:
        if os.path.isfile(zip_target):
            print('\nDeleting local zip file:')
            print(zip_target)
            os.remove(zip_target)
