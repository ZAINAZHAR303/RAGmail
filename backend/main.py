from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from contextlib import asynccontextmanager
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from src.email_generator import EmailGenerator

# Initialize email generator
email_generator = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    global email_generator
    try:
        email_generator = EmailGenerator()
        print("✓ RAGmail Email Generator initialized successfully!")
    except Exception as e:
        print(f"✗ Failed to initialize Email Generator: {str(e)}")
        raise
    yield
    # Cleanup on shutdown
    email_generator = None

app = FastAPI(title="RAGmail API", version="1.0.0", lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize email generator
email_generator = None

async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    global email_generator
    try:
        email_generator = EmailGenerator()
        print("✓ RAGmail Email Generator initialized successfully!")
    except Exception as e:
        print(f"✗ Failed to initialize Email Generator: {str(e)}")
        raise
    yield
    # Cleanup on shutdown
    email_generator = None

app = FastAPI(title="RAGmail API", version="1.0.0", lifespan=lifespan)

class ProfessorRequest(BaseModel):
    professor_name: str
    university_name: str
    research_domain: str
    paper_title: Optional[str] = None
    paper_summary: Optional[str] = None
    force_project: Optional[str] = None

class EmailResponse(BaseModel):
    email: str
    selected_project: str
    relevance_score: int
    success: bool
    message: str

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "RAGmail API is running",
        "version": "1.0.0"
    }

@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "email_generator_ready": email_generator is not None,
        "vector_db_loaded": email_generator is not None
    }

@app.post("/api/generate-email", response_model=EmailResponse)
async def generate_email(request: ProfessorRequest):
    """
    Generate a personalized email for a professor based on their research interests
    """
    if email_generator is None:
        raise HTTPException(status_code=503, detail="Email generator not initialized")
    
    try:
        # Generate the email
        result = email_generator.generate_email(
            professor_name=request.professor_name,
            university_name=request.university_name,
            research_domain=request.research_domain,
            paper_title=request.paper_title,
            paper_summary=request.paper_summary,
            force_project=request.force_project
        )
        
        return EmailResponse(
            email=result['email'],
            selected_project=result['project_title'],
            relevance_score=result['relevance_score'],
            success=True,
            message="Email generated successfully"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate email: {str(e)}"
        )

@app.get("/api/projects")
async def get_projects():
    """Get list of all available projects"""
    import json
    
    try:
        with open(os.path.join(os.path.dirname(__file__), 'data', 'projects.json'), 'r') as f:
            projects = json.load(f)
        
        # Return simplified project list
        return {
            "success": True,
            "projects": [
                {
                    "id": p["id"],
                    "title": p["title"],
                    "domain": p["domain"],
                    "description": p["description"]
                }
                for p in projects
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch projects: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
