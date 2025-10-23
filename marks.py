import csv
import random

# Assign one random float (5.0 - 10.0) to each unique roll number
def assign_float_to_rollnos(csv_filename):
    rollno_numbers = {}
    
    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            roll_no = row.get('roll no') or row.get('roll_no') or row.get('Roll No.(8 Digits)')
            if roll_no and roll_no not in rollno_numbers:
                random_float = round(random.uniform(5.0, 10.0), 2)  # rounded to 2 decimal places
                rollno_numbers[roll_no] = random_float

    return rollno_numbers

# Save to CSV
def save_to_csv(data_dict, output_filename):
    with open(output_filename, 'w', newline='') as csvfile:
        fieldnames = ['roll no', 'random_float']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for roll_no, value in data_dict.items():
            writer.writerow({'roll no': roll_no, 'random_float': value})

# Example usage
input_csv = 'response.csv'  # Replace with your actual CSV filename
output_csv = 'marks.csv'

result = assign_float_to_rollnos(input_csv)
save_to_csv(result, output_csv)

print(f"Assigned random float values to roll numbers and saved in {output_csv}.")
