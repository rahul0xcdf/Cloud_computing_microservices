from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.get("/simulate/{concept}")
def simulate(concept: str):
    if concept not in ["pipe", "shared_memory"]:
        return {"error": "Unsupported concept"}
    try:
        output = subprocess.check_output(["bash", "run_sim.sh", concept], stderr=subprocess.STDOUT)
        return {"concept": concept, "simulation_output": output.decode()}
    except subprocess.CalledProcessError as e:
        return {"error": "Simulation failed", "details": e.output.decode()}
