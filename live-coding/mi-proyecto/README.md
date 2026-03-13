# 📝 Foro de Mensajes - Aplicación Web Segura

Aplicación web de foro público donde los usuarios pueden registrarse, iniciar sesión y publicar mensajes. Desarrollada con Python/Flask (backend) y HTML/CSS/JavaScript (frontend).

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Requisitos](#-requisitos)
- [Instalación y Despliegue](#-instalación-y-despliegue)
- [Uso de la Aplicación](#-uso-de-la-aplicación)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Seguridad](#-seguridad)
- [Tecnologías](#-tecnologías)
- [Solución de Problemas](#-solución-de-problemas)

---

## ✨ Características

### Funcionalidades Principales
- ✅ **Registro de usuarios** con validación de contraseña segura
- ✅ **Inicio de sesión** con autenticación segura
- ✅ **Foro público** visible para todos (con o sin login)
- ✅ **Publicar mensajes** (requiere autenticación)
- ✅ **Editar mensajes propios**
- ✅ **Eliminar mensajes propios**
- ✅ **Vista "Mis Mensajes"** para gestionar tus publicaciones
- ✅ **Cierre de sesión automático** al cerrar el navegador

### Características de Seguridad
- 🔒 Contraseñas hasheadas con bcrypt (cost factor 12)
- 🔒 Validación de contraseña en tiempo real (8+ caracteres, mayúscula, minúscula, número)
- 🔒 Sesiones seguras (HttpOnly, SameSite, no persistentes)
- 🔒 Protección contra SQL Injection (consultas parametrizadas)
- 🔒 Protección contra XSS (escape de HTML)
- 🔒 Protección contra CSRF (CORS configurado)
- 🔒 Autorización: solo el autor puede editar/eliminar sus mensajes
- 🔒 Timeout de inactividad (30 minutos)

### Experiencia de Usuario
- 🎨 Diseño moderno y responsive
- 🎨 Validaciones visuales en tiempo real
- 🎨 Feedback inmediato de errores
- 🎨 Navegación por rutas (#inicio, #login, #registro, #foro, #mis-mensajes)

---

## 📦 Requisitos

### Software Necesario
- **Python 3.8+** (recomendado 3.11)
- **pip** (gestor de paquetes de Python)

### Dependencias Python
```
Flask==2.3.0
Flask-CORS==4.0.0
bcrypt==4.0.1
```

---

## 🚀 Instalación y Despliegue

### Opción 1: Despliegue Manual (Recomendado para Desarrollo)

#### Paso 1: Clonar o Descargar el Proyecto
```bash
cd live-coding/mi-proyecto
```

#### Paso 2: Instalar Dependencias del Backend
```bash
cd backend-python
pip install Flask Flask-CORS bcrypt
```

#### Paso 3: Iniciar el Backend
```bash
python app.py
```

El backend estará corriendo en: **http://localhost:3000**

Deberías ver:
```
✅ Base de datos SQLite inicializada
🚀 Servidor corriendo en http://localhost:3000
📝 Presiona Ctrl+C para detener
💾 Usando SQLite - Base de datos: database.db
```

#### Paso 4: Iniciar el Frontend (Nueva Terminal)
```bash
cd frontend
python -m http.server 8000
```

El frontend estará corriendo en: **http://localhost:8000**

#### Paso 5: Acceder a la Aplicación
Abre tu navegador y ve a: **http://localhost:8000**

---

### Opción 2: Despliegue con Docker

#### Requisitos
- Docker instalado
- Docker Compose instalado

#### Paso 1: Construir y Levantar los Contenedores
```bash
cd live-coding/mi-proyecto
docker-compose up --build
```

#### Paso 2: Acceder a la Aplicación
Abre tu navegador y ve a: **http://localhost:8000**

#### Detener los Contenedores
```bash
docker-compose down
```

---

## 📖 Uso de la Aplicación

### 1. Registro de Usuario

1. Ve a **http://localhost:8000**
2. Haz clic en **"Registrarse"** en el header
3. Completa el formulario:
   - **Email**: tu@email.com
   - **Contraseña**: Mínimo 8 caracteres, incluye mayúscula, minúscula y número
   - **Confirmar Contraseña**: Repite la contraseña

**Validaciones en Tiempo Real:**
- ✓ Mínimo 8 caracteres
- ✓ Al menos una mayúscula (A-Z)
- ✓ Al menos una minúscula (a-z)
- ✓ Al menos un número (0-9)
- ✓ Las contraseñas coinciden

4. Haz clic en **"Registrarse"**
5. Serás redirigido al login automáticamente

### 2. Iniciar Sesión

1. Ve a **http://localhost:8000/#login**
2. Ingresa tu email y contraseña
3. Haz clic en **"Iniciar Sesión"**
4. Serás redirigido al home con todos los mensajes del foro

### 3. Ver el Foro Público

- **Sin login**: Puedes ver todos los mensajes pero no publicar
- **Con login**: Puedes ver y publicar mensajes
- Los mensajes muestran: autor, fecha y contenido

### 4. Publicar un Mensaje

1. Inicia sesión
2. Haz clic en **"Foro de Mensajes"** en el header (o ve a #foro)
3. Escribe tu mensaje (máximo 500 caracteres)
4. Haz clic en **"Publicar"**
5. Serás redirigido al home donde verás tu mensaje

### 5. Editar un Mensaje

1. Ve a **"Mis Mensajes"** en el header
2. Verás todos tus mensajes
3. Haz clic en **"✏️ Editar"** en el mensaje que quieras modificar
4. Modifica el texto
5. Haz clic en **"Actualizar"**

### 6. Eliminar un Mensaje

1. Ve a **"Mis Mensajes"**
2. Haz clic en **"🗑️ Eliminar"** en el mensaje que quieras borrar
3. Confirma la eliminación
4. El mensaje se eliminará permanentemente

### 7. Cerrar Sesión

**Opción 1: Manual**
- Haz clic en **"Cerrar Sesión"** en el header

**Opción 2: Automática**
- Cierra la pestaña o el navegador
- La sesión se cerrará automáticamente

---

## 📁 Estructura del Proyecto

```
mi-proyecto/
├── backend-python/          # Backend Flask
│   ├── app.py              # Aplicación principal
│   ├── database.db         # Base de datos SQLite (se crea automáticamente)
│   ├── requirements.txt    # Dependencias Python
│   └── ver_db.py          # Script para ver la base de datos
│
├── frontend/               # Frontend HTML/CSS/JS
│   ├── index.html         # Página principal
│   ├── script.js          # Lógica de la aplicación
│   └── style.css          # Estilos
│
├── docker-compose.yml     # Configuración Docker Compose
├── .gitignore            # Archivos ignorados por Git
└── README.md             # Este archivo
```

---

## 🔐 Seguridad

### Autenticación y Autorización

#### Contraseñas Seguras
- Hasheadas con **bcrypt** (cost factor 12)
- Nunca se almacenan en texto plano
- Requisitos de fortaleza:
  - Mínimo 8 caracteres
  - Al menos una mayúscula
  - Al menos una minúscula
  - Al menos un número

#### Sesiones Seguras
- **HttpOnly**: Las cookies no son accesibles desde JavaScript
- **SameSite=Lax**: Protección contra CSRF
- **No persistentes**: Se eliminan al cerrar el navegador
- **Timeout**: 30 minutos de inactividad

#### Autorización
- Solo el autor puede editar/eliminar sus mensajes
- Verificación en backend (no se confía en frontend)
- Mensajes de error genéricos (no revelan información)

### Protección contra Ataques

#### SQL Injection
```python
# ✅ CORRECTO: Consultas parametrizadas
cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))

# ❌ INCORRECTO: Concatenación directa
cursor.execute(f'SELECT * FROM usuarios WHERE email = "{email}"')
```

#### XSS (Cross-Site Scripting)
```javascript
// ✅ CORRECTO: Escape de HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
```

#### CSRF (Cross-Site Request Forgery)
- CORS configurado con orígenes específicos
- Cookies con SameSite=Lax
- Credenciales requeridas en todas las peticiones

### Validación de Datos

#### Backend (Nunca confiar en frontend)
- Email: formato regex + normalización + longitud máx 255
- Contraseña: fortaleza validada
- Mensajes: 1-500 caracteres + sanitización
- IDs: validación de tipo y rango

#### Frontend (UX)
- Validación en tiempo real
- Feedback visual inmediato
- Prevención de errores

---

## 🛠️ Tecnologías

### Backend
- **Python 3.11**: Lenguaje de programación
- **Flask 2.3**: Framework web
- **SQLite**: Base de datos
- **bcrypt**: Hashing de contraseñas
- **Flask-CORS**: Manejo de CORS

### Frontend
- **HTML5**: Estructura
- **CSS3**: Estilos (con Pico.css)
- **JavaScript ES6+**: Lógica
- **Fetch API**: Comunicación con backend

### Infraestructura
- **Docker**: Contenedorización
- **Docker Compose**: Orquestación

---

## 🐛 Solución de Problemas

### El backend no inicia

**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solución**:
```bash
cd backend-python
pip install Flask Flask-CORS bcrypt
```

---

### El frontend no carga

**Error**: `Failed to fetch` o errores de CORS

**Solución**:
1. Verifica que el backend esté corriendo en puerto 3000
2. Verifica que el frontend esté corriendo en puerto 8000
3. Revisa la consola del navegador (F12) para más detalles

---

### No puedo iniciar sesión

**Error**: "Credenciales inválidas"

**Solución**:
1. Verifica que el email esté registrado
2. Verifica que la contraseña sea correcta
3. Si olvidaste la contraseña, registra un nuevo usuario

---

### La sesión no se cierra al cerrar el navegador

**Solución**:
1. Asegúrate de cerrar **completamente** el navegador (no solo la pestaña)
2. Verifica que no haya otras pestañas abiertas con la aplicación
3. Limpia las cookies del navegador (F12 → Application → Cookies)

---

### Error al publicar mensaje

**Error**: "No autenticado"

**Solución**:
1. Verifica que hayas iniciado sesión
2. Si la sesión expiró (30 min), inicia sesión de nuevo
3. Recarga la página (F5)

---

### La base de datos está corrupta

**Solución**:
```bash
cd backend-python
rm database.db
python app.py
```
Esto creará una nueva base de datos vacía.

---

### Ver el contenido de la base de datos

```bash
cd backend-python
python ver_db.py
```

Esto mostrará:
- Lista de usuarios (email, fecha de registro)
- Lista de mensajes (autor, texto, fecha)
- Estadísticas

---

## 📊 API Endpoints

### Autenticación

#### POST `/api/registro`
Registrar un nuevo usuario.

**Body**:
```json
{
  "email": "usuario@email.com",
  "password": "Password123",
  "confirmPassword": "Password123"
}
```

**Respuesta exitosa** (201):
```json
{
  "message": "Usuario registrado exitosamente"
}
```

---

#### POST `/api/login`
Iniciar sesión.

**Body**:
```json
{
  "email": "usuario@email.com",
  "password": "Password123"
}
```

**Respuesta exitosa** (200):
```json
{
  "message": "Login exitoso",
  "email": "usuario@email.com"
}
```

---

#### POST `/api/logout`
Cerrar sesión (requiere autenticación).

**Respuesta exitosa** (200):
```json
{
  "message": "Sesión cerrada exitosamente"
}
```

---

#### GET `/api/session`
Verificar estado de sesión.

**Respuesta exitosa** (200):
```json
{
  "authenticated": true,
  "email": "usuario@email.com"
}
```

---

### Mensajes

#### GET `/api/mensajes`
Obtener todos los mensajes del foro (público).

**Respuesta exitosa** (200):
```json
[
  {
    "id": 1,
    "texto": "Hola mundo",
    "autor": "usuario@email.com",
    "created_at": "2026-03-13 10:30:00"
  }
]
```

---

#### POST `/api/mensajes`
Publicar un nuevo mensaje (requiere autenticación).

**Body**:
```json
{
  "texto": "Mi mensaje aquí"
}
```

**Respuesta exitosa** (201):
```json
{
  "id": 2,
  "texto": "Mi mensaje aquí",
  "autor": "usuario@email.com",
  "created_at": "2026-03-13 10:35:00"
}
```

---

#### PUT `/api/mensajes/:id`
Editar un mensaje propio (requiere autenticación).

**Body**:
```json
{
  "texto": "Mensaje editado"
}
```

**Respuesta exitosa** (200):
```json
{
  "id": 2,
  "texto": "Mensaje editado",
  "autor": "usuario@email.com",
  "created_at": "2026-03-13 10:35:00"
}
```

---

#### DELETE `/api/mensajes/:id`
Eliminar un mensaje propio (requiere autenticación).

**Respuesta exitosa** (200):
```json
{
  "message": "Mensaje eliminado exitosamente"
}
```

---

#### GET `/api/mis-mensajes`
Obtener solo los mensajes del usuario autenticado (requiere autenticación).

**Respuesta exitosa** (200):
```json
[
  {
    "id": 2,
    "texto": "Mi mensaje",
    "autor": "usuario@email.com",
    "created_at": "2026-03-13 10:35:00"
  }
]
```

---

## 📝 Notas Adicionales

### Base de Datos
- **SQLite**: Base de datos local en archivo `database.db`
- Se crea automáticamente al iniciar el backend
- Tablas: `usuarios` y `mensajes`

### Puertos
- **Backend**: 3000
- **Frontend**: 8000

### Límites
- **Email**: Máximo 255 caracteres
- **Contraseña**: 8-128 caracteres
- **Mensaje**: 1-500 caracteres
- **Mensajes por consulta**: 100 (para prevenir sobrecarga)

### Sesión
- **Duración**: Hasta cerrar el navegador
- **Timeout de inactividad**: 30 minutos
- **Cierre automático**: Al cerrar pestaña/navegador

---

## 🎓 Créditos

Proyecto desarrollado para el hackathon DAM/DAW.

**Requisitos cumplidos**:
- ✅ Registro y login con contraseñas hasheadas
- ✅ Foro público de mensajes
- ✅ Editar y eliminar mensajes propios
- ✅ Validación en backend
- ✅ Protección contra ataques comunes
- ✅ Manejo de errores apropiado
- ✅ Despliegue con Docker

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible para fines educativos.

---

**Versión**: 2.1  
**Fecha**: 13 de marzo de 2026  
**Estado**: ✅ Producción Ready
