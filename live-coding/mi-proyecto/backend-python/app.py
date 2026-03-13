from flask import Flask, request, jsonify, session
from flask_cors import CORS
import sqlite3
import bcrypt
import os
import re
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'mi-secreto-super-seguro-cambiar-en-produccion')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # True en producción con HTTPS
# Sesión no persistente: se cierra al cerrar el navegador
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Timeout de inactividad

# Configurar CORS
CORS(app, supports_credentials=True, origins=['http://localhost:8000', 'http://127.0.0.1:8000'])

# Base de datos SQLite
DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            texto TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES usuarios(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Base de datos SQLite inicializada")

# Inicializar base de datos
init_db()

# Utilidades de validación
def validate_email(email):
    """Valida formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_text(text):
    """Sanitiza texto para prevenir XSS básico"""
    if not text:
        return text
    # Eliminar caracteres peligrosos
    text = text.strip()
    return text

def validate_password_strength(password):
    """Valida que la contraseña sea segura"""
    if len(password) < 8:
        return False, 'La contraseña debe tener al menos 8 caracteres'
    if not re.search(r'[A-Z]', password):
        return False, 'La contraseña debe contener al menos una mayúscula'
    if not re.search(r'[a-z]', password):
        return False, 'La contraseña debe contener al menos una minúscula'
    if not re.search(r'[0-9]', password):
        return False, 'La contraseña debe contener al menos un número'
    return True, 'Contraseña válida'

# Middleware de autenticación
def require_auth(f):
    """Decorador para proteger rutas que requieren autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'No autenticado. Por favor inicia sesión.'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Manejador de errores global
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Recurso no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

@app.errorhandler(Exception)
def handle_exception(error):
    # No exponer detalles del error en producción
    app.logger.error(f'Error no manejado: {str(error)}')
    return jsonify({'error': 'Ha ocurrido un error. Por favor intenta de nuevo.'}), 500

# RUTAS DE AUTENTICACIÓN

@app.route('/api/registro', methods=['POST'])
def registro():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Datos inválidos'}), 400
            
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        confirm_password = data.get('confirmPassword', '')
        
        # Validaciones
        if not email or not password or not confirm_password:
            return jsonify({'error': 'Todos los campos son obligatorios'}), 400
        
        # Validar formato de email
        if not validate_email(email):
            return jsonify({'error': 'Formato de email inválido'}), 400
        
        # Validar longitud de email
        if len(email) > 255:
            return jsonify({'error': 'El email es demasiado largo'}), 400
        
        if password != confirm_password:
            return jsonify({'error': 'Las contraseñas no coinciden'}), 400
        
        # Validar fortaleza de contraseña
        is_valid, message = validate_password_strength(password)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Verificar si el email ya existe
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM usuarios WHERE email = ?', (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            conn.close()
            return jsonify({'error': 'El email ya está registrado'}), 400
        
        # Hash de la contraseña con bcrypt (cost factor 12)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
        
        # Insertar usuario
        cursor.execute('INSERT INTO usuarios (email, password) VALUES (?, ?)', 
                      (email, hashed_password))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        app.logger.info(f'Nuevo usuario registrado: {email}')
        return jsonify({'message': 'Usuario registrado exitosamente'}), 201
    
    except sqlite3.Error as e:
        app.logger.error(f'Error de base de datos en registro: {e}')
        return jsonify({'error': 'Error al registrar usuario'}), 500
    except Exception as e:
        app.logger.error(f'Error en registro: {e}')
        return jsonify({'error': 'Error al registrar usuario'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Datos inválidos'}), 400
            
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'error': 'Email y contraseña son obligatorios'}), 400
        
        # Validar formato de email
        if not validate_email(email):
            return jsonify({'error': 'Credenciales inválidas'}), 401
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT id, email, password FROM usuarios WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        
        # Mensaje genérico para no revelar si el usuario existe
        if not user:
            return jsonify({'error': 'Credenciales inválidas'}), 401
        
        user_id, user_email, hashed_password = user
        
        # Verificar contraseña
        if not bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            return jsonify({'error': 'Credenciales inválidas'}), 401
        
        # Regenerar ID de sesión para prevenir session fixation
        session.clear()
        session['user_id'] = user_id
        session['user_email'] = user_email
        # Sesión no persistente: se cierra al cerrar el navegador
        session.permanent = False
        
        app.logger.info(f'Usuario autenticado: {user_email}')
        return jsonify({'message': 'Login exitoso', 'email': user_email}), 200
    
    except sqlite3.Error as e:
        app.logger.error(f'Error de base de datos en login: {e}')
        return jsonify({'error': 'Error al iniciar sesión'}), 500
    except Exception as e:
        app.logger.error(f'Error en login: {e}')
        return jsonify({'error': 'Error al iniciar sesión'}), 500

@app.route('/api/logout', methods=['POST'])
@require_auth
def logout():
    user_email = session.get('user_email', 'unknown')
    session.clear()
    app.logger.info(f'Usuario desconectado: {user_email}')
    return jsonify({'message': 'Sesión cerrada exitosamente'}), 200

@app.route('/api/session', methods=['GET'])
def check_session():
    if 'user_id' in session:
        return jsonify({'authenticated': True, 'email': session.get('user_email')}), 200
    else:
        return jsonify({'authenticated': False}), 200

# RUTAS DE MENSAJES

@app.route('/api/mensajes', methods=['GET'])
def get_mensajes():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Limitar resultados para prevenir sobrecarga
        cursor.execute('''
            SELECT m.id, m.texto, m.created_at, u.email as autor
            FROM mensajes m
            JOIN usuarios u ON m.user_id = u.id
            ORDER BY m.created_at DESC
            LIMIT 100
        ''')
        
        mensajes = []
        for row in cursor.fetchall():
            # Solo devolver datos necesarios, sin información sensible
            mensajes.append({
                'id': row[0],
                'texto': row[1],
                'created_at': row[2],
                'autor': row[3]
            })
        
        conn.close()
        return jsonify(mensajes), 200
    
    except sqlite3.Error as e:
        app.logger.error(f'Error de base de datos al obtener mensajes: {e}')
        return jsonify({'error': 'Error al obtener mensajes'}), 500
    except Exception as e:
        app.logger.error(f'Error al obtener mensajes: {e}')
        return jsonify({'error': 'Error al obtener mensajes'}), 500

@app.route('/api/mensajes', methods=['POST'])
@require_auth
def post_mensaje():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Datos inválidos'}), 400
            
        texto = sanitize_text(data.get('texto', ''))
        
        if not texto:
            return jsonify({'error': 'El mensaje no puede estar vacío'}), 400
        
        if len(texto) < 1:
            return jsonify({'error': 'El mensaje es demasiado corto'}), 400
        
        if len(texto) > 500:
            return jsonify({'error': 'El mensaje no puede exceder 500 caracteres'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO mensajes (user_id, texto) VALUES (?, ?)', 
                      (session['user_id'], texto))
        conn.commit()
        mensaje_id = cursor.lastrowid
        
        # Obtener el mensaje completo (sin exponer datos sensibles)
        cursor.execute('''
            SELECT m.id, m.texto, m.created_at, u.email as autor
            FROM mensajes m
            JOIN usuarios u ON m.user_id = u.id
            WHERE m.id = ?
        ''', (mensaje_id,))
        
        row = cursor.fetchone()
        mensaje = {
            'id': row[0],
            'texto': row[1],
            'created_at': row[2],
            'autor': row[3]
        }
        
        conn.close()
        app.logger.info(f'Mensaje publicado por usuario {session["user_email"]}')
        return jsonify(mensaje), 201
    
    except sqlite3.Error as e:
        app.logger.error(f'Error de base de datos al publicar mensaje: {e}')
        return jsonify({'error': 'Error al publicar mensaje'}), 500
    except Exception as e:
        app.logger.error(f'Error al publicar mensaje: {e}')
        return jsonify({'error': 'Error al publicar mensaje'}), 500

@app.route('/api/mensajes/<int:mensaje_id>', methods=['DELETE'])
@require_auth
def delete_mensaje(mensaje_id):
    try:
        # Validar que el ID sea positivo
        if mensaje_id <= 0:
            return jsonify({'error': 'ID de mensaje inválido'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM mensajes WHERE id = ?', (mensaje_id,))
        mensaje = cursor.fetchone()
        
        if not mensaje:
            conn.close()
            return jsonify({'error': 'Mensaje no encontrado'}), 404
        
        # Verificar autorización: solo el autor puede eliminar
        if mensaje[0] != session['user_id']:
            conn.close()
            app.logger.warning(f'Usuario {session["user_email"]} intentó eliminar mensaje ajeno')
            return jsonify({'error': 'No tienes permiso para eliminar este mensaje'}), 403
        
        cursor.execute('DELETE FROM mensajes WHERE id = ?', (mensaje_id,))
        conn.commit()
        conn.close()
        
        app.logger.info(f'Mensaje {mensaje_id} eliminado por {session["user_email"]}')
        return jsonify({'message': 'Mensaje eliminado exitosamente'}), 200
    
    except sqlite3.Error as e:
        app.logger.error(f'Error de base de datos al eliminar mensaje: {e}')
        return jsonify({'error': 'Error al eliminar mensaje'}), 500
    except Exception as e:
        app.logger.error(f'Error al eliminar mensaje: {e}')
        return jsonify({'error': 'Error al eliminar mensaje'}), 500

@app.route('/api/mensajes/<int:mensaje_id>', methods=['PUT'])
@require_auth
def update_mensaje(mensaje_id):
    try:
        # Validar que el ID sea positivo
        if mensaje_id <= 0:
            return jsonify({'error': 'ID de mensaje inválido'}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Datos inválidos'}), 400
            
        texto = sanitize_text(data.get('texto', ''))
        
        if not texto:
            return jsonify({'error': 'El mensaje no puede estar vacío'}), 400
        
        if len(texto) < 1:
            return jsonify({'error': 'El mensaje es demasiado corto'}), 400
        
        if len(texto) > 500:
            return jsonify({'error': 'El mensaje no puede exceder 500 caracteres'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM mensajes WHERE id = ?', (mensaje_id,))
        mensaje = cursor.fetchone()
        
        if not mensaje:
            conn.close()
            return jsonify({'error': 'Mensaje no encontrado'}), 404
        
        # Verificar autorización: solo el autor puede editar
        if mensaje[0] != session['user_id']:
            conn.close()
            app.logger.warning(f'Usuario {session["user_email"]} intentó editar mensaje ajeno')
            return jsonify({'error': 'No tienes permiso para editar este mensaje'}), 403
        
        cursor.execute('UPDATE mensajes SET texto = ? WHERE id = ?', (texto, mensaje_id))
        conn.commit()
        
        # Obtener el mensaje actualizado (sin exponer datos sensibles)
        cursor.execute('''
            SELECT m.id, m.texto, m.created_at, u.email as autor
            FROM mensajes m
            JOIN usuarios u ON m.user_id = u.id
            WHERE m.id = ?
        ''', (mensaje_id,))
        
        row = cursor.fetchone()
        mensaje_actualizado = {
            'id': row[0],
            'texto': row[1],
            'created_at': row[2],
            'autor': row[3]
        }
        
        conn.close()
        app.logger.info(f'Mensaje {mensaje_id} editado por {session["user_email"]}')
        return jsonify(mensaje_actualizado), 200
    
    except sqlite3.Error as e:
        app.logger.error(f'Error de base de datos al editar mensaje: {e}')
        return jsonify({'error': 'Error al editar mensaje'}), 500
    except Exception as e:
        app.logger.error(f'Error al editar mensaje: {e}')
        return jsonify({'error': 'Error al editar mensaje'}), 500

@app.route('/api/mis-mensajes', methods=['GET'])
@require_auth
def get_mis_mensajes():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Solo devolver mensajes del usuario autenticado
        cursor.execute('''
            SELECT m.id, m.texto, m.created_at, u.email as autor
            FROM mensajes m
            JOIN usuarios u ON m.user_id = u.id
            WHERE m.user_id = ?
            ORDER BY m.created_at DESC
            LIMIT 100
        ''', (session['user_id'],))
        
        mensajes = []
        for row in cursor.fetchall():
            mensajes.append({
                'id': row[0],
                'texto': row[1],
                'created_at': row[2],
                'autor': row[3]
            })
        
        conn.close()
        return jsonify(mensajes), 200
    
    except sqlite3.Error as e:
        app.logger.error(f'Error de base de datos al obtener mis mensajes: {e}')
        return jsonify({'error': 'Error al obtener mensajes'}), 500
    except Exception as e:
        app.logger.error(f'Error al obtener mis mensajes: {e}')
        return jsonify({'error': 'Error al obtener mensajes'}), 500

if __name__ == '__main__':
    print('🚀 Servidor corriendo en http://localhost:3000')
    print('📝 Presiona Ctrl+C para detener')
    print('💾 Usando SQLite - Base de datos: database.db')
    app.run(host='0.0.0.0', port=3000, debug=True)
