import csv
import numpy as np
from collections import defaultdict

# Input and Output File Paths
input_file = 'quantified_results.csv'
output_file = 'dispersion_results.csv'

# Read the input CSV
responses = defaultdict(list)
question_titles = {}
with open(input_file, 'r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for row in reader:
        question = row['Question Number']
        percentage = float(row['Assigned y_k (%)'])
        title = row['Question Title']
        responses[question].append(percentage)
        
        # Store the question title for later use
        if question not in question_titles:
            question_titles[question] = title

# Prepare data for output
output_rows = [("Question Number", "Question Title", "Degree of Dispersion (Std Dev)")]

# Calculate dispersion (standard deviation) for each question
for question, percentages in responses.items():
    question_title = question_titles[question]  # Retrieve the correct title for the question
    std_dev = np.std(percentages)  # Calculate standard deviation
    output_rows.append((question, question_title, f"{std_dev:.2f}"))

# Write the results to the output CSV
with open(output_file, 'w', newline='', encoding='utf-8') as f_out:
    writer = csv.writer(f_out)
    writer.writerows(output_rows)

print(f"✅ Degree of dispersion results written to '{output_file}' successfully!")
