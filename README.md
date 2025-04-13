# 🧠 OS Concepts API - Microservice for System Calls

A lightweight FastAPI-based microservice that provides system call code snippets, explanations, and outputs for various Operating System (OS) concepts. Ideal for students, educators, and developers exploring system-level programming.

---

## 🚀 Features

- 🔍 Query system call concepts like `fork`, `exec`, `pipe`, `shared memory`, etc.
- ✅ Syntax-highlighted code with explanation and expected output
- 📘 Swagger UI for testing the API
- 🐳 Docker support for easy deployment

---

## 🛠️ Quickstart

You can run this project either **natively** or using **Docker**. Just use the following single block to do everything.

### 📦 Clone, Run Locally, or Use Docker (All-in-One)

```bash
# Clone the repository
git clone https://github.com/rahul0xcdf/Cloud_computing_microservices.git

# Navigate into the directory
cd Cloud_computing_microservices

# Option 1: Run Locally with Python
pip install -r requirements.txt
uvicorn main:app --reload

# Access locally at:
# http://127.0.0.1:8000/docs

# Option 2: Run using Docker
# (Build the image and run the container)
docker build -t os-concepts-api .
docker run -p 8000:8000 os-concepts-api

# Access Docker container API at:
# http://localhost:8000/docs
