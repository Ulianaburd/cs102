def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    alf = 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alf_low = alf.lower()
    shift = int(3)
    plaintext = input(str())
    ciphertext = ''
    for i in plaintext:
        m = alf.find(i)
        n = m + shift
        if i in alf:
            ciphertext += alf[n]
        else:
            ciphertext += i
    print(ciphertext)
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    alf = 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alf_low = alf.lower()
    shift = int(3)
    ciphertext = input(str())
    plaintext = ''
    for i in ciphertext:
        m = alf.find(i)
        n = m - shift
        if i in alf:
            plaintext += alf[n]
        else:
            plaintext += i
    print(plaintext)
    return plaintext