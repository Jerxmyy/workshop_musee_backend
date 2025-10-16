# Configuration CORS Dynamique

## Vue d'ensemble

La configuration CORS de l'API MuseoFile s'adapte automatiquement à l'environnement (développement vs production) en utilisant des variables d'environnement.

## Variables d'environnement

### Variables principales

- **`FRONTEND_URL`** : URL principale de votre frontend en production

  - Exemple : `https://votre-site.com`
  - Cette URL sera automatiquement ajoutée aux origines CORS autorisées

- **`PRODUCTION_URL`** : URL de production alternative (optionnel)

  - Exemple : `https://www.votre-site.com`
  - Permet d'ajouter une URL de production supplémentaire

- **`CORS_ORIGINS`** : URLs CORS supplémentaires (optionnel)
  - Format : URLs séparées par des virgules
  - Exemple : `https://staging.votre-site.com,https://admin.votre-site.com`

### URLs par défaut (développement)

Les URLs suivantes sont toujours incluses pour le développement local :

- `http://localhost:5173` (Vite/Vue)
- `http://localhost:3000` (React/Next.js)

## Configuration automatique

### En développement

```bash
# Aucune variable d'environnement nécessaire
# Les URLs localhost sont automatiquement incluses
python main.py
```

### En production

```bash
# Définir l'URL de production
export FRONTEND_URL="https://votre-site.com"
python main.py
```

### Configuration avancée

```bash
# URL principale
export FRONTEND_URL="https://votre-site.com"

# URL alternative
export PRODUCTION_URL="https://www.votre-site.com"

# URLs supplémentaires
export CORS_ORIGINS="https://staging.votre-site.com,https://admin.votre-site.com"

python main.py
```

## Logging

Au démarrage, l'API affiche :

- Les URLs de développement configurées
- Les URLs détectées depuis les variables d'environnement
- Le total des origines CORS autorisées

Exemple de sortie :

```
🔒 Configuration CORS:
   📍 URLs de développement: ['http://localhost:5173', 'http://localhost:3000']
   🌍 URLs d'environnement: ['https://votre-site.com']
   ✅ Total des origines autorisées: 3
```

## Avantages

- ✅ Configuration automatique selon l'environnement
- ✅ URLs de développement toujours disponibles
- ✅ Facile à déployer en production
- ✅ Support de multiples URLs
- ✅ Logging clair de la configuration
- ✅ Gestion des erreurs gracieuse
- ✅ Suppression automatique des doublons
