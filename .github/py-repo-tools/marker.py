import argparse
import os
import re

def update_file(file_path: str, start_marker: str, end_marker: str, new_content: str):
    """
    Updates the content between HTML comment markers (start_marker and end_marker) in the given file.
    Only considers markers inside proper HTML comments. Does nothing if file or markers are missing.
    """
    if not os.path.exists(file_path):
        print(f"File '{file_path}' does not exist. No action taken.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Compile regex patterns to detect markers inside comments
    start_pattern = re.compile(rf"<!--\s*{re.escape(start_marker)}\s*-->")
    end_pattern = re.compile(rf"<!--\s*{re.escape(end_marker)}\s*-->")

    start_index = end_index = None

    # Find the first line containing the start marker inside a comment
    for i, line in enumerate(lines):
        if start_pattern.search(line):
            start_index = i
            break

    # Find the first line after start_index containing the end marker inside a comment
    if start_index is not None:
        for i, line in enumerate(lines[start_index + 1:], start=start_index + 1):
            if end_pattern.search(line):
                end_index = i
                break

    if start_index is None or end_index is None:
        print(f"No block found between '{start_marker}' and '{end_marker}' inside comments in '{file_path}'. No action taken.")
        return

    print(f"Updating existing block in '{file_path}'...")

    # Replace content between markers, preserving the marker lines
    lines[start_index:end_index + 1] = [
        lines[start_index].rstrip('\n') + "\n",
        new_content + "\n",
        lines[end_index].rstrip('\n') + "\n"
    ]

    # Write changes back to the file
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print("File updated successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Update text strictly inside HTML comment markers in an existing file"
    )
    parser.add_argument("file_path", help="File to modify")
    parser.add_argument("start_marker", help="Start comment marker (e.g., GOURCE-VIDEO-START)")
    parser.add_argument("end_marker", help="End comment marker (e.g., GOURCE-VIDEO-END)")
    parser.add_argument("text", help="Text to insert between the markers")
    args = parser.parse_args()

    update_file(args.file_path, args.start_marker, args.end_marker, args.text)
