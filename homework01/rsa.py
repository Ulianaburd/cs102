import random
from typing import Tuple


def is_prime(new: int) -> bool:
    """
    >>> is_prime(2)
    True
    >>> is_prime(11)
    True
    >>> is_prime(8)
    False
    """
    if new <= 1:
        return False
    for i in range(2, new // 2 + 1):
        if new % i == 0:
            return False
    return True


def generate_keypair(p: int, q: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both numbers must be prime.")
    elif p == q:
        raise ValueError("p and q cannot be equal")

    new = p * q

    phi = (p - 1) * (q - 1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)
    # Return public and private keypair
    # Public key is (e, new) and private key is (d, new)
    return ((e, new), (d, new))


def gcd(a: int, b: int) -> int:
    """
    >>> gcd(12, 15)
    3
    >>> gcd(3, 7)
    1
    """
    while b:
        a, b = b, a % b
    return a


def multiplicative_inverse(e: int, phi: int) -> int:
    """
    >>> multiplicative_inverse(7, 40)
    23
    """
    n_1 = 0
    n_2 = 1
    pr = phi
    while e != 0:
        d = pr // e
        n_1, n_2 = n_2, n_1 - d * n_2
        pr, e = e, pr - d * e
    if pr > 1:
        return 0
    if n_1 < 0:
        n_1 = n_1 + phi
    return n_1
