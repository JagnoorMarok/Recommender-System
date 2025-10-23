import csv
from collections import Counter

# Input and Output File Paths
input_file = 'response.csv'       # Your original questionnaire CSV
output_file = 'quantified_results.csv'  # Output CSV with y_k values

all_responses = []

# Read and clean responses
with open(input_file, 'r', encoding='utf-8-sig') as file:
    reader = csv.reader(file)
    header = next(reader)  # Header row
    for row in reader:
        if len(row) > 4:
            # Extract only the first letter (option) from each answer, lowercased
            cleaned = [cell.strip()[0].lower() for cell in row[4:] if cell.strip()]
            all_responses.append(cleaned)

# Transpose to get columns (i.e., questions)
question_columns = list(zip(*all_responses))

# Prepare data for output
output_rows = [("Question Number", "Question Title", "Option", "Assigned y_k (%)")]

for q_index, responses in enumerate(question_columns):
    option_counts = Counter(responses)
    total_responses = sum(option_counts.values())
    question_title = header[q_index + 4]

    # Sort options alphabetically: a, b, c, ...
    sorted_options = sorted(option_counts.keys())
    
    # Calculate percentages
    percentages = [(option_counts[opt] / total_responses) * 100 for opt in sorted_options]

    # Calculate cumulative y_k
    y_values = []
    cumulative = 0
    for percent in percentages:
        cumulative += percent
        y_values.append(cumulative)

    # Store results in reverse order (from least to most preferred)
    for opt, y_k in zip(sorted_options[::-1], y_values[::-1]):
        output_rows.append((f"Q{q_index + 1}", question_title, opt.upper(), f"{y_k:.2f}"))

# Write to CSV
with open(output_file, 'w', newline='', encoding='utf-8') as f_out:
    writer = csv.writer(f_out)
    writer.writerows(output_rows)

print(f"\n✅ Quantified results written to '{output_file}' successfully!")
