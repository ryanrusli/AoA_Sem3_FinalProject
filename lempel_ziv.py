import timeit

def LzwCompression(data):
    start=timeit.default_timer()
    global dictionary1, indices
    dictionary1 = list(asciilist)
    word = ''
    text = "" 
    compressedf = open('LZWCompressedtest_cities.txt', 'wb')
    indices = []
    for c in data:
        if (word + c) in dictionary1:
            word = word + c
        else:
            if word!= "":
                # print(dictionary1.index(word))
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
    print("It took",end-start,"second(s) to compress.")

def LzwDecompression(filename):
    
    data = open(filename, 'rb')
    start = timeit.default_timer()
    global dictionary2 , indices
    dictionary2 = list(asciilist)
    
    bit_string = ""
    byte = data.read(1)
    while(byte != b""):
#        print(byte)
        byte = ord(byte)
        bits = bin(byte)[2:].rjust(8, '0')
#        print(bin(byte))
        bit_string += bits
        byte = data.read(1)
#    print(bit_string)
#    depaddedData = remove_padding(bit_string)
#    print(depaddedData)
#    print(bit_string)
    data = decode_text(bit_string, dictionary2)
    
#    data.close()
#    print(data)
    indices = data.split(' ')
#    print(indices[-2])
    
    indices.pop()
    indices.pop(0)
    indices.pop()
    print(indices[-1])
    y = int(indices[0])
    element = str(dictionary2[y]) 
    decompressedf = open('LZWDecompressedtest_cities.txt', 'w+')
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
    print("It took", end - start, "second(s) to compress.")


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
        
#    print(decoded_text)
    return decoded_text

asciilist = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', ' ', '\t', '\n', '\r', '\x0b', '\x0c']

filename =input("    Please Enter The Filename : ")
filename = filename + '.txt'

print("		1-Compression		2-Decompression")
choose = int(input("    Please Choose an Action : "))
if (choose == 1):
    f = open(filename, 'r')
    source = f.read()
    LzwCompression(source)
    dict1 = open('Compression_Dictionary.txt', 'w+')
    dict1.write("Sequence of indices which represent the compressed result : " + str(indices) + "\r\n")
    dict1.write("Created dictionary for compression : " + str(dictionary1) + "\r\n")
    dict1.close()
elif(choose == 2):
    
#    print(source)
    LzwDecompression(filename)
    dict2 = open('Decompression_Dictionary.txt', 'w+')
    dict2.write("Sequence of indices which represent the decompressed result : " + str(indices) + "\r\n")
    dict2.write("Created dictionary for decompression : " + str(dictionary2) + "\r\n")
    dict2.close()
f.close()

