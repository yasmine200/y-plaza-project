import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
from werkzeug.utils import secure_filename
from models.dao import recuperer_biens_a_vendre, ajouter_bien_bdd, supprimer_bien_bdd, recuperer_bien_par_id, modifier_bien_bdd

app = Flask(__name__)
app.secret_key = 'y_plaza_super_secret_key_2026'

# --- CONFIGURATION DE L'UPLOAD (Version Blindée) ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

USERS = {
    "admin@yplaza.fr": {"mdp": "admin123", "role": "Admin"},
    "commercial@yplaza.fr": {"mdp": "comm123", "role": "Commercial"}
}

def role_requis(*roles_autorises):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'utilisateur' not in session:
                flash("Veuillez vous connecter pour accéder à cette page.", "warning")
                return redirect(url_for('login'))
            if session.get('role') not in roles_autorises:
                flash("Accès refusé.", "danger")
                return redirect(url_for('accueil'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        mdp = request.form['mdp']
        if email in USERS and USERS[email]['mdp'] == mdp:
            session['utilisateur'] = email
            session['role'] = USERS[email]['role']
            flash(f"Bienvenue, connecté en tant que {session['role']}.", "success")
            return redirect(url_for('accueil'))
        else:
            flash("Identifiants incorrects.", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Vous avez été déconnecté.", "success")
    return redirect(url_for('accueil'))

@app.route('/')
def accueil():
    biens = recuperer_biens_a_vendre()
    return render_template('accueil.html', biens=biens)

@app.route('/ajouter', methods=('GET', 'POST'))
@role_requis('Admin', 'Commercial')
def ajouter():
    if request.method == 'POST':
        titre = request.form['titre']
        description = request.form['description']
        prix = request.form['prix']
        surface = request.form['surface']
        ville = request.form['ville']
        
        # --- GESTION DE L'UPLOAD DE L'IMAGE ---
        file = request.files.get('image')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            chemin_complet = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(chemin_complet)
            image_url = f"/static/uploads/{filename}"
        else:
            image_url = "https://images.unsplash.com/photo-1560518883-ce09059eeffa?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"

        ajouter_bien_bdd(titre, description, prix, surface, ville, image_url)
        
        flash("L'annonce a été publiée avec succès !", "success")
        return redirect(url_for('accueil'))

    return render_template('ajouter.html')

@app.route('/modifier/<int:id>', methods=('GET', 'POST'))
@role_requis('Admin', 'Commercial')
def modifier(id):
    # On récupère le bien actuel pour pré-remplir le formulaire
    bien = recuperer_bien_par_id(id)
    if bien is None:
        flash("Ce bien n'existe pas.", "warning")
        return redirect(url_for('accueil'))

    if request.method == 'POST':
        titre = request.form['titre']
        description = request.form['description']
        prix = request.form['prix']
        surface = request.form['surface']
        ville = request.form['ville']
        
        # --- GESTION DE L'IMAGE LORS DE LA MODIFICATION ---
        file = request.files.get('image')
        if file and file.filename != '':
            # Si on upload une NOUVELLE photo, on la sauvegarde
            filename = secure_filename(file.filename)
            chemin_complet = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(chemin_complet)
            image_url = f"/static/uploads/{filename}"
        else:
            # Sinon, on GARDE l'ancienne photo du bien
            image_url = bien.image_url

        # On envoie tout à la base de données
        modifier_bien_bdd(id, titre, description, prix, surface, ville, image_url)
        
        flash("L'annonce a été modifiée avec succès !", "success")
        return redirect(url_for('accueil'))

    # Si on arrive sur la page en mode GET, on affiche le formulaire pré-rempli
    return render_template('modifier.html', bien=bien)

@app.route('/supprimer/<int:id>', methods=['POST'])
@role_requis('Admin')
def supprimer(id):
    supprimer_bien_bdd(id)
    flash('Le bien a été retiré de la base de données.', 'danger')
    return redirect(url_for('accueil'))

@app.route('/bien/<int:id>')
def details(id):
    bien = recuperer_bien_par_id(id)
    if bien is None:
        flash("Ce bien immobilier n'existe pas.", "warning")
        return redirect(url_for('accueil'))
    return render_template('details.html', bien=bien)

if __name__ == '__main__':
    app.run(debug=True)