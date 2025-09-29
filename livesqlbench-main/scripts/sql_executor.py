#!/usr/bin/env python3
"""
SQL执行器模块 - 负责安全执行SQL查询
"""

from typing import Dict, Any


class SQLExecutor:
    """SQL执行器类 - 负责安全执行SQL查询"""
    
    def __init__(self, db):
        """
        初始化SQL执行器
        
        Args:
            db: 数据库连接实例
        """
        self.db = db
    
    def execute_sql_safely(self, sql: str) -> Dict[str, Any]:
        """
        安全执行SQL并返回结果
        
        Args:
            sql: 要执行的SQL语句
            
        Returns:
            包含执行结果或错误信息的字典
        """
        try:
            # 限制查询结果数量，避免返回过多数据
            limited_sql = sql.strip()
            if not limited_sql.upper().startswith('SELECT'):
                return {
                    'success': False,
                    'error': 'Only SELECT queries are allowed',
                    'result': None
                }
            
            # 添加LIMIT限制（如果没有的话）
            if 'LIMIT' not in limited_sql.upper():
                limited_sql += ' LIMIT 100'
            
            # 执行SQL
            result = self.db.run(limited_sql)
            
            return {
                'success': True,
                'error': None,
                'result': result,
                'row_count': len(result.split('\n')) if result else 0
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'result': None
            }