# this script reads an input file containing lines that start with either 'L' or 'R' followed by a number.
# It processes each line to convert 'L' prefixed numbers to negative values and 'R' prefixed numbers to positive values.
# This is a simplified version for testing

import os

INPUT_FILE = "input.txt"
OUTPUT_FILE = "parsed_output.txt"

def parse_line(line: str):
    line = line.strip()
    if not line:
        return None

    letter = line[0].upper()
    number = line[1:]

    if not number.isdigit():
        raise ValueError(f"Invalid format: {line}")

    value = int(number)

    # L = negative, R = positive
    if letter == "L":
        value = -value
    elif letter == "R":
        value = value
    else:
        raise ValueError(f"Unknown direction letter: {line}")

    return f"{letter} {value}"

def main():
    # Overwrite file each run
    with open(OUTPUT_FILE, "w") as out:
        with open(INPUT_FILE, "r") as f:
            for line in f:
                parsed = parse_line(line)
                if parsed:
                    out.write(parsed + "\n")

    print(f"Done! Parsed output saved to: {os.path.abspath(OUTPUT_FILE)}")

if __name__ == "__main__":
    main()
