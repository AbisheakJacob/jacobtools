# Graph Report - .  (2026-06-22)

## Corpus Check
- Corpus is ~15,633 words - fits in a single context window. You may not need a graph.

## Summary
- 334 nodes · 435 edges · 26 communities (19 shown, 7 thin omitted)
- Extraction: 80% EXTRACTED · 20% INFERRED · 0% AMBIGUOUS · INFERRED: 87 edges (avg confidence: 0.66)
- Token cost: 0 input · 98,497 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Graphify Skill & Exports|Graphify Skill & Exports]]
- [[_COMMUNITY_BigQuery Manager Layer|BigQuery Manager Layer]]
- [[_COMMUNITY_Data IO ReadWrite|Data IO Read/Write]]
- [[_COMMUNITY_Connector Facade & Base Contract|Connector Facade & Base Contract]]
- [[_COMMUNITY_AnalystStack Docs & Roadmap|AnalystStack Docs & Roadmap]]
- [[_COMMUNITY_Settings & Error Handling|Settings & Error Handling]]
- [[_COMMUNITY_Format CLI|Format CLI]]
- [[_COMMUNITY_Code Formatters (PythonSQL)|Code Formatters (Python/SQL)]]
- [[_COMMUNITY_Client Wrappers (Auth)|Client Wrappers (Auth)]]
- [[_COMMUNITY_BigQuery Connector Tests|BigQuery Connector Tests]]
- [[_COMMUNITY_DataReader Tests|DataReader Tests]]
- [[_COMMUNITY_DataWriter Tests|DataWriter Tests]]
- [[_COMMUNITY_Python Formatter Tests|Python Formatter Tests]]
- [[_COMMUNITY_Excel Cell Parsing|Excel Cell Parsing]]
- [[_COMMUNITY_Metadata Extraction|Metadata Extraction]]
- [[_COMMUNITY_Test Fixtures|Test Fixtures]]
- [[_COMMUNITY_BigQuery Table ID Utils|BigQuery Table ID Utils]]
- [[_COMMUNITY_Logging|Logging]]
- [[_COMMUNITY_Package Init|Package Init]]
- [[_COMMUNITY_Docs Build Workflow|Docs Build Workflow]]
- [[_COMMUNITY_Graphify Knowledge Graph|Graphify Knowledge Graph]]
- [[_COMMUNITY_Token Reduction Benchmark|Token Reduction Benchmark]]
- [[_COMMUNITY_GraphML Export|GraphML Export]]
- [[_COMMUNITY_SVG Export|SVG Export]]
- [[_COMMUNITY_Audit Trail|Audit Trail]]

## God Nodes (most connected - your core abstractions)
1. `Graphify Skill` - 20 edges
2. `GoogleBigQueryConnector` - 19 edges
3. `QueryManager` - 16 edges
4. `QueryExecutionError` - 13 edges
5. `DataWriter` - 12 edges
6. `MetadataManager` - 11 edges
7. `BaseConnector` - 10 edges
8. `BigQueryClientWrapper` - 10 edges
9. `DataReader` - 10 edges
10. `handle_format()` - 9 edges

## Surprising Connections (you probably didn't know these)
- `DataReader` --uses--> `DataReader`  [INFERRED]
  test/io/test_io_reader.py → src/AnalystStack/io/reader.py
- `DataWriter` --uses--> `DataWriter`  [INFERRED]
  test/io/test_io_writer.py → src/AnalystStack/io/writer.py
- `AnalystStack (docs home)` --semantically_similar_to--> `AnalystStack Toolkit`  [INFERRED] [semantically similar]
  docs/docs/index.md → README.md
- `IO Module` --semantically_similar_to--> `io facade`  [INFERRED] [semantically similar]
  README.md → docs/docs/io.md
- `GoogleBigQueryConnector` --semantically_similar_to--> `GoogleBigQueryConnector (docs)`  [INFERRED] [semantically similar]
  README.md → docs/docs/connectors.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Connector Error Hierarchy** — connectors_datapackageerror, connectors_configurationerror, connectors_connectionerror, connectors_queryexecutionerror, connectors_validationerror [EXTRACTED 0.95]
- **AnalystStack Core Modules** — readme_connectors, readme_io, readme_formatting [EXTRACTED 0.85]
- **CI Quality Gates** — workflows_ci, workflows_tox, workflows_pypipublish [EXTRACTED 0.85]
- **Graphify Build Pipeline (detect → extract → cluster → output)** — skill_graphify_detect, skill_graphify_ast_extraction, skill_graphify_semantic_extraction, skill_graphify_clustering, skill_graphify_graph_json [EXTRACTED 1.00]
- **Graphify Graph Outputs** — skill_graphify_html_viz, skill_graphify_graph_report, skill_graphify_graph_json, skill_graphify_obsidian_vault [EXTRACTED 1.00]
- **Graphify Query/Path/Explain Interface** — references_query_bfs, references_query_dfs, references_query_path, references_query_explain, references_query_query_expansion [EXTRACTED 1.00]

## Communities (26 total, 7 thin omitted)

### Community 0 - "Graphify Skill & Exports"
Cohesion: 0.06
Nodes (51): Graphify Skill Trigger, Graphify Add URL, Watch Debounce, URL Ingest Pipeline, Folder Watcher (--watch), FalkorDB Export, MCP Stdio Server, Neo4j Export (+43 more)

### Community 1 - "BigQuery Manager Layer"
Cohesion: 0.08
Nodes (21): MetadataManager, Dedicated to schema extraction. Notice how we 'inject' the QueryManager so we do, Handles schema and structural metadata extraction from INFORMATION_SCHEMA., ProfilerManager, Dedicated to heavy analyticial queries like calculating fill rates, Generates data quality statistics and profiles., QueryManager, Dedicated to executing SQL and moving data (+13 more)

### Community 2 - "Data IO Read/Write"
Cohesion: 0.09
Nodes (19): DataIOManager, Facade for all IO operations., DataReader, Handles comprehensive data ingestion into DataFrames., Reads a specific range of an Excel sheet into a DataFrame., Reads a CSV file with advanced parsing options., Reads Parquet files natively., Render a Jinja2 template and return the resulting string.          ``source`` ca (+11 more)

### Community 3 - "Connector Facade & Base Contract"
Cohesion: 0.09
Nodes (17): ABC, GoogleBigQueryConnector, The Facade (The Final Connecter)  This is what your end-users will interact with, Expert-level facade combining client, query, metadata, and profiling logic., Returns BigQuery specific data types for a table., Calculates column-level completion percentage., BaseConnector, The Abstract Base  This enforces a strict contract. Any future connector (Snowfl (+9 more)

### Community 4 - "AnalystStack Docs & Roadmap"
Cohesion: 0.08
Nodes (30): BaseConnector Contract, ConfigurationError, ConnectionError, Databricks Connector, DataPackageError, GoogleBigQueryConnector (docs), QueryExecutionError, ValidationError (+22 more)

### Community 5 - "Settings & Error Handling"
Cohesion: 0.13
Nodes (14): BigQuerySettings, DatabricksSettings, Uses standard dataclasses to pull from environment variables, avoiding hardcoded, Manages default settings for the BigQuery environment., Manages default settings for the Databricks environment., DatabricksConnector, The Facade (The Final Connecter)  This is what your end-users will interact with, Expert-level facade combining client, query, metadata, and profiling logic (+6 more)

### Community 6 - "Format CLI"
Cohesion: 0.18
Nodes (15): _format_python(), _format_sql(), handle_format(), main(), Lint or format a SQL file (SQLFluff operates directly on the file)., Handles the 'analyststack format' command., The main entry point for the CLI., Lint or format a Python file (operates on the file's contents as a string). (+7 more)

### Community 7 - "Code Formatters (Python/SQL)"
Cohesion: 0.13
Nodes (8): PythonFormatter, Handles Python linting and formatting using Black and AST., Checks for fundamental Python syntax errors without executing the code., Formats Python code using Black's uncompromising standards., Handles SQL linting and formatting using SQLFluff., config_path: Path to a .sqlfluff file containing your preset requirements., SQLFormatter, Any

### Community 8 - "Client Wrappers (Auth)"
Cohesion: 0.18
Nodes (9): BigQueryClientWrapper, The Bigquery Engine (Composition Module)  Isolates authentication and API connec, Wraps the native Google BigQuery client securely., Client, connnect, DatabricksClientWrapper, Wraps the Databricks client securely, ConnectionError (+1 more)

### Community 9 - "BigQuery Connector Tests"
Cohesion: 0.13
Nodes (9): connector(), mock_bq_client(), Tests for AnalystStack.connectors.GoogleBigQueryConnector.  The native ``google., Patches the native BigQuery client used inside the client wrapper., A pre-initialised connector wired to the mocked client., A missing project id (arg and env) raises ConfigurationError., test_initialization_missing_project_id(), test_read_data_failure() (+1 more)

### Community 10 - "DataReader Tests"
Cohesion: 0.17
Nodes (3): DataReader, Tests for AnalystStack.io.reader.DataReader (jinja + csv)., reader()

### Community 11 - "DataWriter Tests"
Cohesion: 0.20
Nodes (3): DataWriter, Tests for AnalystStack.io.writer.DataWriter (csv, markdown, txt)., writer()

### Community 12 - "Python Formatter Tests"
Cohesion: 0.22
Nodes (3): formatter(), Tests for AnalystStack.format.python.PythonFormatter., PythonFormatter

### Community 13 - "Excel Cell Parsing"
Cohesion: 0.32
Nodes (6): Tests for AnalystStack.io.utils.parse_excel_cell., test_parse_excel_cell_invalid_raises(), test_parse_excel_cell_is_case_insensitive(), test_parse_excel_cell_valid(), parse_excel_cell(), Parses an Excel cell reference (e.g., 'C4') into 0-indexed row/col integers

### Community 14 - "Metadata Extraction"
Cohesion: 0.29
Nodes (4): MetadataManager, Dedicated to schema extration. We are injecting the QueryManager to not repeat, Handles schema and structural metadata extraction, QueryManager

### Community 15 - "Test Fixtures"
Cohesion: 0.40
Nodes (4): DataFrame, Shared pytest fixtures for the AnalystStack test suite., A small, well-formed DataFrame reused across IO and connector tests., sample_dataframe()

### Community 16 - "BigQuery Table ID Utils"
Cohesion: 0.50
Nodes (3): construct_full_table_id(), Any BQ specific text parsing or helper functions, Safely constructs a standard BigQuery standard SQL table reference.

### Community 17 - "Logging"
Cohesion: 0.50
Nodes (3): Logger, get_logger(), Creates and returns a configured logger.

## Knowledge Gaps
- **39 isolated node(s):** `Namespace`, `Any`, `Any`, `Logger`, `DataFrame` (+34 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GoogleBigQueryConnector` connect `Connector Facade & Base Contract` to `Client Wrappers (Auth)`, `BigQuery Manager Layer`, `Settings & Error Handling`, `BigQuery Connector Tests`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Why does `QueryManager` connect `BigQuery Manager Layer` to `Client Wrappers (Auth)`, `Connector Facade & Base Contract`, `Metadata Extraction`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Why does `BaseConnector` connect `Connector Facade & Base Contract` to `Settings & Error Handling`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `GoogleBigQueryConnector` (e.g. with `BigQueryClientWrapper` and `MetadataManager`) actually correct?**
  _`GoogleBigQueryConnector` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `QueryManager` (e.g. with `GoogleBigQueryConnector` and `MetadataManager`) actually correct?**
  _`QueryManager` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `QueryExecutionError` (e.g. with `QueryManager` and `.execute_read()`) actually correct?**
  _`QueryExecutionError` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `DataWriter` (e.g. with `DataWriter` and `DataIOManager`) actually correct?**
  _`DataWriter` has 2 INFERRED edges - model-reasoned connections that need verification._