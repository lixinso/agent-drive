from pathlib import Path
from azure.storage.blob import BlobServiceClient
from ..core import StorageProvider

class AzureProvider(StorageProvider):
    """
    Azure Blob Storage provider.
    Connects via Entra ID (DefaultAzureCredential) enabling true RBAC data-plane access.
    """
    
    def __init__(self, account_url: str = None, container_name: str = None, credential=None, connection_string: str = None):
        self.container_name = container_name
        
        if connection_string:
            self.service = BlobServiceClient.from_connection_string(conn_str=connection_string)
        elif credential and account_url:
            self.service = BlobServiceClient(account_url=account_url, credential=credential)
        else:
            raise ValueError("Must provide either connection_string, or both account_url and credential")
            
        self.container_client = self.service.get_container_client(self.container_name)
        # We don't auto-create the container here as Entra ID Storage Blob Data Contributor 
        # often restricts container creation. The container should be provisioned by IaC.

    def put(self, local_file_path: str, destination_path: str) -> str:
        # Azure Blob Storage uses virtual directories, so we don't need to create parent folders
        blob_client = self.container_client.get_blob_client(destination_path)
        
        with open(local_file_path, "rb") as source_file:
            blob_client.upload_blob(source_file, overwrite=True)
            
        return f"agentdrive://azure/{self.container_name}/{destination_path}"

    def get(self, uri: str, download_path: str) -> str:
        prefix = f"agentdrive://azure/{self.container_name}/"
        if not uri.startswith(prefix):
            raise ValueError(f"Invalid URI for this AzureProvider instance: {uri}")
            
        blob_path = uri[len(prefix):]
        blob_client = self.container_client.get_blob_client(blob_path)
        
        dest = Path(download_path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        
        with open(dest, "wb") as file_handle:
            download_stream = blob_client.download_blob()
            file_handle.write(download_stream.readall())
            
        return str(dest)
