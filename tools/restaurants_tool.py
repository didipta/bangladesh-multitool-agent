from pathlib import Path

from langchain_core.language_models.chat_models import BaseChatModel

from tools.sql_tool_base import (
    make_db_tool,
    inspect_schema as _inspect_schema,
)


DB_PATH = (
    Path(__file__).parent.parent
    / "databases"
    / "restaurants.db"
)

TABLE_NAME = "restaurants"


DESCRIPTION = """
Use this tool for questions about restaurants in Bangladesh.

The database contains restaurant information such as
restaurant names, locations, cuisine, ratings and other
fields available in the restaurants database.

Use this tool for:

- restaurant searches
- restaurant counts
- restaurants by city
- restaurants by district
- restaurants by location
- cuisine searches
- restaurant ratings
- highly rated restaurants

Examples:

"Find restaurants in Dhaka."

"Show restaurants in Dhanmondi."

"Which restaurants have ratings above 4?"

"Find Bengali restaurants."

"How many restaurants are in Dhaka?"

Do NOT use this tool for:

- hospitals
- institutions
- healthcare policy
- general knowledge
"""


def get_restaurants_tool(
    llm: BaseChatModel,
):
    return make_db_tool(
        llm=llm,
        db_path=DB_PATH,
        table_name=TABLE_NAME,
        tool_name="RestaurantsDBTool",
        description=DESCRIPTION,
    )


def inspect_schema():
    _inspect_schema(
        DB_PATH,
        TABLE_NAME,
    )


if __name__ == "__main__":
    inspect_schema()