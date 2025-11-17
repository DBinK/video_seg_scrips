# main.py
from rich import print
from pathlib import Path

from utils import list_subfolders
from metadata import generate_metadata
from payment import calc_payment_to_yaml, get_info_from_yaml
from clip import clip_video_ffmpeg, generate_srt
import yaml


def process_multi_dataset(root_str: str):
    sub_folders = list_subfolders(root_str)

    for folder in sub_folders:
        print(f"\n[开始处理] {folder}")

        generate_srt(str(folder))
        # clip_video_ffmpeg(str(folder))
        generate_metadata(str(folder))
        calc_payment_to_yaml(str(folder))

        print(f"[完成] {folder}")


def generate_all_fee_yaml(root_str: str):
    root = Path(root_str)
    sub_folders = list_subfolders(root_str)

    result_list = []
    total_payment = 0.0

    for folder in sub_folders:
        info = get_info_from_yaml(str(folder))
        if info is None:
            continue

        name, fee, segments, seconds = info

        result_list.append({
            "name": name,
            "fee": fee,
            "segments": segments,
            "seconds": seconds,
        })

        total_payment += fee

    out_yaml = root / "report.yaml"

    data = {
        "root_dir": root.name,
        "total_payment": round(total_payment, 2),
        "datasets": result_list,
    }

    out_yaml.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8"
    )

    print(f"[汇总] 已生成: {out_yaml}")
    print(f"[总计] {total_payment} CNY")


if __name__ == "__main__":
    # 手动测试
    process_multi_dataset("./dataset/ziji")
    generate_all_fee_yaml("./dataset/ziji")
