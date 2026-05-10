"""
data_manager.py — CRUD sur fichier JSON.
"""
import json, os
from collections import Counter
from models import Projet


class DataManager:
    def __init__(self, fichier="data/projets.json"):
        self.fichier = fichier
        os.makedirs(os.path.dirname(fichier), exist_ok=True)
        if not os.path.exists(self.fichier):
            self._ecrire([])

    def _lire(self):
        try:
            with open(self.fichier, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _ecrire(self, d):
        with open(self.fichier, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=4)

    def ajouter_projet(self, p):
        d = self._lire()
        for x in d:
            if x.get("libelle", "").lower() == p.libelle.lower():
                return False
        d.append(p.to_dict())
        self._ecrire(d)
        return True

    def obtenir_projet(self, libelle):
        for p in self._lire():
            if p.get("libelle", "").lower() == libelle.lower():
                return Projet.from_dict(p)
        return None

    def supprimer_projet(self, libelle):
        d = self._lire()
        n = [p for p in d if p.get("libelle", "").lower() != libelle.lower()]
        if len(n) == len(d):
            return False
        self._ecrire(n)
        return True

    def modifier_projet(self, ancien, nouveau):
        d = self._lire()
        for i, p in enumerate(d):
            if p.get("libelle", "").lower() == ancien.lower():
                nouveau.date_ajout = p.get("date_ajout", nouveau.date_ajout)
                d[i] = nouveau.to_dict()
                self._ecrire(d)
                return True
        return False

    def rechercher(self, mot):
        m = mot.lower()
        return [Projet.from_dict(p) for p in self._lire()
                if any(m in str(v).lower() for v in p.values())]

    def obtenir_tous(self):
        return [Projet.from_dict(p) for p in self._lire()]

    def nombre_projets(self):
        return len(self._lire())

    def statistiques(self):
        projets = self.obtenir_tous()
        techs, comps, types = [], [], []
        for p in projets:
            techs.extend(p.get_all_tech_tags())
            comps.extend(p.get_competences_tags())
            if p.type_projet:
                types.append(p.type_projet)
        return {
            "total": len(projets),
            "technologies_uniques": len(set(techs)),
            "competences_uniques": len(set(comps)),
            "top_technologies": Counter(techs).most_common(6),
            "top_competences": Counter(comps).most_common(6),
            "types": Counter(types).most_common(),
            "completion_moyenne": int(sum(p.completion_pct() for p in projets) / max(len(projets), 1)),
        }
