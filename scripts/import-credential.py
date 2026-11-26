#!/usr/bin/env python3
"""Import the lab SSH credential into the bundled n8n after owner setup."""

import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent


def main() -> int:
    key_path = PROJECT_DIR / "state" / "keys" / "automation"
    if not key_path.is_file():
        print("Lab key is missing. Run docker compose up -d first.", file=sys.stderr)
        return 1

    try:
        with urllib.request.urlopen("http://127.0.0.1:5680/rest/settings", timeout=5) as response:
            settings = json.load(response)["data"]
    except (urllib.error.URLError, KeyError, ValueError) as error:
        print(f"Cannot check n8n setup: {error}", file=sys.stderr)
        return 1

    if settings["userManagement"]["showSetupOnFirstLoad"]:
        print("Create the owner account at http://localhost:5680 first.", file=sys.stderr)
        return 1

    credential = {
        "id": "lccs-ssh-playground-automation-v1",
        "name": "SSH Playground Automation",
        "type": "sshPrivateKey",
        "data": {
            "host": "ssh-target",
            "port": 22,
            "username": "automation",
            "privateKey": key_path.read_text(),
            "passphrase": "",
        },
    }

    result = subprocess.run(
        ["docker", "compose", "exec", "-T", "-u", "node", "n8n", "n8n", "import:credentials", "--input=/dev/stdin"],
        cwd=PROJECT_DIR,
        input=json.dumps([credential]),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0 or "Successfully imported 1 credential." not in result.stdout:
        print("Credential import failed. Check n8n owner setup and Compose logs.", file=sys.stderr)
        return 1

    print("Imported SSH Playground Automation into the owner’s personal credentials. Refresh n8n to see it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
