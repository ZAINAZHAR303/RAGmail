# RAGmail Backend

FastAPI backend for the RAGmail email generation system.

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure environment:**
Copy `.env.example` to `.env` and add your Groq API key:
```bash
cp .env.example .env
```

3. **Initialize vector database (first time only):**
```bash
python init_db.py
```

4. **Run the server:**
```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### `GET /`
Health check endpoint

### `GET /api/health`
Detailed health check with system status

### `POST /api/generate-email`
Generate personalized email

**Request Body:**
```json
{
  "professor_name": "Dr. Michael Chen",
  "university_name": "MIT",
  "research_domain": "multi-agent systems, NLP",
  "paper_title": "Coordinated Multi-Agent Planning",
  "paper_summary": "explores coordination mechanisms",
  "force_project": "HireFlow"  // optional
}
```

**Response:**
```json
{
  "email": "Subject: ...\n\nDear ...",
  "selected_project": "HireFlow",
  "relevance_score": 9,
  "success": true,
  "message": "Email generated successfully"
}
```

### `GET /api/projects`
Get list of all available projects

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
