import ast
import os
import sys

from error import fs_corrupted;
from bcolors import *


print("Please enter the name of file system which needs to be started. ",end="")
print(f"{bcolors.OKCYAN}DONT FORGET EXTENSION (.txt){bcolors.ENDC}\nYou would have used this name while you ran {bcolors.WARNING} initialize_fs.py {bcolors.ENDC}\n")
fname = input()

addr_space = {}
memmap = {}
part_info = {}
inode_table = []
data = []
global current_inode
current_inode = 0;
global dic_locs
dic_locs = {}
free_blocks = []
out_scope_block = float('inf')
parent = "root"
parents_stack = []

from error import file_not_a_dir
def get_dir_table(inode):
    global inode_table
    dir_table = {}
    if inode_table[inode][1] == 1:
        file_not_a_dir()
        return
    if len(data) != 0:
        for i in range(len(inode_table[inode][9])):
            dir_table.update(data[inode_table[inode][9][i]])
        return dir_table
    else:
        return {}

def update_file_link_n_parent_dir(filename,current_dir_inode):
    index ,length = -1, -1
    inode2traverse = -1

    # addr_list corresponding to current_inode, must contain dictionary for directory
    rang = len(inode_table[current_dir_inode][9]);

    # this function should not run if len(data) == 0
    if len(data)!=0:

        # loop through addr_list
        for i in range(rang):

            # read dictionary corresponding to this index of addr_list
            temp = data[inode_table[current_dir_inode][9][i]]

            # check if file exists in dictionary corresponding to this index of addr_list
            if filename in temp:

                # if file found then note its inode, for traversal use later
                inode2traverse = temp[filename]

                # note index of addr_list whose corresponding dictionary contain file
                index = i

                # get length of dictionary corresponding to this index of addr_list
                length = len(temp)
                if length > 1:
                    del temp[filename]
                    data[inode_table[current_dir_inode][9][i]] = temp;
                    return inode2traverse
                else:
                    # its better to put it equal to small string
                    data[inode_table[current_dir_inode][9][i]] = "x";

                    if len(inode_table[current_dir_inode][9]) == 1:
                            inode_table[current_dir_inode][9] = [-1]
                            return inode2traverse
                    inode_table[current_dir_inode][9].pop(index)
                    return inode2traverse
    return  False


def read_dict(txt_dict):
    return ast.literal_eval(txt_dict)
def read_addr_space(fname):
    with open(fname, "r") as f:
        for line in f:
            global addr_space;
            try:
                addr_space = read_dict(line);
            except:
                fs_corrupted()
                return
            break

def read_partition_info(fname):
    global part_info;
    part_info_arr  = read_content(fname, [addr_space["mbr"][0],addr_space["mbr"][1]])
    part_info = read_dict(part_info_arr[0])

def read_free_blocks_info(fname):
    global free_blocks;
    free_blocks_str = read_content(fname,[addr_space["fb"][0],addr_space["fb"][1]])
    for str in free_blocks_str:
        free_blocks.extend([int(x) for x in str.split()])



def read_inode_table(fname):
    global inode_table;
    inode_table  = read_content(fname, [addr_space["ib"][0],addr_space["ib"][1]], inode=True)

    for i in range(len(inode_table)):
        inode_table[i][0] = int(inode_table[i][0]);
        inode_table[i][1] = int(inode_table[i][1]);
        inode_table[i][3] = int(inode_table[i][3])
        inode_table[i][-1] =[int(x) for x in  inode_table[i][-1].split('_')]
        if inode_table[i][1] == 0 and inode_table[i][-1][0] != -1:
            for j in range(len(inode_table[i][-1])):
                dic_locs[str(inode_table[i][-1][j])] = True;

def read_data(fname):
    global dic_locs
    if len(dic_locs) == 0:
        return
    global data;
    rang = [int(addr_space['ib'][1])+1,float('inf')];
    content = [];
    with open(fname, "r") as f:
        for i, line in enumerate(f):
            if i < rang[0]:
                continue
            if i > rang[1]:
                break
            if str(i-rang[0]) in dic_locs:
                content.append(read_dict(line))
            else:
                content.append(line[0:])

    data = content;

def read_content(fname, range, inode=False):
    content = [];
    with open(fname, "r") as f:
        for i,line in enumerate(f):
            if i<range[0]:
                continue
            if i>range[1]:
                break
            if inode:
                content.append((line[0:-1]).split())
            else:
                content.append(line[0:-1])


    return content;




def start():

    if not os.path.exists(fname):
            # or raise error for not yet having partition
        fs_corrupted()
        return
    else:

        read_addr_space(fname)
        read_partition_info(fname)
        read_free_blocks_info(fname)
        read_inode_table(fname)
        read_data(fname)
        global  out_scope_block;
        n_inode = addr_space["ib"];
        out_scope_block = n_inode[1]-n_inode[0]+1;




start()
