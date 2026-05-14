from .core import AgentDrive, StorageProvider
from .providers.local import LocalProvider
from .providers.azure import AzureProvider

__version__ = "0.1.0"
from .auth import EntraIDAuthenticator, IdentityContext

from .providers.azure_blob import AzureBlobProvider
from .providers.azure_files import AzureFileShareProvider
from .providers.mounted import MountedProvider

__all__ = ["AgentDrive", "StorageProvider", "LocalProvider", "AzureBlobProvider", "AzureFileShareProvider", "MountedProvider", "EntraIDAuthenticator", "IdentityContext"]
