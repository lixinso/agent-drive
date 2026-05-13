import abc
from typing import Optional

class StorageProvider(abc.ABC):
    @abc.abstractmethod
    def put(self, local_file_path: str, destination_path: str) -> str:
        """Uploads a file and returns a Claim Check URI."""
        pass

    @abc.abstractmethod
    def get(self, uri: str, download_path: str) -> str:
        """Downloads a file from a Claim Check URI to the local path."""
        pass

class AgentDrive:
    def __init__(self, provider: StorageProvider):
        self.provider = provider

    def put(self, local_file_path: str, agent_id: str, filename: str) -> str:
        """Upload a file into the specific agent's workspace."""
        dest = f"{agent_id}/{filename}"
        return self.provider.put(local_file_path, dest)

    def get(self, uri: str, download_path: str) -> str:
        """Retrieve a file using its Claim Check URI."""
        return self.provider.get(uri, download_path)
