import os

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

from functools import wraps

from werkzeug.utils import secure_filename

from werkzeug.security import check_password_hash

from models.dao import (
    recuperer_biens_a_vendre,
    ajouter_bien_bdd,
    supprimer_bien_bdd,
    recuperer_bien_par_id,
    modifier_bien_bdd,
    recuperer_utilisateur_par_email,
)



app = Flask(__name__)

# Clé secrète lue depuis l'environnement (valeur de repli pour le développement).
app.secret_key = os.environ.get('YPLAZA_SECRET_KEY', 'dev-secret-change-me')



# --- CONFIGURATION DE L'UPLOAD (Version Blindée) ---

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)



app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Extensions d'images autorisées pour l'upload (sécurité).
EXTENSIONS_AUTORISEES = {'png', 'jpg', 'jpeg', 'webp', 'gif'}


def extension_autorisee(nom_fichier):
    return '.' in nom_fichier and \
        nom_fichier.rsplit('.', 1)[1].lower() in EXTENSIONS_AUTORISEES



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

        utilisateur = recuperer_utilisateur_par_email(email)

        if utilisateur and check_password_hash(utilisateur['mot_de_passe_hash'], mdp):

            session['utilisateur'] = email

            session['role'] = utilisateur['role']

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

@role_requis('Commercial')

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

            if not extension_autorisee(file.filename):

                flash("Format d'image non autorisé (png, jpg, jpeg, webp, gif).", "danger")

                return render_template('ajouter.html')

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

@role_requis('Commercial')

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

            if not extension_autorisee(file.filename):

                flash("Format d'image non autorisé (png, jpg, jpeg, webp, gif).", "danger")

                return render_template('modifier.html', bien=bien)

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

@role_requis('Commercial')

def supprimer(id):

    supprimer_bien_bdd(id)

    flash('Le bien a été retiré de la base de données.', 'danger')

    return redirect(url_for('accueil'))



@app.route('/api/biens')

def api_biens():
    """API REST : expose la liste des biens au format JSON."""
    biens = recuperer_biens_a_vendre()
    return jsonify([bien.to_dict() for bien in biens])


@app.route('/bien/<int:id>')

def details(id):

    bien = recuperer_bien_par_id(id)

    if bien is None:

        flash("Ce bien immobilier n'existe pas.", "warning")

        return redirect(url_for('accueil'))

    return render_template('details.html', bien=bien)



if __name__ == '__main__':

    app.run(debug=True)