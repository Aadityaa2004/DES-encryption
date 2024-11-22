import random

#fnction for finding gcd of two numbers using euclidean algorithm
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

#uses extened euclidean algorithm to get the d value
def get_d(e, z):
    d, x0, x1 = 0, 0, 1
    orig_z = z
    while e > 1:
        q = e // z
        e, z = z, e % z
        x0, x1 = x1 - q * x0, x0
    if e == 0:
        raise ValueError("No modular inverse exists.")
    return x1 + orig_z if x1 < 0 else x1
    
def is_prime(num):
    if num <= 1:
        return False
    
    # Iterate from 2 to n / 2
    for i in range(2, num//2 + 1):
        # If num is divisible by any number between 2 and n / 2, it is not prime
        if (num % i) == 0:
            return False
    
    return True

def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')

    n = p * q
    z = (p - 1) * (q - 1)

    # Choose e
    e = random.randrange(2, z)
    while gcd(e, z) != 1:
        e = random.randrange(2, z)

    # Calculate d
    d = get_d(e, z)

    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    e, n = pk
    # Convert plaintext character to an integer
    plaintext_int = ord(plaintext)
    # Encrypt the integer
    cipher = pow(plaintext_int, e, n)
    return cipher

def decrypt(pk, ciphertext):
    d, n = pk
    # Decrypt the integer
    plain_int = pow(ciphertext, d, n)
    # Ensure the value fits within valid ASCII range (0-255)
    plain_int = plain_int % 256
    # Convert back to character
    plain = chr(plain_int)
    return plain

