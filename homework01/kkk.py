def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
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
