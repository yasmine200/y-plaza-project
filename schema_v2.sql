
-- 1. Table AGENCE (Agencies)
CREATE TABLE agence (
    id_agence INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(100) NOT NULL,
    adresse VARCHAR(255) NOT NULL,
    code_postal VARCHAR(10) NOT NULL,
    ville VARCHAR(100) NOT NULL
);

-- 2. Table UTILISATEUR (Users - Staff interne Y-Plaza)
CREATE TABLE utilisateur (
    id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
    id_agence INTEGER NOT NULL,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email_pro VARCHAR(255) UNIQUE NOT NULL,
    mot_de_passe_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK(role IN ('Admin', 'Directeur', 'Commercial')),
    FOREIGN KEY (id_agence) REFERENCES agence(id_agence) ON DELETE CASCADE
);

-- 3. Table CLIENT (Customers - Prospects, acheteurs, vendeurs)
CREATE TABLE client (
    id_client INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    telephone VARCHAR(20) NOT NULL,
    budget_max REAL,
    criteres_recherche TEXT
);

-- 4. Table BIEN_IMMOBILIER (Properties - Cœur du métier)
CREATE TABLE bien_immobilier (
    id_bien INTEGER PRIMARY KEY AUTOINCREMENT,
    id_agence INTEGER NOT NULL,
    id_client_proprietaire INTEGER NOT NULL,
    reference VARCHAR(50) UNIQUE NOT NULL,
    type_bien VARCHAR(50) NOT NULL CHECK(type_bien IN ('Maison', 'Appartement', 'Local pro', 'Terrain')),
    surface REAL NOT NULL,
    nb_pieces INTEGER NOT NULL,
    prix_affiche REAL NOT NULL,
    ville VARCHAR(100) NOT NULL,
    statut VARCHAR(50) DEFAULT 'Disponible' CHECK(statut IN ('Disponible', 'Sous compromis', 'Vendu')),
    FOREIGN KEY (id_agence) REFERENCES agence(id_agence),
    FOREIGN KEY (id_client_proprietaire) REFERENCES client(id_client)
);

-- 5. Table VISITE (Visits - Suivi commercial)
CREATE TABLE visite (
    id_visite INTEGER PRIMARY KEY AUTOINCREMENT,
    id_bien INTEGER NOT NULL,
    id_client INTEGER NOT NULL,
    id_utilisateur INTEGER NOT NULL,
    date_visite DATETIME NOT NULL,
    compte_rendu TEXT,
    statut VARCHAR(50) DEFAULT 'Planifiée' CHECK(statut IN ('Planifiée', 'Réalisée', 'Annulée')),
    FOREIGN KEY (id_bien) REFERENCES bien_immobilier(id_bien) ON DELETE CASCADE,
    FOREIGN KEY (id_client) REFERENCES client(id_client),
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

-- 6. Table TRANSACTION (Transactions - Ventes finalisées)
CREATE TABLE transaction_immo (
    id_transaction INTEGER PRIMARY KEY AUTOINCREMENT,
    id_bien INTEGER NOT NULL UNIQUE,
    id_client_acheteur INTEGER NOT NULL,
    id_utilisateur INTEGER NOT NULL,
    date_vente DATE NOT NULL,
    prix_final_vendu REAL NOT NULL,
    commission_agence REAL,
    FOREIGN KEY (id_bien) REFERENCES bien_immobilier(id_bien),
    FOREIGN KEY (id_client_acheteur) REFERENCES client(id_client),
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);