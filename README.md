# 🤖 Agentic AI IT Support System

**FastAPI-based Multi-Agent Architecture with RAG (Retrieval Augmented Generation)**

A production-ready, intelligent IT support automation system that leverages multiple autonomous AI agents working sequentially to classify, resolve, and escalate IT support requests. The system uses RAG technology for accurate issue classification and resolution recommendations.

---

## 🌟 Key Features

### 1. **User Interaction Features**
- ✅ Web-based interface for submitting IT support requests
- ✅ Real-time ticket status tracking
- ✅ User authentication and authorization (JWT-based)
- ✅ Role-based access control (User, IT Staff, Admin)
- ✅ Notification messages for resolutions and escalations

### 2. **Agentic AI Architecture**
- ✅ **Multi-agent system** with 6 specialized agents
- ✅ **Sequential agent orchestration** via FastAPI
- ✅ **Autonomous decision-making** without human intervention (when possible)
- ✅ **Context passing** through structured JSON between agents
- ✅ **Human-in-the-loop** escalation for complex issues
- ✅ **RAG-powered classification** using semantic search

### 3. **AI Agents**

#### **UI Agent**
- Captures and validates user input
- Structures request data for downstream agents
- Input sanitization and validation

#### **Classification Agent** (RAG-Powered)
- Uses sentence transformers for semantic embeddings
- ChromaDB vector database for similarity search
- Identifies issue category with confidence scores
- Assigns priority levels (low, medium, high, critical)
- Supports 10+ issue categories

#### **Decision Agent**
- Evaluates classification confidence
- Determines auto-resolve vs. escalation path
- Applies business rules and thresholds
- Routes requests to appropriate agents

#### **Resolution Agent**
- Provides step-by-step solutions from knowledge base
- Generates formatted resolution instructions
- Handles predefined IT issues automatically
- Returns success/failure status

#### **Escalation Agent**
- Packages full context for human IT staff
- Creates escalation tickets with priority
- Assigns to IT support team
- Provides estimated response times

#### **Logging Agent**
- Stores all ticket data in SQLite database
- Maintains full audit trail of agent actions
- Tracks processing times and confidence scores
- Supports analytics and monitoring

### 4. **Backend & FastAPI Features**
- ✅ RESTful APIs for all operations
- ✅ Asynchronous request handling (async/await)
- ✅ Automatic API documentation (Swagger UI at `/docs`)
- ✅ Modular agent endpoints
- ✅ Central orchestration workflow
- ✅ Database connection pooling

### 5. **Data Handling**
- ✅ Structured JSON communication between agents
- ✅ SQLite database with SQLAlchemy ORM
- ✅ Pydantic schemas for validation
- ✅ Complete audit trail and query history
- ✅ Knowledge base management

### 6. **Security & Reliability**
- ✅ JWT token-based authentication
- ✅ Password hashing (bcrypt)
- ✅ Input validation and sanitization
- ✅ Role-based access control
- ✅ Error handling and fallback mechanisms
- ✅ Safe escalation when AI confidence is low

### 7. **Analytics & Monitoring**
- ✅ Ticket volume tracking
- ✅ Resolution time measurement
- ✅ Agent performance statistics
- ✅ Category and priority distribution
- ✅ Real-time dashboard
- ✅ Success rate metrics

---

## 📁 Project Structure

```
Agentic-AI-ITSupport/
├── main.py                    # FastAPI main application & orchestration
├── config.py                  # Application configuration
├── database.py                # Database setup and session management
├── models.py                  # SQLAlchemy database models
├── schemas.py                 # Pydantic schemas for validation
├── auth.py                    # Authentication & authorization
├── agents.py                  # All AI agents implementation
├── rag_system.py              # RAG system with ChromaDB
├── knowledge_base.json        # IT support knowledge base
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
├── static/
│   └── style.css              # Frontend styles
├── templates/
│   ├── index.html             # Main support form
│   ├── dashboard.html         # Analytics dashboard
│   └── login.html             # Login page
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone or navigate to the project directory**

2. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Create `.env` file** (copy from `.env.example`):
   ```powershell
   cp .env.example .env
   ```
   
   Update the SECRET_KEY in `.env`:
   ```
   SECRET_KEY=your-secret-key-here-change-this
   ```

4. **Run the application**:
   ```powershell
   python main.py
   ```

   Or with uvicorn:
   ```powershell
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the application**:
   - **Main Interface**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs
   - **Dashboard**: http://localhost:8000/dashboard

6. **Default Login**:
   - Username: `admin`
   - Password: `admin123`

---

## 💡 How It Works

### Workflow Overview

```
User Request → UI Agent → Classification Agent (RAG) → Decision Agent
                                ↓
                    Auto-Resolve or Escalate?
                    ↙                        ↘
        Resolution Agent                Escalation Agent
                    ↓                            ↓
            Logging Agent              Logging Agent
                    ↓                            ↓
            Issue Resolved!            Ticket Escalated to IT
```

### Detailed Process

1. **User submits IT issue** via web interface
2. **UI Agent** validates and structures the request
3. **Logging Agent** creates a ticket in the database
4. **Classification Agent** uses RAG to:
   - Generate embeddings of the issue description
   - Perform semantic search in ChromaDB
   - Find the most relevant knowledge base entry
   - Assign category, priority, and confidence score
5. **Decision Agent** evaluates:
   - Classification confidence
   - Issue priority
   - Auto-resolvability flag
   - Determines resolution path
6. **Resolution or Escalation**:
   - **Auto-Resolve**: Resolution Agent provides step-by-step solution
   - **Escalate**: Escalation Agent forwards to human IT staff
7. **Logging Agent** records all agent actions and updates ticket status

---

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info

### Workflow
- `POST /api/workflow/process` - Main workflow endpoint (processes IT request)

### Tickets
- `GET /api/tickets` - List tickets (filtered by role)
- `GET /api/tickets/{ticket_id}` - Get ticket details
- `PATCH /api/tickets/{ticket_id}` - Update ticket (IT staff only)
- `GET /api/tickets/{ticket_id}/logs` - Get agent logs for ticket

### Analytics
- `GET /api/analytics/dashboard` - Dashboard metrics (IT staff only)

### Health
- `GET /health` - Health check endpoint

---

## 🗃️ Knowledge Base Categories

The system includes pre-configured knowledge for:

1. **Password Reset** - Account recovery and login issues
2. **Network Connectivity** - WiFi and internet problems
3. **Software Installation** - Application installation requests
4. **Email Issues** - Outlook and email problems
5. **VPN Access** - Remote access and VPN connectivity
6. **Printer Issues** - Printing and printer connectivity
7. **Hardware Issues** - Equipment malfunctions and repairs
8. **Account Access** - Permission and authorization requests
9. **Microsoft Office Issues** - Office application problems
10. **Security and Malware** - Security concerns and threats

---

## 🧪 Testing

### Test the RAG system:
```powershell
python rag_system.py
```

### Test individual components:
```powershell
# Test database setup
python database.py

# Run the full application
python main.py
```

### Example API Requests:

**Register User**:
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"test123","role":"user"}'
```

**Submit IT Request**:
```bash
curl -X POST "http://localhost:8000/api/workflow/process" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"issue_description":"I forgot my password"}'
```

---

## 🔧 Configuration

### Environment Variables

Edit `.env` file:

```env
# Application
APP_NAME=Agentic IT Support System
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Security
SECRET_KEY=your-secret-key-change-this
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=sqlite+aiosqlite:///./it_support.db

# Agent Configuration
AUTO_RESOLVE_CONFIDENCE_THRESHOLD=0.7
MAX_RESOLUTION_ATTEMPTS=3
```

---

## 👥 User Roles

### User
- Submit IT support requests
- View own tickets
- Check ticket status

### IT Staff
- All user permissions
- View all tickets
- Update ticket status
- Assign tickets
- Access analytics dashboard

### Admin
- All IT staff permissions
- Manage users
- System configuration
- Full dashboard access

---

## 📈 Future Enhancements

- [ ] Integration with OpenAI GPT for more intelligent responses
- [ ] Email notifications for ticket updates
- [ ] Multi-language support
- [ ] Real-time chat support
- [ ] Integration with Slack/Teams
- [ ] Mobile app
- [ ] Advanced analytics and reporting
- [ ] Knowledge base auto-learning from resolutions
- [ ] SLA tracking and alerts

---

## 🛠️ Technology Stack

- **Backend**: FastAPI, Python 3.8+
- **Database**: SQLite with SQLAlchemy (async)
- **RAG**: Sentence Transformers, ChromaDB
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **API Docs**: Swagger UI (automatic)

---

## 📝 License

This is an educational/demo project. For production use, ensure proper security audits and compliance.

---

## 👨‍💻 Author

Built as a demonstration of agentic AI systems with RAG technology and FastAPI.

---

## 🆘 Support

For issues or questions:
1. Check the API documentation at `/docs`
2. Review the logs in the console
3. Check database for ticket status

---

**Note**: This system demonstrates a production-ready architecture but should be enhanced with additional security measures, monitoring, and testing before deploying to a real production environment.
