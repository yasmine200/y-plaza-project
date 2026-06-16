# 🏠 Y-Plaza — Plateforme Immobilière

Site web qui permet aux agences Y-Plaza de gérer la vente et l'achat de biens
immobiliers (maisons, appartements…) au même endroit.

## 1. Comment c'est construit

Le code est organisé en **MVC** (Modèle-Vue-Contrôleur) : les données, l'affichage
et la logique sont séparés.

- **Backend :** Flask (Python) — gère les pages, les connexions et les actions.
- **Base de données :** SQLite3 — stocke les agences, les utilisateurs et les biens.
- **Frontend :** Bootstrap 5 — affichage qui s'adapte au téléphone, tablette et PC.

```
y-plaza-project/
├── app.py                 # Routes Flask (contrôleur)
├── init_db.py             # Création + alimentation de la base
├── schema_v2.sql          # Schéma SQL de référence
├── analyse_donnees.py     # Analyse de données (estimation de prix)
├── requirements.txt       # Dépendances Python
├── config/database.py     # Connexion à la base SQLite
├── models/                # Données (classe d'un bien + accès à la base)
│   ├── bien_immobilier.py
│   └── dao.py
├── templates/             # Vues (HTML / Jinja2)
└── static/uploads/        # Images des biens
```

## 2. Ce qu'on peut faire (CRUD)

Gérer les annonces de biens immobiliers :

- **Ajouter** un bien avec une photo (seuls les formats d'image sont acceptés).
- **Voir** les annonces (page d'accueil + page de détail).
- **Modifier** les infos d'un bien et changer sa photo.
- **Supprimer** un bien (réservé au pôle Commercial, voir la matrice des droits).

## 3. Analyse de données & API

- **Analyse de données :** le script `analyse_donnees.py` (Pandas + scikit-learn)
  lit la base `y_plaza.db` et estime un prix à partir de la surface.
- **API :** l'adresse `GET /api/biens` renvoie la liste des biens en JSON (utile
  pour brancher une autre application dessus).

## 4. Sécurité & accessibilité

- Connexion par la table `utilisateurs` avec des **mots de passe chiffrés** (Werkzeug).
- Chaque page sensible vérifie le rôle de l'utilisateur (`@role_requis`).
- Les requêtes SQL utilisent des **paramètres** (empêche les injections SQL).
- À l'upload, seuls les fichiers image sont acceptés (`png, jpg, jpeg, webp, gif`).
- La clé secrète Flask vient d'une variable d'environnement `YPLAZA_SECRET_KEY`.
- Attributs ARIA pour les lecteurs d'écran (accessibilité).

## 5. Qui a le droit de faire quoi

Il y a **5 rôles**, un par pôle de l'entreprise. Comme demandé dans la matrice
des droits, seul le pôle **Commercial** peut ajouter, modifier ou supprimer des
biens. Les autres pôles peuvent seulement **regarder**.

| Pôle / Rôle | Email | Mot de passe | Droits sur les biens |
|-------------|-------|--------------|----------------------|
| Commercial (siège) | `commercial@yplaza.fr` | `comm123` | Lecture + **Écriture** |
| Commercial (Marseille) | `commercial.marseille@yplaza.fr` | `comm123` | Lecture + **Écriture** |
| Direction | `direction@yplaza.fr` | `dir123` | Lecture seule |
| Communication & Marketing | `marketing@yplaza.fr` | `mkt123` | Lecture seule |
| Administratif - RH - Juridique | `rh@yplaza.fr` | `rh123` | Lecture seule |
| IT et Support | `it@yplaza.fr` | `it123` | Lecture seule |

## 6. Installation

```bash
# 1. Cloner le dépôt
git clone <url-du-depot>
cd y-plaza-project

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Créer et alimenter la base de données
python init_db.py

# 4. Lancer l'application
python app.py
```

Le site est ensuite accessible dans le navigateur sur http://127.0.0.1:5000.

---
*Développeur Backend : Yasmine Fakir — Projet UF INFRA & DEV, Ynov Informatique.*