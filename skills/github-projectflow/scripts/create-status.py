#!/usr/bin/env python3
"""create-status.py — Verify the board's status mapping: the `Status` field exists and has
the options `Todo`, `In Progress`, `Done`, `Blocked`.

Default: check & report (exit 0 = PASS, exit 1 = FAIL).
--fix: repair automatically (create the missing field/options; existing options are kept).

Usage:
  python3 scripts/create-status.py              # board number from .github/projectflow.json
  python3 scripts/create-status.py --number 3   # manual override
  python3 scripts/create-status.py --fix        # auto-fix
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import (  # noqa: E402
    REQUIRED_STATUSES, CONFIG_FILE, repo_info, get_project,
    ensure_status_field, load_config, require_gh,
)


def main():
    ap = argparse.ArgumentParser(description="Verify the project board Status field")
    ap.add_argument("--number", type=int, default=None,
                    help=f"Board number (default: from {CONFIG_FILE})")
    ap.add_argument("--fix", action="store_true", help="Auto-fix anything missing")
    args = ap.parse_args()

    require_gh()
    if args.number is None:
        config = load_config()
        if not config or "project_number" not in config:
            print(f"No --number given and {CONFIG_FILE} not found. "
                  "Run detect-board.py or create-board.py first.")
            sys.exit(1)
        args.number = config["project_number"]
        print(f"Using board #{args.number} from {CONFIG_FILE}")
    info = repo_info()
    proj, status_field = get_project(info["owner"], args.number, info["is_org"])

    if status_field is None:
        print("FAIL: field 'Status' not found.")
        if args.fix:
            ensure_status_field(proj["id"], None)
            print("FIXED: Status field created with all options.")
            return
        print(f"Fix: python3 scripts/create-status.py --number {args.number} --fix")
        sys.exit(1)

    have = [o["name"] for o in status_field.get("options", [])]
    missing = [s for s in REQUIRED_STATUSES if s not in have]
    if missing:
        print(f"FAIL: missing options: {', '.join(missing)} (found: {', '.join(have)})")
        if args.fix:
            ensure_status_field(proj["id"], status_field)
            print("FIXED: options added (existing options preserved).")
            return
        print(f"Fix: python3 scripts/create-status.py --number {args.number} --fix")
        sys.exit(1)

    print(f"PASS: Status field complete → {', '.join(have)}")


if __name__ == "__main__":
    main()
