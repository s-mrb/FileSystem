
from  settings import *
from mount import *
from  create import makeFile
from hard_write import hardWrite
from move import  move
from delete import deleteFile
from OpenFile import Open
from delete import deleteFile
from move import move
from chDir import chDir
from memory import blocksConsumedByFile, freeBlocks,showMasterBlock
from bcolors import *
from ls import ls
from error import wrong_argument,wrong_command
from mount import  current_inode,parents_stack,inode_table,data


def repl():
    global current_inode
    global inode_table
    global data
    global parents_stack
    print(f"\n{bcolors.OKGREEN}MOUNTED SUCCESSFULLY{bcolors.ENDC}")
    print(f"{bcolors.OKCYAN}You have been entered in CLI (enter e to exit CLI){bcolors.ENDC}\n")
    
    while True:
        command = input()
        arg = command.split()
        # e to exit
        if command == 'e':
            break

        if arg[0] == "ls":
            if len(arg) == 1:
                ls(current_inode)
                print("");
            else:
                wrong_argument()
                print("");
                continue
            continue

        if arg[0] == "parent":
            print("");
            pass


        # make_file filename dir
        if arg[0] == "makeFile":
            if len(arg) != 3:
                wrong_argument()
                print("");
                continue
            filename = arg[1]
            dir = int(arg[2])
            dir = 1 if dir else 0;
            makeFile(filename=filename, dir=dir, current_inode=current_inode)
            print(f"{bcolors.OKGREEN}{bcolors.OKCYAN}{filename}{bcolors.ENDC} has been created{bcolors.ENDC}\n")
            continue

        # print data
        if arg[0] == "data":

            if len(arg) != 2:
                wrong_argument()
                print("");
                continue

            if int(arg[1]) == -1:
                for content in data:
                    print(content)

            else:
                print(data[int(arg[1])])
            print("");
            continue

        if arg[0] == "open":

            if len(arg) != 2:
                wrong_argument()
                continue

            filename = arg[1]
            # mode = arg[2] no longer needed
            opened_file = Open(filename);

            open = True
            print(f"{bcolors.OKGREEN}{filename}{bcolors.ENDC} now open.\nEnter {bcolors.OKCYAN}close{bcolors.ENDC} to close this file.")
            while open == True:
                
                arg2 = input().split()
                if arg2[0] == "write":
                    if len(arg2)!=1:
                        wrong_argument()
                        continue
                    print(f"Please enter the start location for writing the text\nEnter {bcolors.OKCYAN}@e{bcolors.ENDC} to exit write mode.")
                    loc = input();
                    if loc == "@e":
                        continue
                    loc = int(loc)
                    print(f"Please enter the text to be written to {bcolors.OKGREEN}{filename}{bcolors.ENDC} from position {bcolors.OKGREEN}{loc}{bcolors.ENDC}.\nEnter {bcolors.OKCYAN}@e{bcolors.ENDC} to exit write mode.")
                    text = input();
                    if text == "@e":
                        continue;
                    opened_file.write(text, loc=loc)

                if arg2[0] == "read":
                    if len(arg2)!= 1:
                        wrong_argument()
                        continue
                        
                    print(f"Please enter the space separated {bcolors.OKGREEN}start{bcolors.ENDC} and {bcolors.OKGREEN}end{bcolors.ENDC} locations for reading the text, {bcolors.OKGREEN}-1{bcolors.ENDC} as end to read till end.\nEnter {bcolors.OKCYAN}@e{bcolors.ENDC} to exit read mode.")
                    loc = input();
                    if loc == "@e":
                        continue
                    loc = [int(x) for x in loc.split()]			
                    print(opened_file.read(start=loc[0], end=loc[1]))

                if arg2[0] == "truncate":
                    if len(arg2)!=2:
                        wrong_argument()
                        continue
                    size = int(arg2[1])
                    opened_file.truncate(size)

                if arg2[0] == "close":
                    break

                print()
            continue

        if arg[0] == "delete":
            if len(arg)!= 2:
                wrong_argument()
                print("");
                continue
            filename = arg[1]
            deleteFile(filename=filename, current_inode=current_inode)
            print(f"{bcolors.OKGREEN}{bcolors.OKCYAN}{filename}{bcolors.ENDC} has been deleted{bcolors.ENDC}\n")
            continue

        if arg[0] == "move":
            if len(arg) != 3:
                wrong_argument()
                print("");
                continue
            file1 = arg[1];
            file2 = arg[2]

            flag = move(file1, file2, current_inode)
            if flag == -1:
                print("");
                continue;
            print(f"{bcolors.OKGREEN}{bcolors.OKCYAN}{file1}{bcolors.ENDC} has been moved in {bcolors.OKCYAN}{file1}{bcolors.ENDC}{bcolors.ENDC}\n")
            continue

        if arg[0] == "memmap":
            if len(arg) > 2:
                wrong_argument()
                print("");
                continue
            if len(arg) == 1:
                for list in inode_table:
                    print(list)
            else:
                index = int(arg[1]);
                print(inode_table[index])
            print("");
            continue

        if arg[0] == "saveChanges":
            filename = input(f"Please name saved file, {bcolors.WARNING}you can also overwrite existing file{bcolors.ENDC}, don't forget extension .txt\nEnter {bcolors.OKCYAN}-1{bcolors.ENDC} to go back to CLI\n");
            if filename == "-1":
            	print("");
            	continue
            hardWrite(filename)
            print(f"{bcolors.OKGREEN}{bcolors.OKCYAN}{filename}{bcolors.ENDC} has been updated{bcolors.ENDC}\n")
            continue

        if arg[0] == "chDir":
            if len(arg) != 2:
                wrong_argument()
                print("");
                continue
            global parents_stack
            filename = arg[1];

            if filename == "..":
                if current_inode == 0:
                    print("");
                    continue
                else:
                    current_inode = parents_stack.pop(-1)
                    print(f"{bcolors.OKGREEN}Moved to {bcolors.OKCYAN}parent directory{bcolors.ENDC}.{bcolors.ENDC}\n")
                    continue
            parent = int(current_inode)
            
            flag = chDir(filename,current_inode,inode_table)
            if flag == -1:
                print("");
                continue;
            current_inode = flag;
            parents_stack.extend([parent])
            print(f"{bcolors.OKGREEN}Moved to {bcolors.OKCYAN}{filename}{bcolors.ENDC}.{bcolors.ENDC}\n")
            continue
	
        if arg[0] == "currentInode":
            print(f"{bcolors.OKGREEN}{current_inode}{bcolors.ENDC}")
            print("");
            continue

        if arg[0] == "partitionInfo":
            print(f"{bcolors.BOLD}It shows {bcolors.OKCYAN}disk number{bcolors.ENDC} and {bcolors.OKCYAN}start and end address{bcolors.ENDC} for each disk{bcolors.ENDC}")
            for key in part_info:
                print(key + " " + str(part_info[key]))
            print("");
            continue

        if arg[0] == "blockSize":
            print(
                f"{bcolors.BOLD}Block size in {bcolors.OKCYAN}bytes{bcolors.ENDC}, it is assumed that one char takes one Byte, although you can update size of int in settings{bcolors.ENDC}")
            print(f"{bcolors.OKGREEN}{block_size}{bcolors.ENDC}")
            print("");
            continue

        if arg[0] == "logicalSpace":
            print(f"{bcolors.BOLD}Logical space is the total possible number of entries in inode table{bcolors.ENDC}")
            print(
                f"{bcolors.BOLD}It shows total logical space.\n{bcolors.WARNING}Note:{bcolors.ENDC} if logical space is consumed you can not create new files, even though physical might be available{bcolors.ENDC}");
            print("logical_space: " + f"{bcolors.OKGREEN}{str((len(inode_table)))}{bcolors.ENDC}")
            print("");
            continue

        if arg[0] == "physicalSpace":
            print(f"{bcolors.OKGREEN}{str(disk_size)}{bcolors.ENDC}" + " MB")
            print("");
            continue

        if arg[0] == "freeBlocks":
            freeBlocks()
            print("");
            continue

        if arg[0] == "blocksConsumed":
            if len(arg) != 2:
                wrong_argument()
                print("");
                continue
            filename = arg[1];
            try:
                b = blocksConsumedByFile(filename)
                if b[0] == -1:
                    print(f"{bcolors.BOLD}File doesn't consume any memory block as no data is present in it{bcolors.ENDC}")
                else:
                    print(f"{bcolors.OKGREEN}{b}{bcolors.ENDC}")
            except:
                print(f"{bcolors.BOLD}File is not present{bcolors.ENDC}")
            print("");
            continue

        if arg[0] == "masterBlock":
            showMasterBlock()
            print("");
            continue

        else:
            wrong_command()
            print("");

        print()


