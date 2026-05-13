# 📦 Agent Drive

**The Enterprise File System and Workspace for Autonomous AI Agents.**

## ❓ The Problem
*   **Context Window Limits:** Passing large files (PDFs, datasets, videos) directly through LLM context is expensive, slow, and often hits token limits.
*   **Messy Handovers:** How does a human hand a 500MB dataset to an AI agent? How does an AI agent deliver a generated 1GB video back to the human?
*   **Data Compliance:** In enterprise environments, AI agents need standard access controls, just like human employees.

## 💡 The Solution: "Claim Check" Pattern
Agent Drive introduces a simple philosophy for AI operations: **Pass the pointer, not the payload.**

*   Instead of sending a file in the chat, the human uploads it to the "Agent Drive" and sends a URI (the Claim Check). 
*   The Agent uses the URI to read the file directly from its mounted drive or via SDK.
*   When the Agent finishes working, it saves the output to the Drive and replies with the new URI.

## ✨ Key Features
*   **Enterprise Identity (Entra ID):** Built-in Azure AD integration. Agents access their workspaces automatically via Managed Identities; Operators use `az login`.
*   **Role-Based Access Control (RBAC):** Strict workspace isolation by default. Identities with the `AgentDrive.Admin` role can manage cross-workspace handovers.
*   **Dedicated Agent Workspaces:** Every AI agent gets its own isolated drive (like any Cloud Drive, but for AI).
*   **Standardized Handover:** Seamless Human ↔ Agent and Agent ↔ Agent file sharing.
*   **Pluggable Architecture:** Designed to work via direct OS-level SMB/NFS mounts (for Agent VMs) or via API/SDK (Python/Node.js).

## 🚀 Quick Start (v0.1 MVP)

Currently, the SDK supports a `LocalProvider` for easy zero-setup testing, and an extensible `StorageProvider` base for cloud backends.

```bash
git clone https://github.com/lixinso/agent-drive.git
cd agent-drive
pip install -e .
```

Run the example:
```bash
python examples/01_human_agent_handover.py
```
