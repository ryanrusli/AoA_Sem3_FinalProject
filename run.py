'''CLI to run the compression algorithms'''
import argparse 

from huffman_coding import HuffmanCoding
from lempel_ziv import lzw_compress, lzw_decompress
from shannon_fano_structure import ShannonFano

def main():
    '''Command Line Interface using argparse'''
    parser = argparse.ArgumentParser(description="Hello World!")
    
    # arguments that will be parsed by the command line
    parser.add_argument('--compress',  
                        '-c',
                        help='Will perform compression')

    parser.add_argument('--decompress',
                        '-dc',
                        help='Will perform decompression')
    
    parser.add_argument('--dictionary',
                        '-d',
                        help='Which dictionary to choose')

    parser.add_argument('file', 
                    type=str,
                    help='Specified text file to be compressed')

    args = parser.parse_args() # parse the arguments

    # HuffmanCoding object 
    # hc = HuffmanCoding(args.file)

    if args.compress == 'huffman':
        '''compress using huffman'''
        huffman_compress(args.file)

    elif args.decompress == 'huffman':
        huffman_decompress(args.file, args.dictionary)  

    elif args.compress == 'lzw':
        '''compress using lempel-ziv-welch algorithm'''
        lzw_compression(args.file)
        
    elif args.decompress == 'lzw':
        '''Decompressing using LZW. Expected input should be a compressed lzw file'''
        lzw_decompress(args.file)

    elif args.compress == 'shannon-fano':
        '''compress using shannon-fano'''
        shannon_fano_compression(args.file) 
    
    elif args.decompress == 'shannon-fano':
        shannon_fano_decompression(args.file, args.dictionary)



def shannon_fano_decompression(filename, dict_name):
    '''Decompressing using shannon fano'''
    print('Decompressing...')

    dc = ShannonFano(filename)
    dc.decompression(dict_name)

def shannon_fano_compression(filename):
    '''Compressing using shannon-fano'''
    print("Compressing using shannon-fano...")

    c = ShannonFano(filename)
    c.compression()

def lzw_compression(filename):
    '''Compress using lzw'''
    print('Compressing using Lempel-Ziv-Welch...')

    with open(filename, 'r') as f:
        f_data = f.read()
        lzw_compress(f_data)

    print('{} has been compressed.'.format(f))

def huffman_compress(filename):
    '''Compress using huffman compress'''
    print('Compressing using huffman')
    
    instance = HuffmanCoding()
    instance.compress(filename)

    # print('{} has been compressed.'.format(filename))

def huffman_decompress(filename, dict_name):
    instance = HuffmanCoding()
    instance.decompress(filename, dict_name)
       
main()
