import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class SupabaseConfig:
    def __init__(self):
        self.url = os.getenv('SUPABASE_URL')
        self.anon_key = os.getenv('SUPABASE_ANON_KEY')
        self.service_role_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        
        if not all([self.url, self.anon_key, self.service_role_key]):
            raise ValueError("Variables d'environnement Supabase manquantes. Vérifiez votre fichier .env")
    
    def get_client(self) -> Client:
        """Retourne le client Supabase avec la clé anonyme"""
        return create_client(self.url, self.anon_key)
    
    def get_service_client(self) -> Client:
        """Retourne le client Supabase avec la clé service role (pour les opérations admin)"""
        return create_client(self.url, self.service_role_key)

# Instance globale de configuration
supabase_config = SupabaseConfig()
