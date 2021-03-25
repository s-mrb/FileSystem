from mount import get_dir_table

# global current_inode
from error import file_not_a_dir, file_not_found
def chDir(file_name, current_inode,inode_table ):
    dir_table = get_dir_table(current_inode)
    if file_name not in dir_table:
        file_not_found()
        return -1

    new_inode = dir_table[file_name]
    if inode_table[new_inode][1] == 0:
        return new_inode
    else:
        file_not_a_dir()
        return -1




