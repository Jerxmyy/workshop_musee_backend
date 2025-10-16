from typing import List, Dict, Any, Optional
from supabase_config import supabase_config
from supabase import Client

class SupabaseFavouritesService:
    def __init__(self):
        self.client: Client = supabase_config.get_client()
        self.service_client: Client = supabase_config.get_service_client()
    
    async def add_favourite(self, user_id: str, musee_id: str, musee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Ajouter un musée aux favoris d'un utilisateur"""
        try:
            # Vérifier si le musée existe déjà dans la table musees
            musee_result = self.service_client.table('musees').select('identifiant').eq('identifiant', musee_id).execute()
            
            if not musee_result.data:
                # Le musée n'existe pas, l'ajouter à la table musees
                musee_to_insert = {
                    "identifiant": musee_id,
                    **musee_data
                }
                self.service_client.table('musees').insert(musee_to_insert).execute()
            
            # Ajouter le favori
            favourite_data = {
                "user_id": user_id,
                "musee_id": musee_id
            }
            
            result = self.service_client.table('favourites').insert(favourite_data).execute()
            
            if result.data:
                return {
                    "success": True,
                    "message": "Musée ajouté aux favoris",
                    "favourite": result.data[0]
                }
            else:
                return {
                    "success": False,
                    "error": "Erreur lors de l'ajout du favori"
                }
                
        except Exception as e:
            if "duplicate key" in str(e).lower() or "unique constraint" in str(e).lower():
                return {
                    "success": False,
                    "error": "Ce musée est déjà dans vos favoris"
                }
            return {
                "success": False,
                "error": f"Erreur lors de l'ajout du favori: {str(e)}"
            }
    
    async def remove_favourite(self, user_id: str, musee_id: str) -> Dict[str, Any]:
        """Retirer un musée des favoris d'un utilisateur"""
        try:
            result = self.service_client.table('favourites').delete().eq('user_id', user_id).eq('musee_id', musee_id).execute()
            
            if result.data:
                return {
                    "success": True,
                    "message": "Musée retiré des favoris"
                }
            else:
                return {
                    "success": False,
                    "error": "Favori non trouvé"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la suppression du favori: {str(e)}"
            }
    
    async def get_user_favourites(self, user_id: str) -> Dict[str, Any]:
        """Récupérer tous les favoris d'un utilisateur avec les données des musées"""
        try:
            result = self.service_client.table('favourites').select(
                """
                id,
                date_ajout,
                musees (
                    identifiant,
                    nom_officiel,
                    adresse,
                    lieu,
                    code_postal,
                    ville,
                    region,
                    departement,
                    telephone,
                    url,
                    categorie,
                    domaine_thematique,
                    themes,
                    histoire,
                    atout,
                    artiste,
                    personnage_phare,
                    interet,
                    protection_batiment,
                    protection_espace,
                    refmer,
                    annee_creation,
                    date_de_mise_a_jour,
                    coordonnees
                )
                """
            ).eq('user_id', user_id).execute()
            
            if result.data:
                return {
                    "success": True,
                    "favourites": result.data
                }
            else:
                return {
                    "success": True,
                    "favourites": []
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la récupération des favoris: {str(e)}"
            }
    
    async def is_favourite(self, user_id: str, musee_id: str) -> Dict[str, Any]:
        """Vérifier si un musée est dans les favoris d'un utilisateur"""
        try:
            result = self.service_client.table('favourites').select('id').eq('user_id', user_id).eq('musee_id', musee_id).execute()
            
            return {
                "success": True,
                "is_favourite": len(result.data) > 0
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la vérification du favori: {str(e)}"
            }
    
    async def get_favourites_count(self, user_id: str) -> Dict[str, Any]:
        """Récupérer le nombre de favoris d'un utilisateur"""
        try:
            result = self.service_client.table('favourites').select('id', count='exact').eq('user_id', user_id).execute()
            
            return {
                "success": True,
                "count": result.count if hasattr(result, 'count') else len(result.data)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors du comptage des favoris: {str(e)}"
            }
    
    async def search_favourites(self, user_id: str, search_term: str) -> Dict[str, Any]:
        """Rechercher dans les favoris d'un utilisateur"""
        try:
            result = self.service_client.table('favourites').select(
                """
                id,
                date_ajout,
                musees (
                    identifiant,
                    nom_officiel,
                    adresse,
                    lieu,
                    ville,
                    region,
                    departement,
                    categorie,
                    themes
                )
                """
            ).eq('user_id', user_id).ilike('musees.nom_officiel', f'%{search_term}%').execute()
            
            return {
                "success": True,
                "favourites": result.data,
                "search_term": search_term
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de la recherche dans les favoris: {str(e)}"
            }
