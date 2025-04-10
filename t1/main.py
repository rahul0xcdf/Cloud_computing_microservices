from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import json

app = FastAPI()

class ConceptRequest(BaseModel):
    concept: str
    details: Optional[str] = None

# Load snippets from file or hardcoded dictionary
with open("snippets.json") as f:
    snippets = json.load(f)

@app.post("/api/os-concept")
def get_os_concept(data: ConceptRequest):
    concept = data.concept.lower()
    detail = data.details.lower() if data.details else "default"

    if concept not in snippets:
        raise HTTPException(status_code=404, detail="Concept not found")

    snippet_data = snippets[concept].get(detail) or snippets[concept].get("default")
    if not snippet_data:
        raise HTTPException(status_code=404, detail="No snippet available for given detail")

    return {
        "concept": concept,
        "code": snippet_data["code"],
        "explanation": snippet_data.get("explanation", ""),
        "potential_output": snippet_data.get("potential_output", "")
    }
