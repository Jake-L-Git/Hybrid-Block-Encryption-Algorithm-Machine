import hashlib
import random
from helper_functions import sbox1, sbox2, sbox3, sbox4, sbox5, sbox6, sbox7, sbox8


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

def permutations(segments, user):

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
def permutation_input(segments, user, inv = None):

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





# this function performs the xor operation on 2 binary string inputs
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

















