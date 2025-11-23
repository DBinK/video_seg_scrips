# 视频数据集处理工具

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

默认情况下，程序会处理项目根目录下 `dataset/ziji1` 目录的数据集。

处理自己的数据，请修改 [main.py](main.py) 中的调用参数。

```python
# main.py

# ... main.py 中的代码

if __name__ == "__main__":

    root_dir = "dataset/ziji1"  # 数据集目录

    # 处理多个数据
    process_multi_dataset(root_dir)

    # 生成总报告
    generate_all_fee_yaml(root_dir)

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

