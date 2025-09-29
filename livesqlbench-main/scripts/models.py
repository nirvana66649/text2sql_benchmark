"""
数据模型模块 - 包含Pydantic模型定义
"""

from pydantic import BaseModel, Field
from typing import List

class TableList(BaseModel):
    """表列表模型"""
    tables: List[str] = Field(description="List of relevant table names")

class TableSelection(BaseModel):
    """表选择结果模型"""
    tables: List[str] = Field(description="List of relevant table names")
    confidence_score: float = Field(description="Confidence score between 0.0 and 1.0", ge=0.0, le=1.0)
    reasoning: str = Field(description="Brief explanation of the selection reasoning")
    selection_method: str = Field(description="Method used for table selection")

class ConfidenceEvaluation(BaseModel):
    """置信度评估结果模型"""
    confidence_score: float = Field(description="Confidence score between 0.0 and 1.0", ge=0.0, le=1.0)
    reasoning: str = Field(description="Brief explanation of the confidence evaluation")
    status: str = Field(description="Evaluation status: success or error")

class ExampleSelectionResult(BaseModel):
    """示例选择结果模型"""
    selected_examples: List[dict] = Field(description="List of selected examples")
    selection_method: str = Field(description="Method used for selection")
    total_examples: int = Field(description="Total number of available examples")
    selected_count: int = Field(description="Number of selected examples")
    few_shot_text: str = Field(description="Formatted few-shot examples text")