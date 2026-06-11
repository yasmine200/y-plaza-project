import sqlite3

def get_db_connection():
    try:
        conn = sqlite3.connect('y_plaza.db')
        conn.row_factory = sqlite3.Row # Permet de lire les données facilement
        return conn
    except Exception as e:
        print(f"Erreur SQLite: {e}")
        return None