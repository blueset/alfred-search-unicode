#!/usr/local/bin/python3
"""
Search for Unicode 12.1 Emoji Descriptions

uni binary from: https://github.com/arp242/uni
Twemoji updated to 12.1.4
"""

import sys
import re
import subprocess
import json
import unicodedata
from pathlib import Path

if len(sys.argv) >= 2:
    query = sys.argv[1]

    try:
        out: str = subprocess.check_output(
            ["./uni", "-q", "emoji", query]).decode()

        out = out.strip().splitlines()
    except subprocess.CalledProcessError:
        out = []

else:
    out = []

data = []

for i in out[:20]:
    match = re.match(
        r"^([^ ]+?) (.+?)  +(.+?)  +(.+?)$", i)
    if not match:
        continue
    char, name, cat, sub_cat = match.groups()

    lookup_char = char.replace('\ufe0f', '')
    hexes = tuple(hex(ord(i))[2:].lower() for i in lookup_char)
    lookup_sequence = "-".join(hexes)
    uid = "_".join(hexes)
    c_hex = " ".join(f"U+{i.upper()}" for i in hexes)
    name = name.title()

    p = Path(f"twemoji/{lookup_sequence}.png")
    if p.exists():
        icon_path = str(p)
    else:
        icon_path = "emoji.png"

    data.append({
        "uid": f"emoji_{lookup_sequence}",
        "title": f"{char} — {name}",
        "subtitle": f"{c_hex}: {cat}, {sub_cat}",
        "arg": char,
        "text": {
            "copy": char,
            "largetype": char
        },
        "icon": {
            "path": icon_path
        }
    })

json.dump({"items": data}, sys.stdout)
