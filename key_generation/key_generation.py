import hashlib

def hash_generation(key):
    #do we need specific input key???
    content = key
    hash_object = hashlib.sha256(content.encode())  
    binary_hash = hash_object.hexdigest()
    input_block_256 = bin(int(binary_hash, 16))[2:].zfill(256)
    return input_block_256

def hash_segmentation(input_block_256):
    segments =[]
    for i in range(0,8):
        segments += [input_block_256[i:i+32]]
    return segments

def permutations(segments):
    permu_pairs = [(0,2), (1,3), (4,6), (5,7)]
    joint_segs = []
    permuted_segments = []
    new_segs = []

    for i, j in permu_pairs:
        x = segments[i] + segments[j]
        joint_segs += [x]

    
    IP_tables = [
        [46, 29, 4, 38, 58, 10, 53, 52, 43, 22, 47, 63, 56, 60, 35, 15, 27, 23, 5, 
        7, 45, 12, 50, 13, 59, 24, 31, 40, 26, 1, 11, 14, 30, 9, 19, 41, 34, 37, 54, 
        61, 18, 3, 62, 55, 51, 17, 20, 2, 21, 44, 48, 6, 42, 16, 49, 57, 39, 0, 32, 25, 8, 33, 36, 28],

        [51, 44, 27, 12, 47, 58, 29, 39, 1, 46, 26, 62, 36, 33, 25, 60, 57, 38, 
        50, 53, 16, 28, 20, 4, 10, 0, 11, 32, 37, 6, 55, 34, 3, 59, 17, 7, 9, 45, 
        43, 35, 63, 41, 31, 52, 56, 19, 48, 14, 8, 15, 42, 54, 18, 5, 49, 23, 21, 24, 61, 2, 13, 30, 22, 40],

        [26, 23, 7, 50, 34, 17, 53, 47, 4, 55, 29, 12, 42, 22, 58, 1, 28, 40, 36, 45, 
        43, 52, 33, 9, 63, 8, 57, 24, 5, 59, 56, 30, 16, 60, 21, 44, 18, 49, 54, 32, 2, 
        38, 41, 37, 6, 0, 13, 27, 11, 15, 39, 25, 46, 48, 14, 3, 51, 31, 35, 62, 10, 19, 61, 20],

        [40, 36, 4, 6, 16, 3, 28, 30, 23, 49, 51, 5, 34, 2, 63, 61, 43, 27, 13, 47, 24, 
        19, 60, 41, 10, 14, 46, 62, 17, 50, 58, 21, 54, 8, 26, 44, 7, 32, 9, 37, 31, 35, 
        22, 38, 53, 48, 39, 45, 18, 52, 33, 20, 59, 56, 11, 42, 55, 1, 15, 57, 0, 12, 25, 29]


        ]

    for seg, perm_table in zip(joint_segs, IP_tables):
        # Apply the permutation: reorder the bits according to the perm_table
        permuted_segment = ''.join(seg[i] for i in perm_table)
        permuted_segments.append(permuted_segment)
    
    perm_seg_str = ''.join(permuted_segments)
    for i in range(0,8):
        new_segs += [perm_seg_str[i:i+32]]

        
    return new_segs



############## (now starting message proccessing)
# so far have it splitting up input message into 256 bit blocks
# next step is to then break the individual blocks into 32 bit blocks
# merge with specified blocks to be 4 64 bit blocks
# then run these through permutation tables
# lastly break back into 32 bit blocks
# after this I can run encryption


def split_into_256_bit_blocks(large_string: str):
    # Step 1: Convert the string into its binary representation
    binary_message = ''.join(format(ord(char), '08b') for char in large_string)
    
    # Step 2: Split the binary message into 256-bit blocks (32 bytes = 256 bits)
    block_size = 256
    blocks = [binary_message[i:i + block_size] for i in range(0, len(binary_message), block_size)]
    
    if len(blocks[-1]) < block_size:
        blocks[-1] = blocks[-1].ljust(block_size, '0') 

    return blocks



x = split_into_256_bit_blocks('This is a large string that we want to split into 256-bit blocks.')
print(x)

test1 = hash_generation("1234")
test1cont = hash_segmentation(test1)
test2 = permutations(test1cont)
print('')
print(test2)
print('')