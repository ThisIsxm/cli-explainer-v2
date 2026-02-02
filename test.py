#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""快速测试脚本"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from src.config import Config
from src.analyzer import AIAnalyzer
from src.display import Display


def test():
    print("=" * 50)
    print("CLI Explainer v2 - 快速测试")
    print("=" * 50)
    print()
    
    # 加载配置
    print("1. 加载配置...", flush=True)
    try:
        config = Config.load()
        print(f"   ✓ API Base: {config.api_base}")
        print(f"   ✓ Model: {config.model}")
    except Exception as e:
        print(f"   ✗ 配置加载失败: {e}")
        return
    print()
    
    # 初始化
    print("2. 初始化模块...", flush=True)
    analyzer = AIAnalyzer(config)
    display = Display(show_emoji=True)
    
    if not analyzer.is_available():
        print("   ✗ API_KEY 未配置")
        return
    print("   ✓ 模块初始化成功")
    print()
    
    # 测试分析
    test_cases = [
        "ls -la",
        "rm -rf /tmp/test",
        "这是一段普通文本",
        "git push --force origin main",
    ]
    
    for i, content in enumerate(test_cases, 3):
        print(f"{i}. 测试: {content}", flush=True)
        print("-" * 50)
        result = analyzer.analyze(content)
        display.show_result(result)
        print()
    
    print("=" * 50)
    print("✅ 测试完成！")
    print("=" * 50)


if __name__ == "__main__":
    test()
