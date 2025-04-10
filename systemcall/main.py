from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import json

app = FastAPI(
    title="OS Concepts API",
    description="API for retrieving operating system concepts with code examples",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

class ConceptRequest(BaseModel):
    concept: str = Field(..., example="fork", description="The OS concept to retrieve")
    details: Optional[str] = Field(None, example="default", description="Specific details about the concept")

class ConceptResponse(BaseModel):
    concept: str = Field(..., example="fork", description="The requested concept")
    code: str = Field(..., example="```c\n#include <stdio.h>\nint main() {}\n```", description="Code example with syntax highlighting")
    explanation: Optional[str] = Field(None, example="This is an explanation of the concept", description="Detailed explanation of the concept")
    potential_output: Optional[str] = Field(None, example="Expected output of the code", description="Potential output of the code example")

# Load snippets from file
with open("snippets.json") as f:
    snippets = json.load(f)

@app.post(
    "/api/os-concept",
    response_model=ConceptResponse,
    summary="Get OS Concept",
    description="Retrieve an operating system concept with code example and explanation",
    response_description="Concept details with formatted code example"
)
def get_os_concept(data: ConceptRequest):
    concept = data.concept.lower()
    detail = data.details.lower() if data.details else "default"

    if concept not in snippets:
        raise HTTPException(status_code=404, detail="Concept not found")

    snippet_data = snippets[concept].get(detail) or snippets[concept].get("default")
    if not snippet_data:
        raise HTTPException(status_code=404, detail="No snippet available for given detail")

    # Format the response with Markdown-style code blocks
    formatted_code = f"```c\n{snippet_data['code']}\n```"
    
    return ConceptResponse(
        concept=concept,
        code=formatted_code,
        explanation=snippet_data.get("explanation", ""),
        potential_output=snippet_data.get("potential_output", "")
    )

# Add OpenAPI documentation customization
@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to OS Concepts API. Visit /docs for API documentation."}
