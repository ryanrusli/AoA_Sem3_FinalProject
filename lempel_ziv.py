import timeit, os   

def lzw_compress(filename):
    start=timeit.default_timer()

    global dictionary1, indices

    dictionary1 = list(asciilist)
    word = ''
    text = "" 
    compressedf = open('lzw_compressed.txt', 'wb')

    indices = []

    for c in filename:
        if (word + c) in dictionary1:
            word = word + c
        else:
            if word != "":
                text += str(dictionary1.index(word)) + ' '
                indices.append(dictionary1.index(word))
                dictionary1.append(word + c)
                word = c

    text += str(dictionary1.index(word)) + ' '
    encText = get_encoded_text(text, dictionary1)
    padEncText = pad_encoded_text(encText)
    byteArr = get_byte_array(padEncText)
    compressedf.write(byteArr)
    indices.append(dictionary1.index(word))

    end = timeit.default_timer()
    # Print out the duration for lzw compression
    print('{} compressed in {} seconds'.format(filename, end-start))

def lzw_decompress(filename):
    
    data = open(filename, 'rb')
    start = timeit.default_timer()
    global dictionary2 , indices
    dictionary2 = list(asciilist)
    
    bit_string = ""
    byte = data.read(1)

    while(byte != b""):

        byte = ord(byte)
        bits = bin(byte)[2:].rjust(8, '0')

        bit_string += bits
        byte = data.read(1)
    data = decode_text(bit_string, dictionary2)
    indices = data.split(' ') 

    indices.pop()
    indices.pop(0)
    indices.pop()
    print(indices[-1])
    y = int(indices[0])
    element = str(dictionary2[y]) 
    decompressedf = open('LZWDecompressed' + 'some_text.txt', 'w+')
    decompressedf.write(element)
    word = element

    for i in range(1, len(indices)):
        y = int(indices[i])
        if y not in range(len(dictionary2)):
            element = word + element[0]
        else:
            element = dictionary2[y]
        decompressedf.write(str(element))
        dictionary2.append(word + element[0])
        word = element
    end = timeit.default_timer()
    print("{} compressed in {} seconds".format(filename, end-start))
    #print("It took", end - start, "second(s) to compress.")


def get_encoded_text(text, code_book):
    encoded_text = ""
    for character in text.split(" "):
        if (character == ""):
            continue
        else:
            encoded_text += '{0:016b}'.format(int(character))
    return encoded_text


def pad_encoded_text(encoded_text):
    extra_padding = 16 - len(encoded_text) % 16  
    for i in range(extra_padding):
        encoded_text += "0"
            
        
    padded_info = "{0:016b}".format(extra_padding)
    encoded_text = padded_info + encoded_text
    return encoded_text

def get_byte_array(padded_encoded_text):
    if(len(padded_encoded_text) % 16 != 0):
        print("Encoded text not padded properly")
        exit(0)
    b = bytearray()
    for i in range(0, len(padded_encoded_text), 8):
        byte = padded_encoded_text[i:i+8]
        b.append(int(byte, 2))
    return b

def remove_padding(padded_encoded_text):
    padded_info = padded_encoded_text[:8]
    extra_padding = int(padded_info, 2)

    padded_encoded_text = padded_encoded_text[8:] 
    encoded_text = padded_encoded_text[:-1*extra_padding]

    return encoded_text

def decode_text(encoded_text, dictionary1):
    decoded_text = ""

    for i in range(0, len(encoded_text),16):
        byte = encoded_text[i:i+16]
        decoded_text += str(int(byte, 2)) + " " 
        
    return decoded_text

asciilist = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', ' ', '\t', '\n', '\r', '\x0b', '\x0c']


