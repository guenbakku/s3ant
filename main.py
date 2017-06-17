# coding: utf-8

from core.configure import Configure
from core import path

# Configure.set({'base_path': 'test', 'hiep': 'test'})
# Configure.write_to_file()
Configure.initialize()
print(Configure.get('hostname'))
print(Configure.get('access_key_id'))