from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import StdioServerParameters

from agents.utils import get_project_root

PROJECT_ROOT = get_project_root()
COMP_SERVER_SCRIPT = str(PROJECT_ROOT / "mcp_servers" / "mcp_compensation" / "server.py")

comp_tools = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python",
            args=[COMP_SERVER_SCRIPT],
        )
    ),
)

root_agent = Agent(
    name="comp_agent",
    model="gemini-2.5-flash",
    instruction=(
        "You are the Compensation agent.\n"
        "- You ONLY handle questions about salary, CTC, bonuses, and compensation.\n"
        "- Use MCP tools to fetch current compensation details from the database.\n"
        "- Do NOT answer leave, policy, or employee profile questions; those are for other agents.\n"
        "PRESENTATION RULES:\n"
        "Use the employee code provided by the Orchestrator. If none is provided, ask the Orchestrator for the 'logged_in_user' context. and refer the user by name , do not use greetings"
        "- Use a header: '### 💰 Compensation Details'.\n"
        "- Present the salary and bonus in a small **Markdown Table** or a clear bold list.\n"
        "- Use currency formatting (e.g., ₹1,200,000 or $50,000).\n"
        "- Highlight the 'Effective From' date."
    ),
    tools=[comp_tools],
)