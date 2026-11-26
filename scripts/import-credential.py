#!/usr/bin/env python3
"""Import the Low Country Cyber Solutions SSH Playground credential into n8n.

Run this on the host after creating the lab's n8n owner account. The generated
automation private key is passed to the local n8n CLI without printing it.
"""

import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent


def main() -> int:
    # This is the automation identity, not the learner's terminal SSH key.
    key_path = PROJECT_DIR / "state" / "keys" / "automation"
    if not key_path.is_file():
        print("Lab key is missing. Run docker compose up -d first.", file=sys.stderr)
        return 1

    # n8n needs its owner account before a personal credential can be imported.
    try:
        with urllib.request.urlopen("http://127.0.0.1:5680/rest/settings", timeout=5) as response:
            settings = json.load(response)["data"]
    except (urllib.error.URLError, KeyError, ValueError) as error:
        print(f"Cannot check n8n setup: {error}", file=sys.stderr)
        return 1

    if settings["userManagement"]["showSetupOnFirstLoad"]:
        print("Create the owner account at http://localhost:5680 first.", file=sys.stderr)
        return 1

    # Inside Compose, n8n reaches the target by service name on port 22.
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

    # Pass the credential through stdin, avoiding a key in command arguments or
    # a temporary JSON file. Capture CLI output without exposing the key.
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
