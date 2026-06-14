import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db') # Remplace par le nom de ton fichier .db
    conn.row_factory = sqlite3.Row
    return conn

def recuperer_biens(ville=""):
    """Couche de lecture des biens"""
    conn = get_db_connection()
    if ville:
        biens = conn.execute("SELECT * FROM biens WHERE ville LIKE ?", ('%' + ville + '%',)).fetchall()
    else:
        biens = conn.execute("SELECT * FROM biens").fetchall()
    conn.close()
    return biens

def recuperer_statistiques():
    """Couche de calcul des statistiques"""
    conn = get_db_connection()
    total = conn.execute("SELECT COUNT(*) FROM biens").fetchone()[0]
    prix_moyen = conn.execute("SELECT AVG(prix) FROM biens").fetchone()[0]
    conn.close()
    
    # Sécurité si la base est vide
    if prix_moyen is None:
        prix_moyen = 0
        
    return total, prix_moyen