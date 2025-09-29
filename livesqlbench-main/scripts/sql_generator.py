#!/usr/bin/env python3
"""
SQL生成器模块 - 负责双模型SQL生成和智能选择
"""

from typing import Dict, Any
from models import TableSelection, ExampleSelectionResult
from nl2sql_utils import get_selected_mschema


class SQLGenerator:
    """SQL生成器类 - 负责双模型协同生成SQL"""
    
    def __init__(self, llm_openai, llm_anthropic, db_id: str, db):
        """
        初始化SQL生成器
        
        Args:
            llm_openai: OpenAI模型实例
            llm_anthropic: Anthropic模型实例
            db_id: 数据库ID
            db: 数据库连接实例
        """
        self.llm_openai = llm_openai
        self.llm_anthropic = llm_anthropic
        self.db_id = db_id
        self.db = db
    
    def generate_sql_dual_model(self, question: str, table_selection: TableSelection, 
                               example_selection: ExampleSelectionResult = None) -> Dict[str, Any]:
        """
        双模型生成SQL查询：Anthropic + OpenAI 协同生成，自动选择最优SQL
        
        Args:
            question: 自然语言问题
            table_selection: 表选择结果
            example_selection: 示例选择结果
            
        Returns:
            包含SQL和推理过程的字典
        """
        from prompt_builder import PromptBuilder
        from sql_executor import SQLExecutor
        
        # 构建提示词
        prompt_builder = PromptBuilder(self.db_id)
        prompt = prompt_builder.build_sql_generation_prompt(
            question, table_selection, example_selection
        )
        
        try:
            print("🤖 启动双模型SQL生成...")
            
            # 打印完整的SQL生成prompt
            self._print_sql_generation_prompt(prompt, question, table_selection, example_selection)
            
            # 1. Anthropic 生成 SQL
            print("🧠 Anthropic 生成SQL中...")
            response_anthropic = self.llm_anthropic.invoke(prompt)
            sql_anthropic = self._extract_sql_from_anthropic_response(response_anthropic)
            print(f"✅ Anthropic 提取的SQL: {sql_anthropic}")
            
            # 2. OpenAI 生成 SQL
            print("🧠 OpenAI 生成SQL中...")
            response_openai = self.llm_openai.invoke(prompt)
            sql_openai = self._extract_sql_from_response(response_openai.content.strip())
            print(f"✅ OpenAI 提取的SQL: {sql_openai}")
            
            # 3. 使用执行结果比较方法选择最优SQL
            print("🔍 通过执行结果选择最优SQL中...")
            executor = SQLExecutor(self.db)
            selected_sql = self._select_best_sql_with_execution(
                question, sql_anthropic, sql_openai, table_selection, 
                example_selection, executor
            )
            
            return {
                'sql': selected_sql,
                'reasoning': f'双模型协同生成：Anthropic和OpenAI分别生成SQL，自动选择最优结果',
                'confidence': 0.9,
                'anthropic_sql': sql_anthropic,
                'openai_sql': sql_openai,
                'selected_model': 'dual_model_selection'
            }
            
        except Exception as e:
            print(f"❌ 双模型SQL生成失败: {str(e)}")
            # 回退到单模型
            return self._fallback_single_model(prompt, str(e))
    
    def _extract_sql_from_anthropic_response(self, response_anthropic) -> str:
        """从Anthropic响应中提取SQL"""
        raw_anthropic = ""
        if isinstance(response_anthropic.content, list) and len(response_anthropic.content) > 0:
            # 查找 type='text' 的字典，提取 text 字段
            for item in response_anthropic.content:
                if isinstance(item, dict) and item.get('type') == 'text':
                    raw_anthropic = item.get('text', '')
                    break
            if not raw_anthropic:
                raw_anthropic = str(response_anthropic.content)
        else:
            raw_anthropic = response_anthropic.content
        
        return self._extract_sql_from_response(raw_anthropic)
    
    def _extract_sql_from_response(self, response_text: str) -> str:
        """
        从模型响应中提取SQL语句
        
        Args:
            response_text: 模型的原始响应文本
            
        Returns:
            提取的SQL语句
        """
        # 基本清理
        text = response_text.strip().replace(""", "'").replace(""", "'").replace("\\", "")
        
        # 如果是 ```sql 代码块格式，提取SQL
        if "```sql" in text:
            lines = text.strip().splitlines()
            sql_lines = []
            in_sql_block = False
            for line in lines:
                if line.strip().startswith("```sql"):
                    in_sql_block = True
                    continue
                elif line.strip().startswith("```") and in_sql_block:
                    break
                elif in_sql_block:
                    sql_lines.append(line)
            if sql_lines:
                return "\n".join(sql_lines).strip().rstrip(";")
        
        # 如果包含SELECT关键字，尝试提取SQL部分
        if "SELECT" in text.upper():
            # 找到第一个SELECT的位置
            select_pos = text.upper().find("SELECT")
            sql_part = text[select_pos:].strip()
            # 移除可能的结尾分号
            return sql_part.rstrip(";")
        
        # 直接返回清理后的文本
        return text.strip().rstrip(";")
    
    def _select_best_sql_with_execution(self, question: str, sql_anthropic: str, sql_openai: str, 
                                       table_selection: TableSelection, 
                                       example_selection: ExampleSelectionResult,
                                       executor) -> str:
        """
        通过执行SQL并比较结果来选择最优SQL，或生成新的正确SQL
        """
        # 确保tables是列表
        if isinstance(table_selection.tables, str):
            if table_selection.tables.startswith('[') and table_selection.tables.endswith(']'):
                import ast
                try:
                    tables_list = ast.literal_eval(table_selection.tables)
                except:
                    tables_list = [table_selection.tables]
            else:
                tables_list = [table_selection.tables]
        else:
            tables_list = table_selection.tables
            
        selected_table_infos = get_selected_mschema(self.db_id, tables_list)
        
        # 执行两条SQL
        print("🔍 执行Anthropic SQL...")
        result_anthropic = executor.execute_sql_safely(sql_anthropic)
        print(f"✅ Anthropic执行结果: {result_anthropic['success']}, 行数: {result_anthropic.get('row_count', 0)}")
        
        print("🔍 执行OpenAI SQL...")
        result_openai = executor.execute_sql_safely(sql_openai)
        print(f"✅ OpenAI执行结果: {result_openai['success']}, 行数: {result_openai.get('row_count', 0)}")
        
        # 构建few-shot文本
        few_shot_text = example_selection.few_shot_text if example_selection else ""
        
        # 统一的SQL选择/生成prompt
        unified_prompt = f"""你是一位SQLite数据库专家。请分析两条SQL的执行结果，然后按照以下步骤操作：

1. 首先判断两条SQL的执行结果是否相同（忽略顺序、格式、列属性名等无关结果正确性的差异）
2. 如果结果相同且都正确回答了用户问题，请从中选择更优的一条（考虑简洁性、效率、可读性）
3. 如果结果不同或有执行失败，请生成一条新的正确SQL

用户问题: {question}

表结构信息（M-Schema）:
{selected_table_infos}

参考示例:
{few_shot_text}

SQL 1 (Anthropic): {sql_anthropic}
执行状态: {'成功' if result_anthropic['success'] else '失败'}
执行结果: {result_anthropic['result'] if result_anthropic['success'] else result_anthropic['error']}

SQL 2 (OpenAI): {sql_openai}
执行状态: {'成功' if result_openai['success'] else '失败'}
执行结果: {result_openai['result'] if result_openai['success'] else result_openai['error']}

要求：
- 如果选择现有SQL，必须完整返回选中的SQL
- 如果生成新SQL，严格使用提供的表结构中的表名和字段名
- 确保SQL语法正确，符合SQLite标准
- 逻辑正确，能够准确回答用户问题

仅返回最终的SQL语句，不要添加任何解释或代码块标记。
"""
        
        try:
            print("🔍 SQL选择/生成模型的输入prompt:")
            print("=" * 80)
            print(unified_prompt)
            print("=" * 80)
            
            response = self.llm_openai.invoke(unified_prompt)
            selected_sql = response.content.strip()
            
            # 清理SQL
            if selected_sql.startswith("```sql"):
                lines = selected_sql.strip().splitlines()
                selected_sql = "\n".join(line for line in lines if not line.strip().startswith("```")).strip(";")
            
            print(f"🎯 选择/生成的SQL: {selected_sql}")
            return selected_sql
            
        except Exception as e:
            print(f"⚠️ SQL选择/生成失败，使用fallback策略: {str(e)}")
            # 优先返回执行成功的SQL
            if result_anthropic['success'] and not result_openai['success']:
                return sql_anthropic
            elif result_openai['success'] and not result_anthropic['success']:
                return sql_openai
            else:
                return sql_anthropic  # 默认返回Anthropic结果
    
    def _fallback_single_model(self, prompt: str, error: str) -> Dict[str, Any]:
        """单模型回退策略"""
        try:
            print("🔄 回退到单模型生成...")
            response = self.llm_openai.invoke(prompt)
            return {
                'sql': response.content.strip(),
                'reasoning': f'双模型失败，回退到OpenAI单模型生成。错误: {error}',
                'confidence': 0.7
            }
        except Exception as e2:
            return {
                'sql': '',
                'reasoning': f'SQL生成完全失败: {str(e2)}',
                'confidence': 0.0
            }
    
    def _print_sql_generation_prompt(self, prompt: str, question: str, 
                                   table_selection: TableSelection, 
                                   example_selection: ExampleSelectionResult = None):
        """打印SQL生成的完整prompt信息"""
        print("\n" + "="*100)
        print("📋 SQL生成Prompt详情")
        print("="*100)
        
        print(f"🎯 用户问题: {question}")
        print(f"🗃️ 数据库ID: {self.db_id}")
        print(f"📊 选中的表: {', '.join(table_selection.tables)}")
        print(f"🎯 表选择置信度: {table_selection.confidence_score:.2f}")
        
        # 打印few-shot示例信息
        if example_selection and example_selection.few_shot_text:
            print(f"📚 Few-shot方法: {example_selection.selection_method}")
            print(f"📊 可用示例总数: {example_selection.total_examples}")
            print(f"✅ 选中示例数量: {len(example_selection.selected_examples)}")
        else:
            print("⚠️ 未使用Few-shot示例")
        
        print(f"\n🧾 完整Prompt内容:")
        print("-" * 100)
        print(prompt)
        print("-" * 100)
        print(f"📏 Prompt总长度: {len(prompt)} 字符")
        print("="*100 + "\n")