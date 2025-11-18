# payment.py
import yaml
from pathlib import Path
from rich import print
from utils import parse_csv_rows, get_dataset_files


def find_price_and_label(seconds: int, rules: list[dict]):
    for r in rules:
        if r["min"] < seconds <= r["max"]:
            return r["price"], r["label"]
    return 0.0, None


def calc_payment_to_yaml(folder_str: str):
    folder = Path(folder_str)
    # print(f"\n[计价] {folder}")

    result = get_dataset_files(folder)
    if result is None:
        return

    csv_file, _, _ = result
    meta_yaml = folder / "meta.yaml"

    if not meta_yaml.exists():
        print("[警告] 未找到 meta.yaml")
        return

    meta = yaml.safe_load(meta_yaml.read_text(encoding="utf-8"))

    rules = [
        {"min": 5-0.1,  "max": 10, "price": 0.5, "label": "5-10s"},
        {"min": 10, "max": 15, "price": 0.8, "label": "10-15s"},
        {"min": 15, "max": 20+0.1, "price": 1.2, "label": "15-20s"},
    ]   # +- 0.1，确保 5 秒和 20 秒的数据能被正确归类到对应的区间内

    count_by_range = {
        r["label"]: {"count": 0, "price": r["price"], "subtotal": 0.0}
        for r in rules
    }

    total_fee = 0
    count = 0

    for info in parse_csv_rows(csv_file):
        used = info["used_time"]
        count += 1

        price, label = find_price_and_label(used, rules)
        if label:
            count_by_range[label]["count"] += 1
            count_by_range[label]["subtotal"] = round(
                count_by_range[label]["count"] * count_by_range[label]["price"], 2
            )
        total_fee += price

    meta["payment"]["count_by_range"] = count_by_range
    meta["payment"]["total_segments"] = count
    meta["payment"]["total_fee"] = round(total_fee, 2)

    meta_yaml.write_text(
        yaml.safe_dump(meta, allow_unicode=True, sort_keys=False),
        encoding="utf-8"
    )

    print(f"[PAY] total_fee={round(total_fee, 2)}")


def get_info_from_yaml(folder_str: str):
    """返回 (name, fee, segments, seconds)"""
    folder = Path(folder_str)
    meta_yaml = folder / "meta.yaml"

    if not meta_yaml.exists():
        print("[警告] 未找到 meta.yaml")
        return None

    meta = yaml.safe_load(meta_yaml.read_text(encoding="utf-8"))

    return (
        folder.name,
        meta["payment"]["total_fee"],
        meta["payment"]["total_segments"],
        meta["payment"]["total_seconds"],
    )


if __name__ == "__main__":
    print("[payment] OK")
