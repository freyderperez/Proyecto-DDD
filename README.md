# Proyecto DDD

This project implements a microservices architecture using Domain-Driven Design (DDD) principles. It consists of several services including inventory management (ms-inventario), human resources (ms-rrhh), distribution (ms-distribucion), and an API gateway (ms-gateway).

## Prerequisites

- Docker
- Docker Compose

## Startup Instructions

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Run the following command to start all services:

   ```bash
   make up
   ```

4. The services will be available at the following endpoints:
   - API Gateway: http://localhost:8000
   - Inventory Service: http://localhost:8001
   - HR Service: http://localhost:8002
   - Distribution Service: http://localhost:8003
   - RabbitMQ Management Interface: http://localhost:15672

## Additional Commands

- View logs for all services: `make logs`
- Stop services: `docker-compose down`

## Architecture

The project follows DDD with clear separation of concerns:
- **Domain Layer**: Contains entities, value objects, domain services, and events.
- **Application Layer**: Contains use cases and application services.
- **Infrastructure Layer**: Contains repositories, database models, and external integrations.

Services communicate via RabbitMQ for asynchronous messaging and share a PostgreSQL database.