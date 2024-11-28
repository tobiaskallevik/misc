# Get user input for coefficients
a = float(input("Enter coefficient a: "))
b = float(input("Enter coefficient b: "))
c = float(input("Enter coefficient c: "))

# Calculate the discriminant
D = b**2 - 4*a*c

# Function to calculate square root using Newton's method
def sqrt(x):
    if x == 0:
        return 0
    guess = x / 2.0
    while True:
        new_guess = (guess + x / guess) / 2.0
        if abs(new_guess - guess) < 1e-10:
            return new_guess
        guess = new_guess

# Check the value of the discriminant
if D > 0:
    # Two real and distinct roots
    root1 = (-b + sqrt(D)) / (2*a)
    root2 = (-b - sqrt(D)) / (2*a)
    print("The roots are real and distinct:")
    print("Root 1:", root1)
    print("Root 2:", root2)
elif D == 0:
    # One real root
    root = -b / (2*a)
    print("The root is real and repeated:")
    print("Root:", root)
else:
    # Complex roots
    real_part = -b / (2*a)
    imaginary_part = sqrt(-D) / (2*a)
    print("The roots are complex:")
    print("Root 1:", real_part, "+", imaginary_part, "i")
    print("Root 2:", real_part, "-", imaginary_part, "i")