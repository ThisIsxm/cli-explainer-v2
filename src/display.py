# -*- coding: utf-8 -*-
"""结果展示模块 - 使用 Rich 美化输出"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.text import Text

from .analyzer import AnalysisResult


class Display:
    """结果展示器"""

    # 风险等级颜色
    RISK_COLORS = {
        "low": "green",
        "medium": "yellow",
        "high": "red",
        "critical": "bold red",
    }
    
    # 风险等级显示名称
    RISK_NAMES = {
        "low": "🟢 低风险",
        "medium": "🟡 中风险",
        "high": "🔴 高风险",
        "critical": "💀 严重风险",
    }

    def __init__(self, show_emoji: bool = True):
        self.console = Console()
        self.show_emoji = show_emoji

    def show_result(self, result: AnalysisResult) -> None:
        """展示分析结果"""
        if result.error:
            self.show_error(result.error)
            return
            
        if not result.is_command:
            self.show_not_command(result)
            return
        
        self.show_command_analysis(result)

    def show_command_analysis(self, result: AnalysisResult) -> None:
        """展示命令分析结果"""
        # 命令标题
        self.console.print()
        self.console.print(Panel(
            f"[bold cyan]{result.command}[/bold cyan]",
            title="📋 命令" if self.show_emoji else "命令",
            border_style="cyan",
        ))
        
        # 概要
        if result.summary:
            self.console.print(f"\n[bold]概要:[/bold] {result.summary}")
        
        # 详细说明
        if result.description:
            self.console.print(f"\n[bold]详细说明:[/bold]")
            self.console.print(f"  {result.description}")
        
        # 风险评估
        self._show_risk(result)
        
        # 建议
        if result.suggestion:
            self.console.print(f"\n[bold]💡 建议:[/bold] {result.suggestion}")
        
        # 示例
        if result.examples:
            self.console.print(f"\n[bold]📝 相关示例:[/bold]")
            for example in result.examples:
                self.console.print(f"  • {example}")
        
        self.console.print()

    def _show_risk(self, result: AnalysisResult) -> None:
        """展示风险评估"""
        risk_color = self.RISK_COLORS.get(result.risk_level, "white")
        risk_name = self.RISK_NAMES.get(result.risk_level, result.risk_level)
        
        self.console.print()
        
        # 风险面板
        risk_content = Text()
        risk_content.append(f"{risk_name}\n", style=f"bold {risk_color}")
        risk_content.append(f"评分: {result.risk_score}/100\n")
        
        if result.risk_reasons:
            risk_content.append("\n风险因素:\n")
            for reason in result.risk_reasons:
                risk_content.append(f"  • {reason}\n", style=risk_color)
        
        self.console.print(Panel(
            risk_content,
            title="⚠️ 风险评估" if self.show_emoji else "风险评估",
            border_style=risk_color,
        ))

    def show_not_command(self, result: AnalysisResult) -> None:
        """展示非命令提示"""
        self.console.print()
        self.console.print(Panel(
            f"[dim]{result.reason}[/dim]\n\n💡 {result.suggestion}",
            title="ℹ️ 提示" if self.show_emoji else "提示",
            border_style="dim",
        ))
        self.console.print()

    def show_error(self, error: str) -> None:
        """展示错误信息"""
        self.console.print()
        self.console.print(Panel(
            f"[red]{error}[/red]",
            title="❌ 错误" if self.show_emoji else "错误",
            border_style="red",
        ))
        self.console.print()

    def show_info(self, message: str) -> None:
        """展示普通信息"""
        self.console.print(f"[dim]ℹ️  {message}[/dim]")

    def show_success(self, message: str) -> None:
        """展示成功信息"""
        self.console.print(f"[green]✓ {message}[/green]")

    def show_waiting(self, message: str = "正在分析...") -> None:
        """展示等待提示"""
        self.console.print(f"[dim]⏳ {message}[/dim]")
