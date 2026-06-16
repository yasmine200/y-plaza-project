import sqlite3
from werkzeug.security import generate_password_hash

# Source unique de verite du schema : ce fichier cree la base reellement
# utilisee par l'application. Il est volontairement aligne avec schema_v2.sql.
#
# Les roles correspondent aux 5 poles de la "Matrice des droits" du cahier
# des charges. Pour le dossier "Commercial" (= les biens immobiliers), seul
# le pole Commercial dispose de l'ECRITURE ; les autres poles sont en LECTURE.

ROLES = (
    'Direction',
    'Commercial',
    'Communication & Marketing',
    'Administratif - RH - Juridique',
    'IT et Support',
)


def init_db():
    conn = sqlite3.connect('y_plaza.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    # On repart d'une base propre et coherente (projet de demonstration)
    roles_sql = ", ".join("'" + r + "'" for r in ROLES)
    cursor.executescript(f'''
        DROP TABLE IF EXISTS biens;
        DROP TABLE IF EXISTS utilisateurs;
        DROP TABLE IF EXISTS agence;

        -- Agences du reseau Y-Plaza (siege + agences)
        CREATE TABLE agence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            ville TEXT NOT NULL
        );

        -- Staff interne (mots de passe stockes HASHES, jamais en clair)
        -- Le role correspond a l'un des 5 poles de la matrice des droits.
        CREATE TABLE utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            mot_de_passe_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ({roles_sql})),
            agence_id INTEGER,
            FOREIGN KEY (agence_id) REFERENCES agence(id)
        );

        -- Biens immobiliers (coeur du metier)
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
    ''')

    # --- Donnees de depart (seed) ---
    agences = [
        ('Y-Plaza Siège', 'Aix-en-Provence'),   # id 1
        ('Y-Plaza Marseille', 'Marseille'),      # id 2
        ('Y-Plaza Lyon', 'Lyon'),                # id 3
    ]
    cursor.executemany('INSERT INTO agence (nom, ville) VALUES (?, ?)', agences)

    # Un compte par pole (matrice des droits) + un commercial en agence.
    utilisateurs = [
        ('Direction Y-Plaza',  'direction@yplaza.fr',   generate_password_hash('dir123'),  'Direction',                      1),
        ('Commercial Siège',   'commercial@yplaza.fr',  generate_password_hash('comm123'), 'Commercial',                     1),
        ('Comm & Marketing',   'marketing@yplaza.fr',   generate_password_hash('mkt123'),  'Communication & Marketing',      1),
        ('Admin RH Juridique', 'rh@yplaza.fr',          generate_password_hash('rh123'),   'Administratif - RH - Juridique', 1),
        ('IT et Support',      'it@yplaza.fr',          generate_password_hash('it123'),   'IT et Support',                  1),
        ('Commercial Marseille', 'commercial.marseille@yplaza.fr', generate_password_hash('comm123'), 'Commercial',          2),
    ]
    cursor.executemany(
        'INSERT INTO utilisateurs (nom, email, mot_de_passe_hash, role, agence_id) VALUES (?, ?, ?, ?, ?)',
        utilisateurs,
    )

    img = ("https://images.unsplash.com/photo-1560518883-ce09059eeffa"
           "?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80")
    biens = [
        ('Appartement T3 lumineux', 'Bel appartement rénové en centre-ville.', 285000, 68, 'Aix-en-Provence', 'À vendre', img, 2),
        ('Maison familiale avec jardin', 'Maison 5 pièces au calme, proche commodités.', 540000, 130, 'Marseille', 'À vendre', img, 6),
        ('Studio idéal investisseur', 'Studio meublé, fort potentiel locatif.', 119000, 24, 'Aix-en-Provence', 'À vendre', img, 2),
    ]
    cursor.executemany(
        'INSERT INTO biens (titre, description, prix, surface, ville, statut, image_url, agent_id) '
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        biens,
    )

    conn.commit()
    conn.close()
    print("Succès ! Base y_plaza.db créée et alimentée (agences, utilisateurs, biens).")


if __name__ == '__main__':
    init_db()
