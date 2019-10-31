import collections
import operator

import time

import os
import json
import ast
import numpy as np

class ShannonFano:

    def __init__(self, path):
        
        self.path = path
        self.code_book = {}
        self.reverse_mapping = {}

    def create_list(self, text):
        listt = dict(collections.Counter(text))
        list_sorted = sorted(listt.items(), key=operator.itemgetter(1), reverse=True)

        # format the final list as [letters, frequancy, code]
        final_list = []

        for key, value in list_sorted:
            final_list.append([key, value, ''])

        return final_list



    def divide_list(self, listt):
        all_m = []
        left = 0
        right = 0
        for i in range(0, len(listt)):
            for j in range(i + 1, len(listt)):
                right += listt[j][1]

            for l in range(i, -1, -1):
                left += listt[l][1]

            between = abs(right - left)

            all_m.append(between)

            left = 0
            right = 0

        # find min minus
        min = [all_m[0], 0]
        for z in range(1, len(all_m)):
            if all_m[z] < min[0]:
                min = [all_m[z], z]

        # cutting
        index_of_min = min[1]

        return listt[0:index_of_min + 1], listt[index_of_min + 1:]


    def shannon_fano_structure(self, list):
        l1, l2 = self.divide_list(list)
        for i in l1:
            i[2] += '0'
            self.code_book[i[0]] = i[2]

        for i in l2:
            i[2] += '1'
            self.code_book[i[0]] = i[2]

        if len(l1) > 1:
            self.shannon_fano_structure(l1)
        if len(l2) > 1:
            self.shannon_fano_structure(l2)
        
        return self.code_book
    
    def encodeText(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.code_book[character]
        return encoded_text


    def padText(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8  
        for i in range(extra_padding):
            encoded_text += "0"
            
        
        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def createByteArray(self, padded_encoded_text):
        if(len(padded_encoded_text) % 8 != 0):
            print("Encoded text not padded properly")
            exit(0)
        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2))
        return b


    def compression(self):
        
        filename, file_extension = os.path.splitext(self.path)  
        output_path = filename + "_ShannonFanoCompressed" + ".txt"
        dictFile_path = filename + "_ShannonFanoDictionary" + ".txt"     
        
        with open(self.path, 'r') as file, open(output_path, 'wb') as output, open(dictFile_path, 'wb') as dictFile:
            
            text = file.read()
            text = text.rstrip()
            
            compList = self.create_list(text)
            self.shannon_fano_structure(compList)
            self.reverse_mapping =  {value:key for key, value in self.code_book.items()}
            encoded_text = self.encodeText(text)
            padded_text = self.padText(encoded_text)
           
            b = self.createByteArray(padded_text)  
            stringDict = json.dumps(self.reverse_mapping)
#            print(stringDict)
            
            encoded_dictText = ""
            for character in stringDict:
                if (character == ""):
                    continue
                else:
                    encoded_dictText += "{0:08b}".format(ord((character)))
                    
            padded_encoded_dictText = self.padText(encoded_dictText)
            dictFile.write(bytes(padded_encoded_dictText, 'utf-8'))
            output.write(bytes(b))

        print("{} has been compressed into {}".format(self.path, output_path))
    
    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:] 
        encoded_text = padded_encoded_text[:-1*extra_padding]

        return encoded_text


    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""
        for bit in encoded_text:
            current_code += bit
            if(current_code in self.reverse_mapping):
                character = self.reverse_mapping[current_code]
                decoded_text += chr(ord((character)))
                current_code = ""
        return decoded_text
    
    def decompression(self, dict_input): 
        filename, file_extension = os.path.splitext(self.path)  
        output_path = "_ShannonFanoDecompressed" + ".txt"
        dictFile_path = dict_input    

        with open(self.path, 'rb') as compressedFile, open(output_path, 'w+') as output, open(dictFile_path, 'rb') as dictionary:
            
            bit_string = ""
            byte = compressedFile.read(1)

            while(byte != b""):

                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')  
                bit_string += bits
                byte = compressedFile.read(1)
            
            byte = dictionary.read(8)
            codeBook = ""            
                
            while (byte != b""):
                
                byte = int(byte, 2)
                bits = bin(byte)[2:].rjust(8, '0')  

                if (byte != 0):
                    codeBook += chr(byte)
                
                byte = dictionary.read(8)
            
            self.reverse_mapping = eval(codeBook[1:])
            encoded_text = self.remove_padding(bit_string)
            decompressed_text = self.decode_text(encoded_text)
            output.write(decompressed_text.replace("\r\n", "\n"))
        print('{} has been decompressed using {}.'.format(self.path, dict_input))
        return output_path  
        
#comp = Shannon_fano_structure("C:\\Users\\Ryan\\.spyder-py3\\Robinhood.txt")

#start = time.time()
#comp.compression()
#print(time.time() - start)

#comp2 = Shannon_fano_structure("C:\\Users\\Ryan\\.spyder-py3\\Robinhood_ShannonFanoCompressed.txt")

#start = time.time()
#comp2.decompression()
#print(time.time() - start)


