# 🚀 Guía Rápida - Registro Docker

## Inicio Rápido (3 pasos)

### 1. Levantar el registro
```bash
cd docker-registry
docker-compose up -d
```

### 2. Verificar que funciona
- Interfaz web: http://localhost:8081
- API: http://localhost:5000/v2/_catalog

### 3. Usar el registro

```bash
# Etiquetar imagen
docker tag mi-imagen localhost:5000/mi-imagen:v1

# Subir imagen
docker push localhost:5000/mi-imagen:v1

# Descargar imagen
docker pull localhost:5000/mi-imagen:v1
```

## Ejemplo Completo con el Proyecto del Foro

```bash
# 1. Ir a la carpeta del proyecto
cd ../mi-proyecto

# 2. Construir imagen del backend
docker build -t localhost:5000/foro-backend:1.0 ./backend

# 3. Subir al registro
docker push localhost:5000/foro-backend:1.0

# 4. Ver en la interfaz web
# Abrir: http://localhost:8081
```

## Comandos Esenciales

```bash
# Ver imágenes en el registro
curl http://localhost:5000/v2/_catalog

# Ver logs
docker-compose logs -f

# Detener
docker-compose down

# Reiniciar
docker-compose restart
```

## Solución Rápida de Problemas

Si aparece error "HTTP response to HTTPS client":

1. Abrir Docker Desktop
2. Settings → Docker Engine
3. Añadir:
```json
{
  "insecure-registries": ["localhost:5000"]
}
```
4. Apply & Restart

¡Listo! Ya tienes tu registro Docker privado funcionando.
