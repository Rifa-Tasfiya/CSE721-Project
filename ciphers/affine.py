# ciphers/affine.py

alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
            'n','o','p','q','r','s','t','u','v','w','x','y','z']


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
    for i in range(m):
        if (a * i) % m == 1:
            return i
    return None


# ---------- Affine Cipher ----------

def affine_encrypt(plaintext, a, b):
    plaintext = clean_text(plaintext)
    a = a % 26
    b = b % 26

    # check if key is valid
    if euclid_gcd(a, 26) != 1:
        return "Invalid key: gcd(a,26) must be 1"

    ciphertext = ""
    for ch in plaintext:
        p = alphabet.index(ch)
        c = (a * p + b) % 26
        ciphertext += alphabet[c]

    return ciphertext.upper()


def affine_decrypt(ciphertext, a, b):
    ciphertext = clean_text(ciphertext)
    a = a % 26
    b = b % 26
    if euclid_gcd(a, 26) != 1:
        return "Invalid key: gcd(a,26) must be 1"

    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        return "Invalid key: no modular inverse"

    plaintext = ""
    for ch in ciphertext:
        c = alphabet.index(ch)
        p = (a_inv * (c - b)) % 26
        plaintext += alphabet[p]

    return plaintext.lower()
