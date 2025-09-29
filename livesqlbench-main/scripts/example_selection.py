"""
示例选择模块 - 使用简单的语义相似性RAG方式选择few-shot示例
"""

from typing import List, Dict, Any
from langchain_chroma import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

from config import get_embedding_config, EXAMPLE_SELECTION_CONFIG
from models import ExampleSelectionResult

# 示例导入
from bike_1_examples import bike_1_examples
from concert_singer_examples import concert_singer_examples
from customers_and_products_contacts_examples import customers_and_products_contacts_examples
from driving_school_examples import driving_school_examples
from formula_1_examples import formula_1_examples
from hospital_1_examples import hospital_1_examples
from riding_club_examples import riding_club_examples
from soccer_1_examples import soccer_1_examples
from wine_1_examples import wine_1_examples
from world_1_examples import world_1_examples


class ExampleSelector:
    """示例选择器 - 使用语义相似性RAG方式"""
    
    def __init__(self):
        """初始化示例选择器"""
        self.example_map = {
            "bike_1": bike_1_examples,
            "concert_singer": concert_singer_examples,
            "customers_and_products_contacts": customers_and_products_contacts_examples,
            "driving_school": driving_school_examples,
            "formula_1": formula_1_examples,
            "hospital_1": hospital_1_examples,
            "riding_club": riding_club_examples,
            "soccer_1": soccer_1_examples,
            "wine_1": wine_1_examples,
            "world_1": world_1_examples
        }
        
    def build_few_shot_prompt(self, db_id: str, k: int = None) -> FewShotChatMessagePromptTemplate:
        """构建few-shot prompt"""
        if k is None:
            k = EXAMPLE_SELECTION_CONFIG['default_k']
            
        selected_examples = self.example_map.get(db_id)
        if not selected_examples:
            raise ValueError(f"未知数据库 ID：{db_id}")

        vectorstore = Chroma()
        vectorstore.delete_collection()

        embedding_config = get_embedding_config()
        example_selector = SemanticSimilarityExampleSelector.from_examples(
            selected_examples,
            OpenAIEmbeddings(**embedding_config),
            vectorstore,
            k=k,
            input_keys=["input"]
        )

        example_prompt = ChatPromptTemplate.from_messages([
            ("human", "问题：{input}\n推理方式：{reasoning_type}\n常识知识：{commonsense_knowledge}\n对应生成的 SQL 查询语句："),
            ("ai", "{query}")
        ])

        return FewShotChatMessagePromptTemplate(
            example_selector=example_selector,
            example_prompt=example_prompt,
            input_variables=["input", "reasoning_type", "commonsense_knowledge"]
        )

    def generate_few_shot_text(self, few_shot_prompt: FewShotChatMessagePromptTemplate, question: str) -> str:
        """生成few-shot文本"""
        selected_examples = few_shot_prompt.example_selector.select_examples({"input": question})
        texts = []
        for ex in selected_examples:
            texts.append(
                f"Human: 问题：{ex['input']}\n推理方式：{ex['reasoning_type']}\n常识知识：{ex['commonsense_knowledge']}\n对应生成的 SQL 查询语句：\nAI: {ex['query']}"
            )
        return "\n\n".join(texts)

    def get_example_selection_result(self, db_id: str, question: str, selected_tables: List[str] = None, 
                                   method: str = "semantic") -> ExampleSelectionResult:
        """获取示例选择结果 - 使用简单的语义相似性RAG方式"""
        all_examples = self.example_map.get(db_id, [])
        
        # 统一使用传统的语义相似性选择，不再使用复杂的动态选择
        print("📚 使用语义相似性RAG选择few-shot示例...")
        few_shot_prompt = self.build_few_shot_prompt(db_id)
        # 先拿到列表，再生成文本，确保可返回结构化结果
        selected_list = few_shot_prompt.example_selector.select_examples({"input": question})
        example_text = self.generate_few_shot_text(few_shot_prompt, question)
        selected_count = len(selected_list)
        
        return ExampleSelectionResult(
            selected_examples=selected_list if 'selected_list' in locals() else [],
            selection_method="semantic",
            total_examples=len(all_examples),
            selected_count=selected_count,
            few_shot_text=example_text
        )