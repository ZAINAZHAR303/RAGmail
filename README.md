# RAGmail 📧🤖

AI-powered personalized email generator for graduate school professor outreach. Uses RAG (Retrieval-Augmented Generation) to match your projects with professor research interests and generate compelling, customized emails.

## 🏗️ Architecture

**Full-stack application with:**
- **Backend**: FastAPI + LangChain RAG system
- **Frontend**: Next.js 16 with modern React
- **AI**: Groq LLM + ChromaDB vector database

## Features

- 🎯 **Smart Project Matching**: Semantic search finds your most relevant projects based on professor's research
- 🧠 **RAG-Powered**: Uses LangChain + ChromaDB for intelligent retrieval
- ⚡ **Fast Generation**: Groq LLM for quick, high-quality email composition
- 🎨 **Modern UI**: Beautiful, responsive Next.js interface
- 📝 **Template Variants**: Automatically selects appropriate email template
- 💾 **Email Management**: Copy or download generated emails

## 🚀 Quick Start

### Backend Setup

1. **Navigate to backend:**
   ```powershell
   cd backend
   ```

2. **Create virtual environment (if not exists):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Verify `.env` file exists with your Groq API key:**
   ```env
   GROQ_API_KEY=your_api_key_here
   GROQ_MODEL=llama-3.3-70b-versatile
   ```

5. **Initialize vector database:**
   ```powershell
   python init_db.py
   ```

6. **Start backend server:**
   ```powershell
   python main.py
   ```
   Backend runs at: `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend (new terminal):**
   ```powershell
   cd frontend
   ```

2. **Install dependencies:**
   ```powershell
   npm install
   ```

3. **Start development server:**
   ```powershell
   npm run dev
   ```
   Frontend runs at: `http://localhost:3000`

## 📱 Using the Web Interface

1. Open `http://localhost:3000` in your browser
2. Fill in the professor details form:
   - **Professor Name**: e.g., Dr. Michael Chen
   - **University**: e.g., MIT
   - **Research Domain**: e.g., "multi-agent systems, NLP"
   - **Paper Title** (optional): Recent publication title
   - **Paper Summary** (optional): Brief description
   - **Force Project** (optional): Specific project to highlight
3. Click **"🚀 Generate Email"**
4. View the AI-generated email in real-time
5. **Copy** to clipboard or **Download** as text file

## 🔌 API Endpoints

### `POST /api/generate-email`
Generate personalized email

**Request:**
```json
{
  "professor_name": "Dr. Michael Chen",
  "university_name": "MIT",
  "research_domain": "multi-agent systems, NLP",
  "paper_title": "Coordinated Multi-Agent Planning",
  "paper_summary": "explores coordination mechanisms",
  "force_project": "HireFlow"
}
```

**Response:**
```json
{
  "email": "Subject: Prospective Graduate Student...",
  "selected_project": "HireFlow",
  "relevance_score": 8,
  "success": true,
  "message": "Email generated successfully"
}
```

### `GET /api/projects`
Get all available projects

### `GET /api/health`
Health check endpoint

## How It Works

1. **Semantic Search**: Query embedded and searched against project database
2. **Project Ranking**: Top 3 most relevant projects retrieved
3. **LLM Selection**: Groq analyzes and selects best project
4. **Paragraph Generation**: LLM creates compelling connection paragraph
5. **Template Assembly**: Combines fixed highlights + AI paragraph + closing

## Project Structure

```
RAGmail/
├── backend/                    # FastAPI backend
│   ├── data/                  # Your background data
│   │   ├── projects.json      # 12 projects with metadata
│   │   ├── achievements.txt   # Awards and highlights
│   │   ├── research_interests.txt
│   │   ├── skills.txt
│   │   ├── coursework.txt
│   │   └── email_templates.txt
│   ├── src/
│   │   ├── document_loader.py # Load and prepare documents
│   │   ├── vector_store.py    # ChromaDB integration
│   │   ├── rag_chain.py       # RAG matching logic
│   │   └── email_generator.py # Email composition
│   ├── chroma_db/             # Vector database
│   ├── main.py                # FastAPI application
│   ├── init_db.py             # DB initialization
│   ├── requirements.txt
│   └── .env
├── frontend/                   # Next.js frontend
│   ├── app/
│   │   ├── components/
│   │   │   ├── EmailForm.js   # Input form
│   │   │   └── EmailPreview.js # Email display
│   │   ├── page.js            # Main page
│   │   ├── layout.js
│   │   └── globals.css
│   ├── package.json
│   └── .env.local
└── README.md
```

## 🛠️ Tech Stack

**Backend:**
- FastAPI - Modern Python web framework
- LangChain - RAG orchestration
- ChromaDB - Vector database
- Groq API - LLM (llama-3.3-70b-versatile)
- Sentence Transformers - Embeddings (all-MiniLM-L6-v2)

**Frontend:**
- Next.js 16 - React framework with App Router
- Tailwind CSS - Utility-first styling
- React Hooks - State management

## 🎯 Tips for Best Results

1. **Be Specific with Research Domains**:
   - ✓ "multi-agent systems, LangGraph, NLP for automation"
   - ✗ "AI and ML"

2. **Add Paper Context**: Helps select most aligned project

3. **Review Before Sending**: Generated emails are drafts - personalize further!

4. **Force Project**: Use when you know a specific project fits perfectly

## 🔧 Development

**Backend with hot reload:**
```powershell
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend with hot reload:**
```powershell
cd frontend
npm run dev
```

## Customization

### Add New Projects

1. Edit `backend/data/projects.json`
2. Re-initialize database:
   ```powershell
   cd backend
   python init_db.py
   ```

### Change LLM Model

Edit `backend/.env`:
```env
GROQ_MODEL=llama-3.3-70b-versatile  # or other Groq models
```

### Modify UI Styling

Edit `frontend/app/globals.css` or component Tailwind classes

## 🐛 Troubleshooting

**Backend won't start:**
- Ensure virtual environment is activated
- Check if port 8000 is available
- Verify `.env` has valid GROQ_API_KEY

**Frontend API connection failed:**
- Ensure backend is running on port 8000
- Check browser console for CORS errors
- Verify `frontend/.env.local` has correct API URL

**"Vector store not found":**
- Run `python init_db.py` in backend directory
- Verify `backend/chroma_db/` folder exists

**Low relevance scores:**
- Try broader research domain keywords
- Check if your projects align with research area

## 📄 License

MIT License - Built for graduate school applications

---

**Good luck with your applications! 🎓✨**
