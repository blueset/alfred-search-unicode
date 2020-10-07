#!/usr/local/bin/python3

"""
Search for Unicode 12.1 Descriptions

uni binary from: https://github.com/arp242/uni
"""

import sys
import re
import subprocess
import json

if len(sys.argv) >= 2:
    query = sys.argv[1]

    try:
        out: str = subprocess.check_output(["./uni", "-q", "search", query]).decode()

        out = out.strip().splitlines()
    except subprocess.CalledProcessError:
        out = []

    if re.match(r"((U\+)?[0-9A-Fa-f]+ ?)+$", query):
        pr_out: str = subprocess.check_output(["./uni", "-q", "print"] + query.split()).decode()
        if "unknown codepoint" not in pr_out:
            out = pr_out.strip().splitlines() + out
else:
    out = []

data = []

for i in out[:20]:
    match = re.match(
        r"^'(.+?)' +(U\+[0-9A-F]+) +(\d+) +((?:[0-9a-f ]+?)) +(&.+?;) +(.+)$", i)
    if not match:
        continue
    char, c_hex, c_int, _, _, name = match.groups()

    disp_char = char
    out_char = chr(int(c_int))
    name = name.title()
    short_name = name[:name.rindex(" (")]

    data.append({
        "uid": f"unicode_{c_int}",
        "title": f"{disp_char} — {short_name}",
        "subtitle": f"{c_hex} ({c_int}) {name}",
        "arg": out_char,
        "text": {
            "copy": out_char,
            "largetype": out_char
        },
        "icon": {
            "path": "unicode.png"
        },
        "mods": {
            "alt": {
                "subtitle": f"Copy name: {short_name}",
                "arg": short_name,
                "valid": True
            },
            "cmd": {
                "subtitle": f"Copy hex code: {c_hex}",
                "arg": c_hex,
                "valid": True
            },
        },
    })

json.dump({"items": data}, sys.stdout)
