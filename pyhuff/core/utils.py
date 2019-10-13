from collections import Counter
import pickle

def get_file_content(filename):
    content = ''

    with open(filename) as f:
        for line in f:
            content+=line

    # remove all non ascci chars
    # content = ''.join([i if ord(i) < 128 else ' ' for i in content])

    return content

def get_alphabet(filename : str) -> dict:
    """
    This function returns a dictionary containing 
    the histogram of occurrences of a file.

    This dictionary also has the keys 1 and 0, 
    that will abstract a hoffman tree
    """

    content = get_file_content(filename)
    
    char_histogram = Counter(content)

    def format_dict(k, v):
        retn = {}
        retn['probability'], retn['value'] = v, k
        retn[0], retn[1] = None, None
        return retn

    char_histogram = { k: format_dict(k, v) for k,v in char_histogram.items() }

    return char_histogram

def huffman_tree(alphabet):
    while len(alphabet) > 1:
        sorted_alphabet = sorted(alphabet, key=lambda x: alphabet[x]['probability'])

        new_symbol_name = '{0}{1}'.format(
            alphabet[sorted_alphabet[0]]['value'], alphabet[sorted_alphabet[1]]['value']
        )

        new_node = {
            'probability': alphabet[sorted_alphabet[0]]['probability'] + alphabet[sorted_alphabet[1]]['probability'],
            0: alphabet[sorted_alphabet[0]],
            1: alphabet[sorted_alphabet[1]],
            'value': new_symbol_name
        }

        alphabet[new_node['value']] = new_node
        del alphabet[sorted_alphabet[0]]
        del alphabet[sorted_alphabet[1]]

    root = [*alphabet][0]

    return alphabet[root]

def save_huffman_tree(huffman_tree, filename):
    pickle.dump(huffman_tree, open(filename, 'wb'))

def save_ciphered_file(ciphered, filename):
    # TODO: Convert string text to bytes
    pickle.dump(ciphered, open(filename, 'wb'))

def load_huffman_tree(filename):
    huffman_tree = pickle.load(open(filename, 'rb'))
    return huffman_tree

def load_ciphered_file(filename):
    # TODO: Convert bytes to string text
    ciphered = pickle.load(open(filename, 'rb'))
    return ciphered

def save_file_content(deciphered_text, filename):
    with open(filename, "w") as file:
        file.write(deciphered_text)

def huffman_cipher(text, huffman_tree):
    ciphered = ''

    for ch in text:
        current_branch = huffman_tree
        while True:
            if current_branch[0] is None and current_branch[1] is None:
                break

            if ch in current_branch[0]['value']:
                ciphered += '0'
                current_branch = current_branch[0]
            else:
                ciphered += '1'
                current_branch = current_branch[1]

    return ciphered

def huffman_decipher(ciphered, huffman_tree):
    
    plain_text = ''
    current_branch = huffman_tree

    for ch in ciphered:
        if current_branch[0] is None and current_branch[1] is None:
            plain_text += current_branch['value']
            current_branch = huffman_tree
        
        current_branch = current_branch[int(ch)]

    plain_text += current_branch['value']

    return plain_text