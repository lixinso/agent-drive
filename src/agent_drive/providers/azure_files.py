from pathlib import Path
from azure.core.exceptions import ResourceExistsError
from azure.storage.fileshare import ShareServiceClient
from ..core import StorageProvider

class AzureFileShareProvider(StorageProvider):
    """
    Azure File Share provider.
    Currently requires a connection string or SAS token for Python SDK REST operations.
    Best paired with MountedProvider for Agent VMs.
    """
    
    def __init__(self, share_name: str, connection_string: str):
        self.share_name = share_name
        self.service = ShareServiceClient.from_connection_string(conn_str=connection_string)
        self.share_client = self.service.get_share_client(self.share_name)

    def put(self, local_file_path: str, destination_path: str) -> str:
        parts = destination_path.strip("/").split("/")
        file_name = parts[-1]
        dir_parts = parts[:-1]
        
        current_dir = self.share_client.get_root_directory_client()
        for d in dir_parts:
            current_dir = current_dir.get_subdirectory_client(d)
            try:
                current_dir.create_directory()
            except ResourceExistsError:
                pass
                
        file_client = current_dir.get_file_client(file_name)
        with open(local_file_path, "rb") as source_file:
            file_client.upload_file(source_file)
            
        return f"agentdrive://azure-file/{self.share_name}/{destination_path}"

    def get(self, uri: str, download_path: str) -> str:
        prefix = f"agentdrive://azure-file/{self.share_name}/"
        if not uri.startswith(prefix):
            raise ValueError(f"Invalid URI for this AzureFileShareProvider instance: {uri}")
            
        file_path_in_share = uri[len(prefix):]
        file_client = self.share_client.get_file_client(file_path_in_share)
        
        dest = Path(download_path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        
        with open(dest, "wb") as file_handle:
            data = file_client.download_file()
            data.readinto(file_handle)
            
        return str(dest)
