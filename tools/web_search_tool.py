import os

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from langchain_tavily import TavilySearch


class WebSearchInput(BaseModel):
    question: str = Field(
        description=(
            "A general knowledge or current-information "
            "question that requires web search."
        )
    )


DESCRIPTION = """
Use this tool for general knowledge and current information
that cannot be answered reliably from the Bangladesh
institution, hospital or restaurant databases.

Examples:

"What is the role of DGHS in Bangladesh?"

"What is healthcare policy in Bangladesh?"

"What is the history of Bengali cuisine?"

"What is the Bangladesh education policy?"

Use database tools instead when the question asks for
specific records or statistics from the provided datasets.
"""


def get_web_search_tool():

    if not os.getenv("TAVILY_API_KEY"):
        raise ValueError(
            "TAVILY_API_KEY is not configured."
        )

    search = TavilySearch(
        max_results=5,
    )

    def run(question: str) -> str:

        try:
            result = search.invoke(
                {
                    "query": question
                }
            )

            return str(result)

        except Exception as error:
            return (
                f"Web search failed: {error}"
            )

    return StructuredTool.from_function(
        func=run,
        name="WebSearchTool",
        description=DESCRIPTION,
        args_schema=WebSearchInput,
    )