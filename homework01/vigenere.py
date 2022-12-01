def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    key_length = len(keyword)
    key_as_int = [ord(i) for i in keyword]
    plaintext_int = [ord(i) for i in plaintext]

    for i in range(len(plaintext_int)):
        if "A" <= plaintext[i] <= "Z":
            value = (plaintext_int[i] + key_as_int[i % key_length]) % 26
            ciphertext += chr(value + 65)
        elif "a" <= plaintext[i] <= "z":
            value = (plaintext_int[i] + key_as_int[i % key_length] - 2 * ord("a")) % 26
            ciphertext += chr(value + 97)
        else:
            value = ord(plaintext[i])
            ciphertext = str(ciphertext) + str(chr(value))
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    key_length = len(keyword)
    key_as_int = [ord(i) for i in keyword]
    ciphertext_int = [ord(i) for i in ciphertext]

    for i in range(len(ciphertext_int)):
        if "A" <= ciphertext[i] <= "Z":
            value = (ciphertext_int[i] - key_as_int[i % key_length]) % 26
            plaintext += chr(value + 65)
        elif "a" <= ciphertext[i] <= "z":
            value = (ciphertext_int[i] - key_as_int[i % key_length]) % 26
            plaintext += chr(value + 97)
        else:
            value = ord(ciphertext[i])
            plaintext += str(chr(value))
    return plaintext
