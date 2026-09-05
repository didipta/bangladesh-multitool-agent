from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field


class DatabaseQueryInput(BaseModel):
    question: str = Field(
        description=(
            "A natural-language question that should be answered "
            "using the database."
        )
    )


def get_connection(db_path: Path) -> sqlite3.Connection:
    if not db_path.exists():
        raise FileNotFoundError(
            f"Database not found: {db_path}"
        )

    connection = sqlite3.connect(str(db_path))
    connection.row_factory = sqlite3.Row

    return connection


def inspect_schema(
    db_path: Path,
    table_name: str,
) -> None:

    print("\n" + "=" * 60)
    print(f"Database: {db_path}")
    print(f"Table: {table_name}")
    print("=" * 60)

    connection = get_connection(db_path)

    try:
        columns = connection.execute(
            f'PRAGMA table_info("{table_name}")'
        ).fetchall()

        if not columns:
            print("Table does not exist.")
            return

        for column in columns:
            print(
                f"{column['name']} "
                f"| type={column['type']} "
                f"| nullable={not column['notnull']} "
                f"| primary_key={bool(column['pk'])}"
            )

    finally:
        connection.close()


def get_schema(
    db_path: Path,
    table_name: str,
) -> str:

    connection = get_connection(db_path)

    try:
        columns = connection.execute(
            f'PRAGMA table_info("{table_name}")'
        ).fetchall()

        if not columns:
            raise ValueError(
                f"Table '{table_name}' does not exist."
            )

        schema_lines = []

        for column in columns:
            schema_lines.append(
                f"- {column['name']} ({column['type']})"
            )

        return "\n".join(schema_lines)

    finally:
        connection.close()


def validate_sql(sql: str) -> str:
    """
    Allow only read-only SQL.

    The AI agent should only be able to query the database.
    """

    sql = sql.strip()

    if sql.endswith(";"):
        sql = sql[:-1]

    normalized = sql.lower().strip()

    if not normalized.startswith(
        ("select", "with")
    ):
        raise ValueError(
            "Only SELECT/WITH queries are allowed."
        )

    forbidden = [
        "insert ",
        "update ",
        "delete ",
        "drop ",
        "alter ",
        "create ",
        "replace ",
        "attach ",
        "detach ",
        "pragma ",
    ]

    for keyword in forbidden:
        if keyword in normalized:
            raise ValueError(
                f"Forbidden SQL operation detected: {keyword.strip()}"
            )

    return sql


def execute_sql(
    db_path: Path,
    sql: str,
) -> list[dict[str, Any]]:

    sql = validate_sql(sql)

    connection = get_connection(db_path)

    try:
        cursor = connection.execute(sql)

        rows = cursor.fetchall()

        return [
            dict(row)
            for row in rows
        ]

    finally:
        connection.close()


def format_results(
    rows: list[dict[str, Any]],
) -> str:

    if not rows:
        return "No matching records were found."

    return json.dumps(
        rows,
        ensure_ascii=False,
        indent=2,
        default=str,
    )


def make_db_tool(
    llm: BaseChatModel,
    db_path: Path,
    table_name: str,
    tool_name: str,
    description: str,
):
    """
    Create a LangChain database tool.

    The LLM converts the user's natural-language question
    into a read-only SQL query.
    """

    schema = get_schema(
        db_path,
        table_name,
    )

    system_prompt = f"""
You are a SQL expert working with a Bangladesh dataset.

Database table:
{table_name}

Available columns:
{schema}

Your job is to convert the user's question into ONE
safe SQLite SQL query.

Rules:

1. Generate ONLY SELECT or WITH queries.
2. Never INSERT, UPDATE, DELETE, DROP, ALTER, CREATE,
   REPLACE, ATTACH or DETACH.
3. Use only columns that actually exist in the schema.
4. Do not invent columns.
5. Use case-insensitive matching when appropriate.
6. For counting records use COUNT(*).
7. When the user asks for a list, use a reasonable LIMIT.
8. Prefer LIMIT 50 for normal listing queries.
9. Return ONLY SQL.
"""

    def run(question: str) -> str:

        try:
            response = llm.invoke(
                [
                    (
                        "system",
                        system_prompt,
                    ),
                    (
                        "human",
                        question,
                    ),
                ]
            )

            sql = response.content

            if isinstance(sql, list):
                sql = "".join(
                    item.get("text", "")
                    if isinstance(item, dict)
                    else str(item)
                    for item in sql
                )

            sql = str(sql).strip()

            # Remove markdown SQL fences if model adds them
            sql = sql.replace("```sql", "")
            sql = sql.replace("```", "")
            sql = sql.strip()

            print(
                f"\n[{tool_name}] Generated SQL:\n{sql}"
            )

            rows = execute_sql(
                db_path,
                sql,
            )

            return format_results(rows)

        except Exception as error:
            return (
                f"Database query failed: {error}"
            )

    return StructuredTool.from_function(
        func=run,
        name=tool_name,
        description=description,
        args_schema=DatabaseQueryInput,
    )