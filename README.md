# y-plaza-project
## 🛠️ Conception et Choix Techniques

Pour répondre au besoin métier de manière optimale, les choix techniques suivants ont été formalisés :

**1. Architecture Client-Serveur & MVC :**
Le projet suit une logique inspirée du design pattern MVC (Modèle-Vue-Contrôleur) pour une séparation claire des responsabilités :
- **Modèle :** Le dossier `models` et le fichier `database.py` gèrent l'accès aux données.
- **Vue :** Le dossier `templates` gère l'affichage HTML/CSS.
- **Contrôleur :** Le fichier `app.py` orchestre les requêtes (GET/POST) et la logique métier.

**2. Backend (Python / Flask) :**
Le framework Flask a été retenu pour sa légèreté et sa robustesse. Il permet de développer un serveur web rapide tout en produisant un code lisible, modulaire, et respectant les principes de base du développement propre (KISS, DRY).

**3. Base de données (SQLite) :**
Le choix de SQLite s'est imposé pour ce prototype en raison de sa portabilité absolue. Aucune installation de serveur externe (comme MySQL ou Postgres) n'est requise, ce qui facilite grandement l'exécution et l'évaluation du projet.

**4. Frontend & Accessibilité (Bootstrap 5) :**
L'interface a été pensée pour être responsive (compatible PC, tablette, mobile). L'utilisation de Bootstrap 5 permet de garantir des interfaces claires, ergonomiques, et surtout conformes aux bonnes pratiques d'accessibilité web et d'expérience utilisateur (UX).