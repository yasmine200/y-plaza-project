import sqlite3
conn = sqlite3.connect('y_plaza.db') 
try:
    conn.execute("ALTER TABLE biens ADD COLUMN image_url TEXT DEFAULT 'https://images.unsplash.com/photo-1560518883-ce09059eeffa?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'")
    conn.commit()
    print("Colonne image_url ajoutée avec succès !")
except Exception as e:
    print("La colonne existe déjà ou erreur :", e)
finally:
    conn.close()