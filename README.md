# NL2SQL Intelligent Q&A System (Multi-Database)

> Based on **GPT-4o + Claude Sonnet 4** dual-model architecture for natural language to SQL system, integrating M-Schema table structure understanding, intelligent table selection, and simplified RAG retrieval, supporting complex reasoning and multi-database tasks.

---

## 📌 Project Overview

This project implements a high-performance natural language to SQL system (NL2SQL) based on **LangChain + OpenAI GPT-4o + Anthropic Claude Sonnet 4**, using a dual-model architecture and simplified RAG (Retrieval-Augmented Generation) technology to automatically convert user input natural language questions into SQLite executable SQL queries.

The database and training data can be downloaded from the Archer official website: `https://sig4kg.github.io/archer-bench/`.

### 🚀 Key Features

1. ✅ **Dual-Model Architecture**: GPT-4o + Claude Sonnet 4 collaborate to generate and automatically select the optimal SQL
2. ✅ **M-Schema Integration**: Deep understanding of database table structures, field relationships, and constraints
3. ✅ **Intelligent Table Selection**: Strict table name validation and semantic relevance filtering based on Pydantic
4. ✅ **Simplified RAG Retrieval**: Few-shot example retrieval based purely on semantic similarity, avoiding complex weight calculations
5. ✅ **Reasoning Type Recognition**: Supports addition, subtraction, multiplication, division, hypothetical conditions, and commonsense reasoning
6. ✅ **SQL Validation and Repair**: Automatic syntax checking and error repair mechanism
7. ✅ **Multi-Database Compatibility**: Supports 10+ typical database scenarios

---

## ⚙️ Technical Architecture

### 1. Dual-Model Collaborative Architecture

```python
# GPT-4o handles table selection and SQL generation
llm_openai = ChatOpenAI(model='gpt-4o', temperature=0.3)

# Claude Sonnet 4 handles SQL generation and optimization
llm_anthropic = ChatAnthropic(model_name="cc-sonnet-4-20250514-thinking", temperature=0.3)
```

### 2. M-Schema Table Structure Understanding

- link：git clone https://github.com/XGenerationLab/M-Schema
- Integrated M-Schema engine for deep parsing of database table structures
- Automatically extracts table relationships, field types, and constraints
- Supports table associations and field mapping for complex queries

### 3. Intelligent Table Selection Mechanism

```python
class TableList(BaseModel):
    tables: List[str] = Field(description="List of relevant table names")
```

- Uses Pydantic models to strictly control table name output format
- Combines table descriptions and M-Schema for semantic relevance judgment
- Automatically filters irrelevant tables to improve query efficiency

### 4. Simplified RAG Retrieval System

- **Vector Database**: Chroma + OpenAI Embeddings
- **Retrieval Strategy**: Pure semantic similarity matching, returning the most relevant examples
- **Example Format**: Includes reasoning types, commonsense knowledge, and SQL templates
- **Simplified Design**: Removes complex table matching weight calculations, focusing on semantic similarity

### 5. SQL Generation and Optimization

- **Reasoning Type Recognition**: `+` (addition), `-` (subtraction), `*` (multiplication), `/` (division), `H` (hypothetical), `C` (commonsense)
- **Dual-Model Generation**: GPT-4o and Claude generate SQL separately
- **Intelligent Selection**: Automatically selects the optimal SQL based on correctness, syntax compatibility, and efficiency
- **Validation and Repair**: EXPLAIN QUERY PLAN validation + automatic error repair
- **Simplified Process**: Focuses on semantic similarity retrieval, avoiding complex dynamic weight calculations

---

## 🧩 Project Structure

```text
livesqlbench-main/
├── nl2sql.py                     # Main program (dual-model architecture)
├── evaluation.py                 # Batch evaluation script
├── examples/                     # Few-shot examples (organized by database)
│   ├── bike_1_examples.py
│   ├── concert_singer_examples.py
│   └── ...
├── database/                     # Multi-database SQLite files
│   ├── bike_1/
│   ├── concert_singer/
│   └── ...
├── M-Schema/                     # M-Schema table structure engine
│   ├── schema_engine.py
│   ├── m_schema.py
│   └── ...
├── {db_id}_table_description.csv # Table structure description file
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 🧪 Usage Instructions

### 1. Environment Setup

```bash
# Create virtual environment
cd ./livesqlbench/livesqlbench-main
conda create -n livesqlbench python=3.10 -y
conda activate livesqlbench

# Install dependencies
cd ./livesqlbench/livesqlbench-main/config
pip install -r requirements.txt
```

### 2. API Configuration

The system uses the following API endpoints:

- **OpenAI GPT-4o**: `https://api.gpt.ge/v1`
- **Anthropic Claude**: `https://api.gpt.ge`
- **OpenAI Embeddings**: `https://api.gpt.ge/v1`

Please remember to switch to your own base URL
```python
# API Key Configuration Example
api_key = "your api key"
```

### 3. M-Schema Configuration

M-Schema is the core table structure understanding engine of the system and needs to be correctly configured to work properly.

#### 3.1 M-Schema Directory Structure

```text
M-Schema/
├── __init__.py              # Package initialization file
├── schema_engine.py         # Main engine file
├── m_schema.py              # M-Schema core class
├── utils.py                 # Utility functions
├── requirements.txt         # M-Schema-specific dependencies
├── README.md                # M-Schema documentation
└── example.py               # Usage example
```

#### 3.2 M-Schema Dependency Installation, refer to: https://github.com/XGenerationLab/M-Schema

M-Schema requires additional dependencies, ensure installation:

```bash
# Install M-Schema-specific dependencies after activating conda
cd ./livesqlbench/livesqlbench-main
git clone https://github.com/XGenerationLab/M-Schema.git
cd M-Schema
pip install -r requirements.txt
```

#### 3.3 M-Schema Working Principle

The M-Schema engine parses database structures through the following steps:

1. **Database Connection**: Connects to SQLite databases using SQLAlchemy
2. **Metadata Extraction**: Automatically extracts table structures, field types, and constraints
3. **Relationship Analysis**: Analyzes primary key and foreign key relationships between tables
4. **Schema Generation**: Generates structured M-Schema descriptions

#### 3.4 M-Schema Configuration Example

```python
from sqlalchemy import create_engine
from M-Schema.schema_engine import SchemaEngine

# Create database engine
db_path = "database/wine_1/wine_1.sqlite"
abs_path = os.path.abspath(db_path)
db_engine = create_engine(f"sqlite:///{abs_path}")

# Initialize M-Schema engine
schema_engine = SchemaEngine(engine=db_engine, db_name="wine_1")

# Get M-Schema description
mschema = schema_engine.mschema
mschema_str = mschema.to_mschema()
print(mschema_str)
```

#### 3.5 M-Schema Output Format

M-Schema generates descriptions containing:

- **Table Structure**: Table names, field names, data types, constraints
- **Relationship Information**: Primary keys, foreign keys, indexes
- **Semantic Description**: Business meaning and usage of fields
- **Query Suggestions**: Common query patterns and examples

#### 3.6 Troubleshooting

If encountering M-Schema-related errors:

1. **Dependency Issues**: Ensure all M-Schema dependencies are installed
2. **Path Issues**: Check if the database file path is correct
3. **Permission Issues**: Ensure read permissions for the database file
4. **Version Compatibility**: Ensure SQLAlchemy version compatibility (>=1.4.0)

### 4. Usage Modes

#### Interactive CLI Mode

```bash
cd livesqlbench-main/scripts
python nl2sql.py --db_id soccer_1 --question specific question

Example:
python nl2sql.py --db_id soccer_1 --question "Passing scores include 5% curve balls, 5% free kick accuracy, 15% long passes, 20% crosses, 20% vision, and 35% short passes. List the names and current ages of the top 10 players with the highest passing scores."
```

#### Programmatic Call: Call the `generate_sql_only` function, similarly requiring input of database ID and natural language question.

```python
from nl2sql import generate_sql_only

# Single query
sql = generate_sql_only(
    db_id="wine_1",
    question="How many types of wine are produced in Sonoma County, and how many more than those produced in Napa County?"
)
print(sql)

# Batch processing
questions = [
    ("concert_singer", "List the names of all singers"),
    ("bike_1", "Count the number of docking points at each station"),
    ("wine_1", "How many types of wine are produced in Sonoma County, and how many more than those produced in Napa County?")
]

for db_id, question in questions:
    sql = generate_sql_only(db_id, question)
    print(f"Database: {db_id}")
    print(f"Question: {question}")
    print(f"SQL: {sql}\n")
```

### 5. Supported Databases

The system supports the following 10 databases:

- `bike_1` - Bicycle rental system
- `concert_singer` - Concert singer management
- `customers_and_products_contacts` - Customer product contacts
- `driving_school` - Driving school management
- `formula_1` - F1 racing data
- `hospital_1` - Hospital management system
- `riding_club` - Riding club
- `soccer_1` - Soccer data
- `wine_1` - Wine database
- `world_1` - World geography data

---

## 📊 Evaluation and Testing

### 1. Batch Evaluation

The system provides comprehensive evaluation tools to test NL2SQL performance:

```bash
cd livesqlbench-main/scripts

# Run evaluation (requires test file)
python evaluation.py test_data.json

# Create sample test file
python evaluation.py --create-sample

# View usage help
python evaluation.py
```

### 2. Test Data Format

Test files should be in JSON format, each sample containing the following fields:

```json
[
  {
    "db_id": "soccer_1",
    "question": "List the names of all players",
    "gold_sql": "SELECT player_name FROM Player"
  },
  {
    "db_id": "wine_1",
    "question": "How many types of wine are produced in Sonoma County, and how many more than those produced in Napa County?",
    "gold_sql": "SELECT sonoma, sonoma - napa AS diff FROM (SELECT COUNT(*) AS sonoma FROM wine A JOIN appellations B ON A.Appelation = B.Appelation WHERE B.County = 'Sonoma') JOIN (SELECT COUNT(*) AS napa FROM wine A JOIN appellations B ON A.Appelation = B.Appelation WHERE B.County = 'Napa')"
  }
]
```

**Field Description**:
- `db_id`: Database identifier (must be one of the 10 supported databases)
- `question`: Natural language question
- `gold_sql` or `query`: Standard SQL query (used for result comparison)

### 3. Evaluation Metrics

The evaluation system outputs the following metrics:

- **Total Samples**: Total number of samples in the test set
- **SQL Generation Success Count**: Number of samples successfully generating SQL
- **SQL Execution Success Count**: Number of generated SQLs successfully executed
- **Result Match Count**: Number of samples where execution results match the standard answer
- **SQL Execution Result Match Accuracy**: Result match count / total sample count
- **SQL Generation Failure Count**: Number of samples failing to generate SQL
- **SQL Execution Failure Count**: Number of generated SQLs failing to execute

### 4. Reasoning Type Examples

The system supports various reasoning types:

- **Arithmetic Reasoning**: `+` addition, `-` subtraction, `*` multiplication, `/` division
- **Logical Reasoning**: `H` hypothetical condition reasoning, `C` commonsense reasoning
- **Complex Queries**: Multi-table JOIN, subqueries, aggregate functions

---

## 💰 Cost Estimation

### Single Inference Cost

- **Table Selection**: GPT-4o + Pydantic parsing ≈ $0.01
- **RAG Retrieval**: Embedding vector lookup ≈ $0.005
- **SQL Generation**: Dual-model generation + selection ≈ $0.03
- **Validation and Repair**: SQL validation ≈ $0.005

**Total**: Approximately $0.05 per inference

### Batch Evaluation Cost

- Estimated sample size: 500
- Total cost estimate: Approximately $25-$35

---

## 🔧 Technical Details

### 1. Table Selection Process

```python
def select_tables_via_parser(llm, question: str, db_id: str, db: SQLDatabase) -> List[str]:
    # 1. Retrieve table descriptions and M-Schema
    # 2. Use Pydantic parser to strictly control output
    # 3. Validate table name validity
    # 4. Return relevant table list
```

### 2. SQL Generation Process

```python
def generate_sql_only(db_id: str, question: str) -> str:
    # 1. Intelligent table selection
    # 2. Simplified RAG example retrieval (pure semantic similarity)
    # 3. M-Schema extraction
    # 4. Dual-model SQL generation
    # 5. Intelligent selection of optimal SQL
    # 6. Validation and repair
```

### 3. Error Handling Mechanism

- **Syntax Validation**: Validates SQL syntax using `EXPLAIN QUERY PLAN`
- **Automatic Repair**: Automatically calls repair model upon detecting errors
- **Fallback Mechanism**: Returns cleaned original SQL if repair fails

---

## 🙌 Acknowledgments and Notes

- This project is developed based on the **Archer Benchmark** official dataset
- Integrated **M-Schema** table structure understanding engine
- Built using the **LangChain** framework for AI applications
- Supports **OpenAI GPT-4o** and **Anthropic Claude Sonnet 4** dual-model architecture

### Disclaimer

- This project is for academic research and Benchmark submission only
- All model calls are based on public APIs, and call costs must be borne by the user
- Example databases and structures are from the Archer Benchmark official dataset

