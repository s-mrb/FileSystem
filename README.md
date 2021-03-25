

# ABOUT
This is an attempt to mimic low level memory constraints in dynamically typed python and then addressing some of the issues in the design of simple file system. Not tested!!

# Features
 It makes use of arrays and each `fixed size array is treated as one memory block` of hard disk, each block is of fixed siz,
total number of blocks are to be decided when you initialize this file system. It also tried to address problem of `HARD
LINKS` and `SOFT LINKS` and do a TRANSLATION from logical to physical address. A table of inodes is maintained. and..
`EVERYTHING IS A FILE`
You can MOUNT multiple filesystems, one at a time, and changes to each filesystem can be updated in their respective .txt
file. The `.txt file is used as physical drive`, and start address of that drive contains `MasterBlock`, it contains address
of other major Block Groups including `MBR` and `InodeTable` block. `Each line of text file is treated as block, and there
can only be fixed number of characters in each line to mimic memory constraints`, if you just updated a file and it's size
is decreased then rather then reassigning new blocks to entire file it keeps the blocks which are still pointed by file and
remove only the unused blocks, if file size is increased but there is no contigious block available then it stores new
content of file in blocks not contigious with current blocks, NOT A SINGLE CHAR SPACE IS WASTED in previous block where new data would not fit. When a memory is first time read it is empty but when when some data is written in it but the later the file which points to this data is deleted then this data stays there as `Garbage Data`, this feature is added to simulate real hard disk. 
`REPL is used to mimic CLI`


## Further Layout
> let <br>
> `tin` = number of possible inode entries <br>
> `itb` = inode table block <br>
> `MBk` = Meta Blocks, blocks that store meta information of filesystem other then inode table blocks<br>
> `fbb` = free blocks boundry.<br>
> > `fbb` = ceil((`tin`*`int_size`)/(`MBk` size))
<br>
As with all file systems the initialization of it requires access to the meta data of hard disk. Most critical data for a minimal filesystem is<br>
<ol>
<li>Total Memory of System (M)</li>
<li>Total Partitions (P)</li>
<li>Block Size (B)</li>
</ol>

**Block size for Master Block, MBR and FB is**
>                  `MBk_size`     =     6 * log2(`tin`)  Bytes 
In this emulator, while initialization of filesystem this information is to be provided by the user.<br>
Once initialized the filesystem maintains the following memory structure:
##### 1.Master Block 
This blocks contains starting and ending address of major block groups, i.e MBR, Inode block and data block.
> *log2(`tin`) Bytes*<br>
> Size always smaller then default block size (4096 B)<br>

##### 2.MBR Block  Group
MBR contains the partition information and start and end address for each different disc. MBR could take variable number of blocks depending on the amount of metadata one want to store in filesystem for each partition.
>   d = metadata size for one logical disc<br>
>   n = total discs<br>
>   y = total blocks to spare for MBR<br>
>   y = ceil(d*n/`MBk`)<br>
>   memory usage = y * MBk_size <br>

##### 3.Free Blocks Block Group
Total number of `MBk` required for FBB is variable just like MBR, controlled by global variable which is controlled by the amount of meta-data one is willing to add. In the minimal scenario only meta-data in this block is space separated integer values.
>  maximum possible integer will always be less then `tin` <br>
>  Could be a group/could not be a group, depending on the memory consumption.<br>

##### 4.Inode Block Group
Unlike MBR Block and FBB total number of `MBk` in Inode Block Group is not some programmer choice, they are fixed and depends on the `M`

> Size of one inode entry (ies) = itb size = 128 + 2 * log2(`tin`) Bits<br>
<br>
If memeory is byte addressable then `itb` in memory would look like the illustration given below where each block is 8 Bits of size, beware...this physical memory must not be confused with logical memory block.

```    
¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯

                  0   |¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|
                      |          ft             |
                  8   |¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|   
                      | 2x       ap             |
                 24   |¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|
                      |          hl             |
                 32   |¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|
                      |           ┋             |
                      |¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|
                      |          hl             |
               32+x   |¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|    
                      |          own            |
               40+x   |¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|
                      |          ts_c           |
               48+x   |¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|
                      | 2x        ┋             |
               64+x   |¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|
                      |          ts_c           |
               72+x   |¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|
                      |          ts_a           |
               80+x   |¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|
                      | 2x        ┋             |
               96+x   |¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|
                      |          ts_a           |
               104+x  |¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|
                      |          ts_m           |
               112+x  |¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|
                      | 2x        ┋             |
               128+x  |¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|
                      |          ts_m           |
               136+x  |¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|
                      |           a             |
             144+x+y  ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯


x = bytes taken by hardlink entry
y = bytes taken by address/link
¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
```


`ft`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= file type flag, a binary value. **1** Bit but must hold **entire physical block**.<br>
`ap`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= access permissions, **2 Bytes**.<br>
`hl`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= hardlinks, **log2(`tin`)/8 Bytes**.<br>
`own`&nbsp;&nbsp;&nbsp;= ownership, **1 Byte**.<br>
`ts_x`&nbsp;= ts_c, ts_a, ts_m (time stamp for created, last accessed and modified) each take **4 Bytes**.<br>
`a`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= address/link, **log2(`tin`)/8 Bytes**.<br>


##### 5.Data Block Group
Block size in DBG is **4096 B** by default but it could be adjusted while initializing filesystem. Adjustable DBG size means it single filesystem could be used after little change to interface between storage devices of different physical block sizes for optimization purposes.

### High level overview of address spaces for major blocks

<br>

| block group | first block # | last block # |
| ------ | ------ | ------ |
| MBk | 0 | 0 |
| MBRB |1| y+1 |
| FBBG | y+2 | y+1+`fbb`|
| IBG  | (y+2+`fbb`) |`tin`+(2+`fbb`)|


######
# To Run
python3 ./initialize_fs.py <br>
python3 ./start_fs.py
# Commands
### Not Accessable in REPL CLI
**partition()**

```
It does initialization of filesystem, you tell size of entire physical memory (in MB),
 total disks you want and block size in KB. It later does calculation and generates 
 a schema, a design for hard disk in .txt file (hard disk) and use this as filesystem later on.
```
**mount()**

```
It asks for name of file system you want to mount, given the name it will load that 
text file and does necessary processing for running the filesystem, once mountd then
REPL CLI will be presented and you can interact with file system
```



### Accessable within REPL CLI
```diff
- NOTE : commands be written as it is, name and arguments be space separated,
-        in below table in command column the highlited string are arguments
```

```diff
- NOTE : In CLI mode use just `open filename` to open it and no need to pass 
-        arguments to call commands for operations on opened file
```
<br><br>
| Command | Description |
| ------ | ------ |
| ls | List all files within current directory |
| makeFile `filename` `dir`|Creates new file node. <br> `filename:(str)` name of file you want to create. <br> `dir:(0/1)` *0* if you want to create a file other then a directory/folder else *1*|
|data `index`|Shows data blocks. <br>`index:(int)` block index it can be between -1 and any positive number. |
|open  `fname` `mode`|Opens named file in given mode. Returns an object which is used to manipulate this file <br> `mode:(char)` a/r/w <br> <br> **NOTE: Below are the functions you can run on opened file**.<br><br>- write `loc` <br>  Writes data at given location,location is `int`.This **recursive** function underlines append function in it <br><br> - read `start` `end`<br>Reads data from start index to end index, both be `int`.<br><br>- truncate `size`<br>Truncates size bytes, size is `int`. **recursive** natured<br><br>- close<br>Closes the opened file and free opened file descriptor.|
|delete `filename`|This **recursive** function deletes the named file recursively such that all children of this node are deleted<br>`filename:(str)`|
|move `file1` `file2`|Move file1 into file2. Recursively change pointers to file moved<br>`fil1:(str)` Can be a folder or a non dir file.<br>`file2:(str)` Must be a dir.|
|memmap `index(optional)`|Print all the inode table showing all the addresses used and all the links and pointers to the file, to understand this output you must understand schema of txt file, If index given then only that indexed inode row shown|
|saveChanges|If you want to close file system then don't forgot to update it on txt file. This function lets you to save your updated filesysten|
|chDir `filename`|Switch current directory with the directory specified.<br>`filename:(str)` name of directory to move in.<br>**NOTE**`USE .. as filename to move to parent directory`|
|currentInode|Prints the inode current directory is using.|
|partitionInfo|Prints the partition information of the current filesystem.|
|blockSize|Prints the block size in `KB` current file system is using.|
|logicalSpace|Logical space is the total possible number of entries in inode table. <br>It shows total logical space.<br> **Note:** if logical space is consumed you can not create new files, even though physical might be available|
|physiclSpace|Prints the size in `MB` of you filesystem, not the one free but the commulative|
|freeBlocks|Prints the block ids which are not currently pointed by any file.|
|blocksConsumed `filename`|Prints the id of all blocks currently in use by named file if present in current directory|
|masterBlock|Show `content` of MasterBlock, `not the metadata` of it.<br><br>**Major block groups are** <br> - Master Boot Record (`mbr`) Boot record for File System, not system <br> - Free Blocks (`fb`) Contain unused block # to maintain a heap. <br> - Inode Block (`ib`) Contains Inode Table|


<br>
<br>

##### CLI

<div style="text-align:center">
<img src="./img/1.gif" alt="gif showing sample CLI" width="912" height="548" alin="center">
</div>

<br>
<br>




