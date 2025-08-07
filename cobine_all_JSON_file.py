import os
import json

def merge_json_files(folder_path, output_file='merged_EACH.json'):
    merged_data = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    # If the JSON is a list, extend; else append
                    if isinstance(data, list):
                        merged_data.extend(data)
                    else:
                        merged_data.append(data)
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON: {file_path}")

    # Write merged data to output file
    with open(os.path.join(folder_path, output_file), 'w', encoding='utf-8') as out_file:
        json.dump(merged_data, out_file, indent=4, ensure_ascii=False)

    print(f"✅ Merged {len(merged_data)} records into '{output_file}'")

# Example usage
merge_json_files('Item Each Detail Scrap')  # Replace with your folder path
