#!/usr/bin/env python3
"""
SQL验证器模块 - 负责SQL验证和修复
"""

from typing import List
from nl2sql_utils import get_selected_mschema


class SQLValidator:
    """SQL验证器类 - 负责SQL验证和修复"""
    
    def __init__(self, llm_openai, db_id: str, db):
        """
        初始化SQL验证器
        
        Args:
            llm_openai: OpenAI模型实例
            db_id: 数据库ID
            db: 数据库连接实例
        """
        self.llm_openai = llm_openai
        self.db_id = db_id
        self.db = db
    
    def validate_and_repair_sql(self, sql: str, question: str, selected_tables: List[str]) -> str:
        """
        验证SQL语法，如果有问题则尝试修复
        
        Args:
            sql: 待验证的SQL
            question: 原始问题
            selected_tables: 选中的表列表
            
        Returns:
            验证或修复后的SQL
        """
        # 清理 SQL
        sql_clean = self._clean_sql(sql)
        
        try:
            # 使用 EXPLAIN QUERY PLAN 验证语法
            self.db.run(f"EXPLAIN QUERY PLAN {sql_clean}")
            print(f"✅ SQL 验证通过")
            return sql_clean
        except Exception as e:
            print(f"❌ SQL 验证失败：{e}")
            return self._repair_sql(sql_clean, question, selected_tables, str(e))
    
    def _clean_sql(self, sql: str) -> str:
        """清理SQL语句"""
        sql_clean = sql.strip()
        
        # 处理可能的前缀
        if sql_clean.startswith("SQL 1 (Anthropic):") or sql_clean.startswith("SQL 2 (OpenAI):"):
            sql_clean = sql_clean.split(":", 1)[1].strip()
        
        # 处理代码块标记
        if sql_clean.startswith("```sql"):
            lines = sql_clean.strip().splitlines()
            sql_clean = "\n".join(line for line in lines if not line.strip().startswith("```")).strip(";")
        
        return sql_clean
    
    def _repair_sql(self, sql_clean: str, question: str, selected_tables: List[str], error: str) -> str:
        """修复SQL语句"""
        # 尝试修复 SQL，注入选表的 m-schema 帮助模型修复
        selected_table_infos = get_selected_mschema(self.db_id, selected_tables)
        repair_prompt = f"""你是一位 SQLite 专家。请修复以下 SQL 查询语句，确保其符合 SQLite 语法并正确回答用户问题：{question}

错误 SQL：{sql_clean}
错误信息：{error}
数据库表：{self.db.get_usable_table_names()}
表结构（m-schema）：
{selected_table_infos}

输出格式：仅返回修复后的 SQL 语句，无任何注释、代码块标记或多余分号。
"""
        try:
            repaired_response = self.llm_openai.invoke(repair_prompt)
            repaired_sql = repaired_response.content.strip()
            
            # 清理修复后的 SQL
            repaired_sql = self._clean_sql(repaired_sql)
            
            # 再次验证修复后的SQL
            self.db.run(f"EXPLAIN QUERY PLAN {repaired_sql}")
            print(f"✅ 修复后的 SQL 验证通过：{repaired_sql}")
            return repaired_sql
            
        except Exception as repair_error:
            print(f"❌ SQL 修复也失败：{repair_error}")
            return sql_clean  # 返回原始SQL，让调用者决定如何处理