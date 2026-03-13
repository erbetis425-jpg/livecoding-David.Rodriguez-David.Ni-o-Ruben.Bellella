# Registro Docker Privado

Repositorio privado de Docker para almacenar y gestionar imágenes Docker localmente.

## Características

- ✅ Registro Docker privado en puerto 5000
- ✅ Interfaz web de gestión en puerto 8081
- ✅ Persistencia de datos local
- ✅ Capacidad de eliminar imágenes
- ✅ Visualización de contenido y digests

## Requisitos

- Docker y Docker Compose instalados

## Instalación y Ejecución

1. Desde esta carpeta, ejecutar:

```bash
docker-compose up -d
```

2. Acceder a la interfaz web en: http://localhost:8081

3. El registro estará disponible en: http://localhost:5000

## Uso del Registro

### 1. Etiquetar una imagen para el registro local

```bash
docker tag mi-imagen:latest localhost:5000/mi-imagen:latest
```

### 2. Subir imagen al registro

```bash
docker push localhost:5000/mi-imagen:latest
```

### 3. Descargar imagen del registro

```bash
docker pull localhost:5000/mi-imagen:latest
```

### 4. Listar imágenes en el registro (API)

```bash
curl http://localhost:5000/v2/_catalog
```

### 5. Ver tags de una imagen

```bash
curl http://localhost:5000/v2/mi-imagen/tags/list
```

## Ejemplo: Subir el proyecto del foro al registro

Desde la carpeta `mi-proyecto`:

```bash
# Construir la imagen del backend
docker build -t localhost:5000/foro-backend:latest ./backend

# Subir al registro
docker push localhost:5000/foro-backend:latest

# Verificar en la interfaz web: http://localhost:8081
```

## Estructura de Archivos

```
docker-registry/
├── docker-compose.yml      # Configuración de servicios
├── registry-data/          # Datos persistentes (se crea automáticamente)
└── README.md              # Esta guía
```

## Comandos Útiles

### Ver logs del registro
```bash
docker-compose logs -f registry
```

### Detener el registro
```bash
docker-compose down
```

### Detener y eliminar datos
```bash
docker-compose down -v
```

### Reiniciar servicios
```bash
docker-compose restart
```

### Ver estado de los contenedores
```bash
docker-compose ps
```

## Configuración Avanzada (Opcional)

### Habilitar autenticación básica

1. Crear archivo de contraseñas:

```bash
mkdir auth
docker run --rm --entrypoint htpasswd httpd:2 -Bbn usuario password > auth/htpasswd
```

2. Modificar `docker-compose.yml` añadiendo:

```yaml
environment:
  REGISTRY_AUTH: htpasswd
  REGISTRY_AUTH_HTPASSWD_PATH: /auth/htpasswd
  REGISTRY_AUTH_HTPASSWD_REALM: Registry Realm
volumes:
  - ./auth:/auth
```

3. Login en el registro:

```bash
docker login localhost:5000
```

### Habilitar HTTPS (Producción)

Para producción, se recomienda usar certificados SSL/TLS. Consultar la documentación oficial de Docker Registry.

## Solución de Problemas

### Error: "connection refused"
- Verificar que el registro está corriendo: `docker-compose ps`
- Verificar que el puerto 5000 no está en uso

### Error: "server gave HTTP response to HTTPS client"
- Añadir el registro a la lista de registros inseguros en Docker Desktop:
  - Settings → Docker Engine
  - Añadir: `"insecure-registries": ["localhost:5000"]`

### No aparecen imágenes en la interfaz web
- Verificar que las imágenes se subieron correctamente
- Refrescar la página web
- Revisar logs: `docker-compose logs registry-ui`

## Recursos

- [Documentación oficial Docker Registry](https://docs.docker.com/registry/)
- [Docker Registry UI](https://github.com/Joxit/docker-registry-ui)

## Notas de Seguridad

⚠️ Este registro está configurado sin autenticación para desarrollo local. Para producción:
- Habilitar autenticación
- Usar HTTPS
- Configurar firewall
- Implementar backups regulares
