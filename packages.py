#!/usr/bin/env python3
import json
import sys
import os

def load_json(path):
    # Read raw bytes
    try:
        with open(path, 'rb') as f:
            raw = f.read()
    except FileNotFoundError:
        sys.exit(f"Error: '{path}' not found in {os.getcwd()}")

    # Detect BOM for UTF-16 LE/BE, otherwise treat as UTF-8 (stripping a BOM if present)
    if raw.startswith(b'\xff\xfe') or raw.startswith(b'\xfe\xff'):
        text = raw.decode('utf-16')
    else:
        text = raw.decode('utf-8-sig')

    # Parse JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        sys.exit(f"Error parsing JSON in '{path}': {e}")

def main():
    in_path  = 'pkg-list.json'
    out_path = 'pkgs.txt'

    data = load_json(in_path)

    # Write out name=version
    count = 0
    with open(out_path, 'w', encoding='utf-8') as out:
        for pkg in data:
            name    = pkg.get('name')
            version = pkg.get('version')
            if name and version:
                out.write(f"{name}={version}\n")
                count += 1

    print(f"Wrote {count} entries to '{out_path}'")

if __name__ == '__main__':
    main()
