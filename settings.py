import math

global settings



# global fname
# fname="hard_disk.txt"

global directory_dictory_limit_per_block

directory_dictory_limit_per_block = 2
threshold = directory_dictory_limit_per_block

global disks
disks = 5

global block_size
block_size = 4096

global int_size
int_size = 342

global disk_size
disk_size = 50;

global inode_entries
inode_entries = 0

global ints_per_block
ints_per_block = math.floor(block_size / int_size)
