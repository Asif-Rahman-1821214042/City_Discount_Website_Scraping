import json
import csv

# Load JSON file
with open('output_cleaned.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Ensure the data is a list of dictionaries
if isinstance(data, dict):
    data = [data]  # wrap it in a list if it's a single dict

# Extract field names (keys) from the first item
fieldnames = data[0].keys()

# Write CSV file
with open('output.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
