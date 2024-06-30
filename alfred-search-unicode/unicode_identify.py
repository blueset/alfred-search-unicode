#!/usr/bin/python3

"""
Identify characters from Unicode Descriptions

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
        out: str = run_uni_with_arch(["-q", "identify", query, "-f", "%(char q),%(cpoint q),%(dec q),%(utf8 q),%(xml q),%(name q),%(cat q)"])
        out = out.strip().replace("'''", "\\'").splitlines()
        out = list(csv.reader(out, quotechar="'"))
    except subprocess.CalledProcessError:
        out = []
else:
    out = []

data = []

hexes = []
ints = []
utf8s = []
xmls = []

for i in out:
    char, c_hex, c_int, utf8, xml, name, category = i

    disp_char = char.replace("\\'", "'")
    out_char = chr(int(c_int))
    name = name.title()

    hexes.append(c_hex[2:])
    ints.append(c_int)
    utf8s.append(utf8)
    xmls.append(xml)

    data.append({
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
        "valid": False
    })

for i in range(len(hexes)):
    while hexes[i].startswith("00"):
        hexes[i] = hexes[i][2:]

hex_seq = " ".join(hexes)
int_seq = " ".join(ints)
utf8_seq = " ".join(utf8s)
xml_seq = "".join(xmls)
data = [
    {
        "title": hex_seq,
        "subtitle": "Hex sequence in Unicode",
        "arg": hex_seq,
        "text": {
            "copy": hex_seq,
            "largetype": hex_seq
        },
        "icon": {
            "path": "hex.png"
        },
    }, {
        "title": int_seq,
        "subtitle": "Integer sequence in Unicode",
        "arg": int_seq,
        "text": {
            "copy": int_seq,
            "largetype": int_seq
        },
        "icon": {
            "path": "int.png"
        },
    },
    {
        "title": utf8_seq,
        "subtitle": "UTF-8 hex sequence",
        "arg": utf8_seq,
        "text": {
            "copy": utf8_seq,
            "largetype": utf8_seq
        },
        "icon": {
            "path": "utf8.png"
        },
    },
    {
        "title": xml_seq,
        "subtitle": "XML escape sequence",
        "arg": xml_seq,
        "text": {
            "copy": xml_seq,
            "largetype": xml_seq
        },
        "icon": {
            "path": "xml.png"
        },
    }
] + data
json.dump({"items": data}, sys.stdout)
