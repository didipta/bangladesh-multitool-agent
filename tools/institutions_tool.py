from pathlib import Path

from langchain_core.language_models.chat_models import BaseChatModel

from tools.sql_tool_base import (
    make_db_tool,
    inspect_schema as _inspect_schema,
)


DB_PATH = (
    Path(__file__).parent.parent
    / "databases"
    / "institutions.db"
)

TABLE_NAME = "institutions"


DESCRIPTION = """
Use this tool for questions about institutions in Bangladesh.

This includes educational and institutional information
such as universities, colleges, schools, government
institutions and other institutions contained in the
institutions database.

Use this tool for:

- institution searches
- institution counts
- universities
- colleges
- institution types
- institutions by division
- institutions by district
- institutions by upazila
- government/private management information

Examples:

"How many institutions are in Dhaka?"

"Find universities in Dhaka."

"List institutions in Chattogram."

"How many institutions are in Rajshahi?"

"Find government institutions in Bangladesh."

Do NOT use this tool for:

- hospitals
- restaurants
- healthcare policy
- general knowledge
"""


def get_institutions_tool(
    llm: BaseChatModel,
):
    return make_db_tool(
        llm=llm,
        db_path=DB_PATH,
        table_name=TABLE_NAME,
        tool_name="InstitutionsDBTool",
        description=DESCRIPTION,
    )


def inspect_schema():
    _inspect_schema(
        DB_PATH,
        TABLE_NAME,
    )


if __name__ == "__main__":
    inspect_schema()