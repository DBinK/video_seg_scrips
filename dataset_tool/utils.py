# utils.py
from pathlib import Path
from rich import print
import csv

# ================================
#         基础通用工具
# ================================

def parse_csv_rows(csv_file: Path):
    """读取 CSV 行为结构化 dict"""
    with csv_file.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            index = int(row["Index"])
            start_min = int(row["Start_Min"])
            start_sec = int(row["Start_Sec"])
            end_min = int(row["End_Min"])
            end_sec = int(row["End_Sec"])

            start_time = start_min * 60 + start_sec
            end_time = end_min * 60 + end_sec

            yield {
                "index": index,
                "start_min": start_min,
                "start_sec": start_sec,
                "end_min": end_min,
                "end_sec": end_sec,
                "start_time": start_time,
                "end_time": end_time,
                "used_time": end_time - start_time,
            }


def list_subfolders(root_str: str) -> list[Path]:
    """返回 root 下的所有一级子目录"""
    root = Path(root_str)
    sub_folders = [p for p in root.iterdir() if p.is_dir()]
    print(f"[发现] {len(sub_folders)} 个子目录")
    return sub_folders


def get_dataset_files(folder: Path):
    csv_files = list(folder.glob("*.csv"))
    if not csv_files:
        print("[错误] 未找到 CSV")
        return None

    csv_file = csv_files[0]
    base_name = csv_file.stem
    video_file = folder / f"{base_name}.mp4"

    if not video_file.exists():
        print(f"[错误] 找到 CSV {csv_file.name}，但未找到视频 {video_file.name}")
        return None

    return csv_file, video_file, base_name


# ================================
#      测试入口（可选）
# ================================
if __name__ == "__main__":
    print("[utils] OK")
