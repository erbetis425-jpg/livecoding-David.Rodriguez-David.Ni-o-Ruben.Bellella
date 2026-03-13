const API_URL = 'http://localhost:3000/api';

let currentUser = null;
let editingMessageId = null;

// Elementos del DOM
const homeSection = document.getElementById('home-section');
const loginSection = document.getElementById('login-section');
const registroSection = document.getElementById('registro-section');
const foroSection = document.getElementById('foro-section');
const misMensajesSection = document.getElementById('mis-mensajes-section');

const loginForm = document.getElementById('login-form');
const registroForm = document.getElementById('registro-form');
const mensajeForm = document.getElementById('mensaje-form');

const homeMensajesLista = document.getElementById('home-mensajes-lista');
const misMensajesLista = document.getElementById('mis-mensajes-lista');

const loginMessage = document.getElementById('login-message');
const registroMessage = document.getElementById('registro-message');

const btnLogout = document.getElementById('btn-logout');
const navLoginLink = document.getElementById('nav-login-link');
const navRegistroLink = document.getElementById('nav-registro-link');
const navMisMensajesLink = document.getElementById('nav-mis-mensajes-link');
const navUserInfo = document.getElementById('nav-user-info');
const userEmail = document.getElementById('user-email');

const mensajeTexto = document.getElementById('mensaje-texto');
const charCount = document.getElementById('char-count');
const btnSubmitMensaje = document.getElementById('btn-submit-mensaje');
const btnCancelEdit = document.getElementById('btn-cancel-edit');
const foroHeaderTitle = document.getElementById('foro-header-title');

// Sistema de rutas
function navigate(route) {
    // Ocultar todas las secciones
    homeSection.style.display = 'none';
    loginSection.style.display = 'none';
    registroSection.style.display = 'none';
    foroSection.style.display = 'none';
    misMensajesSection.style.display = 'none';
    
    // Mostrar sección según ruta
    switch(route) {
        case 'inicio':
        case '':
            homeSection.style.display = 'block';
            loadPublicMensajes();
            break;
        case 'login':
            if (currentUser) {
                navigate('foro');
            } else {
                loginSection.style.display = 'block';
            }
            break;
        case 'registro':
            if (currentUser) {
                navigate('foro');
            } else {
                registroSection.style.display = 'block';
            }
            break;
        case 'foro':
            if (currentUser) {
                foroSection.style.display = 'block';
            } else {
                navigate('login');
            }
            break;
        case 'mis-mensajes':
            if (currentUser) {
                misMensajesSection.style.display = 'block';
                loadMisMensajes();
            } else {
                navigate('login');
            }
            break;
        default:
            navigate('inicio');
    }
    
    updateNav();
}

// Actualizar navegación según estado de autenticación
function updateNav() {
    if (currentUser) {
        navLoginLink.style.display = 'none';
        navRegistroLink.style.display = 'none';
        navMisMensajesLink.style.display = 'block';
        navUserInfo.style.display = 'block';
        userEmail.textContent = currentUser;
    } else {
        navLoginLink.style.display = 'block';
        navRegistroLink.style.display = 'block';
        navMisMensajesLink.style.display = 'none';
        navUserInfo.style.display = 'none';
    }
}

// Manejar cambios de hash
window.addEventListener('hashchange', () => {
    const hash = window.location.hash.slice(1);
    const route = hash === '/' || hash === '' ? 'inicio' : hash.replace('/', '');
    navigate(route);
});

// Verificar sesión al cargar
checkSession();

// Limpiar sesión al cerrar la ventana/pestaña
window.addEventListener('beforeunload', async () => {
    // Cerrar sesión en el servidor
    try {
        await fetch(`${API_URL}/logout`, {
            method: 'POST',
            credentials: 'include',
            keepalive: true  // Asegura que la petición se complete aunque se cierre la ventana
        });
    } catch (error) {
        console.error('Error al cerrar sesión automáticamente:', error);
    }
});

// Botón cancelar edición
btnCancelEdit.addEventListener('click', () => {
    cancelEdit();
});

// Contador de caracteres
if (mensajeTexto) {
    mensajeTexto.addEventListener('input', () => {
        charCount.textContent = `${mensajeTexto.value.length}/500 caracteres`;
    });
}

// Validación de contraseña en tiempo real
const registroPassword = document.getElementById('registro-password');
const registroConfirm = document.getElementById('registro-confirm');
const reqLength = document.getElementById('req-length');
const reqUppercase = document.getElementById('req-uppercase');
const reqLowercase = document.getElementById('req-lowercase');
const reqNumber = document.getElementById('req-number');
const passwordMatch = document.getElementById('password-match');

if (registroPassword) {
    registroPassword.addEventListener('input', () => {
        const password = registroPassword.value;
        
        // Validar longitud
        if (password.length >= 8) {
            reqLength.classList.add('valid');
            reqLength.classList.remove('invalid');
        } else {
            reqLength.classList.add('invalid');
            reqLength.classList.remove('valid');
        }
        
        // Validar mayúscula
        if (/[A-Z]/.test(password)) {
            reqUppercase.classList.add('valid');
            reqUppercase.classList.remove('invalid');
        } else {
            reqUppercase.classList.add('invalid');
            reqUppercase.classList.remove('valid');
        }
        
        // Validar minúscula
        if (/[a-z]/.test(password)) {
            reqLowercase.classList.add('valid');
            reqLowercase.classList.remove('invalid');
        } else {
            reqLowercase.classList.add('invalid');
            reqLowercase.classList.remove('valid');
        }
        
        // Validar número
        if (/[0-9]/.test(password)) {
            reqNumber.classList.add('valid');
            reqNumber.classList.remove('invalid');
        } else {
            reqNumber.classList.add('invalid');
            reqNumber.classList.remove('valid');
        }
        
        // Verificar coincidencia de contraseñas
        checkPasswordMatch();
    });
}

if (registroConfirm) {
    registroConfirm.addEventListener('input', checkPasswordMatch);
}

function checkPasswordMatch() {
    const password = registroPassword.value;
    const confirm = registroConfirm.value;
    
    if (confirm.length === 0) {
        passwordMatch.textContent = '';
        passwordMatch.classList.remove('match', 'no-match');
        return;
    }
    
    if (password === confirm) {
        passwordMatch.textContent = '✓ Las contraseñas coinciden';
        passwordMatch.classList.add('match');
        passwordMatch.classList.remove('no-match');
    } else {
        passwordMatch.textContent = '✗ Las contraseñas no coinciden';
        passwordMatch.classList.add('no-match');
        passwordMatch.classList.remove('match');
    }
}

// Login
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('login-email').value.trim();
    const password = document.getElementById('login-password').value;

    // Validaciones básicas en frontend
    if (!email || !password) {
        showMessage(loginMessage, 'Email y contraseña son obligatorios', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage(loginMessage, 'Login exitoso', 'success');
            currentUser = data.email;
            loginForm.reset();
            setTimeout(() => {
                window.location.hash = '#inicio';
            }, 500);
        } else {
            showMessage(loginMessage, data.error || 'Error al iniciar sesión', 'error');
        }
    } catch (error) {
        console.error('Error de conexión:', error);
        showMessage(loginMessage, 'Error de conexión con el servidor', 'error');
    }
});

// Registro
registroForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('registro-email').value.trim();
    const password = document.getElementById('registro-password').value;
    const confirmPassword = document.getElementById('registro-confirm').value;

    // Validaciones en frontend
    if (!email || !password || !confirmPassword) {
        showMessage(registroMessage, 'Todos los campos son obligatorios', 'error');
        return;
    }

    if (password !== confirmPassword) {
        showMessage(registroMessage, 'Las contraseñas no coinciden', 'error');
        return;
    }

    if (password.length < 8) {
        showMessage(registroMessage, 'La contraseña debe tener al menos 8 caracteres', 'error');
        return;
    }

    // Validar fortaleza de contraseña
    if (!/[A-Z]/.test(password)) {
        showMessage(registroMessage, 'La contraseña debe contener al menos una mayúscula', 'error');
        return;
    }

    if (!/[a-z]/.test(password)) {
        showMessage(registroMessage, 'La contraseña debe contener al menos una minúscula', 'error');
        return;
    }

    if (!/[0-9]/.test(password)) {
        showMessage(registroMessage, 'La contraseña debe contener al menos un número', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/registro`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ email, password, confirmPassword })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage(registroMessage, 'Registro exitoso. Redirigiendo a login...', 'success');
            registroForm.reset();
            setTimeout(() => {
                document.getElementById('login-email').value = email;
                window.location.hash = '#login';
            }, 1500);
        } else {
            showMessage(registroMessage, data.error || 'Error al registrar usuario', 'error');
        }
    } catch (error) {
        console.error('Error de conexión:', error);
        showMessage(registroMessage, 'Error de conexión con el servidor', 'error');
    }
});

// Publicar mensaje
mensajeForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const texto = mensajeTexto.value.trim();

    // Validaciones en frontend
    if (!texto) {
        alert('El mensaje no puede estar vacío');
        return;
    }

    if (texto.length < 1) {
        alert('El mensaje es demasiado corto');
        return;
    }

    if (texto.length > 500) {
        alert('El mensaje no puede exceder 500 caracteres');
        return;
    }

    try {
        let response;
        if (editingMessageId) {
            // Editar mensaje existente
            response = await fetch(`${API_URL}/mensajes/${editingMessageId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({ texto })
            });
        } else {
            // Crear nuevo mensaje
            response = await fetch(`${API_URL}/mensajes`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({ texto })
            });
        }

        if (response.ok) {
            cancelEdit();
            // Redirigir al home para ver el mensaje publicado
            window.location.hash = '#inicio';
        } else {
            const data = await response.json();
            alert(data.error || 'Error al procesar el mensaje');
            
            // Si no está autenticado, redirigir a login
            if (response.status === 401) {
                currentUser = null;
                window.location.hash = '#login';
            }
        }
    } catch (error) {
        console.error('Error de conexión:', error);
        alert('Error de conexión con el servidor');
    }
});

// Logout
btnLogout.addEventListener('click', async (e) => {
    e.preventDefault();
    try {
        await fetch(`${API_URL}/logout`, {
            method: 'POST',
            credentials: 'include'
        });
        currentUser = null;
        window.location.hash = '#inicio';
    } catch (error) {
        console.error('Error al cerrar sesión:', error);
        // Limpiar sesión local aunque falle el servidor
        currentUser = null;
        window.location.hash = '#inicio';
    }
});

// Verificar sesión
async function checkSession() {
    try {
        const response = await fetch(`${API_URL}/session`, {
            credentials: 'include'
        });
        const data = await response.json();

        if (data.authenticated) {
            currentUser = data.email;
        } else {
            // Asegurar que no hay sesión local
            currentUser = null;
        }
        
        // Navegar a la ruta actual
        const hash = window.location.hash.slice(1);
        const route = hash === '/' || hash === '' ? 'inicio' : hash.replace('/', '');
        navigate(route);
    } catch (error) {
        // Si hay error, limpiar sesión local
        currentUser = null;
        navigate('inicio');
    }
}

// Cargar mensajes públicos (home)
async function loadPublicMensajes() {
    try {
        const response = await fetch(`${API_URL}/mensajes`, {
            credentials: 'include'
        });
        
        if (!response.ok) {
            throw new Error('Error al cargar mensajes');
        }
        
        const mensajes = await response.json();

        if (mensajes.length === 0) {
            homeMensajesLista.innerHTML = '<p>No hay mensajes aún. <a href="#login">Inicia sesión</a> para ser el primero en publicar.</p>';
            return;
        }

        homeMensajesLista.innerHTML = mensajes.map(msg => `
            <div class="mensaje-item">
                <div class="mensaje-header">
                    <span class="mensaje-autor">${escapeHtml(msg.autor)}</span>
                    <span class="mensaje-fecha">${formatDate(msg.created_at)}</span>
                </div>
                <div class="mensaje-texto">${escapeHtml(msg.texto)}</div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error al cargar mensajes:', error);
        homeMensajesLista.innerHTML = '<p class="error">Error al cargar mensajes. Por favor intenta de nuevo.</p>';
    }
}

// Eliminar mensaje
async function deleteMensaje(id) {
    if (!confirm('¿Estás seguro de eliminar este mensaje?')) return;

    try {
        const response = await fetch(`${API_URL}/mensajes/${id}`, {
            method: 'DELETE',
            credentials: 'include'
        });

        if (response.ok) {
            // Recargar la vista actual
            const hash = window.location.hash.slice(1);
            const currentRoute = hash === '/' || hash === '' ? 'inicio' : hash.replace('/', '');
            if (currentRoute === 'mis-mensajes') {
                loadMisMensajes();
            } else {
                loadPublicMensajes();
            }
        } else {
            const data = await response.json();
            alert(data.error || 'Error al eliminar mensaje');
            
            // Si no está autenticado, redirigir a login
            if (response.status === 401) {
                currentUser = null;
                window.location.hash = '#login';
            }
        }
    } catch (error) {
        console.error('Error de conexión:', error);
        alert('Error de conexión con el servidor');
    }
}

// Editar mensaje
function editMensaje(id, texto) {
    editingMessageId = id;
    mensajeTexto.value = texto;
    charCount.textContent = `${texto.length}/500 caracteres`;
    btnSubmitMensaje.textContent = 'Actualizar';
    btnCancelEdit.style.display = 'block';
    foroHeaderTitle.textContent = 'Editar Mensaje';
    window.location.hash = '#foro';
    mensajeTexto.focus();
}

// Cancelar edición
function cancelEdit() {
    editingMessageId = null;
    mensajeTexto.value = '';
    charCount.textContent = '0/500 caracteres';
    btnSubmitMensaje.textContent = 'Publicar';
    btnCancelEdit.style.display = 'none';
    foroHeaderTitle.textContent = 'Publicar Mensaje';
}

// Cargar mis mensajes
async function loadMisMensajes() {
    try {
        const response = await fetch(`${API_URL}/mis-mensajes`, {
            credentials: 'include'
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                currentUser = null;
                window.location.hash = '#login';
                return;
            }
            throw new Error('Error al cargar mensajes');
        }
        
        const mensajes = await response.json();

        if (mensajes.length === 0) {
            misMensajesLista.innerHTML = '<p>No has publicado ningún mensaje aún. <a href="#foro">Publica tu primer mensaje</a></p>';
            return;
        }

        misMensajesLista.innerHTML = mensajes.map(msg => `
            <div class="mensaje-item">
                <div class="mensaje-header">
                    <span class="mensaje-autor">${escapeHtml(msg.autor)}</span>
                    <span class="mensaje-fecha">${formatDate(msg.created_at)}</span>
                </div>
                <div class="mensaje-texto">${escapeHtml(msg.texto)}</div>
                <div class="mensaje-actions">
                    <button class="btn-edit" onclick="editMensaje(${msg.id}, '${escapeHtml(msg.texto).replace(/'/g, "\\'")}')">✏️ Editar</button>
                    <button class="btn-delete" onclick="deleteMensaje(${msg.id})">🗑️ Eliminar</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error al cargar tus mensajes:', error);
        misMensajesLista.innerHTML = '<p class="error">Error al cargar tus mensajes. Por favor intenta de nuevo.</p>';
    }
}

// Utilidades
function showMessage(element, message, type) {
    element.innerHTML = `<p class="${type}">${message}</p>`;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}
