import os
import shutil
from pathlib import Path
from agent_drive import AgentDrive, LocalProvider

def main():
    Path("dummy_dataset.csv").write_text("id,role\n1,operator\n2,worker\n")
    
    provider = LocalProvider(base_path="./shared_workspace")
    
    # 1. Initialize the drive (No Auth for this basic example)
    drive = AgentDrive(provider=provider)

    print("--- OPERATOR SIDE ---")
    print("Uploading dummy_dataset.csv to Agent Drive...")
    # explicitly specifying target_workspace since no Auth is provided
    claim_check_uri = drive.put("dummy_dataset.csv", filename="dataset.csv", target_workspace="agent_worker_01")
    print(f"Operator says: 'Worker, please process this data: {claim_check_uri}'\n")

    print("--- WORKER SIDE ---")
    download_dest = "worker_env/downloaded_data.csv"
    local_path = drive.get(claim_check_uri, download_path=download_dest)
    print(f"Worker reads data from: {local_path}")
    
    Path("worker_env").mkdir(exist_ok=True)
    Path("worker_env/output.json").write_text('{"status": "success", "processed": 2}')
    
    result_uri = drive.put("worker_env/output.json", filename="output.json", target_workspace="agent_worker_01")
    print(f"Worker says: 'Task complete. Results: {result_uri}'\n")

    # Cleanup
    shutil.rmtree("shared_workspace", ignore_errors=True)
    shutil.rmtree("worker_env", ignore_errors=True)
    os.remove("dummy_dataset.csv")

if __name__ == "__main__":
    main()
