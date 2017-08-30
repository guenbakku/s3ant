# coding: utf-8

#
# main.py
#
# s3ant - Backup data to AWS S3 bucket like an ant
#
# @copyright  2017 guenbakku
# @license    MIT
#

import os
import argparse
import core.s3ant as s3ant
from core.configure import Configure


def input():
    ''' Get input from command line. '''
    parser = argparse.ArgumentParser(description='%s - Backup data to AWS S3 bucket.' % s3ant.NAME)
    parser.add_argument('command', help='name of command', choices=['configure', 'backup'])
    parser.add_argument('-n', '--dry-run', dest='dry_run', action='store_true', default=False, help='execute in dry-run mode')
    parser.add_argument('--disable-delete', dest='disable_delete', action='store_true', default=False, help='disable delete old backups')
    parser.add_argument('-v', action='version', version=s3ant.CREDITS)
    return parser.parse_args()


# Here we go
args = input()
if args.command == 'configure':
    Configure.initialize()
else:
    s3ant.backup(
        dry_run=args.dry_run, 
        delete=not args.disable_delete
    )