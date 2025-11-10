"""
配置模块 - 包含数据库路径、LLM配置等常量和配置信息
"""

import os
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

# === 路径配置 ===
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

# 数据库路径配置
DB_PATHS = {
    "bike_1": os.path.join(project_root, "database", "bike_1", "bike_1.sqlite"),
    "concert_singer": os.path.join(project_root, "database", "concert_singer", "concert_singer.sqlite"),
    "customers_and_products_contacts": os.path.join(project_root, "database", "customers_and_products_contacts", "customers_and_products_contacts.sqlite"),
    "driving_school": os.path.join(project_root, "database", "driving_school", "driving_school.sqlite"),
    "formula_1": os.path.join(project_root, "database", "formula_1", "formula_1.sqlite"),
    "hospital_1": os.path.join(project_root, "database", "hospital_1", "hospital_1.sqlite"),
    "riding_club": os.path.join(project_root, "database", "riding_club", "riding_club.sqlite"),
    "soccer_1": os.path.join(project_root, "database", "soccer_1", "soccer_1.sqlite"),
    "wine_1": os.path.join(project_root, "database", "wine_1", "wine_1.sqlite"),
    "world_1": os.path.join(project_root, "database", "world_1", "world_1.sqlite")
}

# M-Schema和示例路径配置
current_dir = Path(__file__).resolve().parent
MSCHEMA_PATH = current_dir.parent / "M-Schema"
EXAMPLES_PATH = current_dir.parent / "examples"

# === LLM配置 ===
# OpenAI配置
OPENAI_CONFIG = {
    "model": "gpt-5-fast",
    "base_url": "your url",
    "api_key": "your api key",
    "temperature": 0.5
}

# Anthropic配置
ANTHROPIC_CONFIG = {
    "model_name": "cc-sonnet-4-20250514-thinking",
    "base_url": "your url",
    "api_key": "your api key",
    "temperature": 0.3
}

# 嵌入模型配置
EMBEDDING_CONFIG = {
    "base_url": "your url",
    "api_key": "your api key",
    "model": "text-embedding-3-large",
    "default_headers": {"User-Agent": "langchain-openai"},
    "http_client": None  # 将在运行时设置为跳过SSL验证的客户端
}

# === 算法参数配置 ===
# 表选择参数
TABLE_SELECTION_CONFIG = {
    "max_coarse_tables": 8,  # 粗选最大表数
    "max_fine_tables": 5,    # 精选最大表数
    "confidence_threshold": 0.4,  # 置信度阈值
    "fallback_max_tables": 8  # fallback最大表数
}

# Few-shot示例选择参数
EXAMPLE_SELECTION_CONFIG = {
    "default_k": 2,  # 默认选择示例数量
    "max_k": 3,      # 最大示例数量
    "min_k": 1,      # 最小示例数量
}

def get_llm_openai():
    """获取OpenAI LLM实例"""
    return ChatOpenAI(**OPENAI_CONFIG)

def get_llm_anthropic():
    """获取Anthropic LLM实例"""
    return ChatAnthropic(**ANTHROPIC_CONFIG)

def get_llm_instance():
    """获取默认LLM实例（OpenAI）"""
    return get_llm_openai()

def get_embedding_config():
    """获取嵌入模型配置"""
    import httpx
    import ssl
    
    # 创建跳过SSL验证的HTTP客户端
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    http_client = httpx.Client(
        verify=False,  # 跳过SSL验证
        timeout=30.0
    )
    
    config = EMBEDDING_CONFIG.copy()
    config["http_client"] = http_client
    return config

def get_db_path(db_id: str) -> str:
    """获取数据库路径"""
    if db_id not in DB_PATHS:
        raise ValueError(f"未知数据库 ID：{db_id}")
    return DB_PATHS[db_id]

def get_project_root() -> str:
    """获取项目根目录"""
    return project_root