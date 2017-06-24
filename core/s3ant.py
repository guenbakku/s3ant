# coding: utf-8

#
# s3ant.py
#
# Backup data to AWS S3 bucket
#
# @copyright  2017 NVB
# @license    MIT
#

import os
from datetime import datetime
from core import utils
from core.configure import Configure
from core.compressor import Compressor
from core.backup import Backup

NAME = 's3ant'
VERSION = '0.1.0'
CREDITS = '%s (v%s)' % (NAME, VERSION)

def run(dry_run=False):
    ''' Execute backup to S3 '''
    Configure.validate()
    try:
        timezone = Configure.get('timezone')
        if timezone:
            os.environ['TZ'] = timezone
        
        zip_source = Configure.get('backup_paths')
        zip_target = utils.abspath('_'.join([
            Configure.get('hostname'),
            datetime.now().strftime('%Y%m%d-%H%M%S'),
            utils.random_str(4)
        ]) + '.zip')
        
        print('Create zip file:')
        cp = Compressor()
        cp.add(zip_source)
        result = cp.zip(zip_target)
        
        print('\nBackup to S3:')
        bk = Backup()
        bk.dry_run = dry_run
        bk.credentials(Configure.get())
        bk.bucket(Configure.get())
        bk.delete_old_backups()
        bk.upload(zip_target)
    finally:
        print('\nDeleting local zip file:')
        if os.path.isfile(zip_target):
            os.remove(zip_target)
        print('OK')
    
    if dry_run:
        print('=====DRY RUN=====')


