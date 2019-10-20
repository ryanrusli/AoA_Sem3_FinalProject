import collections
import operator

class Shannon_fano_structure:

    code_book = {}


    def create_list(self, text):
        list = dict(collections.Counter(text))
        list_sorted = sorted(list.items(), key=operator.itemgetter(1), reverse=True)

        # format the final list as [letters, frquancy, code]
        final_list = []
        for key, value in list_sorted:
            final_list.append([key, value, ''])

        return final_list



    def divide_list(self, list):
        all_m = []
        left = 0
        right = 0
        for i in range(0, len(list)):
            for j in range(i + 1, len(list)):
                right += list[j][1]

            for l in range(i, -1, -1):
                left += list[l][1]

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

        return list[0:index_of_min + 1], list[index_of_min + 1:]


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
    
    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.code_book[character]
        return encoded_text


    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8   
        for i in range(extra_padding):
            encoded_text += "0"
        
        
        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):
        if(len(padded_encoded_text) % 8 != 0):
            print("Encoded text not padded properly")
            exit(0)
        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2))
        return b


    def compression(self, text):
        
        encoded_text = self.get_encoded_text(text)
        padded_text = self.pad_encoded_text(encoded_text)
        
        b = self.get_byte_array(padded_text)        
        
        return bytes(b)

file = open("C:\\Users\\Ryan\\.spyder-py3\\Robinhood.txt")
text = file.read()

comp = Shannon_fano_structure()
compList = comp.create_list(text)
compDict = comp.shannon_fano_structure(compList)

com = comp.compression(text)
file.close()
output = open("C:\\Users\\Ryan\\.spyder-py3\\RobinhoodShannonCOMP.txt", "wb")
output.write(com)
output.close()

#print(com)
