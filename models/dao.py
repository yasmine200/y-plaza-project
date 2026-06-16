import sqlite3
from models.bien_immobilier import BienImmobilier

def get_db_connection():
    """Établit la connexion avec la base de données SQLite"""
    conn = sqlite3.connect('y_plaza.db')
    conn.row_factory = sqlite3.Row
    return conn

def recuperer_biens_a_vendre():
    """Récupère tous les biens immobiliers (READ - Tous)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM biens')
    lignes = cursor.fetchall()
    conn.close()
    
    biens = []
    for ligne in lignes:
        bien = BienImmobilier(
            id=ligne['id'],
            titre=ligne['titre'],
            description=ligne['description'],
            prix=ligne['prix'],
            surface=ligne['surface'],
            ville=ligne['ville'],
            statut=ligne['statut'],
            image_url=ligne['image_url']
        )
        biens.append(bien)
    return biens

def recuperer_bien_par_id(id_bien):
    """Récupère un bien spécifique grâce à son ID (READ - Un seul)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM biens WHERE id = ?', (id_bien,))
    ligne = cursor.fetchone()
    conn.close()
    
    if ligne is None:
        return None
        
    return BienImmobilier(
        id=ligne['id'],
        titre=ligne['titre'],
        description=ligne['description'],
        prix=ligne['prix'],
        surface=ligne['surface'],
        ville=ligne['ville'],
        statut=ligne['statut'],
        image_url=ligne['image_url']
    )

def ajouter_bien_bdd(titre, description, prix, surface, ville, image_url):
    """Ajoute une nouvelle annonce dans la base de données (CREATE)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO biens (titre, description, prix, surface, ville, statut, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (titre, description, prix, surface, ville, 'À vendre', image_url))
    conn.commit()
    conn.close()

def supprimer_bien_bdd(id_bien):
    """Supprime un bien de la base de données (DELETE)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM biens WHERE id = ?', (id_bien,))
    conn.commit()
    conn.close()

def modifier_bien_bdd(id_bien, titre, description, prix, surface, ville, image_url):
    """Met à jour un bien existant dans la base de données (UPDATE)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE biens
        SET titre = ?, description = ?, prix = ?, surface = ?, ville = ?, image_url = ?
        WHERE id = ?
    ''', (titre, description, prix, surface, ville, image_url, id_bien))
    conn.commit()
    cursor.close()
    conn.close()

def recuperer_utilisateur_par_email(email):
    """Récupère un utilisateur du staff par son email (pour l'authentification)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM utilisateurs WHERE email = ?', (email,))
    ligne = cursor.fetchone()
    conn.close()
    return ligne