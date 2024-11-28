def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)

lcm_number = int(input("Enter amount: "))

if lcm_number == 2:
    a = int(input("Enter a number: "))
    b = int(input("Enter a number: "))
    result = lcm(a, b)
    print("The LCM of the numbers is:", result)
    
elif lcm_number == 3:
    a = int(input("Enter a number: "))
    b = int(input("Enter a number: "))
    c = int(input("Enter a number: "))
    result = lcm(lcm(a, b), c)
    print("The LCM of the numbers is:", result)
    
    
else:
    print("This program only supports 2 or 3 numbers")
    