import abc
from typing import Optional

class StorageProvider(abc.ABC):
    @abc.abstractmethod
    def put(self, local_file_path: str, destination_path: str) -> str:
        pass

    @abc.abstractmethod
    def get(self, uri: str, download_path: str) -> str:
        pass

class AgentDrive:
    def __init__(self, provider: StorageProvider, authenticator=None):
        self.provider = provider
        self.authenticator = authenticator
        self.identity = None
        if self.authenticator:
            self.identity = self.authenticator.authenticate()

    def _get_workspace(self, target_workspace: Optional[str] = None) -> str:
        if not self.identity:
            if not target_workspace:
                raise ValueError("No authenticator provided. Must specify target_workspace explicitly.")
            return target_workspace
        
        if target_workspace and target_workspace != self.identity.object_id:
            if not self.identity.is_admin:
                raise PermissionError(f"Identity {self.identity.object_id} lacks Admin role to write to workspace {target_workspace}")
            return target_workspace
        
        return self.identity.object_id

    def put(self, local_file_path: str, filename: str, target_workspace: Optional[str] = None) -> str:
        """Upload a file into the workspace determined by Identity or override."""
        workspace = self._get_workspace(target_workspace)
        dest = f"{workspace}/{filename}"
        return self.provider.put(local_file_path, dest)

    def get(self, uri: str, download_path: str) -> str:
        """Retrieve a file using its Claim Check URI, enforcing RBAC."""
        parts = uri.replace("agentdrive://", "").split("/")
        if len(parts) >= 2:
            workspace = parts[1]
            if self.identity and workspace != self.identity.object_id and not self.identity.is_admin:
                raise PermissionError(f"Identity {self.identity.object_id} lacks Admin role to read from workspace {workspace}")
        
        return self.provider.get(uri, download_path)
