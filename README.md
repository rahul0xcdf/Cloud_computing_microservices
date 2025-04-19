# OS Concepts API - Microservices Collection

A collection of FastAPI-based microservices that provide system call code snippets, IPC mechanisms, and OS concept simulations. Ideal for students, educators, and developers exploring system-level programming and cloud computing concepts.

## Table of Contents

- [System Calls API](#system-calls-api)
- [IPC Service](#ipc-service)
- [API Documentation](#api-documentation)
- [Quickstart Guide](#quickstart-guide)
- [Features](#features)
- [Use Cases](#use-cases)

---

## System Calls API

The System Calls API provides comprehensive information about various operating system system calls and their implementations.

**Features:**
- Query system call concepts like `fork`, `exec`, `pipe`, `shared memory`, etc.
- Syntax-highlighted code with explanation and expected output
- Swagger UI for testing the API
- Docker Compose support for easy deployment

---

## IPC Service

The IPC (Inter-Process Communication) service demonstrates various IPC mechanisms used in operating systems.

**Features:**
- Multiple IPC mechanisms (pipes, shared memory, message queues)
- Code examples with detailed explanations
- Real-world implementation scenarios
- Step-by-step execution guides

---

## API Documentation

Both services provide auto-generated Swagger UI documentation:

- System Calls API: [http://localhost:8001/docs](http://localhost:8001/docs)  
- IPC Service: [http://localhost:8000/docs](http://localhost:8000/docs)

### System Calls API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/system-calls/` | GET | List all available system calls |
| `/system-calls/{call_name}` | GET | Get detailed information about a specific system call |
| `/system-calls/{call_name}/example` | GET | Get code example for a system call |
| `/system-calls/{call_name}/output` | GET | Get expected output for a system call |

### IPC Service Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ipc/mechanisms/` | GET | List all available IPC mechanisms |
| `/ipc/mechanisms/{mechanism}` | GET | Get details about a specific IPC mechanism |
| `/ipc/examples/{mechanism}` | GET | Get implementation examples |
| `/ipc/simulate/{mechanism}` | POST | Run an IPC simulation |

---

## Quickstart Guide

### Using Docker Compose (Recommended)

```bash
git clone https://github.com/yourusername/Cloud_computing_microservices.git
cd Cloud_computing_microservices
```

Run all services with Docker Compose:
```bash

docker-compose up --build

```
Access the APIs in your browser:

IPC Service: [http://localhost:8000/docs](http://localhost:8000/docs)
System Calls Service: [http://localhost:8001/docs](http://localhost:8001/docs)

Stop all services: 
```bash
docker-compose down
```
## Features

### Integrated Dockerfile and Compose

- Uses `gcc:latest` as base image for system-level tools
- Python virtual environment setup
- Automatically installs required Python packages
- Runs both services via `docker-compose.yml`

### Common Features

- Interactive Swagger UI
- Clean and modular FastAPI architecture
- Syntax-highlighted code with outputs
- Real-world simulation of system concepts

---

## Use Cases

### Educational Purposes

- Teaching OS concepts in CS courses
- Demonstrating system calls and IPC mechanisms

### Development Reference

- Quick lookup of system call or IPC implementations

### System Programming Practice

- Learn and test code snippets for OS-level programming

### Cloud Computing Education

- Hands-on microservices and Docker training
- Understand scalable system design

---

## Notes

- The `docker-compose.yml` file builds and launches both services automatically.
- Each service runs on a separate port (`8000`, `8001`).
- Code examples are meant for Unix/Linux environments.
- For customization, edit `Dockerfile` or `main.py` in each microservice.

