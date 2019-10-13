name='core'

from . import utils

def decode(CIPHERFILE, HUFFMAN_TREE):

    ciphered = utils.load_ciphered_file(filename=CIPHERFILE)

    huffman_tree = utils.load_huffman_tree(filename=HUFFMAN_TREE)
    
    deciphered_text = utils.huffman_decipher(ciphered, huffman_tree)

    utils.save_file_content(deciphered_text, filename='unziped_file.txt')

    print('Successfully decoded file')


def compress(FILENAME):
    histogram = utils.get_alphabet(FILENAME)

    huffman_tree = utils.huffman_tree(histogram)

    plain_text = utils.get_file_content(FILENAME)

    ciphered = utils.huffman_cipher(
        plain_text, 
        huffman_tree
    )

    utils.save_ciphered_file(ciphered, filename='encoded_file.huff')
    utils.save_huffman_tree(huffman_tree, filename='decoding_tree.huff')

    print('Successfully encoded file')
    decode('encoded_file.huff', 'decoding_tree.huff')