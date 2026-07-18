"""Verify HF_TOKEN from .env can access FlyRank/internship-warehouse.

Prints diagnostics only — never prints the token.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"
DATASET_ID = "FlyRank/internship-warehouse"


def load_token() -> str | None:
    if not ENV_PATH.exists():
        return None
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("HF_TOKEN="):
            return line.split("=", 1)[1].strip()
    return None


def main() -> int:
    token = load_token()
    if not token:
        print("FAIL: .env missing or HF_TOKEN not set")
        print("FIX: create .env with HF_TOKEN=hf_... (read token from HF settings)")
        return 1

    if not token.startswith("hf_") or len(token) < 20:
        print("FAIL: HF_TOKEN format looks invalid (expected hf_... read token)")
        return 1

    print("OK: HF_TOKEN present in .env with valid prefix")

    try:
        from huggingface_hub import HfApi, hf_hub_download
    except ImportError:
        print("FAIL: huggingface_hub not installed")
        print("FIX: pip install -r requirements.txt")
        return 1

    api = HfApi(token=token)

    try:
        who = api.whoami()
    except Exception as exc:
        print(f"FAIL: token rejected by Hugging Face ({type(exc).__name__})")
        print("FIX: create a new READ token at https://huggingface.co/settings/tokens")
        return 1

    username = who.get("name") or who.get("fullname") or "unknown"
    print(f"OK: token authenticates as Hugging Face user '{username}'")

    try:
        info = api.dataset_info(DATASET_ID)
    except Exception as exc:
        print(f"FAIL: cannot read dataset metadata ({type(exc).__name__})")
        print(
            "FIX: open https://huggingface.co/datasets/FlyRank/internship-warehouse "
            "while logged in as this account, request access, and accept the terms"
        )
        return 1

    print(f"OK: dataset metadata readable (gated={info.gated}, private={info.private})")

    try:
        path = hf_hub_download(
            repo_id=DATASET_ID,
            repo_type="dataset",
            filename="dim_clients.parquet",
            token=token,
        )
    except Exception as exc:
        print(f"FAIL: cannot download gated file ({type(exc).__name__})")
        print(
            "FIX: ensure this HF account has approved access to the gated dataset "
            "(same account that owns the token in .env)"
        )
        return 1

    size = Path(path).stat().st_size
    print(f"OK: downloaded dim_clients.parquet ({size:,} bytes) from {DATASET_ID}")
    print("SETUP: correct — .env token can access the warehouse release")
    return 0


if __name__ == "__main__":
    sys.exit(main())
