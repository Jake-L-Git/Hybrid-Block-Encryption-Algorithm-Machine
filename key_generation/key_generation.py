import hashlib
import random


# Each step of this process is demonstrated in the output
# I utilized a nested list structure to demonstrate clearly 
# the segments that are created which can help to visualize it


########################################
############ KEY GENERATION ############
########################################


# hash_generation takes a key as input - it then uses the secure hash algorithm to 
# convert this key into a 256 bit block
def hash_generation(key):
    content = key
    hash_object = hashlib.sha256(content.encode())  
    binary_hash = hash_object.hexdigest()
    input_block_256 = bin(int(binary_hash, 16))[2:].zfill(256)
    return input_block_256

# hash_segmentation takes the 256 bit input block (generated from our key)
# and breaks it up into 8 32 bit segments
def hash_segmentation(input_block_256):
    segments =[]
    for i in range(0,256,32):
        segments += [input_block_256[i:i+32]]
    return segments

# generate_IP_tables generates a series of 4 IP Tables for a user
# upon entering their user name, this function also checks the user name
# against a dictionary before creating these IP tables as to allow a 
# user to reuse their unique IP tables

users_list = {}

# generates_IP_tables generates a series of 4 IP Tables for a user (essesntially a random list of numbers 0,63)
def generate_IP_tables(user):
    # if user in list then use their IP tables
    if user in users_list:
        return users_list[user]
    numbers = list(range(64))
    randomized_lists = [random.sample(numbers, len(numbers)) for _ in range(4)]
    #add user and their tables to the list
    users_list[user] = randomized_lists

    return randomized_lists

#this function can create inverse IP tables
def find_inverse_ip(ip_table):
    
    inverse_ip = [0] * len(ip_table)
    for i, value in enumerate(ip_table):
        inverse_ip[value] = i
    
    return inverse_ip

#this uses the above function to make 4 inverse IP tables
def inv_IP_table(IP_tabs):
    inv_IPs = []
    for i in IP_tabs:
        inv_IPs += [find_inverse_ip(i)]
    return inv_IPs


# permutations takes in the 32 bit segments we have created, and now concatinates
# segments (1, 3), (2, 4), (5, 7) and (6, 8) into 4 64 bit segments
# these segments are then each run through a different permutation table (which we generated)
# as to "scramble" the bits, essentially, it iterates through the permutation table and segment parallaly, 
#it looks at the permutation table number, which represents a position, and then puts the number from 
#the segment into that position in a list, this scrambled segment is then broken back up into 8 32 bits 
#segments and outputed

def permutations(segments):

    #creating the 4 64 bit segments
    permu_pairs = [(0,2), (1,3), (4,6), (5,7)]
    joint_segs = []
    permuted_segments = []
    new_segs = []
    IP_tables = generate_IP_tables(user)


    for i, j in permu_pairs:
        x = segments[i] + segments[j]
        joint_segs += [x]

    #using the permutation tables to scramble the segments
    for seg, perm_table in zip(joint_segs, IP_tables):
        permuted_segment = ''.join(seg[i] for i in perm_table)
        permuted_segments.append(permuted_segment)
    
    # break these newly scrambled 4 64 bit segments into 8 32 bit segments and output these segments
    perm_seg_str = ''.join(permuted_segments)
    for i in range(0,8):
        new_segs += [perm_seg_str[i:i+32]]

    return new_segs




############################################
############ MESSAGE PROCESSING ############
############################################


# message processing steps will be very similar to that of key generation
# however, as the text input can be varying sizes, these are slight varirations
# in the functions themselves, and additionally by having seperate functions
# it better illustrates the seperate steps of encryption

# we now take in any text as an input and convert this text
# into segmented block of 256 bits each, we utilize list structures again
# to demonstrate the segmentations
def split_input_text_into_256_bit_blocks(large_string: str):
    
    binary_message = ''.join(format(ord(char), '08b') for char in large_string)

    block_size = 256
    blocks = [binary_message[i:i + block_size] for i in range(0, len(binary_message), block_size)]
    
    if len(blocks[-1]) < block_size:
        blocks[-1] = blocks[-1].ljust(block_size, '0') 
    
    
    return blocks


# hash_segmentation_input then takes these segments 256 bit blocks (generated from our input)
# and breaks each indiviudal block into 8 32 bit segments
def hash_segmentation_input(blocks):
    segments =[]
    for i in range(0, len(blocks)):
        segment_chunk = []
        for j in range(0,256,32):
            segment_chunk += [blocks[i][j:j+32]]
        segments += [segment_chunk]

    return segments


# permutation_input takes in the new 32 bit segments segments (may be multiple segments) 
# each containing 8 32 bits segments and now concatinates these as
# segments (1, 3), (2, 4), (5, 7) and (6, 8) into 4 64 bit segments (there will be multiple)
# segments of 4 64 bit segments. for each larger segment, the 4 64 bit segments
# are then each run through a different permutation tables (same ones as from key_generation)
# as to "scramble" the bits into rnadomized positons found, in the IP tables
# and then broken back up into 8 32 bits segments and outputed
def permutation_input(segments, inv = None):

    # create 32 bit segments
    joint_segs = []
    permu_pairs = [(0,2), (1,3), (4,6), (5,7)]
    permuted_segments_final = []
    IP_tables = generate_IP_tables(user)
    if inv == 'yes':
        IP_tables = inv_IP_table(IP_tables)

    for x in range(len(segments)):
        joint_segs_block = []
        for i, j in permu_pairs:
            y = segments[x][i] + segments[x][j]
            joint_segs_block += [y]
        joint_segs += [joint_segs_block]
        
    # create scramble segments via permutation tables and output
    for i in range(len(joint_segs)):
        permuted_segments = []
        for seg, perm_table in zip(joint_segs[i], IP_tables):
            permuted_segment = ''.join(seg[i] for i in perm_table)
            permuted_segments += [permuted_segment]
        permuted_segments_final += [permuted_segments]
    
    permutated_segments_final_strings = []
    for i in range(len(permuted_segments_final)):
        perm_seg_str = ''.join(permuted_segments_final[i])
        permutated_segments_final_strings += [perm_seg_str]

    final_segments = []

    for i in range(0, len(permutated_segments_final_strings)):
        segment_chunk = []
        for j in range(0,256,32):
            segment_chunk += [permutated_segments_final_strings[i][j:j+32]]
        final_segments += [segment_chunk]

    return final_segments




#####################################
############ ENCRYPTION #############
#####################################


# Takes all the 32 bit segments inputed and expands each to 48 bits using
# an expansion table, the output will be 8 48 bits segments
def key_expansion(segs):
    #from https://github.com/anishLearnsToCode/DES/blob/master/notebook/data-encryption-standard-des.ipynb
    expansion_array = [32, 1, 2, 3, 4, 5,
                4, 5, 6, 7, 8, 9,
                8, 9, 10, 11, 12, 13,
                12, 13, 14, 15, 16, 17,
                16, 17, 18, 19, 20, 21,
                20, 21, 22, 23, 24, 25,
                24, 25, 26, 27, 28, 29,
                28, 29, 30, 31, 32, 1]
    
    expanded_segments = []

    for i in range(len(segs)):
        x = [0] * 48
        for j in range(len(expansion_array)):
            x[j] = segs[i][expansion_array[j] - 1]
        joined_lst = ''.join(x)
        expanded_segments += [joined_lst]
    return expanded_segments


# Takes all the 32 bit segments inputed and expands each to 48 bits using
# an expansion table, the output will be segments of 8 48 bits segments
# same as key expansion, but just accounting for several segments of 8 32 bit segments
def expansion(key_segs):
    #from https://github.com/anishLearnsToCode/DES/blob/master/notebook/data-encryption-standard-des.ipynb
    expansion_array = [32, 1, 2, 3, 4, 5,
                4, 5, 6, 7, 8, 9,
                8, 9, 10, 11, 12, 13,
                12, 13, 14, 15, 16, 17,
                16, 17, 18, 19, 20, 21,
                20, 21, 22, 23, 24, 25,
                24, 25, 26, 27, 28, 29,
                28, 29, 30, 31, 32, 1]
    
    exp_key_segs = []

    for h in key_segs:
        expanded_segment = []
        for i in range(len(h)):
            x = [0] * 48
            for j in range(len(expansion_array)):
                x[j] = h[i][expansion_array[j] - 1]
            joined_lst = ''.join(x)
            expanded_segment += [joined_lst]
        exp_key_segs += [expanded_segment]
    return exp_key_segs





# this is a help function that performs the xor operation on 2 binary string inputs
def xor_op(x, y):
    xor_bits = ''.join(['1' if x[i] != y[i] else '0' for i in range(len(x))]) 
    return xor_bits


# this function takes all of the 256 bit chunks of the input segments
# and xors them with the key segment
def xor_segments(key_segs, text_segs):
    xor_segments = []
    for seg in text_segs:
        xor_ind_segs = []
        for j in range(8):
            x = xor_op(seg[j], key_segs[j])
            xor_ind_segs += [x]
        xor_segments += [xor_ind_segs]
    return xor_segments


# now that the segments have been XORed with the key segment
# each 48 bit segments ends up going through S-boxes, and has 6 bit chunks
# go through each of the 8 s-boxes, so this function simply takes each 
# 48 bit segments and breaks it up further into 6 bit segments
# at this point our nested lists get complex but we can still see the
# structure in our output code

def fortyeight_to_six_segs(forty_eight_segs):
    six_bit_segs = []
    for i in forty_eight_segs:
        segments_seg = []
        for j in i:
            segments_ind = []
            for k in range(0, 48, 6):
                segments_ind += [j[k:k+6]]
            segments_seg += [segments_ind]
        six_bit_segs += [segments_seg]
    return six_bit_segs

# Here we have pre created our S-Boxes as used in 
#from https://github.com/anishLearnsToCode/DES/blob/master/notebook/data-encryption-standard-des.ipynb
# These s-boxes will be used on these 48 bits segments, and will be explained via
# the following functions and do not change between users

sbox1 = [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]]
    
sbox2 = [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]]

sbox3 = [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]]

sbox4 = [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]]

sbox5 = [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]]

sbox6 = [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]]

sbox7 = [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]]

sbox8 = [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]

# this is a helper function that takes in 6 bit segments and outputs
# what coordinate of the s-box it is associated with 
# middle 4 bits are the column and the first and last bits create the row
def s_box_coordinate(bin):
    """"Takes a 6-bit binary string as input and returns a 4-bit binary string as output"""
    return bin[0] + bin[5], bin[1: 5]

# this is a helper function that takes in the S-box to search
# as well as the coordinates and locates the number in the s-box
def s_box_search(s_box, row, col):
    row_coord = int(row, 2)
    col_coord = int(col, 2)
    return s_box[row_coord][col_coord]


# this function's purpose is essentially to take in 6bit segments and output them
# as 4 bit segments, however it uses s-boxes to do so and in the process is 
# scrambling the 6 bit segments. It essentially is using the 6 bit segments to 
# create coordinates that choose a number from a 4x16 box which is converted
#  to a 4 bit string, it then combines these 4 bits strings to have 8 32 bit segments again
def s_box_func(xor_segments):

    sbox_list = [sbox1, sbox2, sbox3, sbox4, sbox5, sbox6, sbox7, sbox8]
    z = 0

    final_sbox_segments = []
    num_bits = 4  # Ensure it has 4 bits

    for i in xor_segments:
        s_box_segment = []
        for j in i:
            s_box_num = 0
            s_box_str = ''
            for k in j:
                coords = s_box_coordinate(k)
                s_box_val = s_box_search(sbox_list[s_box_num], coords[0], coords[1])
                s_box_val_bin = format(s_box_val, f'0{num_bits}b')
                s_box_str += str(s_box_val_bin)
                s_box_num += 1
            s_box_segment += [s_box_str]
        final_sbox_segments += [s_box_segment]
    return final_sbox_segments
                

# finally, all of the segments with 8 32 bit segments are combined to create
# our final encrypted message
def encrypted_message(final_sbox_segments):
    encrypted_message_final = ''
    for i in range(len(final_sbox_segments)):
        encrypted_piece = ''.join(final_sbox_segments[i])
        encrypted_message_final += encrypted_piece
    return encrypted_message_final   




#####################################
############ DECRYPTION #############
#####################################


# first we need to create a function to invert our s-boxes, as the first step will be inserting our
# cypher text back through these s-boxes
def invert_s_box(s_box):
        inverse_s_box = [[0] * len(s_box[0]) for _ in range(len(s_box))]

        # Iterate through each row and column of the S-box
        for row_index in range(len(s_box)):
            for col_index in range(len(s_box[row_index])):
                # The value in the S-box tells us the column of the inverse S-box
                value = s_box[row_index][col_index]
                inverse_s_box[row_index][value] = col_index
        
        return inverse_s_box

sbox1_invt = invert_s_box(sbox1)
sbox2_invt = invert_s_box(sbox2)
sbox3_invt = invert_s_box(sbox3)
sbox4_invt = invert_s_box(sbox4)
sbox5_invt = invert_s_box(sbox5)
sbox6_invt = invert_s_box(sbox6)
sbox7_invt = invert_s_box(sbox7)
sbox8_invt = invert_s_box(sbox8)

#storing our inverted s_boxes in a list for easy access
inverse_sboxes = [sbox1_invt, sbox2_invt, sbox3_invt,sbox4_invt,sbox5_invt,sbox6_invt,sbox7_invt,sbox8_invt]

#now, we insert our cypher text back through the inverse s-boxes, this is supposed to undo the shuffling
# caused by them and transofrm each 4bit segment to a 6bit segment
# essentially, we are using the previous output of the sbox to locate the previous coordinates
# however, since multiple coordinates coorispond to the same value in our original sbox
# there are multiple possibilities that this function can output.
# it would be impossible to figure out which one is correct, so for simplicity i have chosen a random one
# HOWEVER THIS IS MEANS THAT THE DECRYPTION WILL NOT WORK
#This is a flaw with this encryption model we used from the document, and therefore is not able to be decrypted
# by running the cypher text back through the algorithm
def inverse_sbox_segment(sbox, sbox_output):
    bin_to_dec = int(sbox_output, 2)
    for row in range(4):
        for col in range(16):
            if sbox[row][col] == bin_to_dec:
                row_bin = f'{row:02b}'
                col_bin = f'{col:04b}'
                input_value = row_bin[0] + col_bin + row_bin[1]
                return input_value  

#here we run each 4 bit segment through our inverse sboxes utilixing the above function
def four_bit_segments_through_sboxes(segments):
    six_bit_segs = []
    for seg in segments:
        segs_lists = []
        for piece in seg:
            split_segment = [piece[i:i+4] for i in range(0, len(piece), 4)]
            sbox_num = 0
            sbox_list = []
            for split in split_segment:
                sbox = inverse_sboxes[sbox_num]
                x = inverse_sbox_segment(sbox, split)
                sbox_list += [x]
            segs_lists += [sbox_list]
        six_bit_segs += [segs_lists]
    return six_bit_segs

# here, we simply combine out 6 bit segments into 48 bit segments
def six_bit_segs_to_fourty_eight(segments):
    for i in range(len(segments)):
        for j in range(len(segments[i])):
            six_bit = ''.join(segments[i][j])
            segments[i][j] = six_bit
    return segments

#here, we use an inverse expansion table to tranform out 48 bit segments back into their
#32 bit segments. This simply works by mapping them back to their original positions
def inverse_expansion(expanded_list):
    inverse_expansion_table = [1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14, 
    17, 18, 19, 20, 21, 22, 25, 26, 27, 28, 29, 30,
    0, 7, 8, 15, 16, 23, 24, 31]

    inv_exp_seg = []
    for i in expanded_list:
        result = []
        for expanded_data in i:
            original_data = ['0'] * len(inverse_expansion_table)
            for i, original_pos in enumerate(inverse_expansion_table):
                original_data[original_pos] = expanded_data[i]
            result += [''.join(original_data)]
        inv_exp_seg += [result]
    return inv_exp_seg




##########################################
############ EXTRA FUNCTIONS #############
##########################################

# this is a helper function that takes in a binary string and converts
# it to ascii
def bin_to_text(binary_str):
    
    ascii_text = ""
    
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i+8]  
        ascii_char = chr(int(byte, 2)) 
        ascii_text += ascii_char
    return ascii_text


###############################
############ MAIN #############
###############################

quit_option = "c"
#continues to run until a user quits the program
while quit_option != "q":

    #taking input
    user = input("user: ")
    key = input("key (use your email): ")
    text_input = input("text to encrypt: ")

    #key generation
    hash_gen = hash_generation(key)
    print('\nHashed Key: ', hash_gen)
    hash_seg = hash_segmentation(hash_gen)
    print('\nSegmented Hash Key: ',hash_seg)
    perm = permutations(hash_seg)
    print('\nPermutated Hash Key: ',perm)


    #message processing
    split_256 = split_input_text_into_256_bit_blocks(text_input)
    print('\nInput Text 256 bit blocks: ',perm)
    hash_seg_inp = hash_segmentation_input(split_256)
    print('\nInput Text 256 bit segmented blocks: ',perm)
    perm_inp = permutation_input(hash_seg_inp)
    print('\n Permutated Input Text blocks: ',perm)
    

    #xoring 48 bit segments and segmenting them to 6 bit segments
    key_exp = key_expansion(perm)
    print('\nExpanded Key Segments: ',key_exp)
    expan = expansion(perm_inp)
    print('\nExpanded Input Segments: ',expan)
    xor_segs = xor_segments(key_exp, expan)
    print('\n XORed Key and Text Segments: ',xor_segs)
    forty_eight_to_six = fortyeight_to_six_segs(xor_segs)
    print('\n XORed Segments, 6 bit Segments: ',forty_eight_to_six)

    # running the 6 bit segments through s-boxes
    s_box_complete = s_box_func(forty_eight_to_six)
    print('\nAfter running through S-Boxes: ',s_box_complete)

    # formatting the final encrypted message
    final_encryption = encrypted_message(s_box_complete)
    cipher_text = bin_to_text(final_encryption)
    print('\nEncrypted text: ', cipher_text)

    #running the cipher text back through the inverse sboxes (4 bit segments to 6 bit segments)
    four_bits_through_sboxes = four_bit_segments_through_sboxes(s_box_complete)
    print('\nCreate Four Bit Segments then Run back through Inverse S-Boxes: ', four_bits_through_sboxes)

    #merging the six bit segments into 48 bit segments
    six_fourty_eight = six_bit_segs_to_fourty_eight(four_bits_through_sboxes)
    print('\nSix_to_Fourty_Eight: ', six_fourty_eight)

    #XORing these segments back with the key to get the original segments
    xor_segs = xor_segments(key_exp, six_fourty_eight)
    print('\nXORed Key and Decryption Segments: ',xor_segs)

    #Inverse expanding the segments (shrink them) by putting bits back to their original spots
    inv_exp = inverse_expansion(xor_segs)
    print('\nInverse Expanded Segments: ',inv_exp)

    #Running these segments through the IP^-1 tables (inverse permutation tables) to undo the scrambling
    inv_perm = permutation_input(inv_exp, 'yes')
    print('\n Permutated Input Text blocks: ', inv_perm)

    #formatting and printing the final decrypted message
    #again this will be wrong because of our issue with the s boxes
    final_decryption = encrypted_message(inv_perm)
    plain_text = bin_to_text(final_decryption)
    print('\nDecrypted text: ', plain_text)

    #option for user to quit or continue program
    quit_option = input("press q to quit function: ")















