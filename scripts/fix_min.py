import csv
from pathlib import Path

def normalize_row(row, prefix):
    min_key = f"{prefix}_Min"
    sec_key = f"{prefix}_Sec"
    if min_key not in row or sec_key not in row:
        return
    try:
        total_secs = int(row[sec_key])
    except ValueError:
        return
    minutes, seconds = divmod(total_secs, 60)
    row[min_key] = f"{minutes:02d}"
    row[sec_key] = f"{seconds:02d}"

def fix_file(path):
    if not path.is_file():
        return
    with path.open("r", newline="") as source:
        reader = csv.DictReader(source)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    if not rows or not fieldnames:
        return

    prefixes = {
        name.rsplit("_", 1)[0]
        for name in fieldnames
        if name.endswith("_Sec")
    }

    for row in rows:
        for prefix in prefixes:
            normalize_row(row, prefix)

    with path.open("w", newline="") as dest:
        writer = csv.DictWriter(dest, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def main(dir_str: str):
    dir_path = Path(dir_str)
    for csv_path in sorted(dir_path.rglob("*.csv")):
        fix_file(csv_path)

if __name__ == "__main__":
    target_dir = r"D:\\Desktop\\sp_data\\Ziji"  # 需要处理的目录，直接在这里修改路径
    main(target_dir)
