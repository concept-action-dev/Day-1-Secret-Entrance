#!/usr/bin/env python
"""

/ * File: AdventofCode-2025/Day-1-Secret-Entrance/parse_lr.py
/ * Description: Day 1 - Secret Entrance - L/R Instruction Parser
Parse L/R instructions into signed integers, with flexible output and a second
processing loop.

Usage examples:
    python parse_lr.py input.txt output.txt
    python parse_lr.py input.txt output.csv --format csv
    python parse_lr.py input.txt output.json --format json --verbose
    python parse_lr.py input.txt output.txt --strict
"""

import argparse
import csv
import json
import logging
import os
import re
from typing import Any, Dict, List, Optional


# Lines like: L10, R5, L  3, r100, etc.
LINE_RE = re.compile(r"^\s*([LlRr])\s*(\d+)\s*$")


def setup_logging(verbose: bool = False) -> None:
    """Configure basic logging."""
    level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


def parse_line(line: str, line_number: int, strict: bool = False) -> Optional[Dict[str, Any]]:
    """
    Parse a single line like 'L10' or 'R5'.

    Returns a record dict or None (for blank/malformed when not strict).
    """
    original = line.rstrip("\n")
    line = line.strip()

    if not line:
        logging.info("Skipping blank line %d", line_number)
        return None

    m = LINE_RE.match(line)
    if not m:
        msg = f"Malformed line {line_number}: {original!r}"
        if strict:
            # In strict mode we abort on the first bad line
            raise ValueError(msg)
        logging.warning(msg)
        return None

    letter = m.group(1).upper()
    num_str = m.group(2)
    value = int(num_str)

    # L = negative, R = positive
    if letter == "L":
        value = -value

    record = {
        "index": line_number,  # original line number in the input file
        "letter": letter,      # 'L' or 'R'
        "value": value,        # signed integer
    }
    return record


def parse_file(input_path: str, strict: bool = False) -> List[Dict[str, Any]]:
    """Read the entire file and return a list of parsed records."""
    records: List[Dict[str, Any]] = []

    with open(input_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            rec = parse_line(line, i, strict=strict)
            if rec is not None:
                records.append(rec)

    logging.info("Parsed %d records from %s", len(records), input_path)
    return records


def write_text(records: List[Dict[str, Any]], output_path: str) -> None:
    """Write output as simple text: 'L -10'."""
    with open(output_path, "w", encoding="utf-8") as out:
        for r in records:
            out.write(f"{r['letter']} {r['value']}\n")


def write_csv(records: List[Dict[str, Any]], output_path: str) -> None:
    """Write output as CSV with columns: index,letter,value."""
    with open(output_path, "w", encoding="utf-8", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=["index", "letter", "value"])
        writer.writeheader()
        writer.writerows(records)


def write_json(records: List[Dict[str, Any]], output_path: str) -> None:
    """Write output as pretty-printed JSON."""
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(records, out, indent=2)


# 🔁  SECOND LOOP: where you work with the signed numbers
# placeholder for next part of code
def process_values(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Example "second loop" over the signed values.

    Right now this:
      - walks through the values in order
      - keeps a running total (like moving left/right on a line)
      - tracks farthest left and right positions reached

    You can replace or extend this with whatever you need.
    """
    position = 0
    max_right = 0
    max_left = 0

    for r in records:
        position += r["value"]
        if position > max_right:
            max_right = position
        if position < max_left:
            max_left = position

    return {
        "final_position": position,
        "max_right": max_right,
        "max_left": max_left,
        "count": len(records),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Parse L/R instructions into signed numbers and write them to a file."
    )
    parser.add_argument("input", help="Path to input text file.")
    parser.add_argument("output", help="Path to output file (will be OVERWRITTEN).")
    parser.add_argument(
        "-f",
        "--format",
        choices=["text", "csv", "json"],
        default="text",
        help="Output format (default: text).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat malformed lines as errors (abort) instead of skipping.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging.",
    )

    args = parser.parse_args(argv)
    setup_logging(verbose=args.verbose)

    logging.info("Reading from %s", args.input)

    try:
        records = parse_file(args.input, strict=args.strict)
    except FileNotFoundError:
        logging.error("Input file not found: %s", args.input)
        return 1
    except ValueError as e:
        logging.error(str(e))
        return 1

    # 🔁 Run the second loop / processing step
    stats = process_values(records)
    logging.info(
        "Processed %d values. Final position=%d, max_right=%d, max_left=%d",
        stats["count"],
        stats["final_position"],
        stats["max_right"],
        stats["max_left"],
    )

    # Write output in the requested format, overwriting any existing file
    if args.format == "text":
        write_text(records, args.output)
    elif args.format == "csv":
        write_csv(records, args.output)
    else:
        write_json(records, args.output)

    logging.info("Wrote %d records to %s", len(records), args.output)

    # Small human-readable summary on stdout
    print(f"Done. Output saved to:\n  {os.path.abspath(args.output)}")
    print("Summary from second loop:")
    print(f"  final_position = {stats['final_position']}")
    print(f"  max_right      = {stats['max_right']}")
    print(f"  max_left       = {stats['max_left']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
