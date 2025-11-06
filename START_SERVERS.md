# 🚀 How to Start RAGmail Servers

## Quick Start Commands

### Terminal 1 - Backend (FastAPI)
```powershell
cd 'E:\Github Repos\RAGmail\backend'
& 'E:\Github Repos\RAGmail\myenv\Scripts\python.exe' -m uvicorn main:app --host 0.0.0.0 --port 8000
```

**Backend will be available at:** `http://localhost:8000`

### Terminal 2 - Frontend (Next.js)
```powershell
cd 'E:\Github Repos\RAGmail\frontend'
npm run dev
```

**Frontend will be available at:** `http://localhost:3000`

---

## ✅ Verification

### Check Backend Health
Open in browser: `http://localhost:8000/api/health`

Should return:
```json
{
  "status": "healthy",
  "email_generator_ready": true,
  "vector_db_loaded": true
}
```

### Check Frontend
Open in browser: `http://localhost:3000`

Should see the RAGmail UI with form and preview panels.

---

## 🔍 API Documentation

Interactive API docs (Swagger UI): `http://localhost:8000/docs`

---

## 🛑 Stopping Servers

Press `Ctrl+C` in each terminal window to stop the servers.

---

## 🐛 Troubleshooting

**Backend fails to start:**
- Ensure virtual environment exists: `E:\Github Repos\RAGmail\myenv\`
- Check if vector database is initialized: Run `python init_db.py` in backend folder
- Verify `.env` file has `GROQ_API_KEY`

**Frontend fails to start:**
- Ensure dependencies are installed: Run `npm install` in frontend folder
- Check if port 3000 is available

**CORS errors in browser:**
- Ensure backend is running on port 8000
- Check browser console for specific error messages

---

## 📝 Development Mode (Hot Reload)

### Backend with auto-reload:
```powershell
cd 'E:\Github Repos\RAGmail\backend'
& 'E:\Github Repos\RAGmail\myenv\Scripts\python.exe' -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (already has hot reload by default):
```powershell
cd 'E:\Github Repos\RAGmail\frontend'
npm run dev
```

---

## 🎯 Current Status

✅ **Backend:** Running on http://localhost:8000  
✅ **Frontend:** Running on http://localhost:3000  
✅ **Vector Database:** Initialized with 17 documents  
✅ **LLM:** Groq llama-3.3-70b-versatile connected  

**You're ready to generate personalized emails!** 🎉
