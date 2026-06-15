from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import StdioServerParameters

from agents.utils import get_project_root

PROJECT_ROOT = get_project_root()
LEAVE_SERVER_SCRIPT = str(PROJECT_ROOT / "mcp_servers" / "mcp_leave" / "server.py")

leave_tools = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python",
            args=[LEAVE_SERVER_SCRIPT],
        )
    ),
)

root_agent = Agent(
    name="leave_agent",
    model="gemini-2.5-flash",
    instruction=(
        "You are the Leave Management agent. Use the provided MCP tools to manage employee leaves.\n"
        "- To see remaining days: use 'get_leave_balance'.\n"
        "- To see a list of all existing requests: use 'list_my_leaves'.\n"
        "- To create a new leave: use 'book_leave'.\n"
        "- To remove a leave and refund balance: use 'cancel_leave'.\n"
        "Always provide clear details (IDs, dates, reasons) back to the user. "

        "Use the employee code provided by the Orchestrator. If none is provided, ask the Orchestrator for the 'logged_in_user' context."
        "PRESENTATION RULES:\n"
        "- When listing leaves (list_my_leaves), ALWAYS use a **Markdown Table**.\n"
        "- The table columns should be: | ID | Type | Start Date | End Date | Days | Reason |\n"
        "- Use emojis to make the response friendly (e.g., 🏖️ for leave, ✅ for balance).\n"
        "- Bold the total balance when providing it.\n\n"
        "TOOLS GUIDE:\n"
        "- To see remaining days: use 'get_leave_balance'.\n"
        "- To see a list of all existing requests: use 'list_my_leaves'.\n"
        "- To create a new leave: use 'book_leave'.\n"
        "- To remove a leave: use 'cancel_leave'."
    ),
    tools=[leave_tools],
)