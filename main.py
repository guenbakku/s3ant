# coding: utf-8

from core.configure import Configure
from core import utils
from core.compressor import Compressor

source = [utils.abspath('core'), utils.abspath('tmp')]
target = utils.abspath('test.zip')

cp = Compressor() 
cp.configure({'exclude': [utils.abspath('core/compress.py')]})
cp.add(source)
print(cp.zip(target))

# print(utils.which_cmd('zip'))

# Configure.set({'base_path': 'test', 'hiep': 'test'})
# Configure.write_to_file()
# Configure.initialize()
# print(Configure.get('hostname'))
# print(Configure.get('access_key_id'))