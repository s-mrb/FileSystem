from mk_itable import mk_itable;
import math
from settings import *
from environment_var import *
from error import  disks_error
from bcolors import *




def setup():
    global disks, block_size, disk_size;
    disks, block_size,  disk_size = [int(x) for x in (input("Please enter the number of disks, block size(in KB) and disk size(in MB)\nValues must be space separated: x y z\n").split())];
def partition():

    print(f"{bcolors.WARNING}Warning!! all your data if present will be erased, press 'e' to exit and anyother key to continue!!{bcolors.ENDC}")
    redflag = input()
    if redflag=='e':
        exit(0)

    fname = input("Please enter filename with extension (.txt)\n")
    setup();
    inode_entries = (disk_size * 1000 ) // block_size;

    if disks >= inode_entries:
        disks_error()
        return


    print("disks :",disks,"\t\tblock size :",block_size,"\t\tdisk size :",disk_size,"\n");
    print("Total Inode entries : ", inode_entries)
    print(f"{bcolors.OKGREEN}File system {fname} has been successfully initialized, you can now run {bcolors.OKBLUE}python3 ./start_fs.py{bcolors.ENDC}{bcolors.ENDC}\n")

    fr = inode_entries%disks;


    if (fr == 0):
        fr = inode_entries//disks;
        for i in range(disks):
            if "disk"+str(i-1) in inode4disks:
                inode4disks["disk"+str(i)] = [inode4disks["disk"+str(i-1)][1]+1,inode4disks["disk"+str(i-1)][1]+fr];
            else:
                inode4disks["disk" + str(i)] = [1, fr];
    else:
        fr = inode_entries//disks;
        last_block = -1;
        for i in range(disks-1):
            if "disk"+str(i-1) in inode4disks:
                inode4disks["disk"+str(i)] = [inode4disks["disk"+str(i-1)][1]+1,inode4disks["disk"+str(i-1)][1]+fr];
            else:
                inode4disks["disk" + str(i)] = [1,  fr];
            last_block = i+1;

        inode4disks["disk" + str(last_block)] = [inode4disks["disk" + str(last_block - 1)][1] + 1, inode_entries];

    free_blocks_boundry = math.ceil((inode_entries*int_size)/block_size)
    free_blocks = list(range(inode_entries))

    # first line should tell address pace for mbr and inode
    # ?check  : to check whetehr it works, make int size to 342
    addr_space = {"mbr":[1,1],"fb":[2,(2+free_blocks_boundry)-1],"ib":[(2+free_blocks_boundry),(inode_entries+(2+free_blocks_boundry))]}
    ints_per_block = math.floor(block_size/int_size)
    mk_itable(inode_entries=inode_entries, addr_space=addr_space, inode4disks=inode4disks, ints_per_block=ints_per_block,free_blocks=free_blocks, fname=fname)





def switch(option):
    options = {
        "mount": partition()
    }
    return options.get(option);

