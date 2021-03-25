from mount import get_dir_table, current_inode,inode_table, out_scope_block, free_blocks, addr_space
from error import file_not_found
from bcolors import *

def blocksConsumedByFile(filename):
    filename = filename;
    dir_table = get_dir_table(current_inode)
    if filename in dir_table:
        return inode_table[dir_table[filename]][9]
    else:
        file_not_found()
        return



def freeBlocks():
    print("Unused memeory blocks:")
    print(free_blocks)
    print(f"Note: Block# " + f"{bcolors.OKGREEN}{str(out_scope_block)}{bcolors.ENDC}" + f" is {bcolors.OKCYAN}out of scope flag{bcolors.ENDC} for this hard disk,it can be different for different disks"
                                                   " it means this block number doesn't exist "  
                                                   "it is kept to maintain heap of fixed size,"
                                                   " whenever a block is used a new out scope block# is added")


def showMasterBlock():
    print(f"Master block is at start of hard disk and {bcolors.OKGREEN}contain addresses of major block groups{bcolors.ENDC} which are important for starting filesystem.")
    print("Major block groups are:\n"
          f"\n\t-{bcolors.WARNING}Master Boot Record (mbr){bcolors.ENDC}\t\t->\tBoot record for File System, not system"
          f"\n\t-{bcolors.WARNING}Free Blocks (fb){bcolors.ENDC}\t\t\t->\tContain unused block # to maintain a heap."
          f"\n\t-{bcolors.WARNING}Inode Block (ib){bcolors.ENDC}\t\t\t->\tContains Inode Table")
    print()
    print("Block group name with start and end address is given below:")
    for blockGroup in addr_space:
        print("\t"+blockGroup+"\t\t"+str(addr_space[blockGroup]))

