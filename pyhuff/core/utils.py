from collections import Counter

def get_file_content(filename):
    content = ''

    with open(filename) as f:
        for line in f:
            content+=line

    return content

def get_alphabet(filename : str) -> dict:
    """
    This function returns a dictionary containing 
    the histogram of occurrences of a file.

    This dictionary also has the keys 1 and 0, 
    that will abstract a hoffman tree
    """

    content = ''

    with open(filename) as file:
        for line in file:
            content += line
    
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