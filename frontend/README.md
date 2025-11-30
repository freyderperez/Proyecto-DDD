# Frontend Sistema DDD

Aplicación web simple HTML/CSS/JS para gestionar Insumos, Empleados y Entregas.

## Instalación

### Opción 1: Local

1. **IMPORTANTE**: Asegurarse de que el backend esté corriendo primero:
   ```bash
   docker-compose up
   ```
   Esto iniciará PostgreSQL, RabbitMQ, microservicios y gateway en http://localhost:8000

2. Abrir los archivos HTML directamente en el navegador (requiere CORS habilitado o servidor local).

3. Para servidor local simple, usar Python:
   ```bash
   cd frontend
   python -m http.server 8080
   ```

4. Abrir http://localhost:8080 en el navegador.

### Opción 2: Con Docker (Recomendado)

1. Asegurarse de que Docker esté instalado.

2. Desde la raíz del proyecto (donde está docker-compose.yml):
   ```bash
   docker-compose up
   ```

3. Abrir http://localhost:8080 en el navegador (frontend se sirve automáticamente).

## ⚠️ Requisitos para Ver Datos

**El frontend NO mostrará datos si el backend no está corriendo.**

Asegúrate de que todos los servicios estén activos:
- ✅ PostgreSQL (puerto 5432)
- ✅ RabbitMQ (puerto 15672)
- ✅ ms-inventario (internamente)
- ✅ ms-rrhh (internamente)
- ✅ ms-distribucion (internamente)
- ✅ ms-gateway (puerto 8000)
- ✅ frontend (puerto 8080)

Si ves errores de conexión, verifica que `docker-compose ps` muestre todos los servicios como "Up".

## Características

- **Insumos**: CRUD completo con alertas de stock crítico (rojo si stock < min, amarillo si == min).
- **Empleados**: CRUD completo.
- **Entregas**: Crear y eliminar entregas, con selección de insumo y empleado.

## Tecnologías

- HTML5
- CSS3
- JavaScript (ES6+)
- Fetch API

## Estructura del Proyecto

```
frontend/
├── index.html
├── insumos.html
├── empleados.html
├── entregas.html
├── css/
│   └── styles.css
├── js/
│   ├── api.js
│   ├── insumos.js
│   ├── empleados.js
│   └── entregas.js
├── Dockerfile
└── README.md
```

## API

Conecta al Gateway en http://localhost:8000

- Insumos: /inventario/insumos
- Empleados: /rrhh/empleados
- Entregas: /distribucion/entregas