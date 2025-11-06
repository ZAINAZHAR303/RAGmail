# RAGmail 📧🤖

AI-powered personalized email generator for graduate school professor outreach. Uses RAG (Retrieval-Augmented Generation) to match your projects with professor research interests and generate compelling, customized emails.

## Features

- 🎯 **Smart Project Matching**: Semantic search finds your most relevant projects based on professor's research
- 🧠 **RAG-Powered**: Uses LangChain + ChromaDB for intelligent retrieval
- ⚡ **Fast Generation**: Groq LLM for quick, high-quality email composition
- 📝 **Template Variants**: Automatically selects appropriate email template
- 💾 **Email History**: Saves all generated emails with metadata

## Setup

### 1. Install Dependencies

```bash
# Activate your virtual environment
myenv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure Environment

The `.env` file is already created with your Groq API key.

### 3. Initialize Vector Database

```bash
python src/vector_store.py
```

This will:
- Load all your projects, achievements, and background data
- Create embeddings using sentence-transformers
- Store in ChromaDB for fast semantic search

## Usage

### Run the Application

```bash
python main.py
```

### Interactive Prompts

You'll be asked to provide:

1. **Professor Name** (e.g., Dr. Sarah Johnson)
2. **University Name** (e.g., Stanford University)
3. **Research Domain** (e.g., "multi-agent systems, NLP, computer vision")
4. **Recent Paper Title** (optional)
5. **Paper Summary** (optional)
6. **Force Specific Project** (optional - if you want to highlight a particular project)

### Example Session

```
Professor Name: Dr. Michael Chen
University Name: MIT
Research Domain: multi-agent systems and natural language processing
Recent Paper Title: Coordinated Multi-Agent Planning
Paper Summary: explores coordination mechanisms for AI agents
Force Specific Project: [press Enter]

🔄 Generating personalized email...

✓ Email generated!
📊 Selected Project: HireFlow
📈 Relevance Score: 9/10
```

## How It Works

1. **Semantic Search**: Your query (professor's research + paper) is embedded and searched against your project database
2. **Project Ranking**: Top 3 most relevant projects are retrieved
3. **LLM Selection**: Groq LLM analyzes matches and selects the best project
4. **Paragraph Generation**: LLM generates a compelling paragraph connecting your project to professor's work
5. **Template Assembly**: Fixed highlights + generated paragraph + standard closing = complete email

## Project Structure

```
RAGmail/
├── data/                       # Your background data
│   ├── projects.json          # All projects with metadata
│   ├── achievements.txt       # Awards and highlights
│   ├── research_interests.txt # Your research interests
│   ├── skills.txt            # Technical skills
│   ├── coursework.txt        # Academic background
│   └── email_templates.txt   # Template documentation
├── src/
│   ├── document_loader.py    # Load and prepare documents
│   ├── vector_store.py       # ChromaDB vector store
│   ├── rag_chain.py          # RAG matching logic
│   └── email_generator.py    # Email composition
├── chroma_db/                # Vector database (created on init)
├── generated_emails/         # Saved emails
├── main.py                   # CLI application
├── requirements.txt
├── .env
└── README.md
```

## Tech Stack

- **LangChain**: RAG orchestration
- **ChromaDB**: Vector database
- **Sentence Transformers**: Embeddings (all-MiniLM-L6-v2)
- **Groq**: LLM inference (llama-3.3-70b-versatile)
- **Python 3.8+**

## Tips for Best Results

1. **Be Specific with Research Domains**: More specific = better matching
   - ✓ "multi-agent systems, LangGraph, NLP for automation"
   - ✗ "AI and ML"

2. **Add Paper Context**: Helps select most aligned project
3. **Review Before Sending**: Generated emails are drafts - personalize further!
4. **Force Project**: Use when you know a specific project fits perfectly

## Customization

### Add New Projects

Edit `data/projects.json` and re-run:
```bash
python src/vector_store.py
```

### Change LLM Settings

Edit `.env`:
```
GROQ_MODEL=llama-3.3-70b-versatile  # or other Groq models
```

### Modify Templates

Email structure is in `src/email_generator.py`. Fixed sections (highlights, closing) are class constants.

## Troubleshooting

**"Vector store not found"**
- Run `python src/vector_store.py` to initialize

**"No matching projects"**
- Check if `chroma_db/` exists
- Verify projects.json is properly formatted

**Low relevance scores**
- Try broader research domain keywords
- Check if your projects actually align with that research area

## Future Enhancements

- [ ] Web interface (Streamlit/Gradio)
- [ ] Email sending integration
- [ ] Multi-language support
- [ ] Professor research auto-scraping
- [ ] Email A/B testing and analytics

## License

MIT License - Built for graduate school applications

---

**Good luck with your applications! 🎓✨**
