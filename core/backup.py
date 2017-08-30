# coding: utf-8

#
# Handle upload to AWS S3 bucket
#
# @copyright  2017 guenbakku
# @license    MIT
#

import os
import types
import time
import boto3
import core.utils as utils
from datetime import datetime
from core.configure import Configure

class Backup(object):
    ''' Handle backup to AWS S3 bucket '''
    
    def __init__(self):
        self.__config = {
            'credentials': {
                'aws_access_key_id': '',
                'aws_secret_access_key': '',
                'region_name': '',
            },
            'bucket': {
                'bucket': '',
                'bucket_basepath': '',
                'keep_days': 7,
            },
        }
        
        self.__filepath = None
        self.__fullkey = None
        self.__check_level = None
        
        self.delete = True
        self.dry_run = False
    

    def backup(self, filepath):
        ''' Group cleanup and upload in one method '''
        self.filepath(filepath)
        self.cleanup()
        self.upload()


    def cleanup(self):
        ''' Delete old backups in S3 '''
        if self.delete == False:
            return None
        
        self._validate()
        
        s3 = self._s3resource()
        bucket = s3.Bucket(self.__config['bucket']['bucket'])
        keep_seconds = self.__config['bucket']['keep_days'] * 86400
        now = int(time.time())
        for obj in bucket.objects.all():
            # Skip if key does not begin from provided basepath
            basepath = self.__config['bucket']['bucket_basepath']
            in_basepath = utils.is_empty(basepath) or obj.key.startswith(basepath+Configure.SS)
            if not in_basepath:
                continue
            
            # Skip if current key is not same level with current upload key
            is_same_level = self._key_level(obj.key) == self.__check_level
            if not is_same_level:
                continue
            
            # Skip if object does not expired
            last_modified = utils.utc2epoch(obj.last_modified)
            expired = keep_seconds >= 0 and now - last_modified > keep_seconds
            if not expired:
                continue
                
            print('Deleting old %s' % self._obj_uri(obj.key))
            if self.dry_run == False:
                obj.delete()


    def upload(self):
        ''' Upload provided file to S3 '''
        self._validate()
        
        filepath = self.__filepath
        key = self.__fullkey
        bucket = self.__config['bucket']['bucket']
        s3 = self._s3client()

        # Check connection to S3 bucket
        s3.head_bucket(Bucket=bucket)
        
        # Upload file to S3 bucket
        print('Uploading to %s' % self._obj_uri(key))
        if self.dry_run == False:
            s3.upload_file(filepath, bucket, key)


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
        self.__config['bucket']['bucket_basepath'] = \
            self.__config['bucket']['bucket_basepath'].strip(Configure.SS)
        

    def filepath(self, filepath_):
        ''' Set upload filepath '''
        self.__filepath = filepath_
        self.__fullkey = self._fullkey(filepath_)
        self.__check_level = self._key_level(self.__fullkey)


    def _fullkey(self, filepath):
        ''' Create full S3 key of backup file from filepath '''
        key = Configure.SS.join([
            datetime.now().strftime('%Y-%m-%d'),
            os.path.basename(filepath)
        ])
        # Add basepath
        if not utils.is_empty(self.__config['bucket']['bucket_basepath']):
            key = Configure.SS.join([
                self.__config['bucket']['bucket_basepath'],
                key
            ])
        return key
        
    
    def _obj_uri(self, key):
        ''' Return full uri ex: s3://bucket/key of provided key '''
        bucket = self.__config['bucket']['bucket']
        return 's3://%s%s%s' % (bucket, Configure.SS, key)


    def _key_level(self, key):
        ''' Return level of key '''
        return key.count(Configure.SS)

    
    def _validate(self):
        ''' Validate properties '''
        if self.__fullkey is None:
            raise ValueError('Upload key empty')
        

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