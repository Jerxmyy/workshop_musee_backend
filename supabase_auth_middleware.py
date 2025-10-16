from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from supabase_auth_service import SupabaseAuthService

# Instance du service d'authentification
auth_service = SupabaseAuthService()

# Schéma de sécurité pour l'authentification Bearer
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Middleware pour récupérer l'utilisateur actuel à partir du token JWT
    """
    try:
        token = credentials.credentials
        
        # Vérifier le token avec Supabase
        verification_result = await auth_service.verify_token(token)
        
        if not verification_result["success"]:
            raise HTTPException(
                status_code=401,
                detail="Token invalide ou expiré",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Récupérer le profil complet de l'utilisateur
        profile_result = await auth_service.get_user_profile(verification_result["user_id"])
        
        if not profile_result["success"]:
            raise HTTPException(
                status_code=404,
                detail="Profil utilisateur non trouvé"
            )
        
        return profile_result["user"]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Erreur d'authentification: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_optional_user(request: Request) -> Optional[dict]:
    """
    Middleware optionnel pour récupérer l'utilisateur si un token est présent
    (utile pour les endpoints qui fonctionnent avec ou sans authentification)
    """
    try:
        # Vérifier si un header Authorization est présent
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        
        # Extraire le token
        token = auth_header.split(" ")[1]
        
        # Vérifier le token
        verification_result = await auth_service.verify_token(token)
        
        if not verification_result["success"]:
            return None
        
        # Récupérer le profil
        profile_result = await auth_service.get_user_profile(verification_result["user_id"])
        
        if profile_result["success"]:
            return profile_result["user"]
        
        return None
        
    except Exception:
        return None

def require_auth(func):
    """
    Décorateur pour protéger les endpoints qui nécessitent une authentification
    """
    async def wrapper(*args, **kwargs):
        # Cette fonction sera utilisée avec Depends(get_current_user)
        return await func(*args, **kwargs)
    return wrapper

def optional_auth(func):
    """
    Décorateur pour les endpoints qui peuvent fonctionner avec ou sans authentification
    """
    async def wrapper(*args, **kwargs):
        # Cette fonction sera utilisée avec Depends(get_optional_user)
        return await func(*args, **kwargs)
    return wrapper
