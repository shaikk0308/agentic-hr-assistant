from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import StdioServerParameters

from agents.utils import get_project_root

PROJECT_ROOT = get_project_root()
RAG_SERVER_SCRIPT = str(PROJECT_ROOT / "mcp_servers" / "mcp_policies_rag" / "server.py")

policies_rag_tools = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python",
            args=[RAG_SERVER_SCRIPT],
        )
    ),
)

root_agent = Agent(
    name="policy_agent",
    model="gemini-2.5-flash",
    instruction=(
        "You are the Policy agent.\n"
        "- You ONLY answer questions about company policies (leave policy, WFH policy, etc.).\n"
        "- Use the MCP tools to:\n"
        "  * list available policy PDFs (list_policy_pdfs),\n"
        "  * build or refresh the index (build_policy_index),\n"
        "  * search relevant policy text for a question (rag_search_policies).\n"
        "- For each user question:\n"
        "  1) Ensure the index is built at least once per session (call build_policy_index if needed).\n"
        "  2) Call rag_search_policies with the user's natural-language question.\n"
        "  3) Answer ONLY based on the returned policy text; do not invent rules.\n"
    ),
    tools=[policies_rag_tools],
)