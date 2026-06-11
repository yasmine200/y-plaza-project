from flask import Flask, render_template, request, redirect, url_for
from config.database import get_db_connection
from models.bien_immobilier import BienImmobilier

app = Flask(__name__)

# --- ROUTE 1 : LA PAGE D'ACCUEIL ---
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


# --- ROUTE 2 : AJOUTER UN BIEN ---
@app.route('/ajouter', methods=('GET', 'POST'))
def ajouter():
    if request.method == 'POST':
        # On récupère les données tapées dans le formulaire
        titre = request.form['titre']
        description = request.form['description']
        prix = request.form['prix']
        surface = request.form['surface']
        ville = request.form['ville']

        # On les insère dans la base de données
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO biens (titre, description, prix, surface, ville)
            VALUES (?, ?, ?, ?, ?)
        ''', (titre, description, prix, surface, ville))
        conn.commit()
        cursor.close()
        conn.close()

        # On renvoie l'utilisateur vers l'accueil pour voir son nouveau bien
        return redirect(url_for('accueil'))

    # Si c'est un simple GET, on affiche juste la page du formulaire
    return render_template('ajouter.html')


# --- ROUTE 3 : SUPPRIMER UN BIEN ---
@app.route('/supprimer/<int:id>', methods=['POST'])
def supprimer(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM biens WHERE id = ?', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('accueil'))


# --- LANCEMENT DU SERVEUR ---
if __name__ == '__main__':
    app.run(debug=True)