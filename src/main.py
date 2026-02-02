# -*- coding: utf-8 -*-
"""CLI Explainer v2 - 主程序入口

完全 AI 驱动：一次调用完成命令识别、解析、风险评估和解释
"""

import sys
import time
import argparse

from .config import Config
from .analyzer import AIAnalyzer
from .display import Display
from .capturer import Capturer


class App:
    """应用主类"""

    def __init__(self):
        self.config = Config.load()
        self.analyzer = AIAnalyzer(self.config)
        self.display = Display(show_emoji=self.config.show_emoji)

    def analyze_content(self, content: str) -> None:
        """分析内容并展示结果"""
        self.display.show_waiting("正在调用 AI 分析...")
        result = self.analyzer.analyze(content)
        self.display.show_result(result)

    def run_single(self, content: str) -> None:
        """单次分析模式"""
        self.analyze_content(content)

    def run_interactive(self) -> None:
        """交互模式"""
        self.display.console.print(
            "[bold cyan]CLI Explainer v2[/bold cyan] - 交互模式"
        )
        self.display.console.print("输入命令进行分析，输入 [bold]quit[/bold] 退出\n")
        
        while True:
            try:
                content = input("$ ").strip()
                if content.lower() in ("quit", "exit", "q"):
                    self.display.show_info("再见！")
                    break
                if not content:
                    continue
                self.analyze_content(content)
            except KeyboardInterrupt:
                self.display.console.print()
                self.display.show_info("再见！")
                break
            except EOFError:
                break

    def run_clipboard(self) -> None:
        """剪贴板监听模式"""
        self.display.console.print(
            "[bold cyan]CLI Explainer v2[/bold cyan] - 剪贴板监听模式"
        )
        self.display.show_success(f"热键已注册: {self.config.hotkey}")
        self.display.console.print("复制命令后按热键触发分析，按 Ctrl+C 退出\n")
        
        # 创建捕获器
        capturer = Capturer(hotkey=self.config.hotkey)
        
        def on_capture(content: str):
            self.display.console.print(f"\n[dim]>>> 捕获到内容[/dim]")
            self.analyze_content(content)
            self.display.console.print()
        
        try:
            capturer.start(on_capture)
            
            # 保持运行
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.display.console.print()
            self.display.show_info("停止监听...")
        finally:
            capturer.stop()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="CLI Explainer v2 - 完全 AI 驱动的命令解释工具"
    )
    parser.add_argument(
        "command",
        nargs="?",
        help="要分析的命令"
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="交互模式"
    )
    parser.add_argument(
        "-c", "--clipboard",
        action="store_true",
        help="剪贴板监听模式"
    )
    
    args = parser.parse_args()
    
    app = App()
    
    # 检查 AI 可用性
    if not app.analyzer.is_available():
        app.display.show_error("API_KEY 未配置，请在 .env 文件中设置")
        sys.exit(1)
    
    if args.interactive:
        app.run_interactive()
    elif args.clipboard:
        app.run_clipboard()
    elif args.command:
        app.run_single(args.command)
    else:
        # 默认显示帮助
        parser.print_help()


if __name__ == "__main__":
    main()
