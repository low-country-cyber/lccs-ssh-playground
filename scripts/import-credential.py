#!/usr/bin/env python3
"""Import the Low Country Cyber Solutions SSH Playground credentials into n8n.

Run this on the host after creating the lab's n8n owner account. The generated
automation private keys are passed to the local n8n CLI without printing them.
"""

import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
CREDENTIAL_SPECS = (
    (
        "ssh-target",
        "automation",
        "lccs-ssh-playground-automation-v1",
        "SSH Playground Automation",
    ),
    (
        "hidden-target",
        "hidden-automation",
        "lccs-ssh-playground-hidden-automation-v1",
        "SSH Playground Hidden Automation",
    ),
    (
        "ssh-target",
        "report-only",
        "lccs-ssh-playground-report-only-v1",
        "SSH Playground Report Only",
    ),
)
REPORT_KEY_OPTIONS = 'restrict,command="/usr/local/bin/lab-report.sh" '


def main() -> int:
    # The learner's console key never enters n8n. Check the exact public-key
    # lists on both running targets before importing any private halves. The
    # first target has a plain automation key and a restricted report key.
    key_paths = []
    public_keys = {}
    for service, key_name, _, _ in CREDENTIAL_SPECS:
        key_path = PROJECT_DIR / "state" / "keys" / key_name
        public_key_path = PROJECT_DIR / "state" / "keys" / f"{key_name}.pub"
        if not key_path.is_file() or not public_key_path.is_file():
            print("Lab key is missing. Run docker compose up -d first.", file=sys.stderr)
            return 1
        public_keys[key_name] = public_key_path.read_text().strip()
        key_paths.append(key_path)

    expected_keys = {
        "ssh-target": [
            public_keys["automation"],
            REPORT_KEY_OPTIONS + public_keys["report-only"],
        ],
        "hidden-target": [public_keys["hidden-automation"]],
    }
    for service, expected in expected_keys.items():
        target_key = subprocess.run(
            ["docker", "compose", "exec", "-T", service, "cat", "/home/automation/.ssh/authorized_keys"],
            cwd=PROJECT_DIR,
            text=True,
            capture_output=True,
            check=False,
        )
        if target_key.returncode != 0:
            print(f"Cannot read the running {service}. Run docker compose up -d first.", file=sys.stderr)
            return 1
        if target_key.stdout.splitlines() != expected:
            print(
                f"The running {service} uses different automation keys. Another playground clone may be active. "
                "Use one clone for this lab.",
                file=sys.stderr,
            )
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

    # Inside Compose, n8n reaches each target directly by its service name.
    credentials = []
    for (service, _, credential_id, name), key_path in zip(CREDENTIAL_SPECS, key_paths):
        credentials.append({
            "id": credential_id,
            "name": name,
            "type": "sshPrivateKey",
            "data": {
                "host": service,
                "port": 22,
                "username": "automation",
                "privateKey": key_path.read_text(),
                "passphrase": "",
            },
        })

    # Pass credentials through stdin, avoiding keys in command arguments
    # or a temporary JSON file. Capture CLI output without exposing the keys.
    result = subprocess.run(
        ["docker", "compose", "exec", "-T", "-u", "node", "n8n", "n8n", "import:credentials", "--input=/dev/stdin"],
        cwd=PROJECT_DIR,
        input=json.dumps(credentials),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0 or "Successfully imported 3 credentials." not in result.stdout:
        print("Credential import failed. Check n8n owner setup and Compose logs.", file=sys.stderr)
        return 1

    print("Imported all three SSH Playground automation credentials. Refresh n8n to see them.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
