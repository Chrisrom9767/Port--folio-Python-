# 📁 Portfolio — Gestionnaire de Projets

Application de gestion de portfolio développée en **Python** avec **Streamlit**.  
Projet Python 2 — AFI L2 IR — 2025/2026.

## 🚀 Démo en ligne

👉 **[Accéder à l'application](https://votre-app.streamlit.app)**

## 📋 Fonctionnalités

- **Consultation publique** : tout le monde peut voir les projets, statistiques, et rechercher
- **Administration** : seul l'admin peut ajouter, modifier et supprimer des projets
- **11 sections par projet** : infos générales, description, données, méthodologie, technologies, résultats, compétences, difficultés, solutions, perspectives, liens
- **Recherche globale** sur les 28 champs
- **Barre de complétion** par projet
- **Dashboard statistique** avec top technologies et compétences
- **Guide d'utilisation** intégré

## 🔐 Connexion admin

Identifiants par défaut : `admin` / `admin123`

## 🛠️ Lancer en local

```bash
pip install streamlit
streamlit run app.py
```

## 📂 Structure

```
├── app.py              # Application Streamlit (interface)
├── models.py           # Classe Projet (11 sections, 28 champs)
├── data_manager.py     # CRUD sur fichier JSON
├── auth_manager.py     # Authentification admin (SHA-256)
├── requirements.txt    # Dépendances
├── .streamlit/
│   └── config.toml     # Configuration thème
└── data/               # Données (auto-créé)
    ├── projets.json
    └── admin.json
```

## 🧑‍💻 Technologies

- Python 3
- Streamlit
- JSON (stockage)
- SHA-256 (hashage mot de passe)
