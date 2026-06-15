# 🏠 Y-Plaza - Plateforme Immobilière

## 1. Description du projet
[cite_start]Y-Plaza est une application web centralisée de gestion immobilière permettant aux agences de piloter leurs opérations de vente et d'achat de biens[cite: 62]. [cite_start]Ce projet a été réalisé dans le cadre de l'unité de formation "INFRA & DEV" du cursus Ynov Informatique[cite: 12].

## 2. Architecture Technique
[cite_start]Le projet suit une architecture MVC (Modèle-Vue-Contrôleur)[cite: 26].
* [cite_start]**Backend :** Flask (Python) pour la logique métier, la gestion des sessions et le routage[cite: 26].
* [cite_start]**Modèle de données :** SQLite3 pour la gestion relationnelle des biens et des utilisateurs[cite: 35].
* [cite_start]**Frontend :** Bootstrap 5 pour le responsive design, respectant les normes d'accessibilité (WCAG/ARIA)[cite: 29, 31, 32].

## 3. Fonctionnalités (CRUD)
L'application permet une gestion complète des annonces :
* [cite_start]**Create :** Ajout de biens avec upload d'images sécurisé (gestion des types MIME et renommage)[cite: 26].
* [cite_start]**Read :** Affichage dynamique et filtrage des annonces via des requêtes SQL optimisées[cite: 35].
* [cite_start]**Update :** Modification des informations immobilières et remplacement des visuels[cite: 35].
* [cite_start]**Delete :** Suppression sécurisée réservée au rôle `Admin`[cite: 35].

## 4. Analyse et API
* [cite_start]**Analyse de données :** Script `analyse_donnees.py` (Pandas) pour le traitement des tendances du marché (prix moyens, biens populaires)[cite: 37, 38].
* [cite_start]**API REST :** Exposition des données via une route `/api/biens` au format JSON, facilitant l'interopérabilité[cite: 26].

## 5. Sécurité & Accessibilité
* [cite_start]**Sécurité :** Implémentation du contrôle d'accès basé sur les rôles (`@role_requis`) et utilisation de requêtes paramétrées pour prévenir les injections SQL[cite: 26, 35].
* [cite_start]**Accessibilité :** Utilisation d'attributs ARIA pour garantir la compatibilité avec les outils d'assistance (lecteurs d'écran)[cite: 32].

## 6. Installation
1. Cloner le dépôt : `git clone <url-du-depot>`
2. Installer les dépendances : `pip install flask pandas`
3. Lancer l'application : `python app.py`

---
*Développeur Backend : Yasmine Fakir*
[cite_start]*Projet réalisé dans le cadre de l'UF INFRA & DEV[cite: 12].*