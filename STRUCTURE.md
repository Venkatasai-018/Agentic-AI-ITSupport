# 📁 Project Structure

```
Agentic-AI-ITSupport/
│
├── 📄 main.py                      # FastAPI main application & orchestration
│                                   # - All API endpoints
│                                   # - Workflow orchestration
│                                   # - Agent coordination
│
├── 🤖 agents.py                    # AI Agents implementation
│                                   # - UIAgent
│                                   # - ClassificationAgent (RAG)
│                                   # - DecisionAgent
│                                   # - ResolutionAgent
│                                   # - EscalationAgent
│                                   # - LoggingAgent
│
├── 🧠 rag_system.py                # RAG System (Retrieval Augmented Generation)
│                                   # - Sentence transformers
│                                   # - ChromaDB vector database
│                                   # - Semantic search
│                                   # - Knowledge base indexing
│
├── 📚 knowledge_base.json          # IT Support Knowledge Base
│                                   # - 10 issue categories
│                                   # - Solutions and instructions
│                                   # - Keywords and metadata
│
├── 🗄️ database.py                  # Database setup & management
│                                   # - SQLAlchemy async engine
│                                   # - Session management
│                                   # - Database initialization
│
├── 📊 models.py                    # SQLAlchemy Database Models
│                                   # - User model
│                                   # - Ticket model
│                                   # - AgentLog model
│                                   # - KnowledgeBase model
│                                   # - SystemMetrics model
│
├── 📝 schemas.py                   # Pydantic Validation Schemas
│                                   # - Request/Response schemas
│                                   # - Data validation
│                                   # - Type checking
│
├── 🔐 auth.py                      # Authentication & Authorization
│                                   # - JWT token management
│                                   # - Password hashing
│                                   # - Role-based access control
│                                   # - Current user dependency
│
├── ⚙️ config.py                    # Configuration Management
│                                   # - Environment variables
│                                   # - Application settings
│                                   # - Pydantic Settings
│
├── 📦 requirements.txt             # Python Dependencies
│                                   # - FastAPI, Uvicorn
│                                   # - SQLAlchemy
│                                   # - Sentence Transformers
│                                   # - ChromaDB
│                                   # - Authentication libs
│
├── 🔧 .env.example                 # Environment Variables Template
├── 📋 .gitignore                   # Git ignore rules
│
├── 🧪 test_system.py               # Test & demonstration script
│                                   # - RAG system tests
│                                   # - Agent tests
│                                   # - System info display
│
├── ▶️ run.bat                      # Windows startup script
├── ▶️ run.sh                       # Linux/Mac startup script
│
├── 📖 README.md                    # Main Documentation
│                                   # - Complete system overview
│                                   # - Installation guide
│                                   # - Feature list
│                                   # - Usage examples
│
├── 🚀 QUICKSTART.md                # Quick Start Guide
│                                   # - Fast setup instructions
│                                   # - Test examples
│                                   # - Troubleshooting
│
├── 📚 API_DOCUMENTATION.md         # Complete API Reference
│                                   # - All endpoints documented
│                                   # - Request/Response examples
│                                   # - Authentication flows
│
├── 📊 PROJECT_SUMMARY.md           # Project Summary
│                                   # - Implementation status
│                                   # - Architecture overview
│                                   # - Technical specs
│
├── 📁 static/                      # Static files (CSS, JS)
│   └── style.css                   # Global styles
│                                   # - Responsive design
│                                   # - Color scheme
│                                   # - Component styles
│
├── 📁 templates/                   # HTML templates (Jinja2)
│   ├── index.html                  # Main support request form
│   │                               # - Login/Register
│   │                               # - Request submission
│   │                               # - Result display
│   │
│   ├── dashboard.html              # Analytics dashboard
│   │                               # - Metrics cards
│   │                               # - Agent performance
│   │                               # - Ticket list
│   │
│   └── login.html                  # Login page
│                                   # - Simple login form
│
└── 📁 test/                        # Test directory (empty)

Generated Files (after running):
├── 📄 it_support.db                # SQLite database
└── 📁 chroma_db/                   # ChromaDB vector database
```

---

## 📂 File Descriptions

### Core Application (Backend)

| File | Lines | Purpose |
|------|-------|---------|
| `main.py` | ~600 | FastAPI app, all endpoints, orchestration |
| `agents.py` | ~450 | All 6 AI agents with RAG integration |
| `rag_system.py` | ~200 | RAG system with vector search |
| `database.py` | ~50 | Database setup and sessions |
| `models.py` | ~150 | Database models (5 tables) |
| `schemas.py` | ~200 | Pydantic validation schemas |
| `auth.py` | ~150 | JWT auth and RBAC |
| `config.py` | ~50 | Configuration management |

### Data & Configuration

| File | Size | Purpose |
|------|------|---------|
| `knowledge_base.json` | ~8 KB | 10 IT issue categories with solutions |
| `requirements.txt` | ~300 B | Python package dependencies |
| `.env.example` | ~200 B | Environment variables template |

### Frontend

| File | Lines | Purpose |
|------|-------|---------|
| `templates/index.html` | ~350 | Main UI with login and request form |
| `templates/dashboard.html` | ~250 | Analytics and admin dashboard |
| `templates/login.html` | ~80 | Simple login page |
| `static/style.css` | ~400 | Responsive CSS styling |

### Documentation

| File | Lines | Purpose |
|------|-------|---------|
| `README.md` | ~400 | Complete project documentation |
| `QUICKSTART.md` | ~150 | Quick start guide |
| `API_DOCUMENTATION.md` | ~500 | Detailed API reference |
| `PROJECT_SUMMARY.md` | ~400 | Implementation summary |

### Utilities

| File | Purpose |
|------|---------|
| `test_system.py` | Test suite and demo script |
| `run.bat` | Windows startup script |
| `run.sh` | Linux/Mac startup script |

---

## 🔄 Data Flow

```
1. User Input (Web UI)
   ↓
2. FastAPI Endpoint (/api/workflow/process)
   ↓
3. UI Agent (Validation)
   ↓
4. Logging Agent (Create Ticket)
   ↓
5. Classification Agent (RAG Search)
   ↓
6. Decision Agent (Auto-resolve or Escalate?)
   ↓
7a. Resolution Agent           7b. Escalation Agent
    (Provide Solution)             (Forward to Human)
   ↓                              ↓
8. Logging Agent (Update Ticket & Log Actions)
   ↓
9. Response to User
```

---

## 📊 Database Schema

```
users
├── id (PK)
├── username (unique)
├── email (unique)
├── hashed_password
├── full_name
├── role
├── is_active
└── created_at

tickets
├── id (PK)
├── ticket_id (unique)
├── user_id (FK → users)
├── issue_description
├── category
├── priority
├── status
├── resolution_type
├── resolution
├── resolution_instructions
├── confidence_score
├── auto_resolvable
├── requires_human
├── assigned_to
├── created_at
├── updated_at
├── resolved_at
└── closed_at

agent_logs
├── id (PK)
├── ticket_id (FK → tickets)
├── agent_name
├── action
├── input_data (JSON)
├── output_data (JSON)
├── status
├── processing_time_ms
├── confidence_score
├── metadata
├── error_message
└── created_at

knowledge_base
├── id (PK)
├── category
├── title
├── description
├── solution
├── keywords (JSON)
├── auto_resolvable
├── priority_level
├── success_rate
├── usage_count
├── created_at
└── updated_at

system_metrics
├── id (PK)
├── date
├── total_tickets
├── auto_resolved
├── escalated
├── pending
├── avg_resolution_time_seconds
├── avg_confidence_score
├── classification_accuracy
├── resolution_success_rate
├── category_distribution (JSON)
└── priority_distribution (JSON)
```

---

## 🎯 Key Components

### RAG System
- **Model**: all-MiniLM-L6-v2 (sentence transformers)
- **Vector DB**: ChromaDB
- **Embedding Dimension**: 384
- **Search Method**: Cosine similarity

### Authentication
- **Method**: JWT (JSON Web Tokens)
- **Algorithm**: HS256
- **Token Expiry**: 30 minutes (configurable)
- **Password Hashing**: bcrypt

### API Framework
- **Framework**: FastAPI
- **Server**: Uvicorn (ASGI)
- **Async**: Full async/await support
- **Docs**: Automatic OpenAPI/Swagger

---

## 📈 Statistics

### Total Project Size
- **Python Files**: ~2,200 lines
- **HTML/CSS**: ~1,000 lines
- **Documentation**: ~1,500 lines
- **Total**: ~4,700 lines of code

### Dependencies
- **Core**: 6 packages (FastAPI, SQLAlchemy, etc.)
- **AI/RAG**: 3 packages (sentence-transformers, chromadb)
- **Auth**: 3 packages (jose, passlib, bcrypt)
- **Total**: 18 packages

### Features
- **Agents**: 6 autonomous agents
- **API Endpoints**: 15+ RESTful endpoints
- **Database Tables**: 5 models
- **Issue Categories**: 10 supported types
- **User Roles**: 3 levels (user, it_staff, admin)

---

**Complete, production-ready system with all features implemented!** ✅
