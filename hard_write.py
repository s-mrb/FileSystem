
from settings import  *
from mount import inode_table,addr_space,part_info,free_blocks,data

def hardWrite(fname):
    inode_string_table = ""

    for i in range(len(inode_table)):
        inode_table[i][-1] = '_'.join(str(x) for x in inode_table[i][-1]);
        inode_string_table = inode_string_table + ' '.join(str(x) for x in inode_table[i]) + "\n"
    with open(fname, 'w+') as f:
        f.write(str(addr_space) + "\n")
        f.write(str(part_info) + "\n");
        blocks4free_blocks = math.ceil(len(free_blocks) / ints_per_block)
        for i in range(blocks4free_blocks):
            if i == blocks4free_blocks:
                f.write(' '.join(str(x) for x in free_blocks[i * ints_per_block:-1]) + "\n")
            else:
                f.write(' '.join(str(x) for x in free_blocks[i * ints_per_block:(i + 1) * ints_per_block]) + "\n")
        f.write(inode_string_table + '\n'.join(str(x) for x in data))




