import shutil
from pathlib import Path
from ..core import StorageProvider

class LocalProvider(StorageProvider):
    """A local file system provider for testing and single-machine setups."""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def put(self, local_file_path: str, destination_path: str) -> str:
        src = Path(local_file_path)
        dest = self.base_path / destination_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        return f"agentdrive://local/{destination_path}"

    def get(self, uri: str, download_path: str) -> str:
        if not uri.startswith("agentdrive://local/"):
            raise ValueError(f"Invalid URI for LocalProvider: {uri}")
        
        path_suffix = uri.replace("agentdrive://local/", "")
        src = self.base_path / path_suffix
        dest = Path(download_path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        return str(dest)
