# ciphers/caesar.py

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
            'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
            'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def clean_text(text):
    text = text.lower()
    cleaned = ""
    for ch in text:
        if ch in alphabet:
            cleaned += ch
    return cleaned


def encryption_ceaser(plaintext, shift_key):
    plaintext = clean_text(plaintext)
    ciphertext = ""

    for char in plaintext:
        position = alphabet.index(char)
        new_position = (position + shift_key) % len(alphabet)
        ciphertext += alphabet[new_position]

    return ciphertext.upper()


def decryption_ceaser(ciphertext, shift_key):
    ciphertext = clean_text(ciphertext)
    plaintext = ""

    for char in ciphertext:
        position = alphabet.index(char)
        new_position = (position - shift_key) % len(alphabet)
        plaintext += alphabet[new_position]

    return plaintext.lower()
