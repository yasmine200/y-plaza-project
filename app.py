from flask import Flask, render_template
from config.database import get_db_connection
from models.bien_immobilier import BienImmobilier

app = Flask(__name__)

@app.route('/')
def accueil():
    conn = get_db_connection()
    if conn is None:
        return "Erreur : Base de données non connectée."

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM biens WHERE statut = 'A vendre'")
        lignes = cursor.fetchall()
    except:
        lignes = [] 
    
    biens = []
    for ligne in lignes:
        bien = BienImmobilier(
            ligne['id'], ligne['titre'], ligne['description'], 
            ligne['prix'], ligne['surface'], ligne['ville'], ligne['statut']
        )
        biens.append(bien)
        
    cursor.close()
    conn.close()

    return render_template('accueil.html', biens=biens)

if __name__ == '__main__':
    app.run(debug=True)