

from mount import  addr_space, part_info, inode_table,data, current_inode, get_dir_table, read_dict, update_file_link_n_parent_dir,free_blocks

def recurse_inodel(filename, inode2traverse):

    # if inode_table[inode2traverse][3] > 1 then give warning before deleting
    inode_table[inode2traverse][3] = -1

    # We will go to this memeory only if inode2traverse is file
    memory2free = inode_table[inode2traverse][9]
    file_type = inode_table[inode2traverse][1]
    inode_table[inode2traverse][1] = -1
    # if inode2traverse refers to a file(not dir) then just free all memory
    if file_type == 0 and memory2free[0] != -1:
        for i in range(len(memory2free)):
            inner_d = data[memory2free[i]];
            # if inode to be deleted have address list len > 1 then when u read dictionary
            # at address corresponding to ith element of address list then pop that element from address list
            if len(inode_table[inode2traverse][9]) > 1:
                inode_table[inode2traverse][9].pop(0)
            else:
                inode_table[inode2traverse][9] = [-1]
            for key in inner_d:
                recurse_inodel(key,inner_d[key])
    else:
        inode_table[inode2traverse][9] = [-1]

    return


from error import fname_not_in_dir;


def deleteFile(filename, current_inode):
    inode2traverse = update_file_link_n_parent_dir(filename,current_inode);
    if not inode2traverse:
        fname_not_in_dir();
        return
    else:
        recurse_inodel(filename, inode2traverse)






