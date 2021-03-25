
import math

from mount import addr_space, part_info, inode_table, data, current_inode, free_blocks, out_scope_block
from  settings import  *


def makeFile(current_inode, filename, dir=True):
    newfile_inode = False
    file_type = 0 if dir else 1;

    # find inode for new file
    for i in range(len(inode_table)):
        if inode_table[i][3] < 1:
            newfile_inode = i;

            # update references
            inode_table[i][3] = 1

            # update type
            inode_table[i][1] = file_type
            break



    # get address_list of current directory
    addr_list = inode_table[current_inode][9]


    # handle the case when addr_list[0] == -1
    if addr_list[0] == -1:
        addr_list = []

    # find index in addr_list for new data
    index = -1

    for i in range(len(addr_list)):
        if len(data[addr_list[i]]) < threshold:
            index = i;
            break;



    # if index found / there is element in the addr_list which could be filled
    if index > -1:
        data[addr_list[index]].update({filename:newfile_inode})
    else:
        new_address = free_blocks.pop(0);
        addr_list.extend([new_address])
        inode_table[current_inode][9] = addr_list
        free_blocks.extend([out_scope_block])
        free_blocks.sort()

        if len(data) == new_address:
            data.extend([{filename:newfile_inode}])
        else:
            data[new_address] = {filename:newfile_inode}


