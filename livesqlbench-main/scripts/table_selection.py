"""
表选择模块 - 包含多阶段选表和置信度评估功能
"""

import json
import re
from typing import List
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_community.utilities.sql_database import SQLDatabase

from models import TableList, TableSelection, ConfidenceEvaluation
from nl2sql_utils import get_table_details, get_selected_mschema, get_selected_table_infos, parse_json_response, validate_table_names, get_selected_table_details
from config import TABLE_SELECTION_CONFIG

class TableSelector:
    """表选择器类"""
    
    def __init__(self, llm):
        self.llm = llm
        self.parser = PydanticOutputParser(pydantic_object=TableList)
        
    def evaluate_table_selection_confidence(self, question: str, selected_tables: List[str], 
                                           db_id: str, db: SQLDatabase) -> ConfidenceEvaluation:
        """评估选表结果的置信度"""
        try:
            # 获取表的高层次描述和基本结构信息的组合
            from nl2sql_utils import get_table_details
            table_descriptions = get_table_details(db_id)
            
            # 获取选中表的m-schema结构信息（与SQL生成保持一致）
            from nl2sql_utils import get_selected_mschema
            selected_table_infos = get_selected_mschema(db_id, selected_tables)
            
            # 构建置信度评估Prompt（使用更宽松的评估标准）
            confidence_prompt = f"""
你是一个数据库专家，需要评估表选择的置信度。请基于表的功能描述和基本结构来判断。

用户问题：{question}
数据库：{db_id}

### 所有表的功能描述：
{table_descriptions}

### 选中表的结构信息（m-schema格式）：
{selected_table_infos}

请评估选中的表是否足以支持回答用户问题，重点关注：
1. 表的核心功能是否与问题相关
2. 是否包含问题所需的关键字段
3. 表之间的关联关系是否支持查询需求

**评估标准（相对宽松）**：
- 0.9-1.0：表的功能完全匹配问题需求，包含所有关键字段
- 0.7-0.8：表的功能基本匹配，包含主要字段，可能需要一些推理
- 0.5-0.6：表的功能部分相关，包含部分必要字段
- 0.3-0.4：表的功能勉强相关，字段可能不够完整
- 0.0-0.2：表的功能与问题明显不匹配

请严格按照以下JSON格式回答：
{{"confidence_score": 分数}}
"""
            
            # 调用LLM评估
            response = self.llm.invoke(confidence_prompt)
            response_text = response.content.strip()
            
            # 解析响应
            try:
                result = parse_json_response(response_text)
                confidence_score = float(result.get('confidence_score', 0.5))
                reasoning = "评估完成"  # 固定简单说明
            except:
                # 尝试从文本中提取数字
                score_match = re.search(r'(\d+\.?\d*)', response_text)
                confidence_score = float(score_match.group(1)) if score_match else 0.5
                if confidence_score > 1.0:
                    confidence_score = confidence_score / 10.0  # 可能是百分比
                reasoning = "评估完成"  # 固定简单说明
            
            # 确保置信度在有效范围内
            confidence_score = max(0.0, min(1.0, confidence_score))
            
            return ConfidenceEvaluation(
                confidence_score=confidence_score,
                reasoning=reasoning,
                status='success'
            )
                
        except Exception as e:
            print(f"⚠️ 置信度评估失败: {e}")
            return ConfidenceEvaluation(
                confidence_score=0.5,
                reasoning=f'置信度评估失败: {str(e)}',
                status='error'
            )

    def smart_fallback_strategy(self, question: str, db_id: str, db: SQLDatabase, 
                               failed_selection: List[str] = None) -> List[str]:
        """智能fallback策略：表排序而非全选"""
        try:
            print("🔄 启动智能fallback策略...")
            all_tables = db.get_usable_table_names()
            
            if len(all_tables) <= 5:
                print(f"📋 表数量较少({len(all_tables)}个)，直接返回所有表")
                return all_tables
            
            # 获取所有表的高层次描述
            table_details = get_table_details(db_id)
            
            # 构建表排序Prompt
            ranking_prompt = f"""
你是一个数据库专家，需要根据用户问题对表进行相关性排序。

用户问题：{question}
数据库：{db_id}

所有表的描述：
{table_details}

请根据与用户问题的相关性对表进行排序，并选择最相关的5-8个表。

排序标准：
1. 直接相关：表中包含问题直接涉及的实体或概念
2. 间接相关：表中包含可能需要的关联信息
3. 支持信息：表中包含可能有用的补充信息

请严格按照以下JSON格式回答：
{{"ranked_tables": ["table1", "table2", "table3", ...]}}

只返回最相关的5-8个表名，按相关性从高到低排序。
"""
            
            # 调用LLM进行表排序
            response = self.llm.invoke(ranking_prompt)
            
            # 解析响应
            try:
                result = parse_json_response(response.content.strip())
                ranked_tables = result.get('ranked_tables', [])
                
                # 验证表名有效性
                valid_tables = validate_table_names(ranked_tables, all_tables)
                
                if len(valid_tables) >= 3:
                    print(f"✅ 智能fallback成功，选择了{len(valid_tables)}个最相关的表")
                    return valid_tables[:TABLE_SELECTION_CONFIG['fallback_max_tables']]
                else:
                    print(f"⚠️ 智能fallback返回表数量不足，使用前{TABLE_SELECTION_CONFIG['fallback_max_tables']}个表")
                    return all_tables[:TABLE_SELECTION_CONFIG['fallback_max_tables']]
                    
            except Exception as e:
                print(f"⚠️ 智能fallback解析失败: {e}")
                return all_tables[:TABLE_SELECTION_CONFIG['fallback_max_tables']]
                
        except Exception as e:
            print(f"⚠️ 智能fallback失败: {e}")
            return all_tables[:TABLE_SELECTION_CONFIG['fallback_max_tables']] if len(all_tables) > TABLE_SELECTION_CONFIG['fallback_max_tables'] else all_tables

    def select_tables_multi_stage(self, question: str, db_id: str, db: SQLDatabase) -> TableSelection:
        """多阶段选表：粗选+精选，提高准确性"""
        
        # 获取表描述和所有表
        table_description_text = get_table_details(db_id)
        all_tables = db.get_usable_table_names()

        print(f"\n🔍 开始多阶段选表，总表数：{len(all_tables)}")
        
        # === 第一阶段：粗选 ===
        print("📋 第一阶段：粗选（基于表描述快速筛选）")
        coarse_system_msg = f"""你是一个数据库表粗选专家。请基于表的高层次描述，快速筛选出可能与用户问题相关的表。

### 表的高层次描述：
{table_description_text}

### 粗选规则：
1. 宁可多选，不可漏选 - 如果不确定是否相关，倾向于包含该表
2. 重点关注表的核心功能和示例问题，判断是否与用户问题领域相关
3. 考虑多表联查的可能性，包含可能作为连接桥梁的表
4. 至少选择2个表，最多选择{min(TABLE_SELECTION_CONFIG['max_coarse_tables'], len(all_tables))}个表

可选表名：{', '.join(all_tables)}
输出格式：{{"tables": ["表名1", "表名2"]}}"""

        coarse_prompt = PromptTemplate(
            template="{system_msg}\n用户问题：{question}\n\n{format_instructions}",
            input_variables=["system_msg", "question"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

        try:
            formatted_coarse_prompt = coarse_prompt.format_prompt(system_msg=coarse_system_msg, question=question)
            coarse_output = self.llm.invoke(formatted_coarse_prompt.to_string())
            coarse_result = self.parser.parse(coarse_output.content)
            coarse_selected = validate_table_names(coarse_result.tables, all_tables)
            print(f"✅ 粗选结果：{coarse_selected} ({len(coarse_selected)}/{len(all_tables)})")
            
            # 如果粗选结果为空或过少，使用fallback
            if len(coarse_selected) == 0:
                print("⚠️ 粗选结果为空，使用全部表")
                fallback_tables = all_tables
                confidence_result = self.evaluate_table_selection_confidence(question, fallback_tables, db_id, db)
                return TableSelection(
                    tables=fallback_tables,
                    confidence_score=confidence_result.confidence_score,
                    reasoning="粗选结果为空，使用全部表",
                    selection_method="fallback_all_tables"
                )
            elif len(coarse_selected) == 1:
                print("⚠️ 粗选结果过少，直接返回")
                confidence_result = self.evaluate_table_selection_confidence(question, coarse_selected, db_id, db)
                return TableSelection(
                    tables=coarse_selected,
                    confidence_score=confidence_result.confidence_score,
                    reasoning="粗选结果过少，直接返回",
                    selection_method="coarse_only"
                )
                
        except Exception as e:
            print(f"❌ 粗选失败：{e}，使用全部表")
            fallback_tables = all_tables
            confidence_result = self.evaluate_table_selection_confidence(question, fallback_tables, db_id, db)
            return TableSelection(
                tables=fallback_tables,
                confidence_score=confidence_result.confidence_score,
                reasoning="粗选失败，使用全部表",
                selection_method="fallback_coarse_failed"
            )

        # === 第二阶段：精选 ===
        print("🎯 第二阶段：精选（基于详细schema精确筛选）")
        
        # 获取粗选表的详细schema和描述信息
        selected_mschema = get_selected_mschema(db_id, coarse_selected)
        selected_table_descriptions = get_selected_table_details(db_id, coarse_selected)
        
        fine_system_msg = f"""你是一个数据库表精选专家。基于粗选结果，请进行精确的表选择。

### 粗选表的功能描述：
{selected_table_descriptions}

### 粗选表的详细结构（m-schema）：
{selected_mschema}

### 精选规则：
1. 仔细分析用户问题需要哪些具体字段和数据
2. 结合表的功能描述和详细结构，判断表的相关性
3. 检查表之间的关联关系，确保选择的表能够通过JOIN连接
4. 优先选择直接包含问题所需字段的表
5. 如果需要多表联查，确保包含必要的关联表
6. 去除明显不相关的表，但保留核心相关表
7. 必须选择至少1个最相关的表（如果不确定，返回粗选中相关性最高的1-2个）
8. 最终选择1-{min(TABLE_SELECTION_CONFIG['max_fine_tables'], len(coarse_selected))}个最相关的表

候选表（来自粗选）：{', '.join(coarse_selected)}
输出格式：{{"tables": ["表名1", "表名2"]}}"""

        fine_prompt = PromptTemplate(
            template="{system_msg}\n用户问题：{question}\n\n{format_instructions}",
            input_variables=["system_msg", "question"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

        try:
            formatted_fine_prompt = fine_prompt.format_prompt(system_msg=fine_system_msg, question=question)
            fine_output = self.llm.invoke(formatted_fine_prompt.to_string())
            print(f"🔍 精选LLM原始输出: {fine_output.content}")
            fine_result = self.parser.parse(fine_output.content)
            fine_selected = validate_table_names(fine_result.tables, coarse_selected)
            print(f"✅ 精选结果：{fine_selected} ({len(fine_selected)}/{len(coarse_selected)})")
            
            # 如果精选结果为空，回退到粗选结果
            if len(fine_selected) == 0:
                print("⚠️ 精选结果为空，回退到粗选结果")
                confidence_result = self.evaluate_table_selection_confidence(question, coarse_selected, db_id, db)
                return TableSelection(
                    tables=coarse_selected,
                    confidence_score=confidence_result.confidence_score,
                    reasoning="精选结果为空，回退到粗选结果",
                    selection_method="coarse_fallback"
                )
            
            print(f"🎉 多阶段选表完成：{fine_selected}")
            
            # 评估置信度
            print("📊 评估选表置信度...")
            confidence_result = self.evaluate_table_selection_confidence(question, fine_selected, db_id, db)
            confidence_score = confidence_result.confidence_score
            
            print(f"📈 置信度分数: {confidence_score:.2f}")
            
            # 根据置信度决定是否需要fallback
            if confidence_score < TABLE_SELECTION_CONFIG['confidence_threshold']:
                print(f"⚠️ 置信度过低 ({confidence_score:.2f} < {TABLE_SELECTION_CONFIG['confidence_threshold']})，启用智能fallback策略")
                fallback_tables = self.smart_fallback_strategy(question, db_id, db, fine_selected)
                fallback_confidence = self.evaluate_table_selection_confidence(question, fallback_tables, db_id, db)
                return TableSelection(
                    tables=fallback_tables,
                    confidence_score=fallback_confidence.confidence_score,
                    reasoning="智能fallback策略",
                    selection_method="smart_fallback"
                )
            
            return TableSelection(
                tables=fine_selected,
                confidence_score=confidence_score,
                reasoning="多阶段选表",
                selection_method="multi_stage"
            )
            
        except Exception as e:
            print(f"❌ 精选失败：{e}，使用智能fallback策略")
            fallback_tables = self.smart_fallback_strategy(question, db_id, db, [])
            fallback_confidence = self.evaluate_table_selection_confidence(question, fallback_tables, db_id, db)
            return TableSelection(
                tables=fallback_tables,
                confidence_score=fallback_confidence.confidence_score,
                reasoning="精选失败，使用智能fallback策略",
                selection_method="fallback_fine_failed"
            )