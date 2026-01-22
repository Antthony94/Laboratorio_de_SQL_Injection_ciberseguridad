from flask import Flask, render_template, request, g
import sqlite3
import os

app = Flask(__name__)
DB_PATH = "tienda.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def login():
    query_log = ""
    result_msg = ""
    status = "neutral" # neutral, success, danger
    mode = request.form.get('mode', 'vulnerable') # Por defecto vulnerable

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db()
        cursor = conn.cursor()

        if mode == 'vulnerable':
            # ❌ VULNERABLE: Concatenación directa
            query = f"SELECT * FROM usuarios WHERE username = '{username}' AND password = '{password}'"
            query_log = query # Guardamos la query para mostrarla en el frontend
            try:
                cursor.executescript(query) # executescript permite múltiples sentencias (Stacked Queries)
                # Como executescript no devuelve filas, hacemos un fetch manual simple para verificar login
                # Nota: Para simplificar la demo visual usamos execute normal si no hay punto y coma
                if ';' not in username: 
                    cursor.execute(query)
                    user = cursor.fetchone()
                else:
                    user = None
                    result_msg = "⚠️ Sentencia inyectada ejecutada (Posible Blind/Destructive)"
            except Exception as e:
                user = None
                result_msg = f"❌ Error SQL: {e}"
        else:
            # ✅ SEGURO: Parametrizado
            query = "SELECT * FROM usuarios WHERE username = ? AND password = ?"
            query_log = f"QUERY: {query} | PARAMS: ('{username}', '{password}')"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()

        if user:
            result_msg = f"🔓 ¡Bienvenido! Has entrado como: {user['username']}"
            status = "success"
        elif not result_msg: # Si no hubo error previo
            result_msg = "🔒 Acceso Denegado"
            status = "danger"

    return render_template('index.html', query_log=query_log, result_msg=result_msg, status=status, mode=mode)

if __name__ == '__main__':
    # Inicializar BD si no existe
    if not os.path.exists(DB_PATH):
        import db_init
        db_init.crear_bd()
    app.run(host='0.0.0.0', port=5000, debug=True)