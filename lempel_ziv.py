import timeit

def LzwCompression(data):
    start=timeit.default_timer()
    global dictionary1, indices
    dictionary1 = list(asciilist)
    word = ''
    compressedf = open('Compressed_File.txt', 'w')
    indices = []
    for c in data:
        if (word + c) in dictionary1:
            word = word + c
        else:
            if word!="":
                compressedf.write(str(dictionary1.index(word)) + ' ')
                indices.append(dictionary1.index(word))
                dictionary1.append(word + c)
                word = c
    compressedf.write(str(dictionary1.index(word)) + ' ')
    indices.append(dictionary1.index(word))
    end = timeit.default_timer()
    print("It took",end-start,"second(s) to compress.")

def LzwDecompression(data):
    start = timeit.default_timer()
    global dictionary2 , indices
    dictionary2 = list(asciilist)
    decompressedf = open('Decompressed_File.txt', 'w+')
    indices = data.split(' ')
    indices.pop()
    y = int(indices[0])
    element = str(dictionary2[y])
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


asciilist = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', ' ', '\t', '\n', '\r', '\x0b', '\x0c']

filename =input("Please Enter The Filename : ")
filename = filename + '.txt'
f = open(filename, 'r')
source = f.read()
print("1-Compression\n 2-Decompression")
choose = int(input("Please Choose an Action : "))

if (choose == 1):
    LzwCompression(source)
    dict1 = open('Compression_Dictionary.txt', 'w+')
    dict1.write("Sequence of indices which represent the compressed result : " + str(indices) + "\r\n")
    dict1.write("Created dictionary for compression : " + str(dictionary1) + "\r\n")
    dict1.close()
elif(choose == 2):
    LzwDecompression(source)
    dict2 = open('Decompression_Dictionary.txt', 'w+')
    dict2.write("Sequence of indices which represent the decompressed result : " + str(indices) + "\r\n")
    dict2.write("Created dictionary for decompression : " + str(dictionary2) + "\r\n")
    dict2.close()
f.close()
