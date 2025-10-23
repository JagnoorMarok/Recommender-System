import numpy as np

# Assigned values for options A, B, and C
values = [100, 70, 30]

# Calculate the mean of the values
mean_value = np.mean(values)

# Calculate the degree of dispersion (variance)
dispersion = np.sum([(value - mean_value) ** 2 for value in values]) / len(values)

# Print the results
print(f"Assigned Values: A = {values[0]}, B = {values[1]}, C = {values[2]}")
print(f"Mean Value: {mean_value:.2f}")
print(f"Degree of Dispersion: {dispersion:.3f}")
std=np.sqrt(dispersion)
print(std)

# Check if dispersion is less than 10 and reassign if necessary
if dispersion < 10:
    values = [100, 70, 30]  # Reassign values to effectively distinguish options
    print("Reassigned Values: A = 100, B = 70, C = 30")
    dispersion = np.sum([(value - mean_value) ** 2 for value in values]) / len(values)
    print(f"New Degree of Dispersion: {dispersion:.3f}")
    std=np.sqrt(dispersion)
    print(std)


### NOTE: Degree of dispersion is the std variable according to research paper.
    