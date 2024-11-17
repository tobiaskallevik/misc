a = int(input("Enter a number: "))
divisors = [i for i in range(1, a+1) if a % i == 0]

print(divisors)