# metadata.py
from datetime import datetime
from pathlib import Path
import yaml
from rich import print
from csv import DictReader


def generate_metadata(folder_str: str):
    folder = Path(folder_str)

    csv_files = list(folder.glob("*.csv"))
    if not csv_files:
        print(f"[错误] 未找到 CSV：{folder}")
        return

    csv_file = csv_files[0]
    base_name = csv_file.stem
    meta_path = folder / "meta.yaml"

    if meta_path.exists():
        print(f"[注意] meta.yaml 已存在: {meta_path}, 将被覆盖")

    total_seconds = 0
    with csv_file.open("r", encoding="utf-8") as f:
        reader = DictReader(f)
        for row in reader:
            start = int(row["Start_Min"]) * 60 + int(row["Start_Sec"])
            end = int(row["End_Min"]) * 60 + int(row["End_Sec"])
            total_seconds += (end - start)

    meta = {
        "dataset_name": base_name,
        "annotator": "",
        "description": "",
        "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "payment": {
            "count_by_range": {},
            "total_seconds": total_seconds,
            "total_segments": 0,
            "total_fee": 0,
        }
    }

    meta_path.write_text(
        yaml.safe_dump(meta, allow_unicode=True, sort_keys=False),
        encoding="utf-8"
    )

    print(f"[META] 已生成 meta.yaml: {meta_path}")
    print(f"[META] 有效数据总时长: {total_seconds} 秒")


if __name__ == "__main__":
    print("[metadata] OK")
