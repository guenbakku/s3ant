# coding: utf-8

#
# backup.py
#
# Handle upload to AWS S3 bucket
#
# @copyright  2017 NVB
# @license    MIT
#

import os
import types
import time
import boto3
import core.utils as utils
from core.configure import Configure

class Backup(object):
    ''' Handle backup to AWS S3 bucket '''
    
    def __init__(self):
        self.__config = {
            'credentials': {
                'aws_access_key_id': None,
                'aws_secret_access_key': None,
                'region_name': None,
            },
            'bucket': {
                'bucket': None,
                'bucket_basepath': None,
                'keep_days': None,
            },
        }
        self.dry_run = False


    def upload(self, filepath):
        ''' Upload provided file to S3 '''
        key = self._fullkey(filepath)
        bucket = self.__config['bucket']['bucket']
        s3 = self._s3client()

        # Check connection to S3 bucket
        s3.head_bucket(Bucket=bucket)
        
        # Upload file to S3 bucket
        print('Uploading to %s' % self._obj_uri(key))
        if self.dry_run == False:
            s3.upload_file(filepath, bucket, key)
            
            
    def delete_old_backups(self):
        ''' Delete old backup in S3 '''
        s3 = self._s3resource()
        bucket = s3.Bucket(self.__config['bucket']['bucket'])
        keep_seconds = self.__config['bucket']['keep_days'] * 86400
        now = int(time.time())
        for obj in bucket.objects.all():
            # Only remove objects which is inside provided basepath
            in_basepath = self._in_basepath(obj.key)
            if not in_basepath:
                continue
            
            # Only delete expired objects
            last_modified = utils.utc2epoch(obj.last_modified)
            expired = keep_seconds >= 0 and now - last_modified > keep_seconds
            if not expired:
                continue
                
            print('Deleting old backup %s' % self._obj_uri(obj.key))
            if self.dry_run == False:
                obj.delete()

    
    def credentials(self, config):
        ''' Configure credentials '''
        config = dict((k, v) for k, v in config.items()
            if k in self.__config['credentials'])
        self.__config['credentials'].update(config)


    def bucket(self, config):
        ''' Configure bucket '''
        config = dict((k, v) for k, v in config.items()
            if k in self.__config['bucket'])
        self.__config['bucket'].update(config)
        
        
    def _fullkey(self, filepath):
        ''' Return fullkey of backup file in S3 bucket '''
        key = os.path.basename(filepath)
        if self.__config['bucket']['bucket_basepath'] is not None:
            key = '/'.join([
                self.__config['bucket']['bucket_basepath'],
                key
            ])
        return key
        
    
    def _obj_uri(self, key):
        ''' Return full uri ex: s3://bucket/key of provided key '''
        bucket = self.__config['bucket']['bucket']
        return 's3://%s/%s' % (bucket, key)

    
    def _in_basepath(self, key):
        ''' Check a key is inside bucket_basepath or not '''
        basepath = self.__config['bucket']['bucket_basepath']
        # key is regarded that is inside basepath if it's value begins with basepath 
        # and the part after removed basepath from it is one-level-key.
        if not basepath:
            return len(key.split('/')) == 1
        elif key.startswith(basepath+'/'):
            remain = key.replace(basepath+'/', '', 1)
            return len(remain.split('/')) == 1
        else:
            return False


    def _s3client(self):
        ''' Return S3 client object '''
        return self._s3resource().meta.client


    def _s3resource(self):
        ''' Return S3 resource object '''
        resource = boto3.resource(
            's3',
            **self.__config['credentials']
        )
        return resource