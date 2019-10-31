# -*- coding: utf-8 -*-

import heapq
import time
import os
import ast
import json

class Node:

    def __init__(self, char, frequency):
        
        self.char = char
        self.frequency = frequency
        self.leftChild = None
        self.rightChild = None
    
    def __lt__(self, other):
        return self.frequency < other.frequency

    def __eq__(self, other):
        if (other == None):
            return False
        if(not isinstance(other, Node)):
            return False
        return self.frequency == other.frequency
    
class HuffmanCoding:
    
    def __init__(self):
        
        # self.path = path
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}
    
    def createFrequencyDict(self, text):
        frequencyList = {}
        for character in text:
            if not character in frequencyList:
                frequencyList[character] = 0
            frequencyList[character] += 1
        return frequencyList

    def heapify(self, frequencyList):
        for key in frequencyList:
            node = Node(key, frequencyList[key])
            heapq.heappush(self.heap, node)

    def mergeNodes(self):
        while(len(self.heap) > 1):
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = Node(None, node1.frequency + node2.frequency)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)


    def createCharacterCode(self, root, current_code):
        if(root == None):
            return

        if(root.char != None):
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.createCharacterCode(root.left, current_code + "0")
        self.createCharacterCode(root.right, current_code + "1")


    def createBinaryTree(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.createCharacterCode(root, current_code)


    def encodeText(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text


    def padText(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        
        if (extra_padding !=8):
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
#            print(int(byte, 2))
            b.append(int(byte, 2))
        return b


    def compress(self, file_input):
        filename, file_extension = os.path.splitext(file_input)  
        output_path = filename + "_huffman_compressed.txt"
        dictFile_path = filename + "_huffman_dictionary.txt"
        
        with open(file_input, 'r') as file, open(output_path, 'wb') as output, open(dictFile_path, 'wb') as dictFile:
            text = file.read()
            text = text.rstrip()
            
            frequency = self.createFrequencyDict(text)
            self.heapify(frequency)
            self.mergeNodes()
            self.createBinaryTree()
            encoded_text = self.encodeText(text)
            padded_encoded_text = self.padText(encoded_text)
            
            b = self.createByteArray(padded_encoded_text)
            LITERAL_DICT = json.dumps(self.reverse_mapping)
            encoded_dict = ""
            for i in LITERAL_DICT:
                encoded_dict += str(ord(i)) + " "
            encoded_dictText = ""
            for character in LITERAL_DICT:
                if (character == ""):
                    continue
                else:
                    encoded_dictText += "{0:08b}".format(int(ord((character))))
                    
            padded_encoded_dictText = self.padText(encoded_dictText)
            dictFile.write(bytes(padded_encoded_dictText, 'utf-8'))
            output.write(b)

        print("{} has been compressed to {}. Use {} for decompression".format(file_input, output_path, dictFile_path))
        return output_path   
    
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

    def decompress(self, input_path, dict_path):
        '''Decompression needs the compressed file and the dictionary as input'''
        filename, file_extension = os.path.splitext(input_path)
        output_path = filename + "_decompressed" + ".txt"
        dictionary_path = dict_path

        with open(input_path, 'rb') as compressedFile, open(dictionary_path, 'rb') as dictionary, open(output_path, 'w+') as output:
            
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
                codeBook += chr(byte)
#                print(byte)
                byte = dictionary.read(8)
            
            
            self.reverse_mapping = ast.literal_eval(codeBook)
            encoded_text = self.remove_padding(bit_string)
            decompressed_text = self.decode_text(encoded_text)
            output.write(decompressed_text.replace("\r\n", "\n"))
        
        print("{} has been decompressed into {}.".format(input_path, output_path))
        
        return output_path     






