# 🚀 Hack in Saclay 2026 - Mob IA Team

![AI Status](https://img.shields.io/badge/AI-Agentic%20Powerhouse-blueviolet)
![Status](https://img.shields.io/badge/Hackathon-Submission-success)

## 💡 The Vision: Beyond Chatbots, Towards Action Agents

**Welcome to the future of Insurance-Client relationships.**

At **Mob IA**, we believe the era of passive "chatbots" is over. Users don't just want to talk; they want to **do**. 

For **Hack in Saclay 2026**, we present a comprehensive ecosystem powered by **Autonomus Action Agents**. These are not simple conversational interfaces; they are intelligent entities capable of reasoning, using tools, accessing databases, and executing complex workflows to bridge the gap between Insurance providers and their Clients.

We propose **3 interconnected solutions** to revolutionize the industry:

---

## 🏗️ Project Architecture

### 1. 🏢 Smart Claims Management (The Brain)
> *Intelligent Request Management & Dispatcher*

A powerful **AI Workstation** designed for insurance agents to handle internal management efficiently.
- **What it does:** Uses specialized agents to analyze incoming emails, assess urgency, summarize cases, and draft responses.
- **The Magic:**
    - **Dispatcher Agent**: Automatically categorizes and routes tickets.
    - **Validator Agent**: Ensures compliance and accuracy before any action is taken.
    - **Action Capabilities**: Can `issue_reimbursement`, `modify_client_data`, and access deep RAG knowledge.

### 2. 👤 Smart Customer Service (The Client's Right Hand)
> *AI Agentic Augmented Interaction for Individuals*

**FORGET CHATBOTS.** This is an **Action Agent** dedicated to the client.
- **What it does:** Allows clients to interact naturally with their insurance policy, but with the power to *act*.
- **The "Action" Difference:** It doesn't just recite terms. It can:
    - 📂 **Load & Analyze** personal contracts.
    - 📝 **Open Formal Requests** directly in the system.
    - 🧠 **Reason** over complex reimbursement logic (Health, Providence, Savings).
- **Goal:** Frictionless, result-oriented interaction.

### 3. 💼 Smart Company Service (The B2B Powerhouse)
> *Enterprise-Grade Agent for Business Managers*

Built on the same robust agentic framework but tailored for **HR and Business Managers**.
- **What it does:** Streamlines the management of company insurance policies and employee coverage.
- **Action Capabilities:**
    - 👥 **List & Manage Employees**: Instantly query employee status.
    - 📊 **Company Data Analysis**: Deep dive into company contracts.
    - 📨 **Official Claims**: Send verified official claims directly to the insurer.

---

## 🛠️ The Tech Stack (Agentic Core)

We leverage the latest in AI orchestration and local vector search:

*   **Frameworks:** `Streamlit`, `SmolAgents` (The heart of our Agentic logic), `LangChain`
*   **Intelligence:** `OpenAI GPT-5/5.1` (Simulated/Preview), `Hugging Face`
*   **Memory & Knowledge:** `ChromaDB` (Vector Store for RAG), `Docling`
*   **Tools:** Python Interpreter, Custom Tool Definitions

##  Data & Security


Each application maintains its own local data for simulation purposes:

*   **Smart Claims Management/data/**: Contains `clients.json`, `emails.json`, and the `chroma/` vector store.
*   **Smart Customer Service/data/**: Contains individual `client.json` profiles.
*   **Smart Company Service/data/**: Contains `company.json` and employee records.

## 🚀 Getting Started

### Prerequisites
*   Python >= 3.13
*   `uv` (recommended) or `pip`

### Installation

Each project is a standalone application. Navigate to the respective folder and install dependencies:

```bash
# Example for Backend
cd "Smart Claims Management/apps/backend"
uv sync  # or pip install .
```

### Running the Agents

**1. Smart Claims Management:**
```bash
streamlit run "Smart Claims Management/apps/backend/src/app.py"
```

**2. Smart Customer Service:**
```bash
streamlit run "Smart Customer Service/src/app.py"
```

**3. Smart Company Service:**
```bash
streamlit run "Smart Company Service/src/app.py"
```

**Note** : If you encounter import issues, set pythonpath to src for each usecase.
---

*Note: This repository contains highly advanced Agentic Workflows. Proceed with curiosity.* 🤖✨
