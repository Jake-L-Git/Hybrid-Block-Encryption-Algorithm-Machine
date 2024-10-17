import hashlib

def hash_generation(key):
    #do we need specific input key???
    content = key
    hash_object = hashlib.sha256(content.encode('utf-8'))  
    input_block_256 = hash_object.hexdigest()
    return input_block_256

def hash_segmentation(input_block_256):
    segments =[]
    for i in range(0,8):
        segments += [input_block_256[i:i+8]]
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
        [11, 8, 0, 2, 6, 1, 15, 12, 10, 9, 4, 7, 3, 14, 5, 13], 
        [1, 11, 15, 14, 8, 5, 2, 10, 13, 7, 4, 3, 0, 12, 6, 9], 
        [10, 12, 9, 2, 0, 5, 3, 13, 14, 1, 7, 11, 15, 8, 4, 6], 
        [12, 8, 0, 14, 9, 13, 10, 1, 5, 6, 2, 11, 4, 15, 7, 3]
        ]

    for seg, perm_table in zip(joint_segs, IP_tables):
        # Apply the permutation: reorder the bits according to the perm_table
        permuted_segment = ''.join(seg[i] for i in perm_table)
        permuted_segments.append(permuted_segment)
    
    perm_seg_str = ''.join(permuted_segments)
    for i in range(0,8):
        new_segs += [perm_seg_str[i:i+8]]

        
    return new_segs

test1 = hash_generation("1234")
test1cont = hash_segmentation(test1)
test2 = permutations(test1cont)
print(test2)