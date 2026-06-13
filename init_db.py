import sqlite3

def init_db():
    conn = sqlite3.connect('y_plaza.db')
    cursor = conn.cursor()

    # Création des tables
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            mot_de_passe TEXT NOT NULL,
            role TEXT DEFAULT 'client'
        );

        CREATE TABLE IF NOT EXISTS biens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            description TEXT,
            prix REAL NOT NULL,
            surface INTEGER NOT NULL,
            ville TEXT NOT NULL,
            statut TEXT DEFAULT 'A vendre',
            agent_id INTEGER,
            FOREIGN KEY (agent_id) REFERENCES utilisateurs(id)
        );
    ''')
    conn.commit()
    conn.close()
    print("Succès ! Le fichier y_plaza.db a été créé avec les tables.")

if __name__ == '__main__':
    init_db()