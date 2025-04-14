from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "message": "👋 Welcome to the OS Concepts Simulation API!",
        "instructions": "To simulate a concept, use the endpoint: /simulate/{concept}",
        "examples": ["/simulate/pipe", "/simulate/shared_memory"],
        "note": "Currently supported concepts: pipe, shared_memory"
    }

@app.get("/simulate/{concept}")
def simulate(concept: str):
    valid_concepts = ["pipe", "shared_memory"]  # Extend this list as needed
    if concept not in valid_concepts:
        return {"error": "Unsupported concept"}

    try:
        result = subprocess.run(
            ["bash", "run_sim.sh", concept],
            capture_output=True,
            text=True,
            timeout=5
        )
        return {
            "concept": concept,
            "simulation_output": result.stdout.strip()
        }
    except subprocess.CalledProcessError as e:
        return {"error": "Simulation failed", "details": e.stderr}
    except subprocess.TimeoutExpired:
        return {"error": "Simulation timed out"}
