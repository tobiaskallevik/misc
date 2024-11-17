def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd_val, x, y = extended_gcd(a, m)
    if gcd_val != 1:
        return None  # Inverse doesn't exist
    else:
        return x % m

# Gets numbers from user
a = int(input("Enter a number: "))
m = int(input("Enter a modulus: "))

# Calculate the modular inverse
inverse = mod_inverse(a, m)
if inverse is None:
    print("Inverse doesn't exist")
else:
    print("Result", inverse)