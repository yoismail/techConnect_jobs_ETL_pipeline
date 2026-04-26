import shutil
import logging
import os
from pathlib import Path

# Logging Configuration
from etl.logger import section, timed

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PROJECT_ROOT / "data/job_listings"
TRANSFORM_PATH = PROJECT_ROOT / "data/job_listings"


def delete_folder(path: Path):
    if path.exists():
        shutil.rmtree(path)
        logging.info(f"🗑️ Deleted folder: {path}")
    else:
        logging.info(f"⚠️ Folder not found (skipped): {path}")


@timed
def wipe(mode: str):
    mode = mode.lower()

    if mode in ("transformed", "all"):
        delete_folder(TRANSFORM_PATH)

    if mode in ("all listings", "all"):
        delete_folder(OUTPUT_PATH)

    logging.info(f"\033[92m🎉✨ Wipe completed for mode: {mode}\033[0m")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Wipe ETL data folders including transformed and/or all listings.")
    parser.add_argument(
        "mode",
        choices=["transformed", "all listings", "all"],
        help="Choose what to wipe."
    )

    args = parser.parse_args()
    wipe(args.mode)
