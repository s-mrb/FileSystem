from mount import inode_table, current_inode, get_dir_table
from bcolors import *
def ls(current_inode):
    current_dir = get_dir_table(current_inode)

    for i, fil in enumerate(current_dir):
        if inode_table[current_dir[fil]][1] == 0:
            print(f"{bcolors.BOLD}{fil}{bcolors.ENDC}",end="")
            print("\t",end="")
            if i%10 == 0:
                print("");
            continue
        else:
            print(f"{bcolors.OKBLUE}{fil}{bcolors.ENDC}", end="")
            print("\t", end="")
            if i%10 == 0:
                print("");
            continue

    print("")
    return


