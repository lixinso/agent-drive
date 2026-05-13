from ..core import StorageProvider

class AzureProvider(StorageProvider):
    """
    Azure File Share provider (Skeleton).
    To be fully implemented in an upcoming release.
    """
    
    def __init__(self, connection_string: str, share_name: str):
        self.connection_string = connection_string
        self.share_name = share_name
        # self.service = ShareServiceClient.from_connection_string(...)

    def put(self, local_file_path: str, destination_path: str) -> str:
        # TODO: Implement Azure File Share upload
        return f"agentdrive://azure/{self.share_name}/{destination_path}"

    def get(self, uri: str, download_path: str) -> str:
        # TODO: Implement Azure File Share download
        return download_path
