# -*- coding: utf-8 -*-
"""配置管理模块"""

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

import yaml
from dotenv import load_dotenv


@dataclass
class Config:
    """应用配置"""
    api_key: str
    api_base: str
    model: str
    timeout: int
    max_retries: int
    language: str
    show_emoji: bool
    hotkey: str

    @classmethod
    def load(cls, config_path: Optional[str] = None) -> "Config":
        """加载配置"""
        # 加载环境变量
        load_dotenv()
        
        # 确定配置文件路径
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config.yaml"
        
        # 加载 YAML 配置
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        
        ai_config = data.get("ai", {})
        display_config = data.get("display", {})
        hotkey_config = data.get("hotkey", {})
        
        return cls(
            api_key=os.getenv("API_KEY", ""),
            api_base=ai_config.get("api_base", "https://api.deepseek.com"),
            model=ai_config.get("model", "deepseek-chat"),
            timeout=ai_config.get("timeout", 30),
            max_retries=ai_config.get("max_retries", 2),
            language=display_config.get("language", "zh"),
            show_emoji=display_config.get("show_emoji", True),
            hotkey=hotkey_config.get("trigger", "ctrl+shift+e"),
        )
