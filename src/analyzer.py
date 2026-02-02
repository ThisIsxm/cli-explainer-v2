# -*- coding: utf-8 -*-
"""AI 分析引擎 - 核心模块

一次 AI 调用完成：命令识别、解析、风险评估、解释
"""

import json
import re
from typing import Optional
from dataclasses import dataclass, field

import litellm

from .config import Config


# 综合分析 Prompt
ANALYZE_PROMPT = '''你是一个命令行专家。分析用户提供的内容，判断是否为有效的命令行命令，并提供详细命令解释。

用户内容：
```
{content}
```

请严格按照以下 JSON 格式返回（不要添加任何其他文字）：

如果是有效命令：
{{
  "is_command": true,
  "command": "原始命令",
  "summary": "一句话概要（简洁明了）",
  "description": "详细说明命令的功能和每个参数的作用",
  "risk_level": "low/medium/high/critical",
  "risk_score": 0-100,
  "risk_reasons": ["风险原因1", "风险原因2"],
  "suggestion": "给用户的执行建议",
  "examples": ["相关用法示例1", "相关用法示例2"]
}}

如果不是有效命令：
{{
  "is_command": false,
  "reason": "说明为什么不是命令",
  "suggestion": "建议用户应该怎么做"
}}

风险等级说明：
- low: 只读操作，如 ls、cat、echo
- medium: 可能修改配置或安装软件，如 npm install、git commit
- high: 可能删除文件或影响系统，如 rm、chmod 777
- critical: 极度危险，如 rm -rf /、:(){ :|:& };:

请直接返回 JSON，不要有任何其他内容。'''


@dataclass
class AnalysisResult:
    """AI 分析结果"""
    is_command: bool = False
    command: str = ""
    summary: str = ""
    description: str = ""
    risk_level: str = "low"
    risk_score: int = 0
    risk_reasons: list = field(default_factory=list)
    suggestion: str = ""
    examples: list = field(default_factory=list)
    reason: str = ""  # 非命令时的原因
    raw_response: str = ""  # 原始响应
    error: Optional[str] = None  # 错误信息

    def to_dict(self) -> dict:
        return {
            "is_command": self.is_command,
            "command": self.command,
            "summary": self.summary,
            "description": self.description,
            "risk_level": self.risk_level,
            "risk_score": self.risk_score,
            "risk_reasons": self.risk_reasons,
            "suggestion": self.suggestion,
            "examples": self.examples,
            "reason": self.reason,
        }


class AIAnalyzer:
    """AI 分析引擎
    
    一次调用完成所有分析工作
    """

    def __init__(self, config: Config):
        self.config = config
        self._setup_litellm()

    def _setup_litellm(self):
        """配置 LiteLLM"""
        litellm.set_verbose = False
        if self.config.api_base:
            litellm.api_base = self.config.api_base

    def analyze(self, content: str) -> AnalysisResult:
        """分析内容
        
        Args:
            content: 用户输入的内容（剪贴板/命令行）
            
        Returns:
            AnalysisResult: 分析结果
        """
        if not content or not content.strip():
            return AnalysisResult(
                is_command=False,
                reason="内容为空",
                suggestion="请输入或复制一个命令"
            )

        content = content.strip()
        
        try:
            # 构建消息（使用字符串拼接避免format与JSON冲突）
            prompt = ANALYZE_PROMPT.replace("{content}", content)
            messages = [
                {"role": "user", "content": prompt}
            ]
            
            # 调用 AI
            response = litellm.completion(
                model=self.config.model,
                messages=messages,
                api_key=self.config.api_key,
                api_base=self.config.api_base,
                timeout=self.config.timeout,
                temperature=0.1,  # 低温度，更确定性的输出
            )
            
            # 解析响应
            response_text = response.choices[0].message.content.strip()
            return self._parse_response(response_text, content)
            
        except Exception as e:
            import traceback
            error_msg = str(e) if str(e) else repr(e)
            print(f"[DEBUG] AI调用错误: {error_msg}", flush=True)
            print(f"[DEBUG] 错误类型: {type(e).__name__}", flush=True)
            traceback.print_exc()
            return AnalysisResult(
                is_command=False,
                error=f"{type(e).__name__}: {error_msg}",
                reason=f"AI 分析失败: {error_msg}",
                suggestion="请检查 API 配置或网络连接"
            )

    def _parse_response(self, response_text: str, original_content: str) -> AnalysisResult:
        """解析 AI 响应"""
        try:
            # 尝试提取 JSON
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                json_str = json_match.group()
                data = json.loads(json_str)
            else:
                data = json.loads(response_text)
            
            result = AnalysisResult(
                is_command=data.get("is_command", False),
                command=data.get("command", original_content),
                summary=data.get("summary", ""),
                description=data.get("description", ""),
                risk_level=data.get("risk_level", "low"),
                risk_score=data.get("risk_score", 0),
                risk_reasons=data.get("risk_reasons", []),
                suggestion=data.get("suggestion", ""),
                examples=data.get("examples", []),
                reason=data.get("reason", ""),
                raw_response=response_text,
            )
            return result
            
        except json.JSONDecodeError:
            # JSON 解析失败，尝试简单判断
            return AnalysisResult(
                is_command=True,  # 保守起见，当作命令处理
                command=original_content,
                summary="AI 返回格式异常，请查看原始响应",
                description=response_text,
                risk_level="medium",
                raw_response=response_text,
            )

    def is_available(self) -> bool:
        """检查 AI 服务是否可用"""
        return bool(self.config.api_key)
