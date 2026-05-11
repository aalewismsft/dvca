#!/usr/bin/env python3
import datetime as dt
import json
import os
import sys
from pathlib import Path

REQUIRED_KEYS = {"id", "tool", "path", "owner", "expires_on", "status", "reason"}


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    exceptions_file = repo_root / "security" / "exceptions.json"

    if not exceptions_file.exists():
        print(f"::error::Missing exceptions file: {exceptions_file}")
        return 1

    try:
        data = json.loads(exceptions_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"::error::Invalid JSON in {exceptions_file}: {exc}")
        return 1

    exceptions = data.get("exceptions", [])
    if not isinstance(exceptions, list):
        print("::error::`exceptions` must be a list")
        return 1

    today = dt.date.today()
    failed = False

    for idx, item in enumerate(exceptions):
        if not isinstance(item, dict):
            print(f"::error::Exception #{idx} must be an object")
            failed = True
            continue

        missing = REQUIRED_KEYS - set(item.keys())
        if missing:
            print(f"::error::Exception {item.get('id', idx)} missing fields: {sorted(missing)}")
            failed = True

        try:
            expires = dt.date.fromisoformat(str(item.get("expires_on", "")))
        except ValueError:
            print(f"::error::Exception {item.get('id', idx)} has invalid expires_on format; expected YYYY-MM-DD")
            failed = True
            continue

        if item.get("status") == "active" and expires < today:
            print(
                f"::error::Exception {item.get('id', idx)} expired on {expires.isoformat()} "
                f"(owner: {item.get('owner', 'unknown')})"
            )
            failed = True

    mode = os.environ.get("SECURITY_ENFORCEMENT_MODE", "monitor")
    if mode == "monitor" and failed:
        print("::warning::Exception validation failed in monitor mode; convert to enforce mode to fail builds.")
        return 0

    if failed:
        print("::error::Exception validation failed.")
        return 1

    print("Security exceptions validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
