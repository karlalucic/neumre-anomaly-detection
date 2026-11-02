"""Check that the downloaded MVTec AD categories are complete.

Counts images per category and split, compares them with the numbers from the
official dataset description and checks that every defective test image has a
ground truth mask. Prints a table and exits with status 1 on any mismatch.

Usage:
    python scripts/verify_data.py
    python scripts/verify_data.py --root data/mvtec_ad
"""

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ROOT = REPO_ROOT / "data" / "mvtec_ad"

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp"}

# Numbers from Bergmann et al., IJCV 2021.
EXPECTED = {
    "bottle": {"train_good": 209, "test_good": 20, "test_defective": 63, "defect_types": 3},
    "hazelnut": {"train_good": 391, "test_good": 40, "test_defective": 70, "defect_types": 4},
    "tile": {"train_good": 230, "test_good": 33, "test_defective": 84, "defect_types": 5},
}


def list_images(folder: Path) -> list[Path]:
    if not folder.is_dir():
        return []
    return sorted(
        p for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES and not p.name.startswith(".")
    )


def check_category(category_dir: Path) -> tuple[dict[str, int], list[str]]:
    """Return the counts for one category and the list of missing mask files."""
    test_dir = category_dir / "test"
    defect_dirs = sorted(
        d for d in test_dir.iterdir() if d.is_dir() and d.name != "good"
    ) if test_dir.is_dir() else []

    missing_masks = []
    test_defective = 0
    for defect_dir in defect_dirs:
        for image in list_images(defect_dir):
            test_defective += 1
            mask = category_dir / "ground_truth" / defect_dir.name / f"{image.stem}_mask.png"
            if not mask.is_file():
                missing_masks.append(str(mask.relative_to(category_dir.parent)))

    counts = {
        "train_good": len(list_images(category_dir / "train" / "good")),
        "test_good": len(list_images(test_dir / "good")),
        "test_defective": test_defective,
        "defect_types": len(defect_dirs),
    }
    return counts, missing_masks


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help="dataset folder (default: data/mvtec_ad)",
    )
    args = parser.parse_args()
    root = args.root.resolve()

    ok = True
    header = f"{'category':<10} {'check':<15} {'expected':>8} {'found':>8}  status"
    print(header)
    print("-" * len(header))

    for category, expected in EXPECTED.items():
        category_dir = root / category
        if not category_dir.is_dir():
            print(f"{category:<10} {'folder':<15} {'':>8} {'':>8}  MISSING ({category_dir})")
            ok = False
            continue

        counts, missing_masks = check_category(category_dir)
        for key, want in expected.items():
            got = counts[key]
            status = "ok" if got == want else "MISMATCH"
            ok &= got == want
            print(f"{category:<10} {key:<15} {want:>8} {got:>8}  {status}")

        status = "ok" if not missing_masks else f"MISSING {len(missing_masks)}"
        ok &= not missing_masks
        print(f"{category:<10} {'masks':<15} {counts['test_defective']:>8} "
              f"{counts['test_defective'] - len(missing_masks):>8}  {status}")
        for mask in missing_masks[:10]:
            print(f"    missing mask: {mask}")
        if len(missing_masks) > 10:
            print(f"    ... and {len(missing_masks) - 10} more")

    print()
    if ok:
        print("All checks passed.")
    else:
        print("Some checks failed. Re-run scripts/download_data.py after deleting "
              "the affected category folder.")
        sys.exit(1)


if __name__ == "__main__":
    main()
