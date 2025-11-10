#!/usr/bin/env python3
"""
LangGraph Runner：命令行入口
示例：
python -m livesqlbench-main.langgraph_pipeline.graph_runner --db_id hospital_1 --question "如果约翰·史密斯是国际护士节那天出院的，他住了几天院？"
"""
# - - python -m langgraph_pipeline.graph_runner --db_id hospital_1 --question "如果约翰·史密斯是国际护士节那天出院的，他住了几天院？"

import argparse
import json
from typing import Any

from langgraph_pipeline.graph import build_graph, initial_state


def run(db_id: str, question: str) -> dict:
    graph = build_graph(db_id)
    app = graph.compile()

    state = initial_state(db_id, question)
    final_state: Any = app.invoke(state)

    # 汇总输出
    table_selection = final_state.get("table_selection")
    exec_result = final_state.get("exec_result", {})
    out = {
        "db_id": db_id,
        "question": question,
        "selected_tables": table_selection.tables if table_selection else [],
        "confidence_score": getattr(table_selection, "confidence_score", None),
        "sql": final_state.get("sql", ""),
        "exec_success": exec_result.get("success", False),
        "row_count": exec_result.get("row_count", 0),
        "error": exec_result.get("error"),
        "retries": final_state.get("retries", 0),
        "trace": final_state.get("trace", []),
    }
    return out


def main():
    parser = argparse.ArgumentParser(description="NL2SQL LangGraph 管线")
    parser.add_argument("--db_id", type=str, required=True)
    parser.add_argument("--question", type=str, required=True)
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()

    result = run(args.db_id, args.question)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"✅ 结果已保存到: {args.output}")
    else:
        print("\n" + "=" * 50)
        print("🎯 LangGraph NL2SQL 结果:")
        print("=" * 50)
        print(f"问题: {result['question']}")
        print(f"数据库: {result['db_id']}")
        print(f"选择的表: {', '.join(result['selected_tables'])}")
        print(f"置信度: {result['confidence_score']}")
        print(f"最终 SQL:\n{result['sql']}")
        print(f"执行成功: {result['exec_success']}, 行数: {result['row_count']}")
        if result.get("error"):
            print(f"错误: {result['error']}")
        print("轨迹:")
        for step in result.get("trace", []):
            print(" - " + step)


if __name__ == "__main__":
    main()