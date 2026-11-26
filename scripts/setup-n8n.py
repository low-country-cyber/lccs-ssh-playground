#!/usr/bin/env python3
"""Load the bundled SSH Playground credentials and inactive n8n workflows."""

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional


PROJECT_DIR = Path(__file__).resolve().parent.parent
WORKFLOWS_DIR = PROJECT_DIR / "workflows"
CREDENTIAL_ID = "lccs-ssh-playground-automation-v1"
CREDENTIAL_NAME = "SSH Playground Automation"
HIDDEN_CREDENTIAL_ID = "lccs-ssh-playground-hidden-automation-v1"
HIDDEN_CREDENTIAL_NAME = "SSH Playground Hidden Automation"
CREDENTIAL_REFS = {
    "main": {"id": CREDENTIAL_ID, "name": CREDENTIAL_NAME},
    "hidden": {"id": HIDDEN_CREDENTIAL_ID, "name": HIDDEN_CREDENTIAL_NAME},
}


def n8n_cli(*args: str, input_text: Optional[str] = None):
    return subprocess.run(
        ["docker", "compose", "exec", "-T", "-u", "node", "n8n", "n8n", *args],
        cwd=PROJECT_DIR,
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )


def existing_workflows():
    result = n8n_cli("export:workflow", "--all", "--output=/dev/stdout")
    if result.returncode != 0:
        if "No workflows found with specified filters" in result.stdout + result.stderr:
            return []
        raise RuntimeError("Cannot list n8n workflows. Check docker compose logs n8n.")

    # n8n's CLI appends a status line after its JSON output. Parse only the
    # first JSON array, without printing workflow contents or user data.
    decoder = json.JSONDecoder()
    for index, character in enumerate(result.stdout):
        if character != "[":
            continue
        try:
            workflows, _ = decoder.raw_decode(result.stdout[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(workflows, list) and all(isinstance(item, dict) for item in workflows):
            return workflows
    raise RuntimeError("Could not read n8n's workflow list.")


def prepared_workflow(path: Path) -> dict:
    match = re.fullmatch(r"(\d{2})-[a-z0-9-]+\.json", path.name)
    if match is None:
        raise ValueError(f"Unexpected workflow filename: {path.name}")
    workflow = json.loads(path.read_text())
    if workflow.get("active") is not False:
        raise ValueError(f"Workflow must be inactive: {path.name}")
    if not any(node.get("type") == "n8n-nodes-base.manualTrigger" for node in workflow["nodes"]):
        raise ValueError(f"Workflow needs a manual trigger: {path.name}")
    workflow["id"] = f"lccsSshPlayground{match.group(1)}"
    for node in workflow["nodes"]:
        if node.get("type") == "n8n-nodes-base.ssh":
            if "credentials" in node:
                raise ValueError(f"Do not embed a credential in {path.name}")
            # This public marker selects a lab target without putting a
            # credential ID into the checked-in workflow JSON. Remove it from
            # the copy sent to n8n so the editor sees only standard node data.
            credential_key = node.pop("labCredential", "main")
            if credential_key not in CREDENTIAL_REFS:
                raise ValueError(f"Unknown labCredential in {path.name}")
            node["credentials"] = {
                "sshPrivateKey": CREDENTIAL_REFS[credential_key]
            }
    return workflow


def main() -> int:
    try:
        paths = sorted(WORKFLOWS_DIR.glob("[0-9][0-9]-*.json"))
        if not paths:
            raise RuntimeError("No bundled workflows were found.")
        workflows = [prepared_workflow(path) for path in paths]
        if len({workflow["id"] for workflow in workflows}) != len(workflows):
            raise ValueError("Bundled workflow numbers must be unique.")
        if len({workflow["name"] for workflow in workflows}) != len(workflows):
            raise ValueError("Bundled workflow names must be unique.")
    except (OSError, KeyError, TypeError, ValueError, RuntimeError) as error:
        print(error, file=sys.stderr)
        return 1

    credential = subprocess.run(
        [sys.executable, str(PROJECT_DIR / "scripts" / "import-credential.py")],
        cwd=PROJECT_DIR,
        text=True,
        capture_output=True,
        check=False,
    )
    if credential.returncode != 0:
        print(credential.stderr.strip() or "Credential import failed.", file=sys.stderr)
        return 1
    print(credential.stdout.strip())

    try:
        present = existing_workflows()
        existing_ids = {workflow.get("id") for workflow in present}
        existing_names = {workflow.get("name") for workflow in present}
        imported = skipped = 0
        for path, workflow in zip(paths, workflows):
            if workflow["id"] in existing_ids or workflow["name"] in existing_names:
                skipped += 1
                continue
            result = n8n_cli(
                "import:workflow",
                "--input=/dev/stdin",
                input_text=json.dumps([workflow]),
            )
            if result.returncode != 0:
                raise RuntimeError(f"Could not import {path.name}. Check docker compose logs n8n.")
            imported += 1
            existing_ids.add(workflow["id"])
            existing_names.add(workflow["name"])
    except (OSError, KeyError, ValueError, RuntimeError) as error:
        print(error, file=sys.stderr)
        return 1

    print(f"Workflows: {imported} imported, {skipped} already present. Refresh n8n to see them.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
