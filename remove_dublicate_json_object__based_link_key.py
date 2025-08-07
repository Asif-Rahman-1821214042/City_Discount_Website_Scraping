import json

def remove_duplicates_by_link(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    seen_links = set()
    unique_data = []

    for obj in data:
        link = obj.get('Link')
        if link not in seen_links:
            seen_links.add(link)
            unique_data.append(obj)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(unique_data, f, indent=4, ensure_ascii=False)

    print(f"Removed duplicates. {len(unique_data)} unique items saved to {output_file}")

# Example usage
remove_duplicates_by_link('merged_sample.json', 'output_cleaned.json')
