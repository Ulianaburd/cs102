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
    alf = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alf_low = alf.lower()
    ciphertext = ''
    for i in plaintext:
        if i in alf:
            m = alf.index(i)
            n = (m + shift) % 26
            ciphertext += alf[n]
        elif i in alf_low:
            m = alf_low.index(i)
            n = (m + shift) % 26
            ciphertext += alf_low[n]
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
    alf = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alf_low = alf.lower()
    for i in ciphertext:
        if i in alf:
            m = alf.index(i)
            n = (m - shift) % 26
            ciphertext += alf[n]
        elif i in alf_low:
            m = alf_low.index(i)
            n = (m - shift) % 26
            ciphertext += alf_low[n]
    return plaintext