# 🏠 Y-Plaza - Plateforme Immobilière

## 1. Description du projet
Y-Plaza est une application web de gestion immobilière permettant au personnel d'agence de piloter les annonces de vente et d'achat de biens. Ce projet a été réalisé dans le cadre de l'unité de formation "INFRA & DEV" du cursus Ynov Informatique.

## 2. Architecture Technique
Le projet suit une architecture MVC (Modèle-Vue-Contrôleur) :
* **Backend :** Flask (Python) pour la logique métier, la gestion des sessions et le routage.
* **Modèle de données :** SQLite3 pour le stockage des informations immobilières et des comptes collaborateurs.
* **Frontend :** Bootstrap 5 pour le responsive design, avec une attention portée aux standards d'accessibilité (ARIA).

## 3. Fonctionnalités
L'application permet une gestion complète des annonces côté staff :
* **Create :** Ajout de nouveaux biens avec upload d'image (gestion sécurisée des fichiers).
* **Read :** Consultation dynamique et filtrage des annonces en base de données.
* **Update :** Modification des caractéristiques et des visuels des biens existants.
* **Delete :** Suppression sécurisée des annonces (réservé aux comptes `Admin`).

## 4. Analyse de données
Le projet intègre un module d'analyse (`analyse_donnees.py`) utilisant **Pandas** et **Scikit-learn** pour traiter les données issues de la base SQLite, permettant d'extraire des indicateurs sur les biens immobiliers.

## 5. Sécurité
* **Contrôle d'accès :** Implémentation d'un système de rôles (`@role_requis`) restreignant les actions sensibles (suppression/modification) aux collaborateurs autorisés.
* **Prévention :** Utilisation de requêtes SQL paramétrées pour prévenir les injections.
* *Note : Pour la version actuelle, les identifiants sont gérés via une logique applicative simple ; une mise en production réelle intégrerait le hachage des mots de passe (via Werkzeug) et des variables d'environnement.*

## 6. Installation & Prérequis
Pour lancer le projet, assurez-vous d'avoir Python 3 installé.
1. Cloner le dépôt : `git clone <url-du-depot>`
2. Installer les dépendances : `pip install flask pandas scikit-learn numpy`
3. Initialiser la base : `python3 init_db.py`
4. Lancer l'application : `python3 app.py`

---
*Développeurs : Yasmine Fakir (Backend/Dev) & Guylan Richaud (Infrastructure/Réseau)*
