import sqlite3
import pandas as pd

def generer_rapport_ventes():
    conn = sqlite3.connect('y_plaza.db')
    # On charge la table des biens en DataFrame Pandas
    df = pd.read_sql_query("SELECT * FROM biens", conn)
    conn.close()
    
    # 1. Biens les plus chers (Tendance marché)
    top_biens = df.nlargest(3, 'prix')[['titre', 'prix']]
    
    # 2. Moyenne de prix par ville
    prix_moyen = df.groupby('ville')['prix'].mean()
    
    print("--- RAPPORT ANALYTIQUE Y-PLAZA ---")
    print("\nTop 3 des biens les plus valorisés :")
    print(top_biens)
    print("\nPrix moyen par secteur :")
    print(prix_moyen)

if __name__ == '__main__':
    generer_rapport_ventes()