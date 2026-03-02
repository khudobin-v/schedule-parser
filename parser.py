import json
import re

def parse_schedule(text):
    """
    Parse the schedule text into structured JSON format
    """
    lines = text.strip().split('\n')
    
    # Extract header information
    header_ru = lines[0].strip()  # Тюляева
    header_en = lines[1].strip()  # Tyulyaeva
    street_ru = lines[2].strip()  # Индустриальная
    street_num = lines[3].strip()  # 4
    street_en = lines[4].strip()  # Industrialnaya
    
    # Extract day type labels
    day_types_ru = lines[5].split()  # ['Рабочие', 'дни'] + ['Выходные', 'дни']
    day_types_en = lines[6].split()  # ['Business', 'days'] + ['Weekends']
    
    # Separate day types
    business_days_ru = f"{day_types_ru[0]} {day_types_ru[1]}"
    weekend_days_ru = f"{day_types_ru[2]} {day_types_ru[3]}" if len(day_types_ru) >= 4 else f"{day_types_ru[2]}" if len(day_types_ru) >= 3 else ""
    business_days_en = f"{day_types_en[0]} {day_types_en[1]}"
    weekend_days_en = f"{day_types_en[2]} {day_types_en[3]}" if len(day_types_en) >= 4 else f"{day_types_en[2]}" if len(day_types_en) >= 3 else ""
    
    # Parse time schedule data (lines 7-24 contain the actual schedule)
    schedule_data = []
    # We'll stop at the first line that doesn't look like a schedule entry
    for i in range(7, len(lines)):  # Start from line 7
        line = lines[i].strip()
        if not line:
            continue
        
        parts = line.split()
        if parts:
            # Check if the first part looks like an hour (numeric value)
            first_part = parts[0]
            if first_part.isdigit() and 0 <= int(first_part) <= 23:
                # This looks like a valid schedule entry
                hour = first_part
                minutes = parts[1:]  # Remaining parts are minutes
                schedule_data.append({
                    'hour': hour,
                    'minutes': minutes
                })
            else:
                # This doesn't look like a schedule entry, so we've reached the footer
                footer_start = i
                break
        else:
            # Empty line, continue
            continue
    
    # Extract footer info starting from where we stopped parsing schedule
    footer_info = []
    for i in range(footer_start, len(lines)):
        footer_info.append(lines[i].strip())
    
    # Create structured data
    result = {
        'route_info': {
            'stop_ru': header_ru,
            'stop_en': header_en,
            'street_ru': street_ru,
            'street_number': street_num,
            'street_en': street_en
        },
        'day_types': {
            'business_days_ru': business_days_ru,
            'weekend_days_ru': weekend_days_ru,
            'business_days_en': business_days_en,
            'weekend_days_en': weekend_days_en
        },
        'schedule': schedule_data,
        'footer': footer_info
    }
    
    return result

def main():
    # Read the input text
    with open('/workspace/input.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Parse the text
    parsed_data = parse_schedule(text)
    
    # Write to JSON file
    with open('/workspace/output.json', 'w', encoding='utf-8') as f:
        json.dump(parsed_data, f, ensure_ascii=False, indent=2)
    
    print("Parsing completed! Output saved to output.json")
    print(json.dumps(parsed_data, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()