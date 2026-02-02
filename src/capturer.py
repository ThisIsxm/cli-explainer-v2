# -*- coding: utf-8 -*-
"""剪贴板和热键捕获模块"""

import pyperclip
import keyboard
from typing import Callable, Optional


class Capturer:
    """剪贴板和热键捕获器"""

    def __init__(self, hotkey: str = "ctrl+shift+e"):
        self.hotkey = hotkey
        self._callback: Optional[Callable[[str], None]] = None
        self._last_content: str = ""
        self._is_running: bool = False

    def start(self, callback: Callable[[str], None]) -> None:
        """启动捕获
        
        Args:
            callback: 捕获到内容时的回调函数
        """
        self._callback = callback
        self._is_running = True
        
        # 注册热键
        keyboard.add_hotkey(self.hotkey, self._on_hotkey)

    def stop(self) -> None:
        """停止捕获"""
        self._is_running = False
        try:
            keyboard.remove_hotkey(self.hotkey)
        except:
            pass

    def _on_hotkey(self) -> None:
        """热键触发时的处理"""
        if not self._is_running or not self._callback:
            return
        
        # 获取剪贴板内容
        try:
            content = pyperclip.paste()
        except:
            content = ""
        
        if not content or not content.strip():
            return
        
        content = content.strip()
        
        # 检查是否重复
        if content == self._last_content:
            # 重复内容，仍然处理但可以给提示
            pass
        
        self._last_content = content
        self._callback(content)

    def get_clipboard(self) -> str:
        """获取当前剪贴板内容"""
        try:
            return pyperclip.paste() or ""
        except:
            return ""
