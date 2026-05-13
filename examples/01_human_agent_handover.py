import os
import shutil
from pathlib import Path
from agent_drive import AgentDrive, LocalProvider

def main():
    # Setup dummy files for demonstration
    Path("dummy_dataset.csv").write_text("id,name\n1,alice\n2,bob\n")
    
    # 1. Initialize the drive (Human side)
    provider = LocalProvider(base_path="./shared_workspace")
    drive = AgentDrive(provider=provider)

    print("--- HUMAN SIDE ---")
    # 2. Human uploads a file and gets a "Claim Check" URI
    print("Uploading dummy_dataset.csv to Agent Drive...")
    claim_check_uri = drive.put("dummy_dataset.csv", agent_id="agent_004", filename="dataset.csv")
    print(f"Human says: 'Agent, please process this data: {claim_check_uri}'\n")

    # ... (URI is passed via prompt to LLM) ...

    print("--- AGENT SIDE ---")
    # 3. Agent side: receives the URI, downloads the file
    download_dest = "agent_working_dir/downloaded_data.csv"
    local_path = drive.get(claim_check_uri, download_path=download_dest)
    print(f"Agent reads data from: {local_path}")
    
    # 4. Agent does work...
    Path("agent_working_dir").mkdir(exist_ok=True)
    Path("agent_working_dir/agent_output.json").write_text('{"status": "success", "count": 2}')
    
    # 5. Agent uploads result and returns a new URI
    result_uri = drive.put("agent_working_dir/agent_output.json", agent_id="agent_004", filename="output.json")
    print(f"Agent says: 'I am done. Here are the results: {result_uri}'\n")

    # Cleanup demonstration artifacts
    shutil.rmtree("shared_workspace", ignore_errors=True)
    shutil.rmtree("agent_working_dir", ignore_errors=True)
    os.remove("dummy_dataset.csv")

if __name__ == "__main__":
    main()
