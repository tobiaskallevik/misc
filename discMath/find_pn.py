# Gets numbers from user
total_euros = int(input("Total euros:"))
starting_euros = int(input("Starting A euros:"))
p_win = float(input("Prop of winning:"))
p_loose = 1 - p_win


# Boundry conditions
p = [0] * (total_euros + 1)
p[total_euros] = 1

# Calculate the probability of winning
for i in range(total_euros-1, -1, -1):
    p[i] = p_win*p[i+1] + p_loose*p[i-1]
    
# Probability of winning when starting with x euros (print with decimal points not in scientific notation)
print("Result", "{:.20f}".format(p[starting_euros]))

