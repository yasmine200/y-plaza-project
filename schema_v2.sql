-- ============================================================
-- Schéma de la base Y-Plaza
-- Ce fichier documente EXACTEMENT les tables créées par init_db.py
-- et utilisées par l'application (source unique de vérité).
-- ============================================================

PRAGMA foreign_keys = ON;

-- 1. Agences du réseau (siège d'Aix-en-Provence + agences)
CREATE TABLE agence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    ville TEXT NOT NULL
);

-- 2. Staff interne Y-Plaza (mot de passe stocké HASHÉ)
-- Le rôle correspond à l'un des 5 pôles de la matrice des droits.
CREATE TABLE utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    mot_de_passe_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN (
        'Direction',
        'Commercial',
        'Communication & Marketing',
        'Administratif - RH - Juridique',
        'IT et Support'
    )),
    agence_id INTEGER,
    FOREIGN KEY (agence_id) REFERENCES agence(id)
);

-- 3. Biens immobiliers (cœur du métier)
CREATE TABLE biens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    description TEXT,
    prix REAL NOT NULL,
    surface REAL NOT NULL,
    ville TEXT NOT NULL,
    statut TEXT NOT NULL DEFAULT 'À vendre',
    image_url TEXT,
    agent_id INTEGER,
    FOREIGN KEY (agent_id) REFERENCES utilisateurs(id)
);
