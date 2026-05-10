"""
app.py — Application Portfolio Streamlit
Déployable sur Streamlit Cloud via GitHub.
"""

import streamlit as st
from models import Projet
from data_manager import DataManager
from auth_manager import AuthManager

# ══════════════════════════════════════════
#  CONFIG & INIT
# ══════════════════════════════════════════

st.set_page_config(
    page_title="Portfolio — Projets",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS personnalisé
st.markdown("""
<style>
    /* Tags */
    .tag { display:inline-block; font-size:0.72rem; font-weight:600; padding:3px 10px;
           border-radius:14px; background:rgba(124,108,240,0.15); color:#a5b4fc; margin:2px 3px 2px 0; }
    .tag-green { background:rgba(16,185,129,0.12); color:#34d399; }

    /* Type badges */
    .tbadge { display:inline-block; font-size:0.68rem; font-weight:700; padding:2px 9px;
              border-radius:10px; text-transform:uppercase; letter-spacing:0.03em; }
    .t-acad { background:rgba(124,108,240,0.15); color:#a5b4fc; }
    .t-perso { background:rgba(16,185,129,0.12); color:#34d399; }
    .t-pro { background:rgba(245,158,11,0.12); color:#fbbf24; }

    /* Completion bar */
    .cbar { width:100%; height:5px; background:#27272a; border-radius:3px; overflow:hidden; margin:6px 0; }
    .cfill { height:100%; border-radius:3px; }

    /* Section headers */
    .sec-h { font-size:1.1rem; font-weight:700; color:#7c6cf0; margin:16px 0 8px 0;
             padding-bottom:6px; border-bottom:1px solid #27272a; }

    /* Detail label */
    .dlabel { font-size:0.7rem; font-weight:700; color:#71717a; text-transform:uppercase;
              letter-spacing:0.07em; margin-bottom:2px; }

    /* Card */
    .pcard { background:#18181b; border:1px solid #27272a; border-radius:10px; padding:18px;
             margin-bottom:12px; transition:border-color 0.2s; }
    .pcard:hover { border-color:#3f3f46; }

    /* Hide default Streamlit footer */
    footer { visibility:hidden; }
    .stDeployButton { display:none; }

    /* Sidebar spacing */
    section[data-testid="stSidebar"] > div { padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_managers():
    return DataManager(), AuthManager()


dm, am = get_managers()

# ── Session state defaults ──
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "page" not in st.session_state:
    st.session_state.page = "accueil"
if "detail_projet" not in st.session_state:
    st.session_state.detail_projet = None
if "edit_projet" not in st.session_state:
    st.session_state.edit_projet = None


# ══════════════════════════════════════════
#  DONNÉES DÉMO (15 projets génie logiciel)
# ══════════════════════════════════════════

def creer_demos():
    if dm.nombre_projets() > 0:
        return
    from demos import PROJETS_DEMO
    for d in PROJETS_DEMO:
        dm.ajouter_projet(Projet(**d))


creer_demos()


# ══════════════════════════════════════════
#  HELPERS UI
# ══════════════════════════════════════════

def nav(page, **kwargs):
    st.session_state.page = page
    for k, v in kwargs.items():
        st.session_state[k] = v


def render_tags(items, css_class="tag"):
    if not items:
        return ""
    return " ".join(f'<span class="{css_class}">{t}</span>' for t in items)


def type_badge(tp):
    cls = {"Académique": "t-acad", "Personnel": "t-perso", "Professionnel": "t-pro"}.get(tp, "t-acad")
    return f'<span class="tbadge {cls}">{tp}</span>' if tp else ""


def completion_bar(pct):
    color = "#ef4444" if pct < 40 else "#f59e0b" if pct < 70 else "#10b981"
    return f'<div class="cbar"><div class="cfill" style="width:{pct}%;background:{color};"></div></div>'


# ══════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════

with st.sidebar:
    st.markdown("## 📁 Portfolio")
    st.caption("Gestionnaire de Projets")
    st.divider()

    if st.button("🏠 Accueil", use_container_width=True, type="secondary"):
        nav("accueil")
    if st.button("📋 Projets", use_container_width=True, type="secondary"):
        nav("projets")
    if st.button("🔍 Rechercher", use_container_width=True, type="secondary"):
        nav("recherche")
    if st.button("📖 Guide", use_container_width=True, type="secondary"):
        nav("guide")

    if st.session_state.is_admin:
        st.divider()
        st.caption("ADMINISTRATION")
        if st.button("➕ Ajouter un projet", use_container_width=True, type="secondary"):
            nav("ajouter")
        if st.button("🔑 Mon compte", use_container_width=True, type="secondary"):
            nav("profil")

    st.divider()

    if st.session_state.is_admin:
        st.success("🛡️ Admin connecté")
        if st.button("🚪 Déconnexion", use_container_width=True):
            st.session_state.is_admin = False
            nav("accueil")
            st.rerun()
    else:
        if st.button("🔐 Connexion Admin", use_container_width=True, type="primary"):
            nav("login")


# ══════════════════════════════════════════
#  PAGES
# ══════════════════════════════════════════

page = st.session_state.page

# ── LOGIN ──
if page == "login":
    st.title("🔐 Connexion Administrateur")
    st.caption("Connectez-vous pour gérer les projets")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Nom d'utilisateur", placeholder="admin")
            password = st.text_input("Mot de passe", type="password", placeholder="••••••")
            submitted = st.form_submit_button("Se connecter", use_container_width=True, type="primary")

            if submitted:
                if am.connecter(username.strip(), password.strip()):
                    st.session_state.is_admin = True
                    nav("accueil")
                    st.rerun()
                else:
                    st.error("Identifiants incorrects.")

        st.info("Identifiants par défaut : **admin** / **admin123**")
        if st.button("← Retour au portfolio"):
            nav("accueil")
            st.rerun()


# ── ACCUEIL ──
elif page == "accueil":
    st.title("Portfolio de Projets")
    if st.session_state.is_admin:
        st.caption("Tableau de bord administrateur")
    else:
        st.caption("Consultez les projets réalisés")

    stats = dm.statistiques()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Projets", stats["total"])
    c2.metric("Technologies", stats["technologies_uniques"])
    c3.metric("Compétences", stats["competences_uniques"])
    c4.metric("Complétion moy.", f"{stats['completion_moyenne']}%")

    col_a, col_b = st.columns(2)
    with col_a:
        if stats["top_technologies"]:
            st.markdown("#### 🔥 Top technologies")
            tags_html = render_tags([f"{t} ({c})" for t, c in stats["top_technologies"]])
            st.markdown(tags_html, unsafe_allow_html=True)

    with col_b:
        if stats["top_competences"]:
            st.markdown("#### 🎯 Top compétences")
            tags_html = render_tags([f"{c} ({n})" for c, n in stats["top_competences"]], "tag tag-green")
            st.markdown(tags_html, unsafe_allow_html=True)

    if stats["types"]:
        st.markdown("#### 📂 Par type")
        type_html = " ".join(type_badge(f"{t} ({c})") for t, c in stats["types"])
        st.markdown(type_html, unsafe_allow_html=True)

    if stats["total"] == 0:
        st.info("Aucun projet publié.")
        if st.session_state.is_admin:
            if st.button("➕ Ajouter un projet"):
                nav("ajouter")
                st.rerun()


# ── PROJETS ──
elif page == "projets":
    st.title("📋 Projets")
    projets = dm.obtenir_tous()
    st.caption(f"{len(projets)} projet(s) enregistré(s)")

    if st.session_state.is_admin:
        if st.button("➕ Nouveau projet", type="primary"):
            nav("ajouter")
            st.rerun()

    if not projets:
        st.info("Aucun projet enregistré.")
    else:
        for p in projets:
            with st.container(border=True):
                col_t, col_m = st.columns([3, 1])
                with col_t:
                    st.markdown(f"**{p.libelle}**")
                with col_m:
                    badge = type_badge(p.type_projet)
                    st.markdown(f"{badge} <span style='color:#71717a;font-size:0.75rem;'>{p.date_ajout}</span>",
                                unsafe_allow_html=True)

                if p.problematique:
                    st.caption(p.problematique[:150] + ("..." if len(p.problematique) > 150 else ""))

                techs = p.get_all_tech_tags()
                if techs:
                    st.markdown(render_tags(techs[:8]), unsafe_allow_html=True)

                pct = p.completion_pct()
                st.markdown(f"<span style='font-size:0.7rem;color:#71717a;'>Complétion {pct}%</span>{completion_bar(pct)}",
                            unsafe_allow_html=True)

                btn_cols = st.columns([1, 1, 1, 3])
                with btn_cols[0]:
                    if st.button("👁 Détails", key=f"det_{p.libelle}"):
                        nav("details", detail_projet=p.libelle)
                        st.rerun()
                if st.session_state.is_admin:
                    with btn_cols[1]:
                        if st.button("✏️ Modifier", key=f"mod_{p.libelle}"):
                            nav("modifier", edit_projet=p.libelle)
                            st.rerun()
                    with btn_cols[2]:
                        if st.button("🗑 Supprimer", key=f"del_{p.libelle}"):
                            nav("confirmer_sup", detail_projet=p.libelle)
                            st.rerun()


# ── CONFIRMER SUPPRESSION ──
elif page == "confirmer_sup":
    lib = st.session_state.detail_projet
    st.warning(f"⚠️ Voulez-vous vraiment supprimer le projet **« {lib} »** ? Cette action est irréversible.")
    c1, c2, _ = st.columns([1, 1, 4])
    with c1:
        if st.button("Oui, supprimer", type="primary"):
            dm.supprimer_projet(lib)
            st.toast(f"Projet « {lib} » supprimé.", icon="🗑️")
            nav("projets")
            st.rerun()
    with c2:
        if st.button("Annuler"):
            nav("projets")
            st.rerun()


# ── DÉTAILS ──
elif page == "details":
    lib = st.session_state.detail_projet
    projet = dm.obtenir_projet(lib)
    if not projet:
        st.error("Projet non trouvé.")
        if st.button("← Retour"):
            nav("projets")
            st.rerun()
    else:
        # Header
        st.title(f"📌 {projet.libelle}")
        meta_parts = []
        if projet.type_projet:
            meta_parts.append(type_badge(projet.type_projet))
        meta_parts.append(f"<span style='color:#71717a;font-size:0.82rem;'>{projet.date_ajout}</span>")
        if projet.auteur:
            meta_parts.append(f"<span style='color:#71717a;font-size:0.82rem;'>par {projet.auteur}</span>")
        st.markdown(" · ".join(meta_parts), unsafe_allow_html=True)

        # Completion
        pct = projet.completion_pct()
        st.markdown(f"Complétion **{pct}%** {completion_bar(pct)}", unsafe_allow_html=True)

        # Admin actions
        if st.session_state.is_admin:
            ac1, ac2, _ = st.columns([1, 1, 4])
            with ac1:
                if st.button("✏️ Modifier"):
                    nav("modifier", edit_projet=lib)
                    st.rerun()
            with ac2:
                if st.button("🗑 Supprimer"):
                    nav("confirmer_sup", detail_projet=lib)
                    st.rerun()

        # Sections
        pdict = projet.to_dict()
        for sec_key, section in Projet.SECTIONS.items():
            with st.expander(section["titre"], expanded=True):
                for ck, ch in section["champs"].items():
                    val = pdict.get(ck, "")
                    st.markdown(f'<div class="dlabel">{ch["label"]}</div>', unsafe_allow_html=True)
                    if val:
                        if ch["type"] == "url":
                            st.markdown(f"[{val}]({val})")
                        elif ck in ["langages", "librairies", "outils", "frameworks"]:
                            st.markdown(render_tags([t.strip() for t in val.split(",") if t.strip()]),
                                        unsafe_allow_html=True)
                        elif ck == "competences":
                            st.markdown(render_tags([c.strip() for c in val.split(",") if c.strip()], "tag tag-green"),
                                        unsafe_allow_html=True)
                        else:
                            st.write(val)
                    else:
                        st.caption("_Non renseigné_")

        if st.button("← Retour à la liste"):
            nav("projets")
            st.rerun()


# ── AJOUTER ──
elif page == "ajouter":
    if not st.session_state.is_admin:
        st.warning("Accès réservé à l'administrateur.")
        if st.button("🔐 Se connecter"):
            nav("login")
            st.rerun()
    else:
        st.title("➕ Ajouter un projet")
        st.caption("Cliquez sur chaque section pour la déplier")

        form_data = {}
        for sec_key, section in Projet.SECTIONS.items():
            with st.expander(section["titre"], expanded=(sec_key in ["general", "description"])):
                for ck, ch in section["champs"].items():
                    label = ch["label"] + (" *" if ch.get("requis") else "")
                    if ch["type"] == "textarea":
                        form_data[ck] = st.text_area(label, placeholder=ch.get("placeholder", ""),
                                                      key=f"add_{ck}")
                    elif ch["type"] == "select":
                        opts = [""] + ch["options"]
                        form_data[ck] = st.selectbox(label, opts, key=f"add_{ck}")
                    else:
                        form_data[ck] = st.text_input(label, placeholder=ch.get("placeholder", ""),
                                                       key=f"add_{ck}")

        c1, c2, _ = st.columns([1, 1, 4])
        with c1:
            if st.button("✅ Ajouter le projet", type="primary"):
                # Validation
                manquants = []
                for sec in Projet.SECTIONS.values():
                    for ck, ch in sec["champs"].items():
                        if ch.get("requis") and not form_data.get(ck, "").strip():
                            manquants.append(ch["label"])
                if manquants:
                    st.error(f"Champs obligatoires manquants : {', '.join(manquants)}")
                else:
                    clean = {k: v.strip() for k, v in form_data.items()}
                    clean["auteur"] = "admin"
                    if dm.ajouter_projet(Projet(**clean)):
                        st.toast("Projet ajouté !", icon="✅")
                        nav("projets")
                        st.rerun()
                    else:
                        st.error("Un projet avec ce libellé existe déjà.")
        with c2:
            if st.button("Annuler"):
                nav("projets")
                st.rerun()


# ── MODIFIER ──
elif page == "modifier":
    if not st.session_state.is_admin:
        st.warning("Accès réservé à l'administrateur.")
    else:
        lib = st.session_state.edit_projet
        projet = dm.obtenir_projet(lib)
        if not projet:
            st.error("Projet non trouvé.")
        else:
            st.title(f"✏️ Modifier : {projet.libelle}")
            pdict = projet.to_dict()

            form_data = {}
            for sec_key, section in Projet.SECTIONS.items():
                with st.expander(section["titre"], expanded=True):
                    for ck, ch in section["champs"].items():
                        label = ch["label"] + (" *" if ch.get("requis") else "")
                        current = pdict.get(ck, "")
                        if ch["type"] == "textarea":
                            form_data[ck] = st.text_area(label, value=current, key=f"edit_{ck}")
                        elif ch["type"] == "select":
                            opts = [""] + ch["options"]
                            idx = opts.index(current) if current in opts else 0
                            form_data[ck] = st.selectbox(label, opts, index=idx, key=f"edit_{ck}")
                        else:
                            form_data[ck] = st.text_input(label, value=current, key=f"edit_{ck}")

            c1, c2, _ = st.columns([1, 1, 4])
            with c1:
                if st.button("💾 Enregistrer", type="primary"):
                    manquants = []
                    for sec in Projet.SECTIONS.values():
                        for ck, ch in sec["champs"].items():
                            if ch.get("requis") and not form_data.get(ck, "").strip():
                                manquants.append(ch["label"])
                    if manquants:
                        st.error(f"Champs obligatoires manquants : {', '.join(manquants)}")
                    else:
                        clean = {k: v.strip() for k, v in form_data.items()}
                        clean["auteur"] = projet.auteur
                        nouveau = Projet(**clean)
                        if dm.modifier_projet(lib, nouveau):
                            st.toast("Projet modifié !", icon="💾")
                            nav("details", detail_projet=clean["libelle"])
                            st.rerun()
                        else:
                            st.error("Erreur lors de la modification.")
            with c2:
                if st.button("Annuler"):
                    nav("details", detail_projet=lib)
                    st.rerun()


# ── RECHERCHE ──
elif page == "recherche":
    st.title("🔍 Rechercher")
    st.caption("Recherche dans tous les champs : titre, technologies, algorithmes, compétences, résultats...")

    q = st.text_input("Mot-clé", placeholder="Ex : Python, CNN, overfitting...", label_visibility="collapsed")

    if q.strip():
        resultats = dm.rechercher(q.strip())
        if resultats:
            st.success(f"{len(resultats)} résultat(s) pour « {q} »")
            for p in resultats:
                with st.container(border=True):
                    st.markdown(f"**{p.libelle}** {type_badge(p.type_projet)}", unsafe_allow_html=True)
                    if p.problematique:
                        st.caption(p.problematique[:120])
                    techs = p.get_all_tech_tags()
                    if techs:
                        st.markdown(render_tags(techs[:6]), unsafe_allow_html=True)
                    if st.button("Voir les détails", key=f"sr_{p.libelle}"):
                        nav("details", detail_projet=p.libelle)
                        st.rerun()
        else:
            st.info(f"Aucun résultat pour « {q} ».")
    else:
        st.info("Tapez un mot-clé pour lancer la recherche.")


# ── GUIDE ──
elif page == "guide":
    st.title("📖 Guide d'utilisation")

    with st.expander("🚀 Présentation", expanded=True):
        st.write("Application de gestion de portfolio. Tout le monde peut consulter les projets. "
                 "Seul l'administrateur peut ajouter, modifier et supprimer des projets.")

    with st.expander("👥 Droits d'accès"):
        st.markdown("""
| Fonctionnalité | Visiteur | Admin |
|---|---|---|
| Accueil et statistiques | ✅ | ✅ |
| Liste et détails des projets | ✅ | ✅ |
| Recherche | ✅ | ✅ |
| Ajouter un projet | ❌ | ✅ |
| Modifier / Supprimer | ❌ | ✅ |
| Changer le mot de passe | ❌ | ✅ |
""")

    with st.expander("📌 Structure d'un projet (11 sections, 28 champs)"):
        st.markdown("""
| # | Section | Contenu |
|---|---|---|
| 1 | 📋 Informations générales | Libellé, type, date/durée, contexte |
| 2 | 📝 Description | Problématique, objectif, description détaillée |
| 3 | 🗄️ Données utilisées | Source, type, taille, prétraitements |
| 4 | 🔬 Méthodologie | Approche, étapes, algorithmes |
| 5 | 💻 Technologies | Langages, librairies, outils, frameworks |
| 6 | 📊 Résultats | Performances, visualisations, résultats concrets |
| 7 | 🎯 Compétences | Compétences acquises |
| 8 | ⚠️ Difficultés | Problèmes et limitations |
| 9 | ✅ Solutions | Techniques de résolution |
| 10 | 🚀 Perspectives | Améliorations futures |
| 11 | 🔗 Liens | GitHub, démo, rapport |
""")

    with st.expander("📋 Utilisation du formulaire"):
        st.write("Le formulaire d'ajout/modification est organisé en sections dépliables. "
                 "Seuls 4 champs sont obligatoires : libellé, type, problématique et objectif. "
                 "La barre de complétion indique le % de champs remplis.")

    with st.expander("🔐 Connexion admin"):
        st.write("Cliquez sur « Connexion Admin » dans le menu. "
                 "Identifiants par défaut : `admin` / `admin123`. "
                 "Changez le mot de passe via « Mon compte ».")


# ── PROFIL ──
elif page == "profil":
    if not st.session_state.is_admin:
        st.warning("Accès réservé à l'administrateur.")
    else:
        st.title("👤 Mon compte")

        st.markdown("**Identifiant :** admin")
        st.markdown("**Rôle :** 🛡️ Administrateur")

        st.divider()
        st.subheader("🔑 Changer le mot de passe")

        with st.form("mdp_form"):
            ancien = st.text_input("Ancien mot de passe", type="password")
            nouveau = st.text_input("Nouveau mot de passe", type="password")
            confirmer = st.text_input("Confirmer", type="password")
            submitted = st.form_submit_button("Enregistrer")

            if submitted:
                if nouveau != confirmer:
                    st.error("Les mots de passe ne correspondent pas.")
                else:
                    ok, msg = am.changer_mot_de_passe(ancien.strip(), nouveau.strip())
                    if ok:
                        st.success(msg)
                    else:
                        st.error(msg)
