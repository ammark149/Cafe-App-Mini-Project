import json
import csv 
from pathlib import Path


#Location of this python file.
BASE_DIR = Path(__file__).parent


#Loading our json menu
def load_json(file_location):
    file_path = BASE_DIR / file_location
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return {}
    
#Reading files
def load_data(file_location):
    file_path = BASE_DIR / file_location
    data = []
    print(f"Loading data from {file_path}...")
    try:
        with open(file_path,'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"Sorry {file_path} not found.")
    return data

#Writing to files
def save_data(file_location, data_list):
    file_path = BASE_DIR / file_location
    print(f"Saving data to {file_path}...")
    if not data_list:
        return
    column_headers = data_list[0].keys() #Headers for top row
    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=column_headers)
        writer.writeheader()
        writer.writerows(data_list)
