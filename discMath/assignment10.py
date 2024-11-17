from math import gcd

# Function to calculate the modular inverse
def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def rsa(message, decrypt=False):
    # Prime numbers
    p, q = 101, 103
    n = p * q
    phi_n = (p - 1) * (q - 1)
    # Encryption component
    e = 7 
    # Decryption component
    d = modinv(e, phi_n)
    
    # Encrypt: C = M^e mod n
    if not decrypt: return pow(message, e, n)
    # Decrypt: M = C^d mod n
    else: return pow(message, d, n)
    
    
message = 1337

print("Encrypted message: ", rsa(message))
print("Decrypted message: ", rsa(rsa(message), decrypt=True))

    
