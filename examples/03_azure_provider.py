import os
from azure.identity import DefaultAzureCredential
from agent_drive import AgentDrive
from agent_drive.providers.azure import AzureProvider
from agent_drive.auth import EntraIDAuthenticator

def main():
    print("This example demonstrates uploading to a real Azure File Share.")
    account_url = os.getenv("AGENT_DRIVE_ACCOUNT_URL")
    container_name = os.getenv("AGENT_DRIVE_CONTAINER_NAME", "agent-drive-root")
    
    if not account_url:
        print("Please set AGENT_DRIVE_ACCOUNT_URL (e.g., https://<account>.file.core.windows.net) to run.")
        return

    # Use Entra ID for zero-secret data-plane access
    credential = DefaultAzureCredential()
    
    provider = AzureProvider(
        account_url=account_url,
        container_name=container_name,
        credential=credential
    )
    
    # Optional: plug in the authenticator if we want to enforce RBAC logic
    client_id = os.getenv("AGENT_DRIVE_CLIENT_ID")
    auth = EntraIDAuthenticator(credential, client_id) if client_id else None
    
    drive = AgentDrive(provider=provider, authenticator=auth)
    
    print(f"Connecting to {account_url}/{container_name}...")
    
    # Uncomment to test with real files
    # uri = drive.put("local_data.csv", filename="remote_data.csv", target_workspace="operator_workspace")
    # print(f"File uploaded. URI: {uri}")
    
    # drive.get(uri, "downloaded_data.csv")

if __name__ == "__main__":
    main()
