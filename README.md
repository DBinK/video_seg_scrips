# 视频数据集处理工具
[![zread](https://img.shields.io/badge/Ask_Zread-_.svg?style=flat-square&color=00b0aa&labelColor=000000&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTQuOTYxNTYgMS42MDAxSDIuMjQxNTZDMS44ODgxIDEuNjAwMSAxLjYwMTU2IDEuODg2NjQgMS42MDE1NiAyLjI0MDFWNC45NjAxQzEuNjAxNTYgNS4zMTM1NiAxLjg4ODEgNS42MDAxIDIuMjQxNTYgNS42MDAxSDQuOTYxNTZDNS4zMTUwMiA1LjYwMDEgNS42MDE1NiA1LjMxMzU2IDUuNjAxNTYgNC45NjAxVjIuMjQwMUM1LjYwMTU2IDEuODg2NjQgNS4zMTUwMiAxLjYwMDEgNC45NjE1NiAxLjYwMDFaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik00Ljk2MTU2IDEwLjM5OTlIMi4yNDE1NkMxLjg4ODEgMTAuMzk5OSAxLjYwMTU2IDEwLjY4NjQgMS42MDE1NiAxMS4wMzk5VjEzLjc1OTlDMS42MDE1NiAxNC4xMTM0IDEuODg4MSAxNC4zOTk5IDIuMjQxNTYgMTQuMzk5OUg0Ljk2MTU2QzUuMzE1MDIgMTQuMzk5OSA1LjYwMTU2IDE0LjExMzQgNS42MDE1NiAxMy43NTk5VjExLjAzOTlDNS42MDE1NiAxMC42ODY0IDUuMzE1MDIgMTAuMzk5OSA0Ljk2MTU2IDEwLjM5OTlaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik0xMy43NTg0IDEuNjAwMUgxMS4wMzg0QzEwLjY4NSAxLjYwMDEgMTAuMzk4NCAxLjg4NjY0IDEwLjM5ODQgMi4yNDAxVjQuOTYwMUMxMC4zOTg0IDUuMzEzNTYgMTAuNjg1IDUuNjAwMSAxMS4wMzg0IDUuNjAwMUgxMy43NTg0QzE0LjExMTkgNS42MDAxIDE0LjM5ODQgNS4zMTM1NiAxNC4zOTg0IDQuOTYwMVYyLjI0MDFDMTQuMzk4NCAxLjg4NjY0IDE0LjExMTkgMS42MDAxIDEzLjc1ODQgMS42MDAxWiIgZmlsbD0iI2ZmZiIvPgo8cGF0aCBkPSJNNCAxMkwxMiA0TDQgMTJaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik00IDEyTDEyIDQiIHN0cm9rZT0iI2ZmZiIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8L3N2Zz4K&logoColor=ffffff)](https://zread.ai/DBinK/video_seg_scrips)
## 项目结构

```
dataset_tool/
├── main.py          # 主程序入口
├── clip.py          # 视频剪辑和字幕生成
├── metadata.py      # 元数据管理
├── payment.py       # 费用计算
└── utils.py         # 通用工具函数
```

## 快速上手

### 准备数据集

在处理数据之前，需要按照特定的结构组织你的数据集：

```
dataset/                     # 在项目根目录, 新建这个文件夹
└── ziji1/                    # 数据集根目录, 可以是任意名称, 建议交付一次就创建一个文件夹
│   ├── video1_xxx/          # 单个视频数据目录
│   │   ├── video1.mp4       # 视频文件
│   │   └── video1.csv       # 时间戳标记文件
│   ├── video2_xxx/
│   │   ├── video2.mp4
│   │   ├── video2.csv
│   └── ...
├── ziji2/
│   ├── video1_xxx/      
│   │   ├── video1.mp4     
│   │   └── video1.csv      
│   ├── video2_xxx/
│   │   ├── video2.mp4
│   │   ├── video2.csv
│   └── ...
└── ...
```

CSV 文件格式要求：
```csv
Index,Start_Min,Start_Sec,End_Min,End_Sec
1,0,0,0,8
2,0,10,0,15
```


### 指定数据集目录

处理自己的数据，请修改 [main.py](main.py) 中的 `root_list` 列表，将需要处理的数据集目录添加进去。

```python
# main.py

if __name__ == "__main__":

    root_list = [
        # "./dataset/ziji3",
        "./dataset/ziji4",
        "./dataset/ziji5",
        "./dataset/ziji6",
        "./dataset/ziji7",
        "./dataset/ziji8",
    ]

    # 处理每个数据集
    for root_str in root_list:
        process_multi_dataset(root_str)
        generate_report_yaml(root_str)

    # 合并报告
    sum_reports(root_list)

```


### 使用 uv 配置环境 (推荐)

安装 uv:

如果你是 Windows 用户，请使用 PowerShell / CMD 运行以下命令：
```shell 
# Windows
powershell -ExecutionPolicy Bypass -c "irm https://gitee.com/wangnov/uv-custom/releases/latest/download/setup_hooks.ps1 | iex"
```

如果是 macOS 或 Linux 用户，请使用以下命令：
```shell
# macOS / Linux
curl -LsSf https://gitee.com/wangnov/uv-custom/releases/latest/download/setup_hooks.sh | sh
```

安装完后, 可以直接使用 uv 启动项目, 它会自动配置 Python 环境并启动项目

```shell
uv run dataset_tool/main.py
```


### 使用 pip 手动配置环境 (传统方法, 要自己装 Python 环境, 比较麻烦)

先确保电脑已经有 Python 环境, 网上有很多教程, 此处不展开说明如何安装 Python 环境

然后使用 pip 安装所需的依赖项：
```shell
pip install rich pyyaml
```

然后运行主程序：
```shell
python dataset_tool/main.py
```

