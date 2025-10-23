import csv
import random
import string

# Parameters
MIN_LETTERS = 3
MAX_LETTERS = 10

# Read CSV and assign capital letters (A–Z), ensuring uniqueness per roll no
def assign_unique_letters(csv_filename):
    result = []

    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            roll_no = row.get('roll no') or row.get('roll_no') or row.get('Roll No.(8 Digits)')
            if roll_no:
                num_letters = random.randint(MIN_LETTERS, MAX_LETTERS)
                letters = random.sample(string.ascii_uppercase, num_letters)
                for letter in letters:
                    result.append({'roll no': roll_no, 'letter': letter})

    return result

# Save transactional output
def save_to_csv(data, output_filename):
    with open(output_filename, 'w', newline='') as csvfile:
        fieldnames = ['roll no', 'letter']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Example usage
input_csv = 'response.csv'  # Replace with your CSV file path
output_csv = 'courses.csv'

data = assign_unique_letters(input_csv)
save_to_csv(data, output_csv)

print(f"Generated transactional letter assignments for roll numbers in {output_csv}.")
