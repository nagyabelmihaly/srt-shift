import re
from datetime import datetime, timedelta

def shift_time(time_str, shift_ms):
    time_format = "%H:%M:%S,%f"
    original_time = datetime.strptime(time_str, time_format)
    shifted_time = original_time + timedelta(milliseconds=shift_ms)
    return shifted_time.strftime(time_format)[:-3]  # Remove microseconds

def shift_subtitles(input_file, output_file, shift_ms):
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for line in lines:
            time_match = re.match(r'(\d+:\d+:\d+,\d+) --> (\d+:\d+:\d+,\d+)', line)
            if time_match:
                start_time, end_time = time_match.groups()
                shifted_start_time = shift_time(start_time, shift_ms)
                shifted_end_time = shift_time(end_time, shift_ms)
                line = f"{shifted_start_time} --> {shifted_end_time}\n"

            outfile.write(line)

if __name__ == "__main__":
    input_file = input("Enter the input SRT file path: ")
    output_file = input("Enter the output SRT file path: ")
    
    try:
        shift_ms = int(input("Enter the time shift in milliseconds (positive: delay | negative: hasten): "))
    except ValueError:
        print("Invalid input. Please enter a valid integer for time shift.")
        exit()

    shift_subtitles(input_file, output_file, shift_ms)
    print(f"Subtitle times shifted by {shift_ms} milliseconds. Output written to {output_file}")
