from typing import Dict, Any
from supabase_config import supabase_config
from supabase import Client

class SupabaseAuthService:
    def __init__(self):
        self.client: Client = supabase_config.get_client()
        self.service_client: Client = supabase_config.get_service_client()
    
    async def register_user(self, email: str, password: str, nom: str, prenom: str) -> Dict[str, Any]:
        """Inscrire un nouvel utilisateur"""
        try:
            # Inscription avec Supabase Auth
            auth_response = self.client.auth.sign_up({
                "email": email,
                "password": password
            })
            
            if auth_response.user:
                # Créer le profil utilisateur dans la table users
                user_data = {
                    "id": auth_response.user.id,
                    "email": email,
                    "nom": nom,
                    "prenom": prenom
                }
                
                # Utiliser le service client pour insérer dans la table users
                result = self.service_client.table('users').insert(user_data).execute()
                
                return {
                    "success": True,
                    "user": {
                        "id": auth_response.user.id,
                        "email": email,
                        "nom": nom,
                        "prenom": prenom
                    },
                    "session": auth_response.session
                }
            else:
                return {
                    "success": False,
                    "error": "Erreur lors de l'inscription"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur d'inscription: {str(e)}"
            }
    
    async def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """Connecter un utilisateur"""
        try:
            auth_response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if auth_response.user and auth_response.session:
                # Récupérer les données utilisateur
                user_result = self.service_client.table('users').select('*').eq('id', auth_response.user.id).execute()
                
                if user_result.data:
                    user_data = user_result.data[0]
                    return {
                        "success": True,
                        "user": user_data,
                        "session": auth_response.session
                    }
                else:
                    return {
                        "success": False,
                        "error": "Profil utilisateur non trouvé"
                    }
            else:
                return {
                    "success": False,
                    "error": "Identifiants invalides"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur de connexion: {str(e)}"
            }
    
    async def logout_user(self, access_token: str) -> Dict[str, Any]:
        """Déconnecter un utilisateur"""
        try:
            # Définir le token pour cette session
            self.client.auth.set_session(access_token, "")
            
            # Déconnexion
            self.client.auth.sign_out()
            
            return {
                "success": True,
                "message": "Déconnexion réussie"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur de déconnexion: {str(e)}"
            }
    
    async def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Récupérer le profil d'un utilisateur"""
        try:
            result = self.service_client.table('users').select('*').eq('id', user_id).execute()
            
            if result.data:
                return {
                    "success": True,
                    "user": result.data[0]
                }
            else:
                return {
                    "success": False,
                    "error": "Utilisateur non trouvé"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la récupération du profil: {str(e)}"
            }
    
    async def verify_token(self, access_token: str) -> Dict[str, Any]:
        """Vérifier la validité d'un token"""
        try:
            # Définir le token pour cette session
            self.client.auth.set_session(access_token, "")
            
            # Récupérer l'utilisateur actuel
            user = self.client.auth.get_user()
            
            if user:
                return {
                    "success": True,
                    "user_id": user.id,
                    "user": user
                }
            else:
                return {
                    "success": False,
                    "error": "Token invalide"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur de vérification du token: {str(e)}"
            }
