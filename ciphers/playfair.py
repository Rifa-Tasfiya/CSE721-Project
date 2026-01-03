import numpy as np

# Playfair uses 25 letters (I/J combined)
ALPHABET_25 = [
    'a','b','c','d','e','f','g','h',
    'i','k','l','m','n','o','p','q',
    'r','s','t','u','v','w','x','y','z'
]


def clean_text(text):
    text = text.lower()
    text = text.replace('j', 'i')
    cleaned = ""

    for ch in text:
        if ch in ALPHABET_25:
            cleaned += ch

    return cleaned


def make_digraphs(text):
    digraphs = []
    for i in range(0, len(text), 2):
        digraphs.append(text[i:i+2])
    return digraphs


def insert_filler_x(text):
    i = 0
    result = ""

    while i < len(text):
        result += text[i]

        if i + 1 < len(text) and text[i] == text[i+1]:
            result += 'x'
            i += 1
        else:
            if i + 1 < len(text):
                result += text[i+1]
                i += 2
            else:
                i += 1

    return result


def generate_key_matrix(keyword, alphabet):
    keyword = clean_text(keyword)

    unique_key_letters = []
    for ch in keyword:
        if ch not in unique_key_letters:
            unique_key_letters.append(ch)

    combined_letters = []
    for ch in unique_key_letters:
        combined_letters.append(ch)

    for ch in alphabet:
        if ch not in combined_letters:
            combined_letters.append(ch)

    key_matrix = np.array(combined_letters).reshape(5, 5)
    return key_matrix


def find_position(key_matrix, ch):
    for row in range(5):
        for col in range(5):
            if key_matrix[row][col] == ch:
                return row, col


def encrypt_row_rule(key_matrix, r1, c1, r2, c2):
    if c1 == 4:
        new_c1 = 0
    else:
        new_c1 = c1 + 1

    if c2 == 4:
        new_c2 = 0
    else:
        new_c2 = c2 + 1

    return key_matrix[r1][new_c1], key_matrix[r2][new_c2]


def encrypt_column_rule(key_matrix, r1, c1, r2, c2):
    if r1 == 4:
        new_r1 = 0
    else:
        new_r1 = r1 + 1

    if r2 == 4:
        new_r2 = 0
    else:
        new_r2 = r2 + 1

    return key_matrix[new_r1][c1], key_matrix[new_r2][c2]


def encrypt_rectangle_rule(key_matrix, r1, c1, r2, c2):
    char1 = key_matrix[r1][c2]
    char2 = key_matrix[r2][c1]
    return char1, char2


def playfair_encrypt(plaintext, keyword):
    plaintext = clean_text(plaintext)
    plaintext = insert_filler_x(plaintext)

    # if odd length, pad with x
    if len(plaintext) % 2 != 0:
        plaintext += 'x'

    digraphs = make_digraphs(plaintext)
    key_matrix = generate_key_matrix(keyword, ALPHABET_25)

    cipher_text = ""

    for pair in digraphs:
        if len(pair) != 2:
            pair = pair + 'x'

        ch1 = pair[0]
        ch2 = pair[1]

        r1, c1 = find_position(key_matrix, ch1)
        r2, c2 = find_position(key_matrix, ch2)

        if r1 == r2:
            e1, e2 = encrypt_row_rule(key_matrix, r1, c1, r2, c2)
        elif c1 == c2:
            e1, e2 = encrypt_column_rule(key_matrix, r1, c1, r2, c2)
        else:
            e1, e2 = encrypt_rectangle_rule(key_matrix, r1, c1, r2, c2)

        cipher_text += e1 + e2

    return cipher_text.upper()


def decrypt_row_rule(key_matrix, r1, c1, r2, c2):
    if c1 == 0:
        new_c1 = 4
    else:
        new_c1 = c1 - 1

    if c2 == 0:
        new_c2 = 4
    else:
        new_c2 = c2 - 1

    return key_matrix[r1][new_c1], key_matrix[r2][new_c2]


def decrypt_column_rule(key_matrix, r1, c1, r2, c2):
    if r1 == 0:
        new_r1 = 4
    else:
        new_r1 = r1 - 1

    if r2 == 0:
        new_r2 = 4
    else:
        new_r2 = r2 - 1

    return key_matrix[new_r1][c1], key_matrix[new_r2][c2]


def decrypt_rectangle_rule(key_matrix, r1, c1, r2, c2):
    char1 = key_matrix[r1][c2]
    char2 = key_matrix[r2][c1]
    return char1, char2


def playfair_decrypt(ciphertext, keyword):
    ciphertext = clean_text(ciphertext)

    # if odd length ciphertext, pad with x (your requirement)
    if len(ciphertext) % 2 != 0:
        ciphertext += 'x'

    digraphs = make_digraphs(ciphertext)
    key_matrix = generate_key_matrix(keyword, ALPHABET_25)

    plaintext = ""

    for pair in digraphs:
        ch1 = pair[0]
        ch2 = pair[1]

        r1, c1 = find_position(key_matrix, ch1)
        r2, c2 = find_position(key_matrix, ch2)

        if r1 == r2:
            p1, p2 = decrypt_row_rule(key_matrix, r1, c1, r2, c2)
        elif c1 == c2:
            p1, p2 = decrypt_column_rule(key_matrix, r1, c1, r2, c2)
        else:
            p1, p2 = decrypt_rectangle_rule(key_matrix, r1, c1, r2, c2)

        plaintext += p1 + p2

    return plaintext.lower()
