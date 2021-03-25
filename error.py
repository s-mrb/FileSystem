from bcolors import *

def fs_corrupted():
            print(f"{bcolors.FAIL}Error: Your file system is corrupted or not found!!"
                  f"\nRe-initialize your system by running initialize_fs.py{bcolors.ENDC}")
            exit(0)


def wrong_argument():
    print(f"{bcolors.FAIL}Error: Please check your arguments!!{bcolors.ENDC}")
    return

def wrong_command():
    print(f"{bcolors.FAIL}Error: Command not found!!{bcolors.ENDC}")
    return

def fname_not_in_dir():
    print(f"{bcolors.FAIL}Error: File name is not present in current directory!!{bcolors.ENDC}")
    return

def file_not_a_dir():
    print(f"{bcolors.FAIL}Error: File not a directory!!!!{bcolors.ENDC}")




def disks_error():
    print(f"{bcolors.FAIL}Error: Number of disks can not be greater than total inode entries!!{bcolors.ENDC}")




def free_space_not_found():
    print(f"{bcolors.FAIL}Error: Entire disk is used up and no free space is found for new entry!!{bcolors.ENDC}")



def out_of_scope_memory_accessed_in_file():
    print(f"{bcolors.FAIL}Error: Location accessed is not present within this file!!{bcolors.ENDC}")




def trimming_empty_file():
    print(f"{bcolors.FAIL}Error: You can not trim empty file!!{bcolors.ENDC}")




def operation_not_for_folders():
    print(f"{bcolors.FAIL}Error: This operation can not be performed on folders/directories!!{bcolors.ENDC}")





def file_not_found():
    print(f"{bcolors.FAIL}Error: Specified file or directory not found!!{bcolors.ENDC}")




