"""
auth_manager.py — Authentification admin.
"""
import json, hashlib, os


class AuthManager:
    def __init__(self, fichier="data/admin.json"):
        self.fichier = fichier
        os.makedirs(os.path.dirname(fichier), exist_ok=True)
        if not os.path.exists(self.fichier):
            data = {"username": "admin", "password_hash": self._hasher("admin123")}
            with open(self.fichier, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

    @staticmethod
    def _hasher(mdp):
        return hashlib.sha256(mdp.encode()).hexdigest()

    def _lire(self):
        try:
            with open(self.fichier, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}

    def connecter(self, username, mdp):
        a = self._lire()
        return username == a.get("username") and self._hasher(mdp) == a.get("password_hash")

    def changer_mot_de_passe(self, ancien, nouveau):
        if len(nouveau) < 4:
            return False, "Le mot de passe doit avoir au moins 4 caractères."
        a = self._lire()
        if self._hasher(ancien) != a.get("password_hash"):
            return False, "Ancien mot de passe incorrect."
        a["password_hash"] = self._hasher(nouveau)
        with open(self.fichier, "w", encoding="utf-8") as f:
            json.dump(a, f, indent=4)
        return True, "Mot de passe modifié avec succès !"
