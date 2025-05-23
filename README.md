# 微信AI聊天助手

一个基于Python的微信聊天自动回复助手，使用大语言模型API生成智能回复。

## 功能特点

- 自动监听指定联系人/群组的消息
- 基于AI模型生成符合个人语气的回复
- 支持直接回复或通过文件传输助手提供回复建议
- 自定义回复延迟时间
- 完整的聊天日志记录

## 安装

### 环境要求

- Python 3.12+
- Windows操作系统（依赖[wxauto库](https://github.com/cluic/wxauto)）

### 步骤

1. 克隆仓库
```
git clone https://github.com/Qiming-Liu/wechat-ai-assistant
cd wechat-ai-assistant
```

2. 创建并激活虚拟环境
```
uv sync
```

## 配置

1. 复制`.env.example`为`.env`并填写以下配置：
```
OPENAI_API_KEY=your_api_key_here

# 微信相关配置
REPLAY_LIST=["联系人1", "联系人2"]  # 需要自动回复的联系人列表
SUGGEST_LIST=["联系人3", "联系人4"]  # 需要提供回复建议的联系人列表
```

## 使用方法

1. 确保已登录微信电脑版
2. 运行程序
```
uv run main.py
```
3. 程序将自动监听配置的联系人消息，并根据设置进行回复

### 回复模式

- **直接回复模式**：对于`REPLAY_LIST`中的联系人，AI会直接发送回复
- **建议回复模式**：对于`SUGGEST_LIST`中的联系人，AI会将建议回复发送到文件传输助手

## 项目结构

```
wechat-chat-assistant/
├── main.py          # 主程序入口
├── .env             # 环境变量配置
├── .env.example     # 环境变量模板
├── pyproject.toml   # 项目依赖
├── logs/            # 日志目录
└── src/             # 源代码
    ├── ai.py        # AI接口相关
    ├── config.py    # 配置相关
    ├── log.py       # 日志相关
    └── wx.py        # 微信相关
```

## 未来规划

我们计划在未来版本中添加以下功能：

- **聊天历史学习**：系统将能够分析历史对话，学习用户的聊天习惯和语气特点，更准确地模拟个人说话风格
- **多样化回复策略**：根据不同联系人和对话场景，自动调整回复风格和内容
- **情感分析**：识别对话中的情绪变化，提供更符合情境的回应
- **对话数据可视化**：提供聊天统计和分析报告，帮助用户了解自己的沟通模式

这些功能将帮助AI助手更自然地融入日常对话，提供个性化的聊天体验。

## 注意事项

- 请确保微信电脑版处于登录状态
- 建议定期查看日志，了解聊天历史
- 该助手仅供学习和个人使用，请勿用于商业用途

