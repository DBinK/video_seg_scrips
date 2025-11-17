from datetime import datetime
import yaml
import subprocess
from rich import print
from pathlib import Path
import csv



# ============================================================
#                  基础工具（不改）
# ============================================================

def parse_csv_rows(csv_file: Path):
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


def format_srt_time(m, s):
    t = m * 60 + s
    return f"{t//3600:02d}:{(t%3600)//60:02d}:{t%60:02d},000"


def build_output_name(base_name: str, info: dict):
    return (
        f"{base_name}_{info['index']:03d}_"
        f"{info['start_min']:02d}.{info['start_sec']:02d}_"
        f"{info['end_min']:02d}.{info['end_sec']:02d}.mp4"
    )


def log_clip(info: dict):
    print(f"[处理] index={info['index']:03d} [{info['start_time']}s → {info['end_time']}s]")



# ============================================================
#       通用数据定位（自动找到 CSV + 视频 + base_name）
# ============================================================

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



def generate_metadata(folder_str: str):
    """在数据目录下自动生成 metadata.yaml，如果已存在则跳过。"""
    folder = Path(folder_str)

    # 查找 CSV
    csv_files = list(folder.glob("*.csv"))
    if not csv_files:
        print(f"[错误] 未找到 CSV：{folder}")
        return

    csv_file = csv_files[0]
    base_name = csv_file.stem
    meta_path = folder / "metadata.yaml"

    # 已存在就跳过
    if meta_path.exists():
        print(f"[跳过] metadata 已存在: {meta_path}")
        return

    # 计算总时长
    total_seconds = 0
    with csv_file.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            start = int(row["Start_Min"]) * 60 + int(row["Start_Sec"])
            end = int(row["End_Min"]) * 60 + int(row["End_Sec"])
            used = end - start
            total_seconds += used

    # metadata 结构
    meta = {
        "dataset_name": base_name,
        "description": "",     # 供你填写描述
        "annotator": "",       # 可空
        "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "total_seconds": total_seconds,

        "payment": {
            "count_by_range": {},         # 计费后填
            "total_segments": 0,          # 计费后填
            "total_fee": 0,               # 计费后填
        }
    }

    # 写入文件
    meta_path.write_text(yaml.safe_dump(meta, allow_unicode=True), encoding="utf-8")

    print(f"[META] 已生成 metadata: {meta_path}")
    print(f"[META] 采集有效总时长: {total_seconds} 秒")


# ============================================================
#                        计价
# ============================================================

def find_price_and_label(seconds: int, rules: list[dict]):
    for r in rules:
        if r["min"] <= seconds < r["max"]:
            return r["price"], r["label"]
    return 0.0, None



def calc_payment(folder_str: str):
    folder = Path(folder_str)
    print(f"\n[计价] {folder}")

    result = get_dataset_files(folder)
    if result is None:
        return

    csv_file, _, base_name = result

    meta_yaml = folder / "metadata.yaml"
    if not meta_yaml.exists():
        print("[警告] 未找到 metadata.yaml")
        return

    meta = yaml.safe_load(meta_yaml.read_text(encoding="utf-8"))
    rules = [
        {"min": 5,  "max": 10, "price": 0.5, "label": "5-10s"},
        {"min": 10, "max": 15, "price": 0.8, "label": "10-15s"},
        {"min": 15, "max": 20, "price": 1.2, "label": "15-20s"},
    ]

    # 初始化统计结构
    count_by_range = {
        r["label"]: {"count": 0, "price": r["price"], "subtotal": 0.0}
        for r in rules
    }

    total_fee = 0
    total_sec = 0
    count = 0

    for info in parse_csv_rows(csv_file):
        used = info["used_time"]
        total_sec += used
        count += 1

        price, label = find_price_and_label(used, rules)
        if label:
            count_by_range[label]["count"] += 1
            count_by_range[label]["subtotal"] = round(
                count_by_range[label]["count"] * count_by_range[label]["price"], 2
            )
        total_fee += price

    # 写回 metadata
    meta["payment"]["count_by_range"] = count_by_range
    meta["payment"]["total_segments"] = count
    meta["payment"]["total_fee"] = round(total_fee, 2)

    meta_yaml.write_text(yaml.safe_dump(meta, allow_unicode=True), encoding="utf-8")

    print(f"[PAY] updated {meta_yaml.name}: {count} segments, total fee {total_fee} RMB")



# ============================================================
#                      生成字幕
# ============================================================

def generate_srt(folder_str: str):
    folder = Path(folder_str)
    print(f"\n[SRT] {folder}")

    result = get_dataset_files(folder)
    if result is None:
        return

    csv_file, _, base_name = result
    srt_path = folder / f"{base_name}.srt"

    lines = []

    for idx, info in enumerate(parse_csv_rows(csv_file), start=1):
        t_start = format_srt_time(info["start_min"], info["start_sec"])
        t_end = format_srt_time(info["end_min"], info["end_sec"])

        content = f"index={idx} {info['start_min']:02d}:{info['start_sec']:02d} - {info['end_min']:02d}:{info['end_sec']:02d}"

        block = f"{idx}\n{t_start} --> {t_end}\n{content}\n"
        lines.append(block)

    srt_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[SRT] 已生成字幕: {srt_path}")



# ============================================================
#                  FFmpeg 极速剪辑
# ============================================================

def clip_video_ffmpeg(folder_str: str):
    folder = Path(folder_str)
    print(f"\n[剪辑] {folder}")

    result = get_dataset_files(folder)
    if result is None:
        return

    csv_file, video_file, base_name = result

    seg_dir = folder / f"{base_name}_seg"
    seg_dir.mkdir(exist_ok=True)

    for info in parse_csv_rows(csv_file):
        log_clip(info)

        out_name = build_output_name(base_name, info)
        out_path = seg_dir / out_name

        cmd = [
            "ffmpeg",
            "-y",
            "-ss", str(info["start_time"]),
            "-to", str(info["end_time"]),
            "-i", str(video_file),
            "-c:v", "copy",
            "-c:a", "copy",
            str(out_path),
        ]

        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)



# ============================================================
#                  单个数据集处理
# ============================================================

def process_single_dataset(folder_str: str):
    print(f"\n[开始处理] {folder_str}")

    generate_srt(folder_str)
    # clip_video_ffmpeg(folder_str)
    generate_metadata(folder_str)
    calc_payment(folder_str)

    print(f"[完成] {folder_str}")



# ============================================================
#                 批量处理 dataset 根目录
# ============================================================

def process_multi_dataset(root_str: str):
    root = Path(root_str)
    sub_folders = [p for p in root.iterdir() if p.is_dir()]

    print(f"[发现] {len(sub_folders)} 个子目录")
    for folder in sub_folders:
        process_single_dataset(str(folder))



# ============================================================
#                       主入口
# ============================================================

if __name__ == "__main__":
    # process_multi_dataset("./dataset/ziji")
    process_single_dataset("./dataset/ziji/MJ1_205")
