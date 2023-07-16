import json
import re
import glob
import os
import sys
import shutil


def convert_sql_to_json_fixture(sql_file, json_file):    
    with open(sql_file, 'r') as file:
        data = []
        if ".txt" in sql_file:
            for line in file.readlines():
                try:
                    line = line.strip()

                    # Parse table name
                    table_name = re.search(r'`(.+?)`', line).group(1)

                    # Parse column names
                    columns_str = re.search(r'\((`.*?`)\)', line).group(1)
                    columns = re.findall(r'`(.+?)`', columns_str)

                    # Parse values
                    values_str = re.search(r'VALUES \((.*?)\);', line).group(1)

                    # This line is modified to correctly parse both integer and string values
                    values = re.findall(r"(\d+|'[^']*')", values_str)
                    values = [int(v) if v.isdigit() else v.strip("'") for v in values]

                    # Create dictionary for JSON
                    row = {"model": f"{app}.{table_name}", "pk": values[0], "fields": {}}
                    for column, value in zip(columns[1:], values[1:]):
                        row["fields"][column] = value

                    data.append(row)
                except Exception as e:
                    print("Error: ", e)
            try: 
                
                # Write JSON fixture
                with open(json_file, 'w') as outfile:
                    json.dump(data, outfile)
            except Exception as e:
                print("Error: ", e)

# Convert all SQL files to JSON fixtures
directory_path = os.path.abspath(os.getcwd())
sql_folder_path = directory_path + "\\db_sql_inserts"
json_folder_path = directory_path + "\\json_fixtures"

# Create json_fixtures folder if it doesn't exist
if not os.path.exists(json_folder_path):
    os.mkdir(json_folder_path)

# Delete any existing JSON files in json_fixtures
for file_path in glob.glob(json_folder_path + "\\*.json"):
    os.remove(file_path)

list_of_files_path = [sql_folder_path + f"\\{el}" for el in os.listdir(sql_folder_path)]

app = input("Please insert the model name for which you want to create fixtures: ")

for file_path in list_of_files_path:    
    base_name = os.path.basename(file_path).split('.txt')[0] 
    json_path = os.path.join(json_folder_path, base_name + '.json')
    print(f"Converting {file_path} to {json_path}")

    convert_sql_to_json_fixture(file_path, json_path)