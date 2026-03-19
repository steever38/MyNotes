<p align="center">
  <img src="https://i.imgur.com/8DOaNe5.png" alt="Description de l'image" width="700">
</p>

Ce projet est une application web en `Python` / `Flask` adossée à une base de données **SQLite** pour la gestion des notes des **élèves** et des **professeurs**.
Elle inclut des fonctionnalités de sécurité et des pages adaptées aux différents rôles (élève, professeur).

## Installation

- Pour installer les dépendances du projet, exécutez la commande suivante :
```bash
pip install -r requirements.txt 
```
- Ensuite, lancez l'application avec :
```bash
python3 run.py
```
## Liste des utilisateurs
Le fichier `users.xls` contient la liste complète des utilisateurs ainsi que leurs mots de passe.

---
## Page d’accueil

La première page est une page de connexion. L’utilisateur doit :

- **Saisir** son identifiant (format : `Prenom.Nom`)
- **Saisir** son mot de passe attitré
- **Cliquer** sur le bouton **Connexion**

- **Si l’identifiant ou le mot de passe est incorrect**, un message d’erreur s’affiche.
- **Sinon**, l’utilisateur est redirigé vers une page correspondant à son rôle et, **en cas de succès**, le nombre de tentatives de saisie incorrecte est **réinitialisé à 0**.

---

## Sécurité

- **Hachage des mots de passe :**
  - Les mots de passe sont hachés de manière sécurisée en utilisant l'algorithme SHA-256 via la bibliothèque standard de Python :
  - ```python
  hashed_password = hashlib.sha256(password.encode()).hexdigest()
  ```

- **Limitation du nombre d'appels à l'API de connexion :**
  - **Plus de 10 requêtes par minute** depuis une même adresse IP entraîne un **bannissement temporaire de 1 minute** pour l'accès à l'API de connexion.

- **Gestion des tentatives de mot de passe erronées :**
  - Si l’utilisateur saisit un mot de passe incorrect **5 fois d'affilée**, il sera **prévenu à chaque tentative** du nombre de tentatives restantes.
  - Lorsqu'il atteint **5/5 tentatives incorrectes**, son compte est **bloqué pendant 5 minutes**.
  - **Si l'utilisateur entre le bon mot de passe**, le compteur de tentatives erronées est **réinitialisé à 0**.

- **Protection contre les attaques :**
  - **XSS (Cross-Site Scripting) :** Des mesures de validation et d'échappement des données utilisateurs sont mises en place pour éviter l'exécution de scripts malveillants.
  - **SQL Injection :** L'utilisation de requêtes paramétrées et de méthodes de préparation des requêtes empêche l'injection de code SQL malveillant.

---

## Base de données
Le projet repose sur une base de données relationnelle **SQLite**. Voici le schéma de l'architecture des données :
<p align="center">
  <img src="https://i.imgur.com/wiG8vzj.png" alt="Description de l'image" width="500">
</p>


---

## Page Élève

Si l’utilisateur est un **élève**, il est redirigé vers une page contenant :

- **Les moyennes de l’élève**
- **Les évaluations regroupées par matière** dans un même cadre, affichant pour chaque évaluation :
  - L’intitulé
  - La date
  - La moyenne de la classe
  - Le coefficient
  - Sa propre note
- **La moyenne de l’élève dans la matière** est affichée en bas à droite du cadre.
- **La moyenne générale** de l’élève ainsi que celle de sa classe se trouvent tout en bas de la page.
- Un **bouton d’exportation** pour exporter les notes au format CSV.
- Un **bouton de déconnexion** en haut à droite pour revenir à la page d’accueil.

---

## Pages Professeur

Si l’utilisateur est un **professeur**, il est redirigé vers une page qui contient :

- **La liste de toutes ses classes**

### En cliquant sur une classe :

- L’utilisateur est redirigé vers une page affichant **l’ensemble des évaluations de la classe** choisie dans sa matière.

### Pour chaque évaluation, les informations affichées sont :

- L’intitulé
- La moyenne de la classe
- La date
- Le coefficient
- Les notes de chaque élève

### Fonctionnalités disponibles :

- **Modifier une note :** Cliquer sur la note de l’élève et entrer la nouvelle valeur.
- **Supprimer une note :** Cliquer sur le logo poubelle à côté de l’intitulé de la note, puis confirmer en cliquant sur « OK ».
- **Navigation :**
  - Bouton **Retour** pour revenir à la page précédente.
  - Bouton **Déconnexion** pour retourner à la page d’accueil.
- **Exporter les notes :** Un bouton permet d’exporter les notes des élèves au format CSV.
- **Créer une nouvelle évaluation :**
  - En cliquant sur le bouton « Créer une nouvelle évaluation », l’utilisateur est redirigé vers une page où il doit obligatoirement remplir trois champs :
    - L’intitulé de l’évaluation
    - La date de l’évaluation
    - Le coefficient
  - La page comprend également :
    - Un bouton **Déconnexion** pour retourner à la page d’accueil.
    - Un bouton **Retour aux notes** pour revenir à la page précédente.

---

## Page d’Erreur

- **Si l’utilisateur modifie l’URL** pour changer son rôle, il est redirigé vers une page d’erreur indiquant qu’il **n’a pas la permission d’accéder à cette page**.