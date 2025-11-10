#!/usr/bin/env python3
"""
LangGraph 管线：将现有 NL2SQL 模块编排为有状态、可回路的图。

节点：
- table_selection: 多阶段选表（含智能 fallback）
- example_selection: 语义相似性选 few-shot
- sql_generation: 双模型生成 + 选择
- validate_sql: 语法验证与修复（EXPLAIN）
- execute: 执行 SQL，收集结果
- sql_repair: 根据执行错误进行修复，回到 execute（重试上限）

使用：由 graph_runner.py 构建并运行。
"""
from __future__ import annotations

import sys
from typing import Dict, Any, List
from typing import TypedDict
from pathlib import Path

# 兼容导入 scripts 模块
CURRENT_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = CURRENT_DIR.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.append(str(SCRIPTS_DIR))

from langgraph.graph import StateGraph, END
from langchain_community.utilities.sql_database import SQLDatabase

# 复用现有模块
from config import get_llm_instance, get_llm_anthropic, get_db_path, TABLE_SELECTION_CONFIG
from table_selection import TableSelector
from example_selection import ExampleSelector
from sql_generator import SQLGenerator
from sql_executor import SQLExecutor
from sql_validator import SQLValidator
from models import TableSelection as TableSelectionModel, ExampleSelectionResult as ExampleSelectionModel


class GraphState(TypedDict, total=False):
    """Graph 运行时状态"""
    db_id: str
    question: str
    db: Any
    llm_openai: Any
    llm_anthropic: Any
    table_selection: TableSelectionModel
    example_selection: ExampleSelectionModel
    sql: str
    exec_result: Dict[str, Any]
    retries: int
    trace: List[str]


MAX_RETRIES = 2


def build_graph(db_id: str) -> StateGraph:
    """构建 LangGraph，返回可编排的 StateGraph。"""
    # 初始化依赖
    llm_openai = get_llm_instance()
    llm_anthropic = get_llm_anthropic()

    db_path = get_db_path(db_id)
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

    table_selector = TableSelector(llm_openai)
    example_selector = ExampleSelector()
    sql_generator = SQLGenerator(llm_openai, llm_anthropic, db_id, db)
    sql_executor = SQLExecutor(db)
    sql_validator = SQLValidator(llm_openai, db_id, db)

    graph = StateGraph(GraphState)

    # 节点定义
    def table_selection_node(state: GraphState) -> GraphState:
        question = state["question"]
        result = table_selector.select_tables_multi_stage(question, db_id, db)
        trace = state.get("trace", []) + [f"table_selection: {result.tables} (conf={result.confidence_score:.2f})"]
        return {
            **state,
            "table_selection": result,
            "trace": trace,
        }

    def example_selection_node(state: GraphState) -> GraphState:
        question = state["question"]
        ts = state["table_selection"]
        ex_result = example_selector.get_example_selection_result(db_id, question, ts.tables)
        trace = state.get("trace", []) + [f"example_selection: {ex_result.selected_count}/{ex_result.total_examples}"]
        return {**state, "example_selection": ex_result, "trace": trace}

    def sql_generation_node(state: GraphState) -> GraphState:
        question = state["question"]
        ts = state["table_selection"]
        ex = state["example_selection"]
        sql_out = sql_generator.generate_sql_dual_model(question, ts, ex)
        sql = sql_out.get("sql", "").strip()
        trace = state.get("trace", []) + ["sql_generation: dual_model"]
        return {**state, "sql": sql, "trace": trace}

    def validate_sql_node(state: GraphState) -> GraphState:
        question = state["question"]
        ts = state["table_selection"]
        sql = state.get("sql", "")
        validated_sql = sql_validator.validate_and_repair_sql(sql, question, ts.tables)
        trace = state.get("trace", []) + ["validate_sql: EXPLAIN PASS or repaired"]
        return {**state, "sql": validated_sql, "trace": trace}

    def execute_node(state: GraphState) -> GraphState:
        sql = state.get("sql", "")
        exec_result = sql_executor.execute_sql_safely(sql)
        trace = state.get("trace", []) + [f"execute: success={exec_result.get('success', False)}, rows={exec_result.get('row_count', 0)}"]
        return {**state, "exec_result": exec_result, "trace": trace}

    def sql_repair_node(state: GraphState) -> GraphState:
        # 基于执行错误再次修复
        question = state["question"]
        ts = state["table_selection"]
        sql = state.get("sql", "")
        error = state.get("exec_result", {}).get("error", "")
        # 直接使用内部修复以注入运行期错误上下文
        repaired_sql = sql_validator._repair_sql(sql, question, ts.tables, error)  # noqa
        retries = state.get("retries", 0) + 1
        trace = state.get("trace", []) + [f"sql_repair: retry={retries}"]
        return {**state, "sql": repaired_sql, "retries": retries, "trace": trace}

    # 条件路由
    def should_repair(state: GraphState) -> str:
        exec_result = state.get("exec_result", {})
        success = exec_result.get("success", False)
        retries = state.get("retries", 0)
        if success:
            return END
        if retries >= MAX_RETRIES:
            return END
        return "sql_repair"

    # 图装配
    graph.add_node("table_selection", table_selection_node)
    graph.add_node("example_selection", example_selection_node)
    graph.add_node("sql_generation", sql_generation_node)
    graph.add_node("validate_sql", validate_sql_node)
    graph.add_node("execute", execute_node)
    graph.add_node("sql_repair", sql_repair_node)

    graph.set_entry_point("table_selection")
    graph.add_edge("table_selection", "example_selection")
    graph.add_edge("example_selection", "sql_generation")
    graph.add_edge("sql_generation", "validate_sql")
    graph.add_edge("validate_sql", "execute")
    graph.add_conditional_edges("execute", should_repair, {"sql_repair": "sql_repair", END: END})
    graph.add_edge("sql_repair", "execute")

    return graph


def initial_state(db_id: str, question: str) -> GraphState:
    return {
        "db_id": db_id,
        "question": question,
        "retries": 0,
        "trace": [],
    }