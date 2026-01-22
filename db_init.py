import sqlite3

def crear_bd():
    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS usuarios")
    cursor.execute('''
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            email TEXT
        )
    ''')
    cursor.execute("INSERT INTO usuarios (username, password, email) VALUES (?, ?, ?)", 
                   ('admin', 'supersecreto', 'admin@empresa.com'))
    cursor.execute("INSERT INTO usuarios (username, password, email) VALUES (?, ?, ?)", 
                   ('usuario', '1234', 'user@empresa.com'))
    conn.commit()
    conn.close()
    print("Base de datos inicializada.")

if __name__ == "__main__":
    crear_bd()