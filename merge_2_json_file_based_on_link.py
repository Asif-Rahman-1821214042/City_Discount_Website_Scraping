import json

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def merge_json_by_link(file1_path, file2_path, output_path):
    data1 = load_json(file1_path)
    data2 = load_json(file2_path)

    # Build index from file2 using Link
    link_map = {item['Link']: item for item in data2 if 'Link' in item}

    merged_data = []
    for item in data1:
        link = item.get('Link')
        if link and link in link_map:
            merged = {**item, **link_map[link]}  # file2 overrides file1
            merged_data.append(merged)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)

    print(f"Merged {len(merged_data)} items saved to '{output_path}'")

# Example usage:
merge_json_by_link('Done_List/merged.json', 'Item Each Detail Scrap/merged_EACH.json', 'merged_sample.json')


