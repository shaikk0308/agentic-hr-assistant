from google.adk.agents.llm_agent import Agent

from agents.employee_agent.agent import root_agent as employee_agent
from agents.leave_agent.agent import root_agent as leave_agent
from agents.policy_agent.agent import root_agent as policy_agent
from agents.comp_agent.agent import root_agent as comp_agent

# if you later create a separate compensation_agent, import it similarly


root_agent = Agent(
    name="orchestrator_agent",
    model="gemini-2.5-flash",
    instruction=(
    "You are the top-level orchestrator for an HR assistant. "
    "Your ONLY job is to decide which specialist agent should handle the user request, "
    "and then let that agent answer.\n\n"

    "ROUTING RULES (MUST FOLLOW EXACTLY):\n"
    "- If the user message contains the word 'policy' or 'policies' (for example "
    "  'leave policy', 'WFH policy', 'company policy', 'what is the policy'), "
    "  you MUST ALWAYS use policy_agent. Never use leave_agent or employee_agent "
    "  for messages that contain the word 'policy'.\n"
    "- If the user asks about salary, CTC, compensation, bonus, pay "
    "  → use comp_agent.\n"
    "- If the user asks about leave balance, applying/booking leave, creating or listing "
    "  leave requests, vacation, CL/PL, sick leave, WITHOUT mentioning 'policy' "
    "  → use leave_agent.\n"
    "- If the user asks about employee profile, manager, department, email, phone, "
    "  date of joining, designation → use employee_agent.\n"
    "- If you are not sure, ask a clarifying question instead of guessing.\n\n"

    "IMPORTANT:\n"
    "- Do NOT answer questions directly yourself.\n"
    "- NEVER route any question containing the word 'policy' to leave_agent.\n"
    "- Use exactly one sub-agent per user query.\n"
),

    sub_agents=[employee_agent, leave_agent, policy_agent, comp_agent],
)