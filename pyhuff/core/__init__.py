name='core'

from . import utils

def decode(CIPHERFILE, HUFFMAN_TREE):

    ciphered = utils.load_ciphered_file(filename=CIPHERFILE)

    huffman_tree = utils.load_huffman_tree(
        filename=HUFFMAN_TREE
    )
    
    deciphered_text = utils.huffman_decipher(
        ciphered, 
        huffman_tree
    )

    filename = utils.get_directory_reference(CIPHERFILE)

    utils.save_file_content(
        deciphered_text, 
        filename = filename
    )

    print('Successfully decoded file')


def compress(FILENAME):
    histogram = utils.get_alphabet(
        FILENAME, 
        check_non_ascii=True
    )

    huffman_tree = utils.huffman_tree(histogram)

    plain_text = utils.get_file_content(FILENAME)

    ciphered = utils.huffman_cipher(
        plain_text, 
        huffman_tree
    )

    zipped_file = FILENAME.split('.')[0] + '.zip.huff'
    decode_tree = FILENAME.split('.')[0] + '.dec.tree.huff'

    utils.save_ciphered_file(ciphered, filename=zipped_file)
    utils.save_huffman_tree(
        huffman_tree, 
        filename=decode_tree
    )

    ratio = utils.compression_ratio(
        FILENAME, 
        zipped_file, 
        decode_tree
    )

    print('Successfully encoded file.', ratio, " %", " of original size ")
    
    decode(zipped_file, decode_tree)