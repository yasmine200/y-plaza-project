from flask import Flask, render_template, request, redirect, url_for, flash
from config.database import get_db_connection
from models.bien_immobilier import BienImmobilier

app = Flask(__name__)
# Clé secrète obligatoire pour faire fonctionner les messages flash (notifications)
app.secret_key = 'y_plaza_super_secret_key_2026' 

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
        titre = request.form['titre']
        description = request.form['description']
        prix = request.form['prix']
        surface = request.form['surface']
        ville = request.form['ville']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO biens (titre, description, prix, surface, ville)
            VALUES (?, ?, ?, ?, ?)
        ''', (titre, description, prix, surface, ville))
        conn.commit()
        cursor.close()
        conn.close()

        # Le fameux message flash de succès
        flash('L\'annonce a été publiée avec succès !', 'success')
        return redirect(url_for('accueil'))

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
    
    # Message flash de suppression
    flash('Le bien a été retiré de la base de données.', 'danger')
    return redirect(url_for('accueil'))

# --- ROUTE 4 : VOIR LES DÉTAILS D'UN BIEN ---
@app.route('/bien/<int:id>')
def details(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM biens WHERE id = ?', (id,))
    ligne = cursor.fetchone()
    cursor.close()
    conn.close()

    # Si quelqu'un tape un ID qui n'existe pas dans l'URL
    if ligne is None:
        flash('Ce bien immobilier n\'existe pas.', 'warning')
        return redirect(url_for('accueil'))

    # On transforme la ligne de la base de données en objet BienImmobilier
    bien = BienImmobilier(
        ligne['id'], ligne['titre'], ligne['description'], 
        ligne['prix'], ligne['surface'], ligne['ville'], ligne['statut']
    )
    
    return render_template('details.html', bien=bien)

if __name__ == '__main__':
    app.run(debug=True)