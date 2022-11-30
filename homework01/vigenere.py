from homework01.caesar import encrypt_caesar, decrypt_caesar


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
    alf = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    keyword = keyword.upper()
    for i in range(len(plaintext)):
        shift = alf.index(
            keyword[i % len(keyword)])  # вычисление сдвига для конкретной буквы (повторение ключевого слова)
        ciphertext += encrypt_caesar(plaintext[i], shift)
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
    alf = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    keyword = keyword.upper()
    for i in range(len(ciphertext)):
        shift = alf.index(keyword[i % len(keyword)])
        plaintext += decrypt_caesar(ciphertext[i], shift)
    return plaintext
