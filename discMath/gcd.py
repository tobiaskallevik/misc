def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

a = int(input("Enter a number: "))
b = int(input("Enter a number: "))
result = gcd(a,b)
print("The GCD of the numbers is:", result)