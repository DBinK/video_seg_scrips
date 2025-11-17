import subprocess
from rich import print
from pathlib import Path
import csv
from moviepy import VideoFileClip


# ============================================================
#                  通用工具函数
# ============================================================

def parse_csv_rows(csv_file: Path):
    """读取 CSV 统一生成结构化数据"""
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
    """格式化成 SRT 的时间格式"""
    t = m * 60 + s
    return f"{t//3600:02d}:{(t%3600)//60:02d}:{t%60:02d},000"


def build_output_name(base_name: str, info: dict):
    """统一生成输出视频文件名"""
    return (
        f"{base_name}_{info['index']:03d}_"
        f"{info['start_min']:02d}.{info['start_sec']:02d}_"
        f"{info['end_min']:02d}.{info['end_sec']:02d}.mp4"
    )


def log_clip(info: dict):
    print(f"[处理] index={info['index']:03d} [{info['start_time']}s → {info['end_time']}s]")


# ============================================================
#                  单个数据集的核心处理逻辑
# ============================================================

def locate_dataset_files(folder: Path):
    """返回 (csv_file, video_file, base_name)，自动匹配"""
    csv_files = list(folder.glob("*.csv"))
    if not csv_files:
        print("[错误] 未找到 CSV")
        return None

    csv_file = csv_files[0]
    base_name = csv_file.stem
    video_file = folder / f"{base_name}.mp4"

    if not video_file.exists():
        print(f"[错误] 找到 CSV {csv_file.name}，但没有对应视频 {video_file.name}")
        return None

    return csv_file, video_file, base_name


# ============================================================
#               生成字幕 (一个参数)
# ============================================================

def generate_srt(folder: Path):
    result = locate_dataset_files(folder)
    if result is None:
        return

    csv_file, _, base_name = result
    srt_path = folder / f"{base_name}.srt"
    lines = []

    for idx, info in enumerate(parse_csv_rows(csv_file), start=1):
        t_start = format_srt_time(info["start_min"], info["start_sec"])
        t_end = format_srt_time(info["end_min"], info["end_sec"])

        content = (
            f"index={idx} "
            f"{info['start_min']:02d}:{info['start_sec']:02d} - "
            f"{info['end_min']:02d}:{info['end_sec']:02d}"
        )

        block = f"{idx}\n{t_start} --> {t_end}\n{content}\n"
        lines.append(block)

    srt_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[SRT] 已生成字幕: {srt_path}")


# ============================================================
#                   FFmpeg 极速剪辑 (一个参数)
# ============================================================

def clip_video_ffmpeg(folder: Path):
    result = locate_dataset_files(folder)
    if result is None:
        return

    csv_file, video_file, base_name = result

    for info in parse_csv_rows(csv_file):
        log_clip(info)

        out_name = build_output_name(base_name, info)
        out_path = folder / out_name

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
#                  MoviePy 剪辑 (一个参数)
# ============================================================

def clip_video_moviepy(folder: Path):
    result = locate_dataset_files(folder)
    if result is None:
        return

    csv_file, video_file, base_name = result

    with VideoFileClip(str(video_file)) as video:
        for info in parse_csv_rows(csv_file):
            log_clip(info)
            out_name = build_output_name(base_name, info)
            out_path = folder / out_name

            subclip = video.subclipped(info["start_time"], info["end_time"])
            subclip.write_videofile(
                str(out_path),
                codec="libx264",
                audio_codec="aac",
                threads=8,
                preset="ultrafast",
            )


# ============================================================
#                     处理一个 dataset 目录
# ============================================================

def process_single_data(folder_str: str):
    folder = Path(folder_str)
    print(f"\n[开始处理目录] {folder}")

    generate_srt(folder)
    clip_video_ffmpeg(folder)   # 速度飞快, 需要安装 ffmpeg: winget install ffmpeg / sudo apt install ffmpeg
    # clip_video_moviepy(folder)  # 速度较慢, 

    print(f"[完成] {folder}")


# ============================================================
#               批量处理 dataset 根目录
# ============================================================

def process_multi_dataset(root_str: str):
    root = Path(root_str)
    sub_folders = [p for p in root.iterdir() if p.is_dir()]

    print(f"[发现] {len(sub_folders)} 个子数据集")

    for folder in sub_folders:
        process_single_data(str(folder))


# ============================================================
#                       主入口
# ============================================================

if __name__ == "__main__":
    process_multi_dataset("./dataset")
