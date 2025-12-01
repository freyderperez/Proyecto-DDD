# Proyecto DDD - DelegInsumos

Este proyecto implementa una arquitectura de microservicios utilizando principios de Domain-Driven Design (DDD). Consiste en varios servicios incluyendo gestión de inventario (ms-inventario), recursos humanos (ms-rrhh), distribución (ms-distribucion), puerta de enlace API (ms-gateway) y un frontend unificado.

## Prerrequisitos

- Docker
- Docker Compose

## Instrucciones de Inicio

1. Clona el repositorio en tu máquina local.
2. Navega al directorio del proyecto.
3. Ejecuta el siguiente comando para iniciar todos los servicios:

   ```bash
   make up
   ```

4. Los servicios estarán disponibles en los siguientes endpoints:
   - Frontend (Dashboard): http://localhost:8080
   - API Gateway: http://localhost:8000
   - Inventory Service: http://localhost:8001
   - Distribution Service: http://localhost:8002
   - HR Service: http://localhost:8003
   - RabbitMQ Management Interface: http://localhost:15672

## Comandos Adicionales

- Ver logs de todos los servicios: `make logs`
- Detener servicios: `docker-compose down`

## Arquitectura

El proyecto sigue DDD con clara separación de responsabilidades:
- **Capa de Dominio**: Contiene entidades, objetos de valor, servicios de dominio y eventos.
- **Capa de Aplicación**: Contiene casos de uso y servicios de aplicación.
- **Capa de Infraestructura**: Contiene repositorios, modelos de base de datos e integraciones externas.

Los servicios se comunican vía RabbitMQ para mensajería asíncrona y comparten una base de datos PostgreSQL.

## Frontend

El frontend es un dashboard unificado desarrollado con HTML, CSS y JavaScript vanilla. Incluye:

- **Vista Unificada**: Una sola página con métricas en tiempo real y gestión completa de insumos, empleados y entregas.
- **Funcionalidades CRUD**: Crear, leer, actualizar y eliminar para todos los recursos.
- **Estados Visuales**: Colores en filas de tablas según estado (verde para OK/activo, rojo para crítico, etc.).
- **Validaciones**: Confirmación de entregas con verificación de stock disponible.
- **Interfaz Moderna**: Diseño responsive con modales para formularios.

El dashboard se conecta directamente al API Gateway para todas las operaciones.