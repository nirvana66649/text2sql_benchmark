# NL2SQL 智能问答系统（多数据库）

> 基于 **GPT-4o + Claude Sonnet 4** 双模型架构的自然语言转 SQL 系统，集成 M-Schema 表结构理解、智能表选择与简化 RAG 检索，支持复杂推理和多数据库任务。

---

## 📌 项目简介

本项目实现了一个基于 **LangChain + OpenAI GPT-4o + Anthropic Claude Sonnet 4** 的高性能自然语言转 SQL 系统（NL2SQL），采用双模型架构和简化的 RAG（检索增强生成）技术，可将用户输入的自然语言问题自动转化为 SQLite 可执行的 SQL 查询语句。

### 🚀 核心特性

1. ✅ **双模型架构**：GPT-4o + Claude Sonnet 4 协同生成，自动选择最优 SQL
2. ✅ **M-Schema 集成**：深度理解数据库表结构、字段关系和约束条件
3. ✅ **智能表选择**：基于 Pydantic 的严格表名验证和语义相关性筛选
4. ✅ **简化 RAG 检索**：纯语义相似性的 few-shot 示例检索，避免复杂的权重计算
5. ✅ **推理类型识别**：支持加法、减法、乘法、除法、假设条件、常识推理
6. ✅ **SQL 验证与修复**：自动语法检查和错误修复机制
7. ✅ **多数据库兼容**：支持 10+ 个典型数据库场景

---

## ⚙️ 技术架构

### 1. 双模型协同架构

```python
# GPT-4o 负责表选择和 SQL 生成
llm_openai = ChatOpenAI(model='gpt-4o', temperature=0.3)

# Claude Sonnet 4 负责 SQL 生成和优化
llm_anthropic = ChatAnthropic(model_name="cc-sonnet-4-20250514-thinking", temperature=0.3)
```

### 2. M-Schema 表结构理解

- 集成 M-Schema 引擎，深度解析数据库表结构
- 自动提取表关系、字段类型、约束条件
- 支持复杂查询的表关联和字段映射

### 3. 智能表选择机制

```python
class TableList(BaseModel):
    tables: List[str] = Field(description="List of relevant table names")
```

- 使用 Pydantic 模型严格控制表名输出格式
- 结合表描述和 M-Schema 进行语义相关性判断
- 自动过滤无关表，提升查询效率

### 4. 简化 RAG 检索系统

- **向量数据库**：Chroma + OpenAI Embeddings
- **检索策略**：纯语义相似性匹配，返回最相关的示例
- **示例格式**：包含推理类型、常识知识和 SQL 模板
- **简化设计**：移除复杂的表匹配权重计算，专注于语义相似性

### 5. SQL 生成与优化

- **推理类型识别**：`+`（加法）、`-`（减法）、`*`（乘法）、`/`（除法）、`H`（假设）、`C`（常识）
- **双模型生成**：GPT-4o 和 Claude 分别生成 SQL
- **智能选择**：基于正确性、语法兼容性、高效性自动选择最优 SQL
- **验证修复**：EXPLAIN QUERY PLAN 验证 + 自动错误修复
- **简化流程**：专注于语义相似性检索，避免复杂的动态权重计算

---

## 🧩 项目结构

```text
livesqlbench-main/
├── nl2sql.py                     # 主程序（双模型架构）
├── evaluation.py                 # 批量评估脚本
├── examples/                     # few-shot 示例（按数据库组织）
│   ├── bike_1_examples.py
│   ├── concert_singer_examples.py
│   └── ...
├── database/                     # 多数据库 SQLite 文件
│   ├── bike_1/
│   ├── concert_singer/
│   └── ...
├── M-Schema/                     # M-Schema 表结构引擎
│   ├── schema_engine.py
│   ├── m_schema.py
│   └── ...
├── {db_id}_table_description.csv # 表结构描述文件
├── requirements.txt              # Python 依赖包
└── README.md                     # 本文件
```

---

## 🧪 使用说明

### 1. 环境配置

```bash
# 创建虚拟环境
cd ./livesqlbench/livesqlbench-main
conda create -n livesqlbench python=3.10 -y
conda activate livesqlbench

# 安装依赖
cd ./livesqlbench/livesqlbench-main/config
pip install -r requirements.txt
```

### 2. API 配置

系统使用以下 API 端点：

- **OpenAI GPT-4o**：`https://api.gpt.ge/v1`
- **Anthropic Claude**：`https://api.gpt.ge`
- **OpenAI Embeddings**：`https://api.gpt.ge/v1`

please remember to switch to your own base url
```python
# API Key 配置示例
api_key = "your api key"
```

### 3. M-Schema 配置

M-Schema 是系统的核心表结构理解引擎，需要正确配置才能正常工作。

#### 3.1 M-Schema 目录结构

```text
M-Schema/
├── __init__.py              # 包初始化文件
├── schema_engine.py         # 主引擎文件
├── m_schema.py             # M-Schema 核心类
├── utils.py                # 工具函数
├── requirements.txt         # M-Schema 专用依赖
├── README.md               # M-Schema 说明文档
└── example.py              # 使用示例
```

#### 3.2 M-Schema 依赖安装，具体参考：https://github.com/XGenerationLab/M-Schema

M-Schema 需要额外的依赖包，请确保安装：

```bash
# 安装 M-Schema 专用依赖，conda激活之后
git clone https://github.com/XGenerationLab/M-Schema.git
cd M-Schema
pip install -r requirements.txt
```

#### 3.3 M-Schema 工作原理

M-Schema 引擎通过以下步骤解析数据库结构：

1. **数据库连接**：使用 SQLAlchemy 连接到 SQLite 数据库
2. **元数据提取**：自动提取表结构、字段类型、约束条件
3. **关系分析**：分析表间的主键、外键关系
4. **Schema 生成**：生成结构化的 M-Schema 描述

#### 3.4 M-Schema 配置示例

```python
from sqlalchemy import create_engine
from M-Schema.schema_engine import SchemaEngine

# 创建数据库引擎
db_path = "database/wine_1/wine_1.sqlite"
abs_path = os.path.abspath(db_path)
db_engine = create_engine(f"sqlite:///{abs_path}")

# 初始化 M-Schema 引擎
schema_engine = SchemaEngine(engine=db_engine, db_name="wine_1")

# 获取 M-Schema 描述
mschema = schema_engine.mschema
mschema_str = mschema.to_mschema()
print(mschema_str)
```

#### 3.5 M-Schema 输出格式

M-Schema 生成的描述包含：

- **表结构**：表名、字段名、数据类型、约束
- **关系信息**：主键、外键、索引
- **语义描述**：字段的业务含义和用途
- **查询建议**：常用的查询模式和示例

#### 3.6 故障排除

如果遇到 M-Schema 相关错误：

1. **依赖问题**：确保安装了所有 M-Schema 依赖
2. **路径问题**：检查数据库文件路径是否正确
3. **权限问题**：确保有读取数据库文件的权限
4. **版本兼容**：确保 SQLAlchemy 版本兼容（>=1.4.0）

### 4. 使用方式

#### 交互式 CLI 模式

```bash
cd livesqlbench-main/scripts
python nl2sql.py --db_id soccer_1 --question 具体问题

示例：
python nl2sql.py --db_id soccer_1 --question "传球得分包括5%的弧线球、5%的任意球精度、15%的长传、20%的传中、20%的视野和35%的短传。列出传球得分最高的前10名球员的姓名和当前年龄。"
```

#### 程序化调用：调用 `generate_sql_only` 函数，同理还是需要输入数据库 ID 和自然语言问题。

```python
from nl2sql import generate_sql_only

# 单次查询
sql = generate_sql_only(
    db_id="wine_1",
    question="有多少种酒产自索诺玛县，比产自纳帕县的酒多多少？"
)
print(sql)

# 批量处理
questions = [
    ("concert_singer", "列出所有歌手的姓名"),
    ("bike_1", "统计每个车站的停靠点数量"),
    ("wine_1", "有多少种酒产自索诺玛县，比产自纳帕县的酒多多少？")
]

for db_id, question in questions:
    sql = generate_sql_only(db_id, question)
    print(f"数据库: {db_id}")
    print(f"问题: {question}")
    print(f"SQL: {sql}\n")
```

### 5. 支持的数据库

系统支持以下 10 个数据库：

- `bike_1` - 自行车租赁系统
- `concert_singer` - 音乐会歌手管理
- `customers_and_products_contacts` - 客户产品联系
- `driving_school` - 驾校管理
- `formula_1` - F1 赛车数据
- `hospital_1` - 医院管理系统
- `riding_club` - 骑行俱乐部
- `soccer_1` - 足球数据
- `wine_1` - 葡萄酒数据库
- `world_1` - 世界地理数据

---

## 📊 评估与测试

### 1. 批量评估

系统提供了完善的评估工具来测试NL2SQL的性能：

```bash
cd livesqlbench-main/scripts

# 运行评估（需要提供测试文件）
python evaluation.py test_data.json

# 创建示例测试文件
python evaluation.py --create-sample

# 查看使用帮助
python evaluation.py
```

### 2. 测试数据格式

测试文件应为JSON格式，每个样本包含以下字段：

```json
[
  {
    "db_id": "soccer_1",
    "question": "列出所有球员的姓名",
    "gold_sql": "SELECT player_name FROM Player"
  },
  {
    "db_id": "wine_1",
    "question": "有多少种酒产自索诺玛县，比产自纳帕县的酒多多少？",
    "gold_sql": "SELECT sonoma, sonoma - napa AS diff FROM (SELECT COUNT(*) AS sonoma FROM wine A JOIN appellations B ON A.Appelation = B.Appelation WHERE B.County = 'Sonoma') JOIN (SELECT COUNT(*) AS napa FROM wine A JOIN appellations B ON A.Appelation = B.Appelation WHERE B.County = 'Napa')"
  }
]
```

**字段说明**：
- `db_id`：数据库标识符（必须是支持的10个数据库之一）
- `question`：自然语言问题
- `gold_sql` 或 `query`：标准SQL查询（用于结果比较）

### 3. 评估指标

评估系统会输出以下指标：

- **总样本数**：测试集中的样本总数
- **SQL生成成功数**：成功生成SQL的样本数
- **SQL执行成功数**：生成的SQL能够成功执行的样本数
- **结果匹配数**：执行结果与标准答案完全匹配的样本数
- **SQL执行结果匹配准确率**：结果匹配数 / 总样本数
- **SQL生成失败数**：无法生成SQL的样本数
- **SQL执行失败数**：生成的SQL执行出错的样本数

### 4. 推理类型示例

系统支持多种推理类型：

- **算术推理**：`+` 加法、`-` 减法、`*` 乘法、`/` 除法
- **逻辑推理**：`H` 假设条件推理、`C` 常识推理
- **复杂查询**：多表 JOIN、子查询、聚合函数

---

## 💰 成本估算

### 单次推理成本

- **表选择**：GPT-4o + Pydantic 解析 ≈ $0.01
- **RAG 检索**：Embedding 向量查找 ≈ $0.005
- **SQL 生成**：双模型生成 + 选择 ≈ $0.03
- **验证修复**：SQL 验证 ≈ $0.005

**总计**：约 $0.05 每次推理

### 批量评估成本

- 预计样本量：500 条
- 总成本预估：约 $25-$35

---

## 🔧 技术细节

### 1. 表选择流程

```python
def select_tables_via_parser(llm, question: str, db_id: str, db: SQLDatabase) -> List[str]:
    # 1. 获取表描述和 M-Schema
    # 2. 使用 Pydantic 解析器严格控制输出
    # 3. 验证表名有效性
    # 4. 返回相关表列表
```

### 2. SQL 生成流程

```python
def generate_sql_only(db_id: str, question: str) -> str:
    # 1. 智能表选择
    # 2. 简化 RAG 示例检索（纯语义相似性）
    # 3. M-Schema 提取
    # 4. 双模型 SQL 生成
    # 5. 智能选择最优 SQL
    # 6. 验证与修复
```

### 3. 错误处理机制

- **语法验证**：使用 `EXPLAIN QUERY PLAN` 验证 SQL 语法
- **自动修复**：检测到错误时自动调用修复模型
- **回退机制**：修复失败时返回清理后的原始 SQL

---

## 🙌 致谢与说明

- 本项目基于 **Archer Benchmark** 官方数据集开发
- 集成 **M-Schema** 表结构理解引擎
- 使用 **LangChain** 框架构建 AI 应用
- 支持 **OpenAI GPT-4o** 和 **Anthropic Claude Sonnet 4** 双模型架构

### 免责声明

- 本项目仅用于学术研究与 Benchmark 提交
- 所有模型调用基于公开 API，调用成本需自理
- 示例数据库及结构来自 Archer Benchmark 官方数据集
