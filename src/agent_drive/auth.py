import jwt
from typing import List
from azure.identity import DefaultAzureCredential

class IdentityContext:
    def __init__(self, object_id: str, roles: List[str]):
        self.object_id = object_id
        self.roles = roles
    
    @property
    def is_admin(self) -> bool:
        return "AgentDrive.Admin" in self.roles

class EntraIDAuthenticator:
    def __init__(self, credential: DefaultAzureCredential, client_id: str):
        self.credential = credential
        self.client_id = client_id
        
    def authenticate(self) -> IdentityContext:
        # Request a token for the specified application client ID
        scope = f"{self.client_id}/.default"
        token_obj = self.credential.get_token(scope)
        
        # Decode the token (signature verification happens at the cloud provider layer, 
        # the SDK decodes locally to establish workspace context)
        decoded = jwt.decode(token_obj.token, options={"verify_signature": False})
        
        # 'oid' is the Object ID of the user/managed identity. 'sub' is fallback.
        oid = decoded.get("oid") or decoded.get("sub", "unknown_identity")
        roles = decoded.get("roles", [])
        
        return IdentityContext(object_id=oid, roles=roles)
