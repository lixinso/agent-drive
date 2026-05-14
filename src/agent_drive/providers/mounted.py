from pathlib import Path
import shutil
from ..core import StorageProvider

class MountedProvider(StorageProvider):
    """
    Provider for Agent VMs where the Cloud Drive is mounted to the local OS.
    Instead of downloading, get() simply translates the URI to the absolute mount path.
    """
    
    def __init__(self, mount_point: str, uri_prefix: str):
        self.mount_point = Path(mount_point)
        self.uri_prefix = uri_prefix # e.g., "agentdrive://azure-file/agent-drive-root/"

    def put(self, local_file_path: str, destination_path: str) -> str:
        src = Path(local_file_path)
        dest = self.mount_point / destination_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        return f"{self.uri_prefix}{destination_path}"

    def get(self, uri: str, download_path: str) -> str:
        # We ignore download_path because the file is already mounted!
        if not uri.startswith(self.uri_prefix):
            raise ValueError(f"Invalid URI for MountedProvider: {uri}")
            
        path_suffix = uri.replace(self.uri_prefix, "")
        absolute_path = self.mount_point / path_suffix
        
        if not absolute_path.exists():
            raise FileNotFoundError(f"Mounted file not found at {absolute_path}")
            
        return str(absolute_path)
