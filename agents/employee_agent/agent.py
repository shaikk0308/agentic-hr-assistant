from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import StdioServerParameters

from agents.utils import get_project_root

PROJECT_ROOT = get_project_root()
EMPLOYEES_SERVER_SCRIPT = str(PROJECT_ROOT / "mcp_servers" / "mcp_employees" / "server.py")

employees_tools = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python",
            args=[EMPLOYEES_SERVER_SCRIPT],
        )
    ),
)

root_agent = Agent(
    name="employee_agent",
    model="gemini-2.5-flash",
    instruction=(
        "You are the Employee Profile agent.\n"
        "- You answer questions about employee personal details: name, email, phone, "
        "  department, designation, manager, date of joining.\n"
        "- Use MCP tools to fetch employee data from the database.\n"
        "- Do NOT handle leave, compensation, or policy questions; those are for other agents.\n"

        "PRESENTATION RULES:\n"
        "- When providing employee details, use a clean **bulleted list** with bold labels.\n"
        "- Use a header like '### 👤 Employee Profile: [Name]'.\n"
        "- Format dates clearly (e.g., Jan 05, 2026).\n"
        "- If a manager is present, mention them clearly.\n\n"
        "Example format:\n"
        "### 👤 Employee Profile: Rahul Sharma\n"
        "- **Code:** E1001\n"
        "- **Dept:** Engineering\n"
        "- **Role:** Lead Engineer\n"
        "- **Email:** rahul@acme.com"
    ),
    tools=[employees_tools],
)