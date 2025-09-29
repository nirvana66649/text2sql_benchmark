import json
import sqlite3
import os
import sys
from nl2sql import generate_sql_only

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
available_dbs = {
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

def execute_sql(db_path: str, sql: str):
    """执行SQL查询并返回结果"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        print(f"❌ 执行SQL失败: {e}\nSQL内容为：{sql}")
        return None


def evaluate_nl2sql(test_data_path: str):
    """
    评估NL2SQL系统性能
    
    Args:
        test_data_path: 测试数据文件路径，JSON格式
                       每个样本应包含: db_id, question, gold_sql (或 query)
    """
    # 检查测试文件是否存在
    if not os.path.exists(test_data_path):
        print(f"❌ 测试文件不存在: {test_data_path}")
        return
    
    try:
        with open(test_data_path, "r", encoding="utf-8") as f:
            test_samples = json.load(f)
    except Exception as e:
        print(f"❌ 读取测试文件失败: {e}")
        return

    total = len(test_samples)
    correct_result_count = 0
    exec_fail_count = 0
    generation_fail_count = 0

    print(f"🚀 开始评估，共 {total} 个测试样本")
    print("="*60)

    for idx, sample in enumerate(test_samples, 1):
        # 验证样本格式
        if not all(key in sample for key in ["db_id", "question"]):
            print(f"❌ 样本 {idx} 格式错误，缺少必要字段")
            continue
            
        db_id = sample["db_id"]
        question = sample["question"]
        gold_sql = sample.get("gold_sql") or sample.get("query")
        
        if not gold_sql:
            print(f"❌ 样本 {idx} 缺少标准SQL")
            continue
            
        # 验证数据库是否支持
        if db_id not in available_dbs:
            print(f"❌ 样本 {idx} 使用了不支持的数据库: {db_id}")
            continue

        print(f"\n=== 示例 {idx}/{total} ===")
        print(f"📊 数据库: {db_id}")
        print(f"❓ 问题: {question}")

        # 生成SQL
        try:
            pred_sql = generate_sql_only(db_id, question)
        except Exception as e:
            print(f"❌ SQL生成失败: {e}")
            generation_fail_count += 1
            continue

        print(f"🎯 生成SQL: {pred_sql}")
        print(f"✅ 标准SQL: {gold_sql}")

        # 执行SQL并比较结果
        db_path = available_dbs[db_id]
        gold_result = execute_sql(db_path, gold_sql)
        pred_result = execute_sql(db_path, pred_sql)

        if pred_result is None:
            exec_fail_count += 1
            print("❌ 生成SQL执行失败")
            continue

        if gold_result is None:
            print("⚠️ 标准SQL执行失败，跳过此样本")
            continue

        print(f"🧪 标准结果: {gold_result}")
        print(f"🧪 预测结果: {pred_result}")

        # 比较结果
        if gold_result == pred_result:
            print("✅ 结果匹配")
            correct_result_count += 1
        else:
            print("⚠️ 结果集不匹配")

    # 输出评估总结
    print("\n" + "="*60)
    print("📊 评估总结")
    print("="*60)
    print(f"总样本数: {total}")
    print(f"SQL生成成功数: {total - generation_fail_count}")
    print(f"SQL执行成功数: {total - generation_fail_count - exec_fail_count}")
    print(f"结果匹配数: {correct_result_count}")
    print(f"SQL执行结果匹配准确率: {correct_result_count / total:.2%} ({correct_result_count}/{total})")
    print(f"SQL生成失败数: {generation_fail_count}")
    print(f"SQL执行失败数: {exec_fail_count}")


def create_sample_test_file():
    """创建示例测试文件"""
    sample_data = [
        {
            "db_id": "soccer_1",
            "question": "假如总评分低于70的球员的总评分增加了5分，列出总评分和潜在能力差异最大的前三名球员的名字。",
            "gold_sql": "SELECT player_name , MAX ( difference ) FROM ( SELECT B.player_name , ABS ( A.overall_rating - A.potential ) AS difference FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id WHERE A.overall_rating >= 70 UNION SELECT B.player_name , ABS ( A.overall_rating + 5 - A.potential ) AS difference FROM Player_Attributes A JOIN Player B ON A.player_fifa_api_id = B.player_fifa_api_id WHERE A.overall_rating < 70 ) GROUP BY player_name ORDER BY difference DESC LIMIT 3"
        },
        {
            "db_id": "hospital_1", 
            "question": "如果使用过Foo Labs品牌的病人共有10个，使用了Foo Labs品牌的药的病人比使用了Baz Industries品牌的药的病人多多少？",
            "gold_sql": "SELECT 10 - ( SELECT COUNT ( DISTINCT ( Patient ) ) FROM Medication A JOIN Prescribes B ON A.code = B.Medication WHERE A.Brand = \"Baz Industries\" ) AS diff"
        }
    ]
    
    with open("sample_test.json", "w", encoding="utf-8") as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)
    
    print("✅ 已创建示例测试文件: sample_test.json")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  python evaluation.py <test_file.json>  # 运行评估")
        print("  python evaluation.py --create-sample   # 创建示例测试文件")
        sys.exit(1)
    
    if sys.argv[1] == "--create-sample":
        create_sample_test_file()
    else:
        test_file = sys.argv[1]
        evaluate_nl2sql(test_file)
