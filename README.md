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

## 🔌 Supported Providers & Use Cases

Agent Drive supports multiple backends depending on whether you are the Human Operator (uploading over the internet) or the AI Agent (running on a VM).

### 1. Azure File Share + SMB Mounts (Recommended for Heavy I/O)
This is the optimal setup for agents handling massive files (like video rendering or huge datasets).

**For the Operator (Human):** Uses the Storage Account Key to upload over the internet.
```python
from agent_drive import AgentDrive
from agent_drive.providers.azure_files import AzureFileShareProvider

provider = AzureFileShareProvider(
    share_name="agent-drive-root",
    connection_string="DefaultEndpointsProtocol=https;AccountName=..."
)
drive = AgentDrive(provider=provider, authenticator=auth)
uri = drive.put("massive_video.mp4", target_workspace="mrbeast_agent")
# Returns: agentdrive://azure-file/agent-drive-root/mrbeast_agent/massive_video.mp4
```

**For the AI Agent (Worker):** The Azure File Share is mounted to the VM's OS (e.g., via `/etc/fstab`). The Agent uses the `MountedProvider`, which **bypasses downloading entirely** and translates the URI directly to the local Linux path.
```python
from agent_drive import AgentDrive
from agent_drive.providers.mounted import MountedProvider

provider = MountedProvider(
    mount_point="/mnt/agent-drive-root",
    uri_prefix="agentdrive://azure-file/agent-drive-root/"
)
drive = AgentDrive(provider=provider)

# Instant! Zero network I/O.
local_path = drive.get("agentdrive://azure-file/agent-drive-root/mrbeast_agent/massive_video.mp4")
# local_path == "/mnt/agent-drive-root/mrbeast_agent/massive_video.mp4"
```

### 2. Azure Blob Storage (Recommended for Strict Entra ID / Zero-Trust)
If your organization disables Storage Account Keys and mandates Entra ID (OAuth) for all data-plane access, use the Blob provider.

```python
from azure.identity import DefaultAzureCredential
from agent_drive.providers.azure_blob import AzureBlobProvider

# Uses `az login` or VM Managed Identity automatically!
provider = AzureBlobProvider(
    account_url="https://<account>.blob.core.windows.net",
    container_name="agent-drive-root",
    credential=DefaultAzureCredential()
)
```

### 3. LocalProvider (For Testing)
Zero setup. Copies files to a local directory for easy POCs.
