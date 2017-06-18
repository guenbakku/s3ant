# coding: utf-8

import os
from core import utils
from core.configure import Configure
from core.compressor import Compressor
from core.backup import Backup

# Configure.initialize()

cp = Compressor() 
zip_source = [utils.abspath('core')]
zip_target = utils.abspath('test.zip')
cp.configure({'exclude': [utils.abspath('core/compress.py')]})
cp.add(zip_source)
cp.zip(zip_target)

bk = Backup()
bk.dry_run = True
bk.credentials(Configure.get())
bk.bucket(Configure.get())
bk.delete_old_backups()
bk.upload(zip_target)

os.remove(zip_target)