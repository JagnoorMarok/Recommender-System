# Number of students choosing each option
option_counts = [255, 42, 222]  # Example counts for options a1, a2, a3

# Total number of participants
total_participants = sum(option_counts)

# Calculate the percentage for each option
percentages = [(count / total_participants) * 100 for count in option_counts]

# Calculate y_k for each option
y_values = []
cumulative_sum = 0

for percentage in percentages:
    cumulative_sum += percentage
    y_k = cumulative_sum
    y_values.append(y_k)

# Print the results
for i, y_k in enumerate(y_values, start=1):
    print(f"Option a{4-i}: Assigned Value y_{i} = {y_k:.2f}")