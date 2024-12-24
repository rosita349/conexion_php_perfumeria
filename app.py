from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# Configuración de PostgreSQL
DB_HOST = "localhost"
DB_NAME = "DB_Perfumeria"
DB_USER = "postgres"
DB_PASSWORD = "12345"

# Conexión a la base de datos
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Ruta para obtener todos los usuarios
@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT id, username, email, fecha_registro FROM usuarios")
                usuarios = cursor.fetchall()
        return jsonify(usuarios)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para agregar un nuevo usuario
@app.route('/usuarios', methods=['POST'])
def add_usuario():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Datos incompletos"}), 400

    hashed_password = generate_password_hash(password)

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO usuarios (username, email, password) VALUES (%s, %s, %s)",
                    (username, email, hashed_password)
                )
                conn.commit()
        return jsonify({"message": "Usuario agregado con éxito"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para actualizar un usuario
@app.route('/usuarios/<int:id>', methods=['PUT'])
def update_usuario(id):
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Datos incompletos"}), 400

    hashed_password = generate_password_hash(password)

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE usuarios SET username = %s, email = %s, password = %s WHERE id = %s",
                    (username, email, hashed_password, id)
                )
                conn.commit()
        return jsonify({"message": "Usuario actualizado con éxito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para eliminar un usuario
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
                conn.commit()
        return jsonify({"message": "Usuario eliminado con éxito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
