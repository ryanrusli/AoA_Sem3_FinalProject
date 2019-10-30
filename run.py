'''
CLI to run the compression algorithms

author: @manu febie
'''
import argparse 

from huffman_encoding import HuffmanCoding
from lempel_ziv import lzw_compress, lzw_decompress
from shannon_fano import ShannonFano

def main():
    '''Command Line Interface using argparse'''
    parser = argparse.ArgumentParser(description="Hello World!")
    
    # arguments that will be parsed by the command line
    parser.add_argument('--compress',  
                        '-c',
                        help='Will perform compression')

    parser.add_argument('--decompress',
                        '-d',
                        help='Will perform decompression')

    parser.add_argument('file', 
                    type=str,
                    help='Specified text file to be compressed')

    args = parser.parse_args() # parse the arguments

    if args.compress == 'huffman':
        '''compress using huffman'''
        x = HuffmanCoding(args.file)
        x.compress()

    elif args.decompress == 'huffman':
        pass

    elif args.compress == 'lzw':
        '''compress using lempel-ziv-welch algorithm'''
        f = open(args.file, 'r')  
        src = f.read()
        lzw_compress(src)
        f.close()

    elif args.decompress == 'lzw':
        '''Decompressing using LZW'''
        lzw_decompress(args.file)

    elif args.compress == 'shannon-fano':
        '''compress using shannon-fano'''
        file = open(args.file)
        read_file = file.read()

        sf_compress = ShannonFano()
        sf_compressList = sf_compress.create_list(read_file)
        sf_compressDict = sf_compress.shannon_fano(sf_compressList)
        compress = sf_compress.compression(read_file)
        file.close()
        
        output = open('sf_compressed.txt', 'wb')
        output.write(compress)
        output.close()
        
main()
