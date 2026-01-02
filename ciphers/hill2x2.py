import numpy as np

alphabet = [
    'a','b','c','d','e','f','g','h','i','j','k','l','m',
    'n','o','p','q','r','s','t','u','v','w','x','y','z'
]

# ---------- Utility functions ----------

def clean_text(text):
    text = text.lower()
    cleaned = ""
    for ch in text:
        if ch in alphabet:
            cleaned += ch
    return cleaned

def euclid_gcd(a, b):
    if b == 0:
        return a
    else:
        return euclid_gcd(b, a % b)

def mod_inverse(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

def det_2x2_mod26(M):
    return (int(M[0,0]) * int(M[1,1]) - int(M[0,1]) * int(M[1,0])) % 26

def inv_2x2_mod26(M):
    det = det_2x2_mod26(M)
    det_inv = mod_inverse(det, 26)
    if det_inv is None:
        return None

    a = int(M[0,0])
    b = int(M[0,1])
    c = int(M[1,0])
    d = int(M[1,1])

    adj = np.array([
        [ d, -b],
        [-c,  a]
    ], dtype=int)

    return (det_inv * adj) % 26

# ---------- Encryption (ROW-vector) ----------
# C = P * K (mod 26)

def hill_encrypt(plaintext, a, b, c, d):
    plaintext = clean_text(plaintext)

    # pad with x if odd length
    if len(plaintext) % 2 != 0:
        plaintext += 'x'

    key_matrix = np.array([
        [a % 26, b % 26],
        [c % 26, d % 26]
    ], dtype=int)

    det = det_2x2_mod26(key_matrix)
    if euclid_gcd(det, 26) != 1:
        return "Invalid key: determinant has no inverse mod 26"

    ciphertext = ""

    for i in range(0, len(plaintext), 2):
        # 1x2 row vector
        pair_vector = np.array([[
            alphabet.index(plaintext[i]),
            alphabet.index(plaintext[i+1])
        ]], dtype=int)

        # 1x2 result
        cipher_vector = np.dot(pair_vector, key_matrix) % 26

        ciphertext += alphabet[int(cipher_vector[0, 0])]
        ciphertext += alphabet[int(cipher_vector[0, 1])]

    return ciphertext.upper()

# ---------- Decryption (ROW-vector) ----------
# P = C * K^{-1} (mod 26)

def hill_decrypt(ciphertext, a, b, c, d):
    ciphertext = clean_text(ciphertext)

    if len(ciphertext) % 2 != 0:
        return "Invalid ciphertext length"

    key_matrix = np.array([
        [a % 26, b % 26],
        [c % 26, d % 26]
    ], dtype=int)

    inv_key_matrix = inv_2x2_mod26(key_matrix)
    if inv_key_matrix is None:
        return "Invalid key: determinant has no inverse mod 26"

    plaintext = ""

    for i in range(0, len(ciphertext), 2):
        # 1x2 row vector
        pair_vector = np.array([[
            alphabet.index(ciphertext[i]),
            alphabet.index(ciphertext[i+1])
        ]], dtype=int)

        # 1x2 result
        plain_vector = np.dot(pair_vector, inv_key_matrix) % 26

        plaintext += alphabet[int(plain_vector[0, 0])]
        plaintext += alphabet[int(plain_vector[0, 1])]

    return plaintext.lower()
