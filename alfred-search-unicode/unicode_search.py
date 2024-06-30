#!/usr/bin/python3

"""
Search for Unicode Descriptions

uni binary from: https://github.com/arp242/uni
"""

import sys
import re
import subprocess
import json
import csv


def run_uni_with_arch(args: list[str]) -> str:
    try:
        return subprocess.check_output(
            ["./uni-amd64", *args]
        ).decode()
    except OSError:
        try:
            return subprocess.check_output(
                ["./uni-arm64", *args]
            ).decode()
        except OSError:
            return ""
        

if len(sys.argv) >= 2:
    query = sys.argv[1]

    try:
        out: str = run_uni_with_arch(
            ["-q", "search", query, "-f",
                "%(char q),%(cpoint q),%(dec q),%(name q),%(cat q)", ]
        )

        out = out.strip().splitlines()
    except subprocess.CalledProcessError:
        out = []

    if re.match(r"((U\+)?[0-9A-Fa-f]+ ?)+$", query):
        pr_out: str = run_uni_with_arch([
            "-q", "print", "-f", "%(char q),%(cpoint q),%(dec q),%(name q),%(cat q)"
        ] + query.split())
        out = pr_out.strip().splitlines() + out
    
    out = list(csv.reader(out, quotechar="'"))
else:
    out = []

data = []

for i in out[:20]:
    char, c_hex, c_int, name, category = i

    disp_char = char
    try:
        out_char = chr(int(c_int))
    except ValueError:
        out_char = "�"
    name = name.title()

    data.append({
        "uid": f"unicode_{c_int}",
        "title": f"{disp_char} — {name}",
        "subtitle": f"{c_hex} ({c_int}) {category}",
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
                "subtitle": f"Copy name: {name}",
                "arg": name,
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
