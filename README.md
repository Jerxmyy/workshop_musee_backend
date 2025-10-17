# 🚀 MuséeExplorer API

API REST développée avec FastAPI pour la gestion des musées et des favoris utilisateur avec Supabase. Backend moderne et sécurisé pour l'application MuséeExplorer.

## ✨ Fonctionnalités

### 🔐 Authentification

- **Inscription utilisateur** : Création de comptes avec validation
- **Connexion sécurisée** : Authentification avec tokens JWT
- **Gestion des sessions** : Déconnexion et renouvellement de tokens
- **Profil utilisateur** : Récupération et gestion des données personnelles

### ❤️ Gestion des favoris

- **Ajout de favoris** : Sauvegarde des musées préférés
- **Suppression de favoris** : Retrait des musées des favoris
- **Consultation des favoris** : Liste complète des musées favoris
- **Recherche dans les favoris** : Filtrage et recherche textuelle
- **Comptage des favoris** : Statistiques utilisateur

### 🛡️ Sécurité et validation

- **Validation des données** : Contrôle strict avec Pydantic
- **CORS dynamique** : Configuration automatique selon l'environnement
- **Gestion d'erreurs** : Messages d'erreur clairs et structurés
- **Tokens sécurisés** : Authentification JWT avec Supabase

### 📚 Documentation

- **API auto-documentée** : Documentation Swagger/OpenAPI
- **Interface interactive** : Test des endpoints directement
- **Exemples de requêtes** : Documentation complète des paramètres

## 🛠️ Technologies utilisées

### Backend

- **FastAPI** : Framework web moderne et rapide
- **Python 3.8+** : Langage de programmation
- **Supabase** : Backend-as-a-Service (Auth + Database)
- **Pydantic** : Validation et sérialisation des données
- **Uvicorn** : Serveur ASGI
- **python-dotenv** : Gestion des variables d'environnement

### Base de données

- **Supabase PostgreSQL** : Base de données relationnelle
- **Supabase Auth** : Système d'authentification
- **JSONB** : Stockage des données musées

## 🚀 Installation et démarrage

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Compte Supabase

### Installation

```bash
# Cloner le repository
git clone <https://github.com/Jerxmyy/workshop_musee>
cd backend

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows
venv\Scripts\activate
# Sur macOS/Linux
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

L'API sera accessible sur `http://localhost:8000`

### Scripts disponibles

```bash
# Développement
python main.py

# Documentation interactive
# Ouvrir http://localhost:8000/docs

# Documentation ReDoc
# Ouvrir http://localhost:8000/redoc
```

## 🔧 Configuration

### Variables d'environnement

Créez un fichier `.env` à la racine du dossier `backend` :

```env
# Configuration Supabase
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

# Configuration CORS (optionnel)
FRONTEND_URL=https://workshop-musee.vercel.app
PRODUCTION_URL=https://www.votre-site.com
```

### Configuration Supabase

1. Créez un projet sur [Supabase](https://supabase.com)
2. Récupérez l'URL du projet et les clés API
3. Configurez les variables d'environnement
4. Créez les tables nécessaires (voir section Base de données)

### Configuration CORS Dynamique

L'API s'adapte automatiquement à l'environnement (développement vs production) :

#### Variables CORS principales

- **`FRONTEND_URL`** : URL principale de votre frontend en production

  - Exemple : `https://workshop-musee.vercel.app`
  - Cette URL sera automatiquement ajoutée aux origines CORS autorisées

#### URLs par défaut (développement)

Les URLs suivantes sont toujours incluses pour le développement local :

- `http://localhost:5173` (Vite/Vue)

#### Configuration automatique

**En développement :**

```bash
# Aucune variable d'environnement nécessaire
# Les URLs localhost sont automatiquement incluses
python main.py
```

**En production :**

```bash
# Définir l'URL de production
export FRONTEND_URL="https://workshop-musee.vercel.app
python main.py
```

**Configuration avancée :**

```bash
# URL principale
export FRONTEND_URL="https://workshop-musee.vercel.app"

# URL alternative
export PRODUCTION_URL="https://workshop-musee-backend.vercel.app"

python main.py
```

### Personnalisation

- **CORS** : Modifier les variables d'environnement CORS
- **Port** : Changer le port dans `uvicorn.run()`
- **Logs** : Ajuster le niveau de log dans `uvicorn.run()`

## 📁 Structure du projet

```
backend/
├── main.py                          # Point d'entrée de l'API
├── requirements.txt                 # Dépendances Python
├── .env                            # Variables d'environnement (à créer)
├── supabase_config.py              # Configuration Supabase
├── supabase_auth_service.py        # Service d'authentification
├── supabase_favourites_service.py  # Service de gestion des favoris
├── supabase_auth_middleware.py     # Middleware d'authentification
└── README.md                       # Documentation
```

### Services

- **supabase_config.py** : Configuration et connexion à Supabase
- **supabase_auth_service.py** : Gestion de l'authentification (login, register, logout)
- **supabase_favourites_service.py** : Gestion des favoris (CRUD, recherche)
- **supabase_auth_middleware.py** : Middleware de vérification des tokens

## 🔌 API Endpoints

### Santé de l'API

- `GET /` - Informations générales de l'API
- `GET /health` - Vérification de l'état de l'API
- `GET /public/health` - Endpoint de santé publique

### Authentification

- `POST /register` - Inscription d'un nouvel utilisateur
- `POST /login` - Connexion d'un utilisateur
- `POST /logout` - Déconnexion d'un utilisateur
- `GET /profile` - Récupération du profil utilisateur

### Favoris

- `POST /favourites` - Ajouter un musée aux favoris
- `GET /favourites` - Récupérer tous les favoris de l'utilisateur
- `DELETE /favourites/{musee_id}` - Supprimer un musée des favoris
- `GET /favourites/{musee_id}/check` - Vérifier si un musée est en favori
- `GET /favourites/search` - Rechercher dans les favoris
- `GET /favourites/count` - Compter le nombre de favoris

### Documentation interactive

- `GET /docs` - Documentation Swagger UI
- `GET /redoc` - Documentation ReDoc

### Exemples de requêtes

#### Inscription

```bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "nom": "Dupont",
    "prenom": "Jean"
  }'
```

#### Connexion

```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

#### Ajouter un favori

```bash
curl -X POST http://localhost:8000/favourites \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "musee_id": "MUSEE_001",
    "musee_data": {
      "nom": "Musée du Louvre",
      "ville": "Paris",
      "region": "Île-de-France"
    }
  }'
```

## 🔐 Authentification

L'API utilise Supabase Auth pour la gestion de l'authentification :

### Inscription

```json
POST /register
{
  "email": "user@example.com",
  "password": "password123",
  "nom": "Dupont",
  "prenom": "Jean"
}
```

### Connexion

```json
POST /login
{
  "email": "user@example.com",
  "password": "password123"
}
```

### Utilisation des tokens

Les endpoints protégés nécessitent un token d'authentification dans l'en-tête :

```
Authorization: Bearer <access_token>
```

## 🗄 Base de données

### Tables Supabase

#### Table `users`

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR UNIQUE NOT NULL,
  nom VARCHAR NOT NULL,
  prenom VARCHAR NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

#### Table `favourites`

```sql
CREATE TABLE favourites (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  musee_id VARCHAR NOT NULL,
  musee_data JSONB NOT NULL,
  date_ajout TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, musee_id)
);
```

### Index recommandés

```sql
-- Index pour les recherches par utilisateur
CREATE INDEX idx_favourites_user_id ON favourites(user_id);

-- Index pour les recherches par musée
CREATE INDEX idx_favourites_musee_id ON favourites(musee_id);

-- Index pour les recherches textuelles
CREATE INDEX idx_favourites_search ON favourites USING gin(to_tsvector('french', musee_data->>'nom'));
```

## 🚀 Développement

### Démarrer le serveur de développement

```bash
# Activer l'environnement virtuel
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate     # Windows

# Démarrer le serveur
python main.py
```

Le serveur sera accessible sur `http://localhost:8000`

### Tests

```bash
# Tester l'API avec curl
curl http://localhost:8000/health

# Tester l'authentification
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","nom":"Test","prenom":"User"}'
```

### Logs

Les logs sont affichés dans la console avec différents niveaux :

- `INFO` - Informations générales
- `WARNING` - Avertissements
- `ERROR` - Erreurs

## 📦 Déploiement

### Variables d'environnement de production

```env
SUPABASE_URL=your_production_supabase_url
SUPABASE_ANON_KEY=your_production_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_production_service_role_key
FRONTEND_URL=https://workshop-musee.vercel.app
PRODUCTION_URL=https://workshop-musee-backend.vercel.app
```

## 📊 Post-mortem

### Défis rencontrés

1. **Intégration Supabase** : Configuration complexe des services Auth et Database
2. **Gestion des tokens** : Implémentation du middleware d'authentification
3. **Validation des données** : Mise en place de la validation Pydantic stricte
4. **Gestion des erreurs** : Centralisation et standardisation des messages d'erreur
5. **CORS dynamique** : Configuration flexible pour différents environnements

### Solutions apportées

1. **Services modulaires** : Séparation claire des responsabilités (auth, favoris, config)
2. **Middleware robuste** : Vérification automatique des tokens JWT
3. **Modèles Pydantic** : Validation stricte des données d'entrée et de sortie
4. **Gestion d'erreurs centralisée** : Handlers d'exception personnalisés

### Améliorations futures

- [ ] **Cache Redis** : Mise en cache des requêtes fréquentes
- [ ] **Rate limiting** : Limitation du nombre de requêtes par utilisateur
- [ ] **Logs structurés** : Implémentation de logs JSON pour le monitoring
- [ ] **Tests automatisés** : Suite de tests unitaires et d'intégration
- [ ] **Métriques** : Intégration de Prometheus pour le monitoring

## 📝 Licence

Ce projet est développé dans le cadre de ma formation à l'ESD Paris, lors d'un workshop sur l'utilisation des APIs Open Data du Ministère de la Culture.

## 👥 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Dupliquer le projet sur votre compte GitHub
2. Créer une branche feature
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📞 Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue sur GitHub ou à m'envoyer un mail à l'adresse suivante : jeremy.chambon@mail-esd.com
