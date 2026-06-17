# HR AI Assistant using Google ADK, MCP and FastAPI

An AI-powered HR Assistant built using **Google Agent Development Kit (ADK)**, **Model Context Protocol (MCP)**, **FastAPI**, and **Gemini 2.5 Flash**.

The assistant uses a multi-agent architecture where a central orchestrator routes user requests to specialized agents for:

* Employee Profile Management
* Leave Management
* Compensation & Salary Information
* Company Policy Questions (RAG-powered)

The application includes a modern web UI built with FastAPI and supports conversational HR workflows through MCP servers.

---

# Architecture

```text
User
  |
  v
FastAPI Web UI
  |
  v
Orchestrator Agent
  |
  +------------------+
  |                  |
  v                  v
Employee Agent    Leave Agent
  |                  |
  MCP Server      MCP Server

  +------------------+
  |
  v
Compensation Agent
  |
  MCP Server

  +------------------+
  |
  v
Policy Agent
  |
  RAG MCP Server
```

---

# Features

## Employee Agent

Provides:

* Employee profile details
* Employee code
* Department
* Designation
* Email
* Phone
* Manager
* Joining Date

---

## Leave Agent

Provides:

* Leave balance
* Leave history
* Leave application
* Leave cancellation

---

## Compensation Agent

Provides:

* Salary details
* Bonus information
* Compensation records
* Effective compensation dates

---

## Policy Agent

Provides:

* Leave policy information
* Work From Home policy
* Company policies
* RAG-based document search

---

# Technology Stack

## AI & Agent Framework

* Google ADK
* Gemini 2.5 Flash
* MCP (Model Context Protocol)

## Backend

* FastAPI
* Uvicorn
* Python

## RAG

* ChromaDB
* PyPDF

## Frontend

* HTML
* CSS
* JavaScript

---

# Project Structure

```text
employee-assistant/
│
├── agents/
│   ├── orchestrator_agent/
│   ├── employee_agent/
│   ├── leave_agent/
│   ├── comp_agent/
│   └── policy_agent/
│
├── mcp_servers/
│   ├── mcp_employees/
│   ├── mcp_leave/
│   ├── mcp_compensation/
│   └── mcp_policies_rag/
│
├── static/
│   └── index.html
│
├── app.py
├── requirements.txt
├── .env
└── README.md
```

---

# Prerequisites

Install:

* Python 3.11
* Git

Verify:

```bash
python --version
git --version
```

---

# Clone the Repository

```bash
git clone https://github.com/shaikk0308/agentic-hr-assistant.git
cd agentic-hr-assistant
```


---

# Create Virtual Environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Mac/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt

pip install -e

```

---

# Setup Database

```bash
python re-design_dbs.py
```

---


# Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

Replace with your actual Gemini API key.

---

# Run the Application

Start FastAPI:

```bash
uvicorn app:app --reload
```

You should see:

```text
Uvicorn running on:
http://127.0.0.1:8000
```

---

# Open the Application

Open your browser:

```text
http://127.0.0.1:8000
```

The HR Assistant UI should load.

---

# Example Questions

Employee:

```text
Show employee E1001 details
```

Leave:

```text
Show leave balance for E1001
```

Compensation:

```text
What is the salary for E1001?
```

Policy:

```text
What is the Work From Home policy?
```

---

# MCP Servers

This project uses MCP servers to expose HR functionality to AI agents.

Current MCP Servers:

| MCP Server       | Purpose                 |
| ---------------- | ----------------------- |
| mcp_employees    | Employee data           |
| mcp_leave        | Leave management        |
| mcp_compensation | Salary and compensation |
| mcp_policies_rag | Policy search using RAG |

The agents communicate with these MCP servers through Google ADK tool integrations.

---

# RAG Policy Search

The Policy Agent uses:

* PyPDF for PDF parsing
* ChromaDB for vector storage
* MCP server for policy retrieval

Supported queries:

```text
What is the leave policy?

What is the notice period policy?

How many WFH days are allowed?
```

---

# Development

Run in development mode:

```bash
uvicorn app:app --reload
```

Changes to Python files will automatically reload the application.

---

# Troubleshooting

## Missing Dependencies

```bash
pip install -r requirements.txt
```

---

## Invalid API Key

Verify:

```env
GOOGLE_API_KEY=YOUR_KEY
```

---

## MCP Server Errors

Ensure:

* Virtual environment is activated
* Dependencies are installed
* MCP server files exist
* Paths are correct

---

## FastAPI Not Starting

Verify:

```bash
python app.py
```

or

```bash
uvicorn app:app --reload
```

---

