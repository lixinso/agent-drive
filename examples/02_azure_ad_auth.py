import os
from azure.identity import DefaultAzureCredential
from agent_drive import AgentDrive, LocalProvider
from agent_drive.auth import EntraIDAuthenticator

def main():
    print("To run this example, ensure you are logged in via 'az login'")
    print("and set the AGENT_DRIVE_CLIENT_ID environment variable.\n")
    
    client_id = os.getenv("AGENT_DRIVE_CLIENT_ID", "dummy-client-id-replace-me")
    
    try:
        credential = DefaultAzureCredential()
        auth = EntraIDAuthenticator(credential=credential, client_id=client_id)
        drive = AgentDrive(provider=LocalProvider("./shared_workspace"), authenticator=auth)
        
        print(f"Authenticated successfully as Object ID: {drive.identity.object_id}")
        print(f"Has Admin Role: {drive.identity.is_admin}")
        
        # When using Auth, put() automatically routes to the identity's Object ID workspace
        # uri = drive.put("local_file.txt", filename="output.txt")
        # print(f"File uploaded to secure workspace: {uri}")
        
    except Exception as e:
        print(f"Authentication context mapping failed (expected if not logged in to Azure): {e}")

if __name__ == "__main__":
    main()
