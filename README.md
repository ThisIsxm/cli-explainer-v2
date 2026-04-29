# CLI Explainer v2 - 完全 AI 驱动

> 🤖 一次 AI 调用完成命令识别、解析、风险评估和解释

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## ✨ 特性

- **完全 AI 驱动** - 无静态规则，大模型判断一切
- **一次调用** - 单次 AI 请求完成所有分析
- **更智能** - 能理解上下文和复杂命令
- **热键触发** - Ctrl+Shift+E 一键解释
- **极简代码** - 仅 ~500 行核心代码

## 💡 应用场景

**专为 AI 编程时代的开发者设计！**

在使用 Cursor、GitHub Copilot 等 AI 编程助手时，AI 经常会建议执行一些复杂的终端命令。在你不确定这些命令到底会做什么时：

1. 复制 AI 建议的命令
2. 按下 `Ctrl+Shift+E`（启动剪贴板监听模式后）
3. 立即查看该命令的**详细解释**和**潜在风险**
4. 确认安全后，再放心交给系统执行！

## 🚀 快速开始

### 安装

```bash
# 克隆项目
git clone https://github.com/ThisIsxm/cli-explainer-v2.git
cd cli-explainer-v2

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt

# 或者直接安装（支持命令行工具）
pip install -e .
```

### 配置

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env，设置 API Key
API_KEY=sk-your-api-key-here
```

编辑 `config.yaml` 配置 AI 服务：
```yaml
ai:
  api_base: https://openrouter.ai/api/v1
  model: openai/gpt-oss-120b
```

### 使用

```bash
# 方式1：直接运行模块
python -m src.main "ls -la"

# 方式2：安装后使用命令（推荐）
cli-explainer "rm -rf /tmp/test"
cli-explainer -i   # 交互模式
cli-explainer -c   # 剪贴板监听模式
```

## 📸 效果展示

```
╭─────────────────────── 📋 命令 ───────────────────────╮
│ rm -rf /tmp/test                                      │
╰───────────────────────────────────────────────────────╯

概要: 强制递归删除 /tmp/test 目录及其所有内容

╭─────────────────── ⚠️ 风险评估 ───────────────────────╮
│ 🔴 高风险                                              │
│ 评分: 75/100                                          │
│                                                        │
│ 风险因素:                                              │
│   • 递归删除会清空整个目录树                           │
│   • -f 参数跳过确认，误操作无法恢复                    │
╰───────────────────────────────────────────────────────╯

💡 建议: 执行前先用 ls 确认目录内容，考虑使用 -i 参数交互确认
```

## 🏗️ 架构

```
剪贴板/命令 → [单次AI调用] → 结构化结果展示
                  ↓
              返回 JSON:
              - is_command: 是否为命令
              - summary: 概要
              - risk_level: 风险等级
              - suggestion: 建议
```

### 项目结构

```
cli-explainer-v2/
├── src/
│   ├── analyzer.py    # 🤖 AI 分析引擎（核心）
│   ├── display.py     # Rich 美化输出
│   ├── capturer.py    # 剪贴板/热键捕获
│   ├── config.py      # 配置管理
│   └── main.py        # 程序入口
├── config.yaml        # AI 配置
└── requirements.txt
```

## 🆚 与 v1 的区别

| 功能 | [v1](https://github.com/ThisIsxm/cli-command-explainer) | v2 |
|------|:--:|:--:|
| 命令识别 | 静态规则 | AI 判断 |
| 风险评估 | 规则引擎 | AI 评估 |
| 代码量 | ~2000行 | ~500行 |
| 适用场景 | 生产使用 | 极简/实验 |

> 💡 **如需更稳定的版本**，请查看 [cli-command-explainer (v1)](https://github.com/ThisIsxm/cli-command-explainer)

## 📄 许可证

[MIT License](LICENSE)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！
