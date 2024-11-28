# Function to perform modular exponentiation
def modular_exponentiation(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if (exponent % 2) == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

# Get user input
base = int(input("Enter the base: "))
exponent = int(input("Enter the exponent: "))
modulus = int(input("Enter the modulus: "))

# Calculate the result
result = modular_exponentiation(base, exponent, modulus)

# Print the result
print("The result of", base, "^", exponent, "mod", modulus, "is:", result)