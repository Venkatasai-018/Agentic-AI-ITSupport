# 🚀 Quick Start Guide

## Installation & Setup

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Configure Environment
Copy `.env.example` to `.env` and update if needed:
```powershell
cp .env.example .env
```

### 3. Run the Application
```powershell
python main.py
```

Or with uvicorn:
```powershell
uvicorn main:app --reload --port 8000
```

### 4. Access the Application

- **Main Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Dashboard**: http://localhost:8000/dashboard

### 5. Login Credentials

**Default Admin Account:**
- Username: `admin`
- Password: `admin123`

## Testing the System

### Test Queries

Try these example IT issues:

1. **Password Reset**: "I forgot my password and can't login"
2. **Network Issue**: "My WiFi is not connecting"
3. **Email Problem**: "Can't send emails from Outlook"
4. **Printer Issue**: "Printer is not responding"
5. **Hardware Issue**: "My laptop screen is broken"
6. **VPN Access**: "Can't connect to VPN from home"

### Expected Behavior

- **Auto-Resolved**: Password resets, email issues, printer problems
- **Escalated**: Hardware issues, network problems, VPN access

## API Testing

### 1. Get Access Token
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

### 2. Submit IT Request
```bash
curl -X POST "http://localhost:8000/api/workflow/process" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"issue_description":"I forgot my password"}'
```

### 3. View Tickets
```bash
curl -X GET "http://localhost:8000/api/tickets" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Architecture Overview

```
┌─────────────┐
│   User UI   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│      FastAPI Main Application       │
│   (Orchestration & API Endpoints)   │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│        Multi-Agent System           │
├─────────────────────────────────────┤
│ 1. UI Agent (Input Validation)      │
│ 2. Classification Agent (RAG)       │
│ 3. Decision Agent                   │
│ 4. Resolution/Escalation Agent      │
│ 5. Logging Agent                    │
└──────┬──────────────────────────────┘
       │
       ▼
┌──────────────┬─────────────────┐
│  RAG System  │   Database      │
│  (ChromaDB)  │   (SQLite)      │
└──────────────┴─────────────────┘
```

## Key Files

- `main.py` - FastAPI app & orchestration
- `agents.py` - All AI agents
- `rag_system.py` - RAG implementation
- `knowledge_base.json` - IT solutions
- `database.py` - Database setup
- `auth.py` - Authentication

## Troubleshooting

### Issue: ChromaDB Error
**Solution**: Delete `chroma_db/` folder and restart

### Issue: Database Error
**Solution**: Delete `it_support.db` file and restart

### Issue: Authentication Error
**Solution**: Clear browser localStorage and login again

### Issue: Port Already in Use
**Solution**: Use a different port:
```powershell
uvicorn main:app --port 8001
```

## Next Steps

1. ✅ Create a regular user account (not admin)
2. ✅ Submit various IT requests
3. ✅ Check the dashboard for analytics
4. ✅ Review the API documentation at `/docs`
5. ✅ Explore agent logs for each ticket

Enjoy your AI-powered IT Support System! 🎉
