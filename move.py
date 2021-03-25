import math
from settings import  *
from mount import  addr_space, part_info, inode_table,data, \
    current_inode, get_dir_table, read_dict, update_file_link_n_parent_dir,free_blocks,out_scope_block
from error import file_not_a_dir,fname_not_in_dir;



def move(fil1,fil2,parent_dir_inode):
    global inode_table
    dir_table = get_dir_table(parent_dir_inode);
    if fil2 not in dir_table:
        fname_not_in_dir();
        return -1;
        
    if fil2 not in dir_table:
        fname_not_in_dir();
        return -1;
    fil2_inode = dir_table[fil2];
    
    if inode_table[fil2_inode][1] != 0:
        file_not_a_dir()
        return
    else:
        fil1_inode = update_file_link_n_parent_dir(fil1,parent_dir_inode);
        if fil1_inode == None:
            fname_not_in_dir();
        add_link2file(fil1,fil1_inode,fil2_inode);
        return


def add_link2file(file1, file1_inode, file2_inode):
    global data

    # get address_list of fil2
    addr_list = inode_table[file2_inode][9]


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
        data[addr_list[index]].update({file1:file1_inode})
    else:
        new_address = free_blocks.pop(0);
        addr_list.extend([new_address])
        inode_table[file2_inode][9] = addr_list
        free_blocks.extend([out_scope_block])
        free_blocks.sort()

        if len(data) == new_address:
            data.extend([{file1:file1_inode}])
        else:
            data[new_address] = {file1:file1_inode}




# move("public","xx",current_inode)


