"""Add or remove newlines to files in specified directory.

Examples:
    $ python linestripper.py add
    $ python linestripper.py remove
    $ python linestripper.py remove --directory 'data'
    $ python linestripper.py --help
"""

import argparse
from pathlib import Path

ROOT = Path(".")


def strip_newlines(filepath: Path) -> None:
    """Remove newlines from start/end of file."""
    with open(filepath) as f_input:
        data = f_input.read()
        fixed_data = data.rstrip("\n")
        if fixed_data != data:
            print(f"Update {filepath}")
            with open(filepath, "w") as f_output:
                f_output.write(fixed_data)


def add_newline(filepath: Path) -> None:
    """Add a newline to end of file."""
    with open(filepath) as f_input:
        data = f_input.read()
        if data and data[-1] != "\n":
            print(f"Update {filepath}")
            data += "\n"
            with open(filepath, "w") as f_output:
                f_output.write(data)


def main(action: str, directory: str = "solutions", file_ext: str = ".py") -> None:
    """CLI utility to add/remove newlines from all files in directory."""
    print(f"{action} newlines for all {file_ext} files in {directory}")

    if action not in ("add", "remove"):
        raise RuntimeError(f"action must be one of 'add' or 'remove' ('{action}' given)")

    for filepath in (ROOT / directory).glob(f"*{file_ext}"):
        if action == "add":
            add_newline(filepath)
        if action == "remove":
            strip_newlines(filepath)

    print(f"Request to {action} newlines to all files in {directory} is complete!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add or remove newlines to files in specified directory.")
    parser.add_argument('action', choices=['add', 'remove'], help="Action to perform: 'add' or 'remove' newlines.")
    parser.add_argument('--directory', default='solutions', help="Directory to process files in.")
    parser.add_argument('--file_ext', default='.py', help="File extension to filter by.")

    args = parser.parse_args()
    main(args.action, args.directory, args.file_ext)
