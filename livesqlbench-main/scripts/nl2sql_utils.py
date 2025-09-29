"""
工具函数模块 - 包含辅助函数
"""

import os
import pandas as pd
from sqlalchemy import create_engine
from langchain_community.utilities.sql_database import SQLDatabase
from typing import List
import sys
from pathlib import Path

# 添加路径到sys.path
current_dir = Path(__file__).resolve().parent
mschema_path = current_dir.parent / "M-Schema"
examples_path = current_dir.parent / "examples"
sys.path.append(str(mschema_path))
sys.path.append(str(examples_path))

from schema_engine import SchemaEngine
from config import get_project_root, get_db_path

def get_table_details(db_id: str) -> str:
    """获取表结构描述"""
    project_root = get_project_root()
    csv_path = os.path.join(project_root, "data", "table_descriptions", f"{db_id}_table_description.csv")
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"❌ 找不到表结构描述文件：{csv_path}")
    
    df = pd.read_csv(csv_path)
    
    # 检查是否为新格式（包含多列）
    if 'Fields' in df.columns and 'Multi_Table_Questions' in df.columns:
        # 新格式：包含详细的表信息
        table_details = []
        for _, row in df.iterrows():
            detail = f"""表名：{row['Table']}
基本概述：{row['Description']}
字段信息：{row['Fields']}
示例问题：{row['Example_Questions']}
使用建议：{row['Usage_Tips']}
多表联查问题：{row['Multi_Table_Questions']}
关联表：{row['Related_Tables']}
连接条件：{row['Join_Conditions']}
"""
            table_details.append(detail)
        return "\n".join(table_details)
    else:
        # 旧格式：仅包含Table和Description列
        return "\n".join([f"表名：{row['Table']}\n表的基本概述：{row['Description']}\n" for _, row in df.iterrows()])

def get_mschema_str(db_id: str) -> str:
    """获取数据库的M-Schema字符串表示"""
    db_path = get_db_path(db_id)
    abs_path = os.path.abspath(db_path)
    db_engine = create_engine(f"sqlite:///{abs_path}")
    schema_engine = SchemaEngine(engine=db_engine, db_name=db_id)
    mschema = schema_engine.mschema
    return mschema.to_mschema()

def get_selected_table_details(db_id: str, selected_tables: List[str]) -> str:
    """获取选中表的详细描述信息"""
    project_root = get_project_root()
    csv_path = os.path.join(project_root, "data", "table_descriptions", f"{db_id}_table_description.csv")
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"❌ 找不到表结构描述文件：{csv_path}")
    
    df = pd.read_csv(csv_path)
    
    # 筛选出选中的表
    selected_df = df[df['Table'].isin(selected_tables)]
    
    # 检查是否为新格式（包含多列）
    if 'Fields' in df.columns and 'Multi_Table_Questions' in df.columns:
        # 新格式：包含详细的表信息
        table_details = []
        for _, row in selected_df.iterrows():
            detail = f"""表名：{row['Table']}
基本概述：{row['Description']}
字段信息：{row['Fields']}
示例问题：{row['Example_Questions']}
使用建议：{row['Usage_Tips']}
多表联查问题：{row['Multi_Table_Questions']}
关联表：{row['Related_Tables']}
连接条件：{row['Join_Conditions']}
"""
            table_details.append(detail)
        return "\n".join(table_details)
    else:
        # 旧格式：仅包含Table和Description列
        return "\n".join([f"表名：{row['Table']}\n表的基本概述：{row['Description']}\n" for _, row in selected_df.iterrows()])

def get_selected_mschema(db_id: str, selected_tables: List[str]) -> str:
    """获取选中表的M-Schema字符串表示"""
    db_path = get_db_path(db_id)
    abs_path = os.path.abspath(db_path)
    db_engine = create_engine(f"sqlite:///{abs_path}")
    schema_engine = SchemaEngine(engine=db_engine, db_name=db_id)
    mschema = schema_engine.mschema
    
    # 只保留选中的表
    def table_name_without_prefix(fullname: str) -> str:
        return fullname.split('.')[-1]
    
    mschema.tables = {
        name: table for name, table in mschema.tables.items()
        if table_name_without_prefix(name) in selected_tables
    }
    return mschema.to_mschema()

def get_selected_table_infos(db: SQLDatabase, selected_tables: List[str]) -> str:
    """获取选中表的详细信息"""
    try:
        table_infos = []
        for table in selected_tables:
            try:
                # 获取表结构
                table_info = db.get_table_info([table])
                table_infos.append(f"表 {table}:\n{table_info}")
            except Exception as e:
                table_infos.append(f"表 {table}: 无法获取表信息 - {str(e)}")
        return "\n\n".join(table_infos)
    except Exception as e:
        return f"获取表信息失败: {str(e)}"

def parse_json_response(response_text: str) -> dict:
    """解析LLM返回的JSON响应"""
    import json
    import re
    
    try:
        # 尝试直接解析JSON
        return json.loads(response_text)
    except (json.JSONDecodeError, ValueError):
        try:
            # 尝试从文本中提取JSON
            json_match = re.search(r'\{[^}]*\}', response_text)
            if json_match:
                return json.loads(json_match.group())
            else:
                raise ValueError("无法从响应中提取JSON")
        except:
            raise ValueError(f"JSON解析失败，原始响应: {response_text[:100]}...")

def validate_table_names(tables: List[str], allowed_tables: List[str]) -> List[str]:
    """验证表名有效性，返回有效表名列表。
    - 兼容带模式前缀（如 main.Table）
    - 兼容单双引号/反引号包裹
    - 不区分大小写匹配，返回原始允许表名的规范形式
    """
    def normalize(name: str) -> str:
        # 去前后空白
        s = (name or "").strip()
        # 去模式前缀
        if "." in s:
            s = s.split(".")[-1]
        # 去引号/反引号
        if len(s) >= 2 and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'") or (s[0] == s[-1] == "`")):
            s = s[1:-1]
        return s.strip().lower()

    # 构建允许表名的规范化映射（lower -> 原始名）
    allowed_map = {}
    for at in allowed_tables:
        key = normalize(at)
        # 若存在重复规范化键，保留第一次出现（保持顺序稳定）
        if key not in allowed_map:
            allowed_map[key] = at

    valid: List[str] = []
    seen = set()
    for t in tables:
        key = normalize(t)
        if key in allowed_map and allowed_map[key] not in seen:
            valid.append(allowed_map[key])
            seen.add(allowed_map[key])
    return valid

def extract_tables_from_sql(sql_query: str, available_tables: List[str]) -> List[str]:
    """从SQL查询中提取表名"""
    sql_upper = sql_query.upper()
    found_tables = []
    
    for table in available_tables:
        table_upper = table.upper()
        # 检查表名是否在SQL中出现
        if (f" {table_upper}" in sql_upper or 
            f"`{table_upper}`" in sql_upper or 
            f'"{table_upper}"' in sql_upper or
            f"FROM {table_upper}" in sql_upper or
            f"JOIN {table_upper}" in sql_upper):
            found_tables.append(table)
    
    return found_tables