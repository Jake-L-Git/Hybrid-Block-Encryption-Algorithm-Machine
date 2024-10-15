import hashlib

def hash_generation(key):
    #do we need specific input key???
    content = key
    hash_object = hashlib.sha256(content.encode('utf-8'))  
    hex_dig = hash_object.hexdigest()

    return hex_dig

def hash_segmentation(input_block_256):
    segments =[]
    for i in range(0,8):
        segments += [input_block_256[i:i+8]]
    return segments

test1 = hash_generation("1234")
test1cont = hash_segmentation(test1)
print(test1cont)