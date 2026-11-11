"""Run the bundled uni executable for the current macOS architecture."""

import platform
import subprocess
from pathlib import Path


def run_uni_with_arch(args: list[str]) -> str:
    machine = platform.machine()
    if machine == "x86_64":
        arch = "amd64"
    elif machine == "arm64":
        arch = "arm64"
    else:
        raise RuntimeError(f"Unsupported architecture for uni: {machine}")

    binary = Path(__file__).resolve().with_name(f"uni-{arch}")
    return subprocess.check_output([str(binary), *args]).decode()
