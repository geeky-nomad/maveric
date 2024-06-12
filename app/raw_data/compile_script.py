import os
import csv
import json


# Function to extract data from a single file
def extract_data(file_path):
    with open(file_path, 'r') as file:
        data = {}
        options = {}
        for line in file:
            parts = line.strip().split(": ", 1)
            if len(parts) == 2:
                key, value = parts
                if key == "Options":
                    options = parse_options(value)
                else:
                    data[key] = value
        data.update(options)
        return data


# Function to parse options section
def parse_options(options_str):
    options = {}
    for option in options_str.splitlines():
        if ':' in option:
            key, value = option.split(": ")
            options[key.strip()] = ', '.join(value.split(', '))
    return options


# Function to compile data from multiple files


def compile_data():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(current_directory, 'products.csv')
    output_file_json = os.path.join(current_directory, 'products.json')
    all_fieldnames = set()
    all_data = []
    for filename in os.listdir(current_directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(filename)
            data = extract_data(file_path)

            # Update fieldnames if needed
            all_fieldnames.update(data.keys())

            all_data.append(data)
    # Write to CSV
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=all_fieldnames)
        writer.writeheader()
        for data in all_data:
            writer.writerow(data)

    # Write to JSON
    with open(output_file_json, 'w') as jsonfile:
        json.dump(all_data, jsonfile, indent=4)


compile_data()
