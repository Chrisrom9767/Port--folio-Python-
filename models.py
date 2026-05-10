"""
models.py — Classe Projet avec 11 sections détaillées (28 champs).
"""
from datetime import datetime


class Projet:
    """Modélise un projet du portfolio avec 11 sections."""

    SECTIONS = {
        "general": {
            "titre": "📋 Informations générales",
            "champs": {
                "libelle":     {"label": "Libellé du projet", "type": "text", "requis": True, "placeholder": "Ex : Détection de fraudes bancaires"},
                "type_projet": {"label": "Type de projet", "type": "select", "requis": True, "options": ["Académique", "Personnel", "Professionnel"]},
                "date_duree":  {"label": "Date / Durée", "type": "text", "requis": False, "placeholder": "Ex : Janvier 2025 – Mars 2025"},
                "contexte":    {"label": "Contexte", "type": "textarea", "requis": False, "placeholder": "Où et pourquoi ce projet a été réalisé"},
            }
        },
        "description": {
            "titre": "📝 Description du projet",
            "champs": {
                "problematique":    {"label": "Problématique", "type": "textarea", "requis": True, "placeholder": "Quel problème cherchez-vous à résoudre ?"},
                "objectif":         {"label": "Objectif", "type": "textarea", "requis": True, "placeholder": "Ce que le projet doit accomplir"},
                "description_detail": {"label": "Description détaillée", "type": "textarea", "requis": False, "placeholder": "Explication globale du fonctionnement"},
            }
        },
        "donnees": {
            "titre": "🗄️ Données utilisées",
            "champs": {
                "source_donnees": {"label": "Source des données", "type": "text", "requis": False, "placeholder": "Kaggle, API, entreprise..."},
                "type_donnees":   {"label": "Type de données", "type": "text", "requis": False, "placeholder": "Images, texte, tabulaire..."},
                "taille_dataset": {"label": "Taille du dataset", "type": "text", "requis": False, "placeholder": "50 000 lignes, 2 Go..."},
                "pretraitements": {"label": "Prétraitements effectués", "type": "textarea", "requis": False, "placeholder": "Nettoyage, transformation..."},
            }
        },
        "methodologie": {
            "titre": "🔬 Méthodologie",
            "champs": {
                "approche":    {"label": "Approche utilisée", "type": "text", "requis": False, "placeholder": "Machine Learning, Deep Learning, NLP..."},
                "etapes":      {"label": "Étapes du projet", "type": "textarea", "requis": False, "placeholder": "EDA, Feature engineering, Modélisation..."},
                "algorithmes": {"label": "Algorithmes utilisés", "type": "text", "requis": False, "placeholder": "Random Forest, CNN, LSTM..."},
            }
        },
        "technologies": {
            "titre": "💻 Technologies utilisées",
            "champs": {
                "langages":   {"label": "Langages", "type": "text", "requis": False, "placeholder": "Python, R, JavaScript..."},
                "librairies": {"label": "Librairies", "type": "text", "requis": False, "placeholder": "Pandas, Scikit-learn, TensorFlow..."},
                "outils":     {"label": "Outils", "type": "text", "requis": False, "placeholder": "Git, Docker, AWS, Kaggle..."},
                "frameworks": {"label": "Frameworks", "type": "text", "requis": False, "placeholder": "Flask, FastAPI, Django..."},
            }
        },
        "resultats": {
            "titre": "📊 Résultats obtenus",
            "champs": {
                "performances":      {"label": "Performances du modèle", "type": "textarea", "requis": False, "placeholder": "Accuracy, précision, recall..."},
                "visualisations":    {"label": "Visualisations", "type": "textarea", "requis": False, "placeholder": "Graphes, dashboards, courbes..."},
                "resultats_concrets": {"label": "Résultats concrets", "type": "textarea", "requis": False, "placeholder": "Amélioration de X%..."},
            }
        },
        "competences": {
            "titre": "🎯 Compétences acquises",
            "champs": {
                "competences": {"label": "Compétences", "type": "textarea", "requis": False, "placeholder": "Data preprocessing, Modélisation ML/DL..."},
            }
        },
        "difficultes": {
            "titre": "⚠️ Difficultés rencontrées",
            "champs": {
                "difficultes": {"label": "Difficultés", "type": "textarea", "requis": False, "placeholder": "Overfitting, données manquantes..."},
            }
        },
        "solutions": {
            "titre": "✅ Solutions apportées",
            "champs": {
                "solutions": {"label": "Solutions", "type": "textarea", "requis": False, "placeholder": "Data augmentation, tuning..."},
            }
        },
        "perspectives": {
            "titre": "🚀 Perspectives / Améliorations",
            "champs": {
                "perspectives": {"label": "Perspectives", "type": "textarea", "requis": False, "placeholder": "Déploiement, ajout d'un RAG..."},
            }
        },
        "liens": {
            "titre": "🔗 Liens du projet",
            "champs": {
                "lien_github":  {"label": "Lien GitHub", "type": "url", "requis": False, "placeholder": "https://github.com/..."},
                "lien_demo":    {"label": "Lien Démo", "type": "url", "requis": False, "placeholder": "https://..."},
                "lien_rapport": {"label": "Lien Rapport", "type": "url", "requis": False, "placeholder": "https://..."},
            }
        },
    }

    TOUS_CHAMPS = []
    for _s in SECTIONS.values():
        TOUS_CHAMPS.extend(_s["champs"].keys())

    def __init__(self, **kwargs):
        for c in self.TOUS_CHAMPS:
            setattr(self, c, kwargs.get(c, ""))
        self.date_ajout = kwargs.get("date_ajout", "") or datetime.now().strftime("%d/%m/%Y %H:%M")
        self.auteur = kwargs.get("auteur", "")

    def to_dict(self) -> dict:
        d = {c: getattr(self, c, "") for c in self.TOUS_CHAMPS}
        d["date_ajout"] = self.date_ajout
        d["auteur"] = self.auteur
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "Projet":
        return cls(**data)

    def get_all_tech_tags(self) -> list:
        tags = []
        for f in ["langages", "librairies", "outils", "frameworks"]:
            v = getattr(self, f, "")
            if v:
                tags.extend([t.strip() for t in v.split(",") if t.strip()])
        return tags

    def get_competences_tags(self) -> list:
        v = getattr(self, "competences", "")
        return [c.strip() for c in v.split(",") if c.strip()] if v else []

    def completion_pct(self) -> int:
        r = sum(1 for c in self.TOUS_CHAMPS if getattr(self, c, ""))
        return int((r / len(self.TOUS_CHAMPS)) * 100)
