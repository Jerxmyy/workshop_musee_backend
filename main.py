from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List
import uvicorn
import os
import logging

# Import des services
from supabase_auth_service import SupabaseAuthService
from supabase_favourites_service import SupabaseFavouritesService
from supabase_auth_middleware import get_current_user

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_cors_origins() -> List[str]:
    """
    Configure les origines CORS de manière dynamique en fonction de l'environnement.
    
    Returns:
        List[str]: Liste des origines autorisées pour CORS
    """
    # URLs par défaut pour le développement
    default_origins = [
        "http://localhost:5173",  # Port Vite/Vue
        "http://localhost:3000",  # Port React/Next.js
    ]
    
    # URLs depuis les variables d'environnement
    env_origins = []
    
    # FRONTEND_URL - URL principale de production
    frontend_url = os.getenv("FRONTEND_URL")
    if frontend_url:
        env_origins.append(frontend_url)
        logger.info(f"🌐 URL frontend détectée: {frontend_url}")
    
    # PRODUCTION_URL - URL de production alternative
    production_url = os.getenv("PRODUCTION_URL")
    if production_url:
        env_origins.append(production_url)
        logger.info(f"🚀 URL de production détectée: {production_url}")
    
    # CORS_ORIGINS - URLs supplémentaires séparées par des virgules
    cors_origins_env = os.getenv("CORS_ORIGINS")
    if cors_origins_env:
        additional_origins = [url.strip() for url in cors_origins_env.split(",") if url.strip()]
        env_origins.extend(additional_origins)
        logger.info(f"🔗 URLs CORS supplémentaires: {additional_origins}")
    
    # Combiner toutes les URLs et supprimer les doublons
    all_origins = default_origins + env_origins
    unique_origins = list(dict.fromkeys(all_origins))  # Préserve l'ordre et supprime les doublons
    
    # Logging de la configuration finale
    logger.info("🔒 Configuration CORS:")
    logger.info(f"   📍 URLs de développement: {default_origins}")
    if env_origins:
        logger.info(f"   🌍 URLs d'environnement: {env_origins}")
    logger.info(f"   ✅ Total des origines autorisées: {len(unique_origins)}")
    
    return unique_origins

app = FastAPI(
    title="MuseoFile API",
    description="API pour la gestion des musées et favoris avec Supabase",
    version="2.1.0"
)

# Configuration CORS dynamique
ALLOWED_ORIGINS = get_cors_origins()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instances des services
auth_service = SupabaseAuthService()
favourites_service = SupabaseFavouritesService()

# Modèles Pydantic
class UserRegister(BaseModel):
    email: str
    password: str
    nom: str
    prenom: str

class UserLogin(BaseModel):
    email: str
    password: str

class FavouriteCreate(BaseModel):
    musee_id: str
    musee_data: Dict[str, Any]

class FavouriteResponse(BaseModel):
    id: str
    date_ajout: str
    musee: Dict[str, Any]

# Routes de santé
@app.get("/")
async def root():
    return {"message": "MuseoFile API - Service en cours d'exécution"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "MuseoFile API"}

# Routes d'authentification
@app.post("/register")
async def register(user_data: UserRegister):
    """Inscription d'un nouvel utilisateur"""
    result = await auth_service.register_user(
        email=user_data.email,
        password=user_data.password,
        nom=user_data.nom,
        prenom=user_data.prenom
    )
    
    if result["success"]:
        return {
            "message": "Inscription réussie",
            "user": result["user"],
            "access_token": result["session"].access_token if result["session"] else None
        }
    else:
        raise HTTPException(status_code=400, detail=result["error"])

@app.post("/login")
async def login(user_data: UserLogin):
    """Connexion d'un utilisateur"""
    result = await auth_service.login_user(
        email=user_data.email,
        password=user_data.password
    )
    
    if result["success"]:
        return {
            "message": "Connexion réussie",
            "user": result["user"],
            "access_token": result["session"].access_token if result["session"] else None
        }
    else:
        raise HTTPException(status_code=401, detail=result["error"])

@app.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """Déconnexion d'un utilisateur"""
    return {"message": "Déconnexion réussie"}

@app.get("/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    """Récupérer le profil de l'utilisateur connecté"""
    return {
        "user": current_user
    }

# Routes des favoris
@app.post("/favourites")
async def add_favourite(
    favourite_data: FavouriteCreate,
    current_user: dict = Depends(get_current_user)
):
    """Ajouter un musée aux favoris"""
    result = await favourites_service.add_favourite(
        user_id=current_user["id"],
        musee_id=favourite_data.musee_id,
        musee_data=favourite_data.musee_data
    )
    
    if result["success"]:
        return {
            "message": result["message"],
            "favourite": result["favourite"]
        }
    else:
        raise HTTPException(status_code=400, detail=result["error"])

@app.delete("/favourites/{musee_id}")
async def remove_favourite(
    musee_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Retirer un musée des favoris"""
    result = await favourites_service.remove_favourite(
        user_id=current_user["id"],
        musee_id=musee_id
    )
    
    if result["success"]:
        return {"message": result["message"]}
    else:
        raise HTTPException(status_code=404, detail=result["error"])

@app.get("/favourites")
async def get_favourites(current_user: dict = Depends(get_current_user)):
    """Récupérer tous les favoris de l'utilisateur"""
    result = await favourites_service.get_user_favourites(current_user["id"])
    
    if result["success"]:
        return {
            "favourites": result["favourites"],
            "count": len(result["favourites"])
        }
    else:
        raise HTTPException(status_code=500, detail=result["error"])

@app.get("/favourites/{musee_id}/check")
async def check_favourite(
    musee_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Vérifier si un musée est dans les favoris"""
    result = await favourites_service.is_favourite(
        user_id=current_user["id"],
        musee_id=musee_id
    )
    
    if result["success"]:
        return {"is_favourite": result["is_favourite"]}
    else:
        raise HTTPException(status_code=500, detail=result["error"])

@app.get("/favourites/search")
async def search_favourites(
    q: str,
    current_user: dict = Depends(get_current_user)
):
    """Rechercher dans les favoris"""
    result = await favourites_service.search_favourites(
        user_id=current_user["id"],
        search_term=q
    )
    
    if result["success"]:
        return {
            "favourites": result["favourites"],
            "search_term": result["search_term"],
            "count": len(result["favourites"])
        }
    else:
        raise HTTPException(status_code=500, detail=result["error"])

@app.get("/favourites/count")
async def get_favourites_count(current_user: dict = Depends(get_current_user)):
    """Récupérer le nombre de favoris"""
    result = await favourites_service.get_favourites_count(current_user["id"])
    
    if result["success"]:
        return {"count": result["count"]}
    else:
        raise HTTPException(status_code=500, detail=result["error"])

@app.get("/public/health")
async def public_health():
    """Point de contrôle de santé publique"""
    return {"status": "healthy", "public": True}

# Gestion des erreurs
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return {"error": "Endpoint non trouvé", "path": str(request.url)}

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    return {"error": "Erreur interne du serveur", "path": str(request.url)}

if __name__ == "__main__":
    print("🚀 Démarrage du serveur MuseoFile API...")
    print("📡 API disponible sur: http://localhost:8000")
    print("📚 Documentation: http://localhost:8000/docs")
    print("🔧 Interface ReDoc: http://localhost:8000/redoc")
    print(f"🔒 Origines CORS autorisées: {ALLOWED_ORIGINS}")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
