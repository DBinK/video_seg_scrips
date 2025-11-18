# clip.py
import subprocess
from pathlib import Path
from rich import print
from utils import parse_csv_rows, get_dataset_files


def build_output_name(base: str, info: dict):
    return (
        f"{base}_{info['index']:03d}_"
        f"{info['start_min']:02d}.{info['start_sec']:02d}_"
        f"{info['end_min']:02d}.{info['end_sec']:02d}.mp4"
    )


def log_clip(info: dict):
    print(f"[处理] index={info['index']:03d} [{info['start_time']}s → {info['end_time']}s]")


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
            "ffmpeg", "-y",
            "-ss", str(info["start_time"]),
            "-to", str(info["end_time"]),
            "-i", str(video_file),
            "-c:v", "copy",
            "-c:a", "copy",
            str(out_path),
        ]

        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


##################### 字幕 ######################
          
def format_srt_time(m, s):
    t = m * 60 + s
    return f"{t//3600:02d}:{(t%3600)//60:02d}:{t%60:02d},000"


def generate_srt(folder_str: str):
    folder = Path(folder_str)
    # print(f"\n[SRT] {folder}")

    result = get_dataset_files(folder)
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


if __name__ == "__main__":
    print("[clip] OK")
    print("请使用 main.py 运行本模块")
