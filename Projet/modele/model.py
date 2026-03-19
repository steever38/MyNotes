import sqlite3
from .connect import ouvrir_connexion

############# LOGIN #############

def user_exist(user: str):
    """
    Vérifie si l'utilisateur existe dans la table 'utilisateur'.

    Paramètres:
        user (str): L'identifiant de l'utilisateur.

    Retourne:
        bool: True si l'utilisateur existe, False sinon.
    """
    connexion = ouvrir_connexion()
    cursor = connexion.cursor()
    try:
        query = """
            SELECT 1
            FROM utilisateur
            WHERE id_utilisateur = ?
        """
        cursor.execute(query, (user,))
        return cursor.fetchone() is not None
    finally:
        connexion.close()


def lock_info(user: str):
    """
    Récupère les informations de verrouillage et le nombre de tentatives échouées pour un utilisateur.

    Paramètres:
        user (str): L'identifiant de l'utilisateur.

    Retourne:
        tuple: (verrouillage_until, tentatives_echouees) ou None si l'utilisateur n'est pas trouvé.
    """
    connexion = ouvrir_connexion()
    cursor = connexion.cursor()
    try:
        query = """
            SELECT verrouillage_until, tentatives_echouees
            FROM utilisateur
            WHERE id_utilisateur = ?
        """
        cursor.execute(query, (user,))
        return cursor.fetchone()
    finally:
        connexion.close()


def reset_try(user: str):
    """
    Réinitialise le compteur de tentatives échouées et la date de verrouillage pour un utilisateur.

    Paramètres:
        user (str): L'identifiant de l'utilisateur.
    """
    connexion = ouvrir_connexion()
    cursor = connexion.cursor()
    try:
        query = """
            UPDATE utilisateur
            SET tentatives_echouees = 0,
                verrouillage_until = NULL
            WHERE id_utilisateur = ?
        """
        cursor.execute(query, (user,))
        connexion.commit()
    finally:
        connexion.close()


def check_login(user: str, password: str):
    """
    Vérifie les identifiants de connexion et récupère les informations de l'utilisateur.

    Paramètres:
        user (str): L'identifiant de l'utilisateur.
        password (str): Le mot de passe de l'utilisateur.

    Retourne:
        tuple: (id_utilisateur, nom_utilisateur, prenom_utilisateur, role_utilisateur) si les identifiants sont corrects, sinon None.
    """
    connexion = ouvrir_connexion()
    cursor = connexion.cursor()
    try:
        query = """
            SELECT id_utilisateur, nom_utilisateur, prenom_utilisateur, role_utilisateur
            FROM utilisateur
            WHERE id_utilisateur = ? AND mot_de_passe = ?
        """
        cursor.execute(query, (user, password))
        return cursor.fetchone()
    finally:
        connexion.close()


def update_try(user: str):
    """
    Incrémente le compteur de tentatives échouées pour un utilisateur.

    Paramètres:
        user (str): L'identifiant de l'utilisateur.
    """
    connexion = ouvrir_connexion()
    cursor = connexion.cursor()
    try:
        query = """
            UPDATE utilisateur
            SET tentatives_echouees = tentatives_echouees + 1
            WHERE id_utilisateur = ?
        """
        cursor.execute(query, (user,))
        connexion.commit()
    finally:
        connexion.close()


def lock_account(verrouillage_until, user: str):
    """
    Met à jour la date de verrouillage d'un compte utilisateur.

    Paramètres:
        verrouillage_until (datetime): La date/heure jusqu'à laquelle le compte est verrouillé.
        user (str): L'identifiant de l'utilisateur.
    """
    connexion = ouvrir_connexion()
    cursor = connexion.cursor()
    try:
        query = """
            UPDATE utilisateur
            SET verrouillage_until = ?
            WHERE id_utilisateur = ?
        """
        cursor.execute(query, (verrouillage_until, user))
        connexion.commit()
    finally:
        connexion.close()


############# NOTES #############

def get_grade(user: str):
    """
    Récupère les notes d'un élève ainsi que la moyenne de la classe pour chaque évaluation.

    Paramètres:
        user (str): L'identifiant de l'élève.

    Retourne:
        list: Liste de tuples contenant les informations sur chaque note et la moyenne de classe correspondante.
    """
    connexion = ouvrir_connexion()
    cursor = connexion.cursor()
    try:
        query = """
            SELECT n1.nom_matiere,
                   n1.nom_note,
                   n1.date_note,
                   n1.valeur_note,
                   n1.coefficient,
                   COALESCE(AVG(n2.valeur_note), 0) AS moyenne_classe
            FROM note n1
            LEFT JOIN note n2 
              ON n1.nom_note = n2.nom_note 
             AND n1.nom_matiere = n2.nom_matiere
             AND n2.valeur_note <> 0
             AND n2.id_utilisateur IN (
                 SELECT id_utilisateur 
                 FROM eleve 
                 WHERE nom_classe = (SELECT nom_classe FROM eleve WHERE id_utilisateur = ?)
             )
            WHERE n1.id_utilisateur = ?
            GROUP BY n1.nom_matiere, n1.nom_note, n1.date_note, n1.valeur_note, n1.coefficient
            ORDER BY n1.nom_matiere, n1.date_note
        """
        cursor.execute(query, (user, user))
        return cursor.fetchall()
    finally:
        connexion.close()


def general_average(user: str):
    """
    Calcule la moyenne générale pondérée d'un élève en excluant les notes à 0.

    Paramètres:
        user (str): L'identifiant de l'élève.

    Retourne:
        float: La moyenne générale de l'élève.
    """
    connexion = ouvrir_connexion()
    cursor = connexion.cursor()
    try:
        query = """
            SELECT COALESCE(SUM(valeur_note * coefficient) / NULLIF(SUM(coefficient), 0), 0)
            FROM note
            WHERE id_utilisateur = ? AND valeur_note <> 0
        """
        cursor.execute(query, (user,))
        result = cursor.fetchone()
        return result[0] if result and result[0] is not None else 0
    except Exception as e:
        print(f"Erreur lors du calcul de la moyenne générale : {e}")
        return 0
    finally:
        connexion.close()


def class_general_average(user: str):
    """
    Calcule la moyenne générale pondérée de la classe de l'élève.

    Paramètres:
        user (str): L'identifiant de l'élève dont on souhaite connaître la classe.

    Retourne:
        float: La moyenne générale de la classe.
    """
    connexion = ouvrir_connexion()
    cursor = connexion.cursor()
    try:
        query = """
            SELECT COALESCE(SUM(n.valeur_note * n.coefficient) / NULLIF(SUM(n.coefficient), 0), 0)
            FROM note n
            WHERE n.id_utilisateur IN (
                SELECT id_utilisateur 
                FROM eleve 
                WHERE nom_classe = (SELECT nom_classe FROM eleve WHERE id_utilisateur = ?)
            )
            AND n.valeur_note <> 0
        """
        cursor.execute(query, (user,))
        result = cursor.fetchone()
        return result[0] if result and result[0] is not None else 0
    finally:
        connexion.close()


def subject_averages(user: str):
    """
    Calcule la moyenne pondérée pour chaque matière d'un élève en excluant les notes à 0.

    Paramètres:
        user (str): L'identifiant de l'élève.

    Retourne:
        dict: Dictionnaire où la clé est le nom de la matière et la valeur la moyenne correspondante.
    """
    connexion = ouvrir_connexion()
    cursor = connexion.cursor()
    try:
        query = """
            SELECT nom_matiere,
                   COALESCE(SUM(valeur_note * coefficient) / NULLIF(SUM(coefficient), 0), 0) AS moyenne
            FROM note
            WHERE id_utilisateur = ? AND valeur_note <> 0
            GROUP BY nom_matiere
        """
        cursor.execute(query, (user,))
        return {row[0]: row[1] for row in cursor.fetchall()}
    finally:
        connexion.close()


############# PROFESSEUR #############

def teacher_subject(user: str):
    """
    Récupère la matière enseignée par un professeur.

    Paramètres:
        user (str): L'identifiant du professeur.

    Retourne:
        tuple: Contient le nom de la matière ou None si non trouvé.
    """
    connexion = ouvrir_connexion()
    cursor = connexion.cursor()
    try:
        query = """
            SELECT nom_matiere
            FROM professeur
            WHERE id_utilisateur = ?
        """
        cursor.execute(query, (user,))
        return cursor.fetchone()
    finally:
        connexion.close()


def teacher_classes(user: str):
    """
    Récupère la liste des classes associées à un professeur.

    Paramètres:
        user (str): L'identifiant du professeur.

    Retourne:
        list: Liste des classes.
    """
    connexion = ouvrir_connexion()
    cursor = connexion.cursor()
    try:
        query = """
            SELECT nom_classe
            FROM professeur_classe
            WHERE id_utilisateur = ?
            ORDER BY nom_classe;
        """
        cursor.execute(query, (user,))
        return cursor.fetchall()
    finally:
        connexion.close()


def student_number(classe: str):
    """
    Compte le nombre d'élèves dans une classe donnée.

    Paramètres:
        classe (str): Le nom de la classe.

    Retourne:
        tuple: Le résultat du COUNT(*) (le nombre d'élèves).
    """
    connexion = ouvrir_connexion()
    cursor = connexion.cursor()
    try:
        query = """
            SELECT COUNT(*)
            FROM eleve
            WHERE nom_classe = ?
        """
        cursor.execute(query, (classe,))
        return cursor.fetchone()
    finally:
        connexion.close()


def grades_classe(classe: str, matiere: str):
    """
    Récupère les notes des élèves d'une classe pour une matière donnée.

    Paramètres:
        classe (str): Le nom de la classe.
        matiere (str): Le nom de la matière.

    Retourne:
        list: Liste de tuples contenant les informations de chaque note.
    """
    connexion = ouvrir_connexion()
    cursor = connexion.cursor()
    try:
        query = """
            SELECT 
                e.nom_classe,
                e.id_utilisateur,
                u.nom_utilisateur,
                u.prenom_utilisateur,
                n.nom_note,
                n.date_note,
                n.valeur_note,
                n.coefficient,
                n.nom_matiere
            FROM eleve e
            JOIN note n ON e.id_utilisateur = n.id_utilisateur
            JOIN utilisateur u ON e.id_utilisateur = u.id_utilisateur
            WHERE e.nom_classe = ? AND n.nom_matiere = ?
            ORDER BY u.nom_utilisateur;
        """
        cursor.execute(query, (classe, matiere))
        return cursor.fetchall()
    finally:
        connexion.close()


def evaluation_averages(classe: str, matiere: str):
    """
    Calcule la moyenne de chaque évaluation pour une classe et une matière donnée.

    Paramètres:
        classe (str): Le nom de la classe.
        matiere (str): Le nom de la matière.

    Retourne:
        dict: Dictionnaire avec pour clé le nom de l'évaluation et pour valeur sa moyenne.
    """
    connexion = ouvrir_connexion()
    cursor = connexion.cursor()
    try:
        query = """
            SELECT nom_note, COALESCE(AVG(valeur_note), 0) AS moyenne
            FROM note
            WHERE nom_matiere = ? 
              AND id_utilisateur IN (
                  SELECT id_utilisateur 
                  FROM eleve 
                  WHERE nom_classe = ?
              )
              AND valeur_note <> 0
            GROUP BY nom_note
        """
        cursor.execute(query, (matiere, classe))
        return {row[0]: row[1] for row in cursor.fetchall()}
    finally:
        connexion.close()


def update_grade(id_utilisateur: str, matiere: str, nom_note: str, nouvelle_note: float):
    """
    Met à jour la note d'un élève pour une évaluation donnée.

    Paramètres:
        id_utilisateur (str): L'identifiant de l'élève.
        matiere (str): Le nom de la matière.
        nom_note (str): Le nom de l'évaluation.
        nouvelle_note (float): La nouvelle valeur de la note.
    """
    connexion = ouvrir_connexion()
    cursor = connexion.cursor()
    try:
        query = """
            UPDATE note
            SET valeur_note = ?
            WHERE id_utilisateur = ? 
              AND nom_matiere = ? 
              AND nom_note = ?
        """
        cursor.execute(query, (nouvelle_note, id_utilisateur, matiere, nom_note))
        connexion.commit()
    except Exception as e:
        print(f"Erreur lors de la mise à jour de la note : {e}")
    finally:
        connexion.close()


############# NOUVELLE NOTE #############

def get_students_in_class_by_subject(classe: str, matiere: str):
    """
    Récupère la liste des identifiants des élèves d'une classe.
    Pour une matière de langue (allemand, italien, espagnol), seuls les élèves dont le champ lv2 correspond sont retournés.

    Paramètres:
        classe (str): Le nom de la classe.
        matiere (str): Le nom de la matière.

    Retourne:
        list: Liste des id_utilisateur des élèves concernés.
    """
    connexion = ouvrir_connexion()
    cursor = connexion.cursor()
    try:
        if matiere.lower() in ('allemand', 'italien', 'espagnol'):
            query = "SELECT id_utilisateur FROM eleve WHERE nom_classe = ? AND LOWER(lv2) = ?"
            cursor.execute(query, (classe, matiere.lower()))
        else:
            query = "SELECT id_utilisateur FROM eleve WHERE nom_classe = ?"
            cursor.execute(query, (classe,))
        return [row[0] for row in cursor.fetchall()]
    finally:
        connexion.close()


def create_new_note(classe: str, matiere: str, nom_note: str, date_note, coefficient: float):
    """
    Crée une nouvelle évaluation pour tous les élèves d'une classe.
    Pour une matière de langue (allemand, italien, espagnol), seuls les élèves dont le champ lv2 correspond reçoivent la note initialisée à 0.

    Paramètres:
        classe (str): Le nom de la classe.
        matiere (str): Le nom de la matière.
        nom_note (str): Le nom de l'évaluation.
        date_note (date): La date de l'évaluation.
        coefficient (float): Le coefficient de l'évaluation.
    """
    students = get_students_in_class_by_subject(classe, matiere)
    connexion = ouvrir_connexion()
    cursor = connexion.cursor()
    try:
        query = """
            INSERT INTO note (id_utilisateur, nom_matiere, nom_note, date_note, valeur_note, coefficient)
            VALUES (?, ?, ?, ?, 0, ?)
        """
        for student in students:
            cursor.execute(query, (student, matiere, nom_note, date_note, coefficient))
        connexion.commit()
    except Exception as e:
        print(f"Erreur lors de la création de la nouvelle note : {e}")
    finally:
        connexion.close()


def delete_evaluation(classe: str, matiere: str, nom_note: str):
    """
    Supprime une évaluation pour tous les élèves d'une classe donnée.

    Paramètres:
        classe (str): Le nom de la classe.
        matiere (str): Le nom de la matière.
        nom_note (str): Le nom de l'évaluation à supprimer.
    """
    connexion = ouvrir_connexion()
    cursor = connexion.cursor()
    try:
        query = """
            DELETE FROM note
            WHERE nom_matiere = ?
              AND nom_note = ?
              AND id_utilisateur IN (
                  SELECT id_utilisateur FROM eleve WHERE nom_classe = ?
              )
        """
        cursor.execute(query, (matiere, nom_note, classe))
        connexion.commit()
    except Exception as e:
        print(f"Erreur lors de la suppression de l'évaluation : {e}")
    finally:
        connexion.close()