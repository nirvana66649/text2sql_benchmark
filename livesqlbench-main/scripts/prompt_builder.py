#!/usr/bin/env python3
"""
提示词构建器模块 - 负责构建各种类型的提示词
"""

from models import TableSelection, ExampleSelectionResult
from nl2sql_utils import get_selected_mschema


class PromptBuilder:
    """提示词构建器类 - 负责构建各种类型的提示词"""
    
    def __init__(self, db_id: str):
        """
        初始化提示词构建器
        
        Args:
            db_id: 数据库ID
        """
        self.db_id = db_id
    
    def build_sql_generation_prompt(self, question: str, table_selection: TableSelection,
                                   example_selection: ExampleSelectionResult = None) -> str:
        """
        构建SQL生成的提示词
        
        Args:
            question: 自然语言问题
            table_selection: 表选择结果
            example_selection: 示例选择结果
            
        Returns:
            完整的提示词字符串
        """
        # 获取选中表的 m-schema
        selected_table_infos = get_selected_mschema(self.db_id, table_selection.tables)
        
        prompt = f"""你是一个专业的SQL查询生成专家。请根据给定的自然语言问题和数据库表结构，生成准确的SQL查询。

数据库ID: {self.db_id}

相关表结构信息（m-schema 格式）:
{selected_table_infos}

"""
        
        # 添加few-shot示例（如果有）
        if example_selection and example_selection.few_shot_text:
            prompt += f"""参考示例:
{example_selection.few_shot_text}

"""
        
        prompt += f"""自然语言问题: {question}

请生成对应的SQL查询，并提供推理过程。

推理类型说明（用于理解参考示例中的推理方式）：
- + ：需要执行加法运算
- - ：需要执行减法运算
- * ：需要执行乘法运算
- / ：需要执行除法运算
- C ：需要应用常识推理（结合业务逻辑和常识知识）
- H ：需要基于假设或特定条件推理（如假设某种情况下的结果）

要求:
1. 只使用提供的表结构中的表和字段
2. 确保SQL语法正确，符合SQLite标准
3. 考虑数据类型和约束条件
4. 根据问题类型选择合适的推理方式
5. 确保输出的sql符合用户查询要求(包含所有用户问题里包含的字段)

请直接返回SQL查询语句，不需要任何JSON格式、注释或其他内容。"""
        
        return prompt