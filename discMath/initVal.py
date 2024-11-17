def solve_quadratic(a, b, c):
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return None, None  # No real roots
    elif discriminant == 0:
        root = -b / (2*a)
        return root, root
    else:
        root1 = (-b + discriminant**0.5) / (2*a)
        root2 = (-b - discriminant**0.5) / (2*a)
        return root1, root2

def solve_recurrence(x, y, z, a0, a1):
    r1, r2 = solve_quadratic(1, y, z)

    if r1 is None and r2 is None:
        return "No real roots found."

    if r1 != r2:
        A = (a1 - a0 * r2) / (r1 - r2)
        B = a0 - A
        general_solution = "a_n = " + str(A) + "*" + str(r1) + "^n + " + str(B) + "*(" + str(r2) + ")^n"
    else:
        A = a0
        B = (a1 - A * r1) / r1
        general_solution = "a_n = " + str(A) + "*" + str(r1) + "^n + " + str(B) + "*n*" + str(r1) + "^n"

    return general_solution

# Example usage
x = int(input("Enter x: "))
y = int(input("Enter y: "))
z = int(input("Enter z: "))
a0 = int(input("Enter a0: "))
a1 = int(input("Enter a1: "))

general_solution = solve_recurrence(x, y, z, a0, a1)
print("Solution:", general_solution)
