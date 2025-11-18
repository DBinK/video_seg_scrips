# main.py
from rich import print
from pathlib import Path

from utils import list_subfolders
from metadata import generate_metadata
from payment import calc_payment_to_yaml, get_info_from_yaml
from clip import clip_video_ffmpeg, generate_srt
import yaml


def process_multi_dataset(root_str: str):
    """
    处理指定根目录下的所有数据集子目录
    
    对每个子目录执行以下操作：
    1. 生成字幕文件(.srt)
    2. 生成或更新元数据文件(meta.yaml)
    3. 根据剪辑片段计算费用并更新元数据
    
    Args:
        root_str (str): 包含多个数据集的根目录路径
    """

    sub_folders = list_subfolders(root_str)

    for folder in sub_folders:
        print(f"\n[开始处理] {folder}")

        # 生成字幕
        generate_srt(str(folder))

        # 裁剪视频
        # clip_video_ffmpeg(str(folder))

        # 生成元数据
        generate_metadata(str(folder))

        # 计算费用写入元数据
        calc_payment_to_yaml(str(folder))

        print(f"[完成] {folder}")


def generate_report_yaml(root_str: str):
    """
    收集指定根目录下所有数据集的费用信息并生成总报告
    
    遍历所有子目录，从各自的meta.yaml文件中提取费用信息，
    汇总后生成一个总的报告文件(report.yaml)，包含各数据集的费用详情和总费用。
    
    Args:
        root_str (str): 包含多个数据集的根目录路径
    """
    
    root = Path(root_str)
    sub_folders = list_subfolders(root_str)

    result_list = []
    total_payment = 0.0
    total_clips   = 0

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
        total_clips   += segments

    out_yaml = root / "report.yaml"
    total_datasets = len(sub_folders)
    total_payment = round(total_payment, 2)

    data = {
        "root_dir": str(root),
        "total_datasets": total_datasets,
        "total_clips": total_clips,
        "total_payment": total_payment,
        "datasets": result_list,
    }

    out_yaml.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8"
    )

    print("\n所有数据处理完毕")
    print(f"[总计] {total_datasets} 个视频文件")
    print(f"[总计] {total_clips} 个片段")
    print(f"[总计] {total_payment} CNY")
    print(f"[汇总] 已生成报告: {out_yaml}")


if __name__ == "__main__":

    root_dir = "./dataset/ziji2"   # 数据集目录

    # 处理多个数据
    process_multi_dataset(root_dir)

    # 生成总报告
    generate_report_yaml(root_dir)

