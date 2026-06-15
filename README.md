# 🤖 Agentic HR Assistant (Multi-Agent + MCP + RAG)

A HR Assistant built with the **Agent Development Kit (ADK)** and **Gemini**. This project demonstrates a multi-agent architecture where specialist agents collaborate to handle employee data, leave management, compensation, and company policies.

## 🚀 Key Features
- **Multi-Agent Orchestration**: A central synthesizer routes queries to 4 specialist agents (Employee, Leave, Comp, Policy).
- **Model Context Protocol (MCP)**: Custom MCP servers connect the AI directly to 4 local SQLite databases.
- **RAG (Retrieval-Augmented Generation)**: Real-time policy lookup from PDFs using **ChromaDB**.
- **Live Calculations**: Automatic leave balance deduction and refunding logic.
- **Professional UI**: Beautifully formatted Markdown reports and tables via ADK Web.

## 🏗️ Architecture
- **Orchestrator**: Routing and response synthesis.
- **Specialist Agents**: Modular agents with restricted tool access (security guardrails).
- **Data Layer**: Separated SQLite databases for Employees, Leaves, and Compensation.
- **RAG Layer**: Policy PDFs parsed via `pypdf` and indexed in `ChromaDB`.


