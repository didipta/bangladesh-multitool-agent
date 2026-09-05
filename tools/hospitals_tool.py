from pathlib import Path

from langchain_core.language_models.chat_models import BaseChatModel

from tools.sql_tool_base import (
    make_db_tool,
    inspect_schema as _inspect_schema,
)


DB_PATH = (
    Path(__file__).parent.parent
    / "databases"
    / "hospitals.db"
)

TABLE_NAME = "hospitals"


DESCRIPTION = """
Use this tool for questions about hospitals in Bangladesh.

The hospital database contains:

- hospital ID
- hospital name
- Bangla hospital name
- hospital code
- agency
- hospital type
- division
- district
- city corporation
- upazila
- paurasava
- union
- private/public classification

Use this tool for:

- hospital searches
- hospital counts
- hospitals by district
- hospitals by division
- hospitals by upazila
- private hospitals
- public/government hospitals
- hospital type comparisons

Examples:

"How many hospitals are in Dhaka?"

"List hospitals in Chattogram."

"How many hospitals are in Rajshahi Division?"

"Find private hospitals in Dhaka."

"Show hospitals in Uttara."

Do NOT use this tool for:

- universities
- colleges
- institutions
- restaurants
- medical advice
- healthcare policy
- general medical knowledge
"""


def get_hospitals_tool(
    llm: BaseChatModel,
):
    return make_db_tool(
        llm=llm,
        db_path=DB_PATH,
        table_name=TABLE_NAME,
        tool_name="HospitalsDBTool",
        description=DESCRIPTION,
    )


def inspect_schema():
    _inspect_schema(
        DB_PATH,
        TABLE_NAME,
    )


if __name__ == "__main__":
    inspect_schema()