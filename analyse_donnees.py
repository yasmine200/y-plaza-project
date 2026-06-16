import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import sqlite3

def get_data_from_db():
    """Récupère les données des biens depuis la base réelle de l'application."""
    conn = sqlite3.connect('y_plaza.db')
    df = pd.read_sql_query("SELECT surface, prix FROM biens WHERE surface > 0 AND prix > 0", conn)
    conn.close()
    return df

def estimer_prix(surface_cible):
    """Calcule l'estimation du prix selon la surface via régression linéaire."""
    df = get_data_from_db()
    
    if len(df) < 2:  # Besoin d'au moins 2 points pour une droite
        return "Données insuffisantes pour estimation"
        
    X = df[['surface']].values
    y = df['prix'].values
    
    modele = LinearRegression()
    modele.fit(X, y)
    
    prix_estime = modele.predict(np.array([[surface_cible]]))
    return round(prix_estime[0], 2)

# Exemple de test si tu lances le script seul
if __name__ == "__main__":
    test_surface = 80
    estimation = estimer_prix(test_surface)
    print(f"Estimation pour {test_surface}m² : {estimation} €")