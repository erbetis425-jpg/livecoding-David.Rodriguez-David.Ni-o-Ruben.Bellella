import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

print("=" * 80)
print("📊 BASE DE DATOS - FORO DE MENSAJES")
print("=" * 80)

# Ver usuarios
print("\n👥 USUARIOS:")
print("-" * 80)
cursor.execute('SELECT id, email, password, created_at FROM usuarios')
usuarios = cursor.fetchall()

if usuarios:
    print(f"{'ID':<5} {'Email':<30} {'Password (hash)':<35} {'Fecha':<20}")
    print("-" * 80)
    for row in usuarios:
        # Convertir bytes a string si es necesario
        password = row[2]
        if isinstance(password, bytes):
            password = password.decode('utf-8', errors='ignore')
        password_hash = password[:32] + "..." if len(password) > 32 else password
        print(f"{row[0]:<5} {row[1]:<30} {password_hash:<35} {row[3]:<20}")
    print(f"\nTotal usuarios: {len(usuarios)}")
else:
    print("No hay usuarios registrados")

# Ver mensajes
print("\n" + "=" * 80)
print("💬 MENSAJES:")
print("-" * 80)
cursor.execute('''
    SELECT m.id, u.email, m.texto, m.created_at 
    FROM mensajes m 
    JOIN usuarios u ON m.user_id = u.id 
    ORDER BY m.created_at DESC
''')
mensajes = cursor.fetchall()

if mensajes:
    print(f"{'ID':<5} {'Autor':<25} {'Mensaje':<35} {'Fecha':<20}")
    print("-" * 80)
    for row in mensajes:
        mensaje_corto = row[2][:32] + "..." if len(row[2]) > 32 else row[2]
        print(f"{row[0]:<5} {row[1]:<25} {mensaje_corto:<35} {row[3]:<20}")
    print(f"\nTotal mensajes: {len(mensajes)}")
else:
    print("No hay mensajes publicados")

print("\n" + "=" * 80)

# Estadísticas
cursor.execute('SELECT COUNT(*) FROM usuarios')
total_usuarios = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM mensajes')
total_mensajes = cursor.fetchone()[0]

print("📈 ESTADÍSTICAS:")
print(f"  - Total usuarios: {total_usuarios}")
print(f"  - Total mensajes: {total_mensajes}")
if total_usuarios > 0:
    print(f"  - Promedio mensajes por usuario: {total_mensajes / total_usuarios:.2f}")

print("=" * 80)

conn.close()
