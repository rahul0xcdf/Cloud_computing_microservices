# OS Concepts API - Microservices Collection

A collection of FastAPI-based microservices that provide system call code snippets, IPC mechanisms, and OS concept simulations. Ideal for students, educators, and developers exploring system-level programming and cloud computing concepts.

## Table of Contents

- [System Calls API](#system-calls-api)
- [IPC Service](#ipc-service)
- [API Documentation](#api-documentation)
- [Quickstart Guide](#quickstart-guide)
- [Features](#features)
- [Use Cases](#use-cases)

## System Calls API

The System Calls API provides comprehensive information about various operating system system calls and their implementations.

**Features:**
- Query system call concepts like `fork`, `exec`, `pipe`, `shared memory`, etc.
- Syntax-highlighted code with explanation and expected output
- Swagger UI for testing the API
- Docker support for easy deployment

## IPC Service

The IPC (Inter-Process Communication) service demonstrates various IPC mechanisms used in operating systems.

**Features:**
- Multiple IPC mechanisms (pipes, shared memory, message queues)
- Code examples with detailed explanations
- Real-world implementation scenarios
- Step-by-step execution guides

## API Documentation

Both services provide auto-generated Swagger UI documentation:

- System Calls API: http://localhost:8000/docs
- IPC Service: http://localhost:8001/docs

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

## Quickstart Guide

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Cloud_computing_microservices.git
cd Cloud_computing_microservices
```

2. Build and run the services:

For System Calls API:
```bash
docker build -t systemcall-service -f Dockerfile ./systemcall
docker run -p 8000:8000 systemcall-service
```

For IPC Service:
```bash
docker build -t ipc-service -f Dockerfile ./ipc
docker run -p 8001:8000 ipc-service
```

### Running Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the services:
```bash
# System Calls API
cd systemcall
uvicorn main:app --reload --port 8000

# IPC Service
cd ipc
uvicorn main:app --reload --port 8001
```

## Features

### Integrated Dockerfile
- Uses `gcc:latest` as base image for comprehensive build tools
- Sets up Python environment with virtual environment
- Installs necessary Python packages (FastAPI, Uvicorn)
- Handles service-specific requirements automatically
- Supports both services with a single configuration

### Common Features
- Comprehensive API documentation
- Interactive Swagger UI
- Fast and efficient performance
- Secure API endpoints
- Detailed code examples and explanations

## Use Cases

These microservices can be used for:

1. **Educational Purposes:**
   - Teaching OS concepts in computer science courses
   - Demonstrating system calls and IPC mechanisms
   - Providing practical examples for students

2. **Development Reference:**
   - Quick lookup of system call implementations
   - Understanding IPC mechanisms
   - Code examples for common OS operations

3. **System Programming Practice:**
   - Learning system-level programming
   - Understanding process communication
   - Experimenting with different IPC mechanisms

4. **Cloud Computing Education:**
   - Understanding microservices architecture
   - Learning containerization with Docker
   - Practicing API development and documentation

## Notes

- The Dockerfile automatically detects and installs requirements.txt if present
- The run_sim.sh script is made executable if present
- Both services use FastAPI and Uvicorn for the web server
- The services can run simultaneously on different ports
