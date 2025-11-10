#!/usr/bin/env python3
"""
重构后的NL2SQL主模块
整合了表选择、示例选择等功能模块
"""
# python nl2sql.py --db_id hospital_1 --question "如果约翰·史密斯是国际护士节那天出院的，他住了几天院？"
import json
import argparse
from typing import List

# 导入自定义模块
from config import get_llm_instance, get_llm_anthropic, get_db_path
from models import TableSelection, ConfidenceEvaluation, ExampleSelectionResult
from table_selection import TableSelector
from example_selection import ExampleSelector
from nl2sql_utils import get_table_details, get_mschema_str, parse_json_response

# 导入新的解耦模块
from sql_generator import SQLGenerator
from sql_executor import SQLExecutor
from sql_validator import SQLValidator
from prompt_builder import PromptBuilder


class NL2SQLProcessor:
    """NL2SQL处理器主类 - 重构后专注于流程编排"""
    
    def __init__(self, db_id: str):
        """
        初始化NL2SQL处理器
        
        Args:
            db_id: 数据库ID
        """
        self.db_id = db_id
        # 双模型配置
        self.llm_openai = get_llm_instance()  # 用于表选择、示例选择、SQL选择
        self.llm_anthropic = get_llm_anthropic()  # 用于SQL生成
        
        # 初始化各个功能模块
        self.table_selector = TableSelector(self.llm_openai)
        self.example_selector = ExampleSelector()
        
        # 加载数据库表结构
        self.table_details = get_table_details(db_id)
        self.mschema_str = get_mschema_str(db_id)
        
        # 创建SQLDatabase实例
        from langchain_community.utilities.sql_database import SQLDatabase
        db_path = get_db_path(db_id)
        self.db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
        
        # 初始化解耦后的模块
        self.sql_generator = SQLGenerator(self.llm_openai, self.llm_anthropic, self.db_id, self.db)
        self.sql_executor = SQLExecutor(self.db)
        self.sql_validator = SQLValidator(self.llm_openai, self.db_id, self.db)
        self.prompt_builder = PromptBuilder(self.db_id)
        
    def process_question(self, question: str) -> dict:
        """
        处理自然语言问题，生成SQL查询
        
        Args:
            question: 自然语言问题
            
        Returns:
            包含SQL查询和相关信息的字典
        """
        try:
            # 第一步：表选择
            print(f"🔍 开始为问题选择相关表: {question}")
            table_selection_result = self.table_selector.select_tables_multi_stage(
                question, self.db_id, self.db
            )
            
            print(f"✅ 选择的表: {table_selection_result.tables}")
            print(f"📊 置信度: {table_selection_result.confidence_score:.2f}")
            
            # 第二步：示例选择（强制启用 few-shot）
            print("📚 开始选择few-shot示例...")
            example_selection_result = self.example_selector.get_example_selection_result(
                self.db_id, question, table_selection_result.tables
            )
            print(f"✅ 选择了 {len(example_selection_result.selected_examples)} 个示例")
            
            # 第三步：使用解耦后的SQL生成器生成SQL
            print("🔧 开始生成SQL查询...")
            sql_result = self.sql_generator.generate_sql_dual_model(
                question, 
                table_selection_result, 
                example_selection_result
            )
            
            return {
                'question': question,
                'db_id': self.db_id,
                'selected_tables': table_selection_result.tables,
                'confidence_score': table_selection_result.confidence_score,
                'sql_query': sql_result.get('sql', ''),
                'reasoning': sql_result.get('reasoning', ''),
                'example_selection_result': example_selection_result,
                'success': True
            }
            
        except Exception as e:
            print(f"❌ 处理问题时发生错误: {str(e)}")
            return {
                'question': question,
                'db_id': self.db_id,
                'error': str(e),
                'success': False
            }


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='NL2SQL处理器')
    parser.add_argument('--db_id', type=str, required=True, help='数据库ID')
    parser.add_argument('--question', type=str, required=True, help='自然语言问题')
    parser.add_argument('--output', type=str, help='输出文件路径')
    
    args = parser.parse_args()
    
    # 创建处理器
    processor = NL2SQLProcessor(args.db_id)
    
    # 处理问题
    result = processor.process_question(args.question)
    
    # 输出结果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"✅ 结果已保存到: {args.output}")
    else:
        print("\n" + "="*50)
        print("🎯 NL2SQL处理结果:")
        print("="*50)
        if result['success']:
            print(f"问题: {result['question']}")
            print(f"数据库: {result['db_id']}")
            print(f"选择的表: {', '.join(result['selected_tables'])}")
            print(f"生成的SQL:\n{result['sql_query']}")
        else:
            print(f"❌ 处理失败: {result['error']}")


def generate_sql_only(db_id: str, question: str) -> str:
    """
    简化的SQL生成函数，专门用于评估
    
    Args:
        db_id: 数据库ID
        question: 自然语言问题
        
    Returns:
        生成的SQL查询字符串
    """
    try:
        processor = NL2SQLProcessor(db_id)
        result = processor.process_question(question)
        
        if result['success']:
            return result['sql_query']
        else:
            raise Exception(f"SQL生成失败: {result.get('error', '未知错误')}")
            
    except Exception as e:
        raise Exception(f"generate_sql_only执行失败: {str(e)}")


if __name__ == "__main__":
    main()