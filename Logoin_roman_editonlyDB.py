def init_db():
    conn = sqlite3.connect('user_info.db')  # Stelle eine Verbindung zur SQLite-Datenbank her
    c = conn.cursor()  # Erstelle ein Cursor-Objekt

    # Erstelle die Tabelle für Benutzerinformationen, falls diese noch nicht existiert
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL)''')
    
    # Erstelle die Tabelle für Aufgaben, falls diese noch nicht existiert
    c.execute('''CREATE TABLE IF NOT EXISTS task (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 quest TEXT NOT NULL,
		 example TEXT NOT NULL,
                 solution TEXT NOT NULL)''')

    # Erstelle die Tabelle für Benutzeraufgaben, falls diese noch nicht existiert
    c.execute('''CREATE TABLE IF NOT EXISTS UserTask (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 idUser INTEGER NOT NULL,
                 idTask INTEGER NOT NULL,
                 pkt INTEGER,
                 FOREIGN KEY (idUser) REFERENCES users(id),
                 FOREIGN KEY (idTask) REFERENCES task(id))''')

    conn.commit()  # Bestätige die Änderungen
    conn.close()  # Schließe die Verbindung

# Rufe die Funktion auf, um die Datenbank zu erstellen
init_db()