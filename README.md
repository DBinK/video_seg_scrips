# 视频数据集处理工具

## 快速上手

### 安装依赖

在开始使用之前，请确保安装了所需的依赖项：

```bash
pip install rich pyyaml
```

或者如果你使用 uv:

```bash
uv sync
```

### 项目结构

```
dataset_tool/
├── main.py          # 主程序入口
├── clip.py          # 视频剪辑和字幕生成
├── metadata.py      # 元数据管理
├── payment.py       # 费用计算
└── utils.py         # 通用工具函数
```

### 准备数据集

在处理数据之前，需要按照特定的结构组织你的数据集：

```
dataset/
└── ziji/                    # 数据集根目录, 可以是任意名称
    ├── video1_xxx/          # 单个视频数据目录
    │   ├── video1.mp4       # 视频文件
    │   └── video1.csv       # 时间戳标记文件
    └── video2_xxx/
        ├── video2.mp4
        └── video2.csv
```

CSV 文件格式要求：
```csv
Index,Start_Min,Start_Sec,End_Min,End_Sec
1,0,0,0,8
2,0,10,0,15
```

### 使用方法

#### 直接运行主程序


```bash
cd dataset_tool
python main.py
```

默认情况下，程序会处理 `./dataset/ziji` 目录下的数据集。

如需处理其他目录，请修改 [main.py](main.py) 中的调用参数。
```
