"""Download the MVTec AD categories used in this project from Kaggle.

Kaggle serves the dataset as a single archive, so the script downloads it once,
extracts only the selected categories into data/mvtec_ad/<category>/ and
deletes the archive. Categories that are already present are skipped.

Credentials are read by the Kaggle API from ~/.kaggle/kaggle.json, from the
KAGGLE_USERNAME and KAGGLE_KEY environment variables, or from a new-style API
token (~/.kaggle/access_token or KAGGLE_API_TOKEN).

Usage:
    python scripts/download_data.py
    python scripts/download_data.py --categories bottle tile
"""

import argparse
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

KAGGLE_DATASET = "ipythonx/mvtec-ad"
CATEGORIES = ["bottle", "hazelnut", "tile"]
SPLITS = ["train", "test", "ground_truth"]

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DEST = REPO_ROOT / "data" / "mvtec_ad"


def is_present(category_dir: Path) -> bool:
    """A category counts as present if all split folders exist and are not empty."""
    return all(
        (category_dir / split).is_dir() and any((category_dir / split).iterdir())
        for split in SPLITS
    )


def download_archive(download_dir: Path) -> Path:
    """Download the dataset archive from Kaggle and return its path."""
    # Imported here so that --help works without Kaggle credentials.
    from kaggle.api.kaggle_api_extended import KaggleApi

    api = KaggleApi()
    api.authenticate()  # prints help and exits if no credentials are found
    print(f"Downloading {KAGGLE_DATASET} from Kaggle (about 5 GB)...")
    api.dataset_download_files(KAGGLE_DATASET, path=str(download_dir), quiet=False)

    archives = list(download_dir.glob("*.zip"))
    if len(archives) != 1:
        sys.exit(f"Expected one zip archive in {download_dir}, found {len(archives)}.")
    return archives[0]


def extract_categories(archive: Path, categories: list[str], dest: Path) -> None:
    """Extract only the given categories from the archive into dest/<category>/.

    Each category is first extracted into a temporary folder and then moved into
    place, so an interrupted run never leaves a half-extracted category behind.
    """
    with zipfile.ZipFile(archive) as zf:
        members = zf.infolist()
        for category in categories:
            tmp_dir = dest / f".{category}.partial"
            shutil.rmtree(tmp_dir, ignore_errors=True)
            count = 0
            for member in members:
                if member.is_dir():
                    continue
                parts = Path(member.filename).parts
                if ".." in parts:
                    continue
                # Find "<category>/<split>/..." anywhere in the path, so a
                # top-level folder inside the archive does not matter.
                for i in range(len(parts) - 1):
                    if parts[i] == category and parts[i + 1] in SPLITS:
                        target = tmp_dir.joinpath(*parts[i + 1 :])
                        target.parent.mkdir(parents=True, exist_ok=True)
                        with zf.open(member) as src, open(target, "wb") as dst:
                            shutil.copyfileobj(src, dst)
                        count += 1
                        break
            if count == 0:
                shutil.rmtree(tmp_dir, ignore_errors=True)
                sys.exit(f"Category '{category}' not found in {archive.name}.")
            final_dir = dest / category
            shutil.rmtree(final_dir, ignore_errors=True)
            tmp_dir.rename(final_dir)
            print(f"  {category}: extracted {count} files")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--categories",
        nargs="+",
        default=CATEGORIES,
        help=f"categories to extract (default: {' '.join(CATEGORIES)})",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=DEFAULT_DEST,
        help="output folder (default: data/mvtec_ad)",
    )
    args = parser.parse_args()

    dest = args.dest.resolve()
    dest.mkdir(parents=True, exist_ok=True)

    missing = [c for c in args.categories if not is_present(dest / c)]
    for category in args.categories:
        if category not in missing:
            print(f"  {category}: already present, skipping")
    if not missing:
        print("All categories are present. Nothing to do.")
        return

    # The archive goes into a temporary folder next to the data, which is
    # removed afterwards even if the download or extraction fails.
    with tempfile.TemporaryDirectory(dir=dest, prefix=".download-") as tmp:
        archive = download_archive(Path(tmp))
        print(f"Extracting {', '.join(missing)} into {dest}")
        extract_categories(archive, missing, dest)
    print("Done. The archive was deleted.")


if __name__ == "__main__":
    main()
