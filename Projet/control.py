import sqlite3
import hashlib
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .modele import ouvrir_connexion
from .modele import (
    user_exist, lock_info, reset_try, check_login, update_try, lock_account,
    get_grade, general_average, class_general_average, subject_averages,
    teacher_subject, teacher_classes, student_number, grades_classe,
    evaluation_averages, update_grade, create_new_note, delete_evaluation
)



app = Flask(__name__)

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["3000 per day", "500 per hour"]
)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/deconnexion', methods=['POST'])
def deconnexion():
    session.clear()
    return redirect(url_for('index'))


@app.route("/login", methods=["POST"])
@limiter.limit("10 per minute") # Ban IP
def login():
    donnees = request.form
    user = donnees.get('user')
    password = donnees.get('password')

    # Vérification de l'existence de l'utilisateur
    if not user_exist(user):
        return render_template("index.html", erreur="Utilisateur inconnu")

    # Vérification du verrouillage du compte
    lock_infos = lock_info(user)
    if lock_infos:
        verrouillage_timestamp, tentatives = lock_infos
        temps_actuel = datetime.now().timestamp()
        if verrouillage_timestamp and (temps_actuel - verrouillage_timestamp < 300):  # 5 minutes
            temps_restant = int(300 - (temps_actuel - verrouillage_timestamp))
            return render_template("index.html", erreur=f"Compte bloqué. Réessayez dans {temps_restant} secondes")
        elif verrouillage_timestamp and (temps_actuel - verrouillage_timestamp >= 300):
            reset_try(user)

    # Vérification des identifiants
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    result = check_login(user, hashed_password)
    if result:  # Connexion réussie
        reset_try(user)
        id_utilisateur, nom_utilisateur, prenom_utilisateur, role_utilisateur = result
        session['id_utilisateur'] = id_utilisateur
        session['nom_utilisateur'] = nom_utilisateur
        session['prenom_utilisateur'] = prenom_utilisateur
        session['role_utilisateur'] = role_utilisateur

        if role_utilisateur == "eleve":
            return redirect(url_for('eleve'))
        elif role_utilisateur == "professeur":
            return redirect(url_for('professeur'))
    else:
        update_try(user)
        # Récupération du nombre de tentatives échouées
        connexion = ouvrir_connexion()
        try:
            cursor = connexion.cursor()
            cursor.execute("SELECT tentatives_echouees FROM utilisateur WHERE id_utilisateur = ?", (user,))
            tentatives = cursor.fetchone()[0]
        finally:
            connexion.close()

        if tentatives >= 5:
            verrouillage_until = datetime.now().timestamp()
            lock_account(verrouillage_until, user)
            return render_template("index.html", erreur="Compte bloqué. Réessayez dans 5 minutes")
        return render_template("index.html", erreur=f"Identifiants incorrects. {tentatives}/5")


@app.route('/eleve')
def eleve():
    if 'id_utilisateur' not in session:
        return render_template('index.html', erreur="Veuillez vous connecter")

    id_utilisateur = session['id_utilisateur']
    nom_utilisateur = session['nom_utilisateur']
    prenom_utilisateur = session['prenom_utilisateur']
    role_utilisateur = session['role_utilisateur']

    if role_utilisateur != 'eleve':
        return render_template("access-denied.html")

    # Récupération des notes et moyennes via SQL
    notes_brutes = get_grade(id_utilisateur)
    moyenne_generale = general_average(id_utilisateur) or 0
    moyenne_classe_generale = class_general_average(id_utilisateur) or 0
    moyenne_notes = subject_averages(id_utilisateur)

    # Organisation des notes par matière
    matieres_data = {}
    for note in notes_brutes:
        nom_matiere, nom_note, date_note, valeur_note, coefficient, moyenne_classe = note
        if nom_matiere not in matieres_data:
            matieres_data[nom_matiere] = {
                'notes': [],
                'moyenne': moyenne_notes.get(nom_matiere, 0)
            }
        note_data = {
            'nom': nom_note,
            'date': date_note,
            'valeur': float(valeur_note),
            'coefficient': int(coefficient),
            'moyenne_classe': round(moyenne_classe if moyenne_classe is not None else 0, 2)
        }
        matieres_data[nom_matiere]['notes'].append(note_data)

    return render_template("eleve.html",
                           id_utilisateur=id_utilisateur,
                           nom_utilisateur=nom_utilisateur,
                           prenom_utilisateur=prenom_utilisateur,
                           role_utilisateur=role_utilisateur,
                           matieres=matieres_data,
                           moyenne_generale=round(moyenne_generale, 2),
                           moyenne_classe_generale=round(moyenne_classe_generale, 2))


@app.route('/professeur')
def professeur():
    if 'id_utilisateur' not in session:
        return render_template('index.html', erreur="Veuillez vous connecter")

    id_utilisateur = session['id_utilisateur']
    nom_utilisateur = session['nom_utilisateur']
    prenom_utilisateur = session['prenom_utilisateur']
    role_utilisateur = session['role_utilisateur']

    if role_utilisateur != 'professeur':
        return render_template("access-denied.html")

    matiere_tuple = teacher_subject(id_utilisateur)
    matiere_professeur = matiere_tuple[0] if matiere_tuple else None
    session['matiere_professeur'] = matiere_professeur

    classes_tuples = teacher_classes(id_utilisateur)
    classes = [c[0] for c in classes_tuples]

    return render_template("professeur.html",
                           id_utilisateur=id_utilisateur,
                           nom_utilisateur=nom_utilisateur,
                           prenom_utilisateur=prenom_utilisateur,
                           role_utilisateur=role_utilisateur,
                           classes=classes)


@app.route('/professeur/notes', methods=['GET'])
def professeur_notes():
    if 'id_utilisateur' not in session:
        return render_template('index.html', erreur="Veuillez vous connecter")

    id_utilisateur = session['id_utilisateur']
    nom_utilisateur = session['nom_utilisateur']
    prenom_utilisateur = session['prenom_utilisateur']
    role_utilisateur = session['role_utilisateur']

    matiere_professeur = session.get('matiere_professeur')

    if role_utilisateur != 'professeur':
        return render_template("access-denied.html")

    classe = request.args.get('classe')
    classes_tuples = teacher_classes(id_utilisateur)
    classes = [c[0] for c in classes_tuples]

    if classe in classes:
        people_number = student_number(classe)[0]
        # On utilise la matière de la session pour filtrer les notes affichées.
        notes_brutes = grades_classe(classe, matiere_professeur)
        eval_averages = evaluation_averages(classe, matiere_professeur)

        notes_data = {}
        for note in notes_brutes:
            print(note)
            # note: (nom_classe, id_utilisateur, nom_utilisateur, prenom_utilisateur, 
            #        nom_note, date_note, valeur_note, coefficient, nom_matiere)
            _, eleve_id, eleve_nom, eleve_prenom, nom_note, date_note, valeur_note, coefficient, nom_matiere = note
            # On construit une clé composite qui inclut la matière et le nom de l'évaluation.
            composite_key = f"{nom_matiere.replace(' ', '_')}||{nom_note.replace(' ', '_')}"
            if composite_key not in notes_data:
                # Pour la moyenne, on utilise ici la clé par note (puisque dans la requête d'avg on groupe par nom_note)
                # Cela fonctionne si, pour une classe donnée, toutes les notes affichées appartiennent à la même matière.
                notes_data[composite_key] = {
                    'nom_matiere': nom_matiere,
                    'nom_note': nom_note,
                    'date': date_note,
                    'coefficient': coefficient,
                    'eleves': {},
                    'moyenne': f"{eval_averages.get(nom_note, 0):.2f}"
                }
            notes_data[composite_key]['eleves'][f'{eleve_nom} {eleve_prenom}'] = {
                'note': f"{float(valeur_note):.2f}",
                'id_utilisateur': eleve_id
            }

        return render_template("professeur_notes.html",
                               id_utilisateur=id_utilisateur,
                               nom_utilisateur=nom_utilisateur,
                               prenom_utilisateur=prenom_utilisateur,
                               role_utilisateur=role_utilisateur,
                               classe=classe,
                               people_number=people_number,
                               notes=notes_data)
    else:
        return redirect(url_for('professeur'))


@app.route('/update_notes', methods=['POST'])
def update_notes():
    if 'id_utilisateur' not in session:
        return redirect(url_for('index'))

    if session.get('role_utilisateur') != 'professeur':
        return render_template("access-denied.html")

    form_data = request.form
    classe = form_data.get('classe')

    # Parcours des clés correspondant aux notes.
    # Les clés sont maintenant du format : "notes[<matiere>||<nom_note>][eleves][<id_utilisateur>]"
    for key, value in form_data.items():
        if key.startswith('notes['):
            try:
                parts = key.split('][')
                # parts[0] contient "notes[<matiere>||<nom_note>"
                composite = parts[0][6:]  # on enlève "notes["
                # On attend que la clé composite soit séparée par "||"
                subject, nom_note = composite.split('||', 1)
                if parts[1] == 'eleves':
                    eleve_id = parts[2].rstrip(']')
                    nouvelle_note = float(value)
                    # On reconstruit la matière et le nom de l'évaluation en remplaçant les underscores par des espaces.
                    # Cela suppose qu'aucun de ces champs ne contient d'underscores réels.
                    subject_db = subject.replace('_', ' ')
                    nom_note_db = nom_note.replace('_', ' ')
                    update_grade(eleve_id, subject_db, nom_note_db, nouvelle_note)
            except (IndexError, ValueError) as e:
                print(f"Erreur lors du traitement de la clé {key}: {e}")

    return redirect(url_for('professeur_notes', classe=classe))

@app.route('/supprimer_note', methods=['GET'])
def supprimer_note():
    if 'id_utilisateur' not in session:
        return redirect(url_for('index'))
    if session.get('role_utilisateur') != 'professeur':
        return render_template("access-denied.html")

    composite_key = request.args.get('composite_key')
    classe = request.args.get('classe')
    if not composite_key or not classe:
        return redirect(url_for('professeur_notes', classe=classe))
    try:
        # La clé composite a le format "matiere_modifiée||nom_note_modifié"
        subject, nom_note = composite_key.split('||', 1)
        # On reconvertit en remplaçant les underscores par des espaces.
        subject_db = subject.replace('_', ' ')
        nom_note_db = nom_note.replace('_', ' ')
    except Exception as e:
        print("Erreur de décomposition de la clé composite :", e)
        return redirect(url_for('professeur_notes', classe=classe))

    # Suppression de l'évaluation pour la classe donnée
    delete_evaluation(classe, subject_db, nom_note_db)
    return redirect(url_for('professeur_notes', classe=classe))


@app.route('/professeur/nouvelle_note', methods=['GET', 'POST'])
def nouvelle_note():
    if 'id_utilisateur' not in session:
        return render_template('index.html', erreur="Veuillez vous connecter")
    if session.get('role_utilisateur') != 'professeur':
        return render_template("access-denied.html")
    
    
    if request.method == 'GET':
        classe = request.args.get('classe')
        classes_tuples = teacher_classes(session['id_utilisateur'])
        classes = [c[0] for c in classes_tuples]

        if classe not in classes:
            return redirect(url_for('professeur'))
        
        return render_template("nouvelle_note.html",
                               classe=classe,
                               id_utilisateur=session['id_utilisateur'],
                               nom_utilisateur=session['nom_utilisateur'],
                               prenom_utilisateur=session['prenom_utilisateur'],
                               role_utilisateur=session['role_utilisateur'])
    else:  # POST
        nom_note = request.form.get('nom_note')
        date_note = request.form.get('date_note')
        coefficient = request.form.get('coefficient')
        classe = request.form.get('classe')

        try:
            coefficient = float(coefficient)
            if coefficient < 0 or coefficient > 100:
                raise ValueError("Coefficient doit être entre 0 et 100")
        except ValueError:
            return render_template("nouvelle_note.html",
                                   erreur="Coefficient invalide. Doit être entre 0 et 100.",
                                   classe=classe,
                                   id_utilisateur=session['id_utilisateur'],
                                   nom_utilisateur=session['nom_utilisateur'],
                                   prenom_utilisateur=session['prenom_utilisateur'],
                                   role_utilisateur=session['role_utilisateur'])
        # Création de la nouvelle note pour les élèves concernés de la classe
        create_new_note(classe, session['matiere_professeur'], nom_note, date_note, coefficient)
        return redirect(url_for('professeur_notes', classe=classe))


if __name__ == "__main__":
    app.run(debug=True)
