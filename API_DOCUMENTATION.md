# 📚 API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication

All protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

---

## 🔐 Authentication Endpoints

### Register User
Create a new user account.

**Endpoint**: `POST /api/auth/register`

**Request Body**:
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "password123",
  "full_name": "John Doe",
  "role": "user"
}
```

**Roles**: `user`, `it_staff`, `admin`

**Response** (201 Created):
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "role": "user",
  "is_active": true,
  "created_at": "2025-12-19T10:30:00"
}
```

---

### Login
Authenticate and receive JWT token.

**Endpoint**: `POST /api/auth/login`

**Request** (Form Data):
```
username=johndoe
password=password123
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### Get Current User
Get information about the authenticated user.

**Endpoint**: `GET /api/auth/me`

**Headers**:
```
Authorization: Bearer YOUR_TOKEN
```

**Response**:
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "role": "user",
  "is_active": true,
  "created_at": "2025-12-19T10:30:00"
}
```

---

## 🤖 Workflow Endpoints

### Process IT Support Request
Main workflow endpoint - orchestrates all agents to process an IT support request.

**Endpoint**: `POST /api/workflow/process`

**Headers**:
```
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json
```

**Request Body**:
```json
{
  "issue_description": "I forgot my password and can't login to my account"
}
```

**Response** (Auto-Resolved):
```json
{
  "ticket_id": "IT-20251219-1234",
  "status": "resolved",
  "category": "Password Reset",
  "priority": "medium",
  "resolution_type": "automatic",
  "message": "✅ Automatic Resolution - Password Reset and Account Recovery\n\nTo reset your password:\n1. Go to the company password reset portal...",
  "resolution_instructions": "Full step-by-step instructions...",
  "requires_human": false,
  "estimated_resolution_time": "Immediate"
}
```

**Response** (Escalated):
```json
{
  "ticket_id": "IT-20251219-1235",
  "status": "escalated",
  "category": "Hardware Issues",
  "priority": "high",
  "resolution_type": "escalated",
  "message": "📨 Your request has been escalated to our IT support team...",
  "resolution_instructions": null,
  "requires_human": true,
  "estimated_resolution_time": "2-4 hours"
}
```

**Agent Flow**:
1. UI Agent → Validates input
2. Classification Agent (RAG) → Identifies category
3. Decision Agent → Auto-resolve or escalate?
4. Resolution/Escalation Agent → Handles the issue
5. Logging Agent → Records everything

---

## 🎫 Ticket Management Endpoints

### List Tickets
Get a list of tickets (users see their own, admin/IT staff see all).

**Endpoint**: `GET /api/tickets`

**Headers**:
```
Authorization: Bearer YOUR_TOKEN
```

**Query Parameters**:
- `skip` (optional): Number of tickets to skip (default: 0)
- `limit` (optional): Maximum tickets to return (default: 50)
- `status_filter` (optional): Filter by status (new, resolved, escalated, etc.)

**Example**:
```
GET /api/tickets?skip=0&limit=10&status_filter=resolved
```

**Response**:
```json
[
  {
    "id": 1,
    "ticket_id": "IT-20251219-1234",
    "user_id": 1,
    "issue_description": "I forgot my password",
    "category": "Password Reset",
    "priority": "medium",
    "status": "resolved",
    "resolution_type": "automatic",
    "resolution": "Password reset instructions",
    "resolution_instructions": "Full instructions...",
    "confidence_score": 0.95,
    "auto_resolvable": true,
    "requires_human": false,
    "assigned_to": null,
    "created_at": "2025-12-19T10:30:00",
    "resolved_at": "2025-12-19T10:30:15"
  }
]
```

---

### Get Ticket Details
Get detailed information about a specific ticket.

**Endpoint**: `GET /api/tickets/{ticket_id}`

**Headers**:
```
Authorization: Bearer YOUR_TOKEN
```

**Example**:
```
GET /api/tickets/IT-20251219-1234
```

**Response**: Same as single ticket object from list endpoint.

**Authorization**: Users can only view their own tickets. IT staff and admins can view all tickets.

---

### Update Ticket
Update ticket information (IT staff and admin only).

**Endpoint**: `PATCH /api/tickets/{ticket_id}`

**Headers**:
```
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json
```

**Request Body** (all fields optional):
```json
{
  "status": "resolved",
  "resolution": "Issue has been fixed",
  "assigned_to": "John Smith (IT)"
}
```

**Response**: Updated ticket object.

**Authorization**: IT staff and admin only.

---

### Get Ticket Logs
Get all agent logs for a specific ticket.

**Endpoint**: `GET /api/tickets/{ticket_id}/logs`

**Headers**:
```
Authorization: Bearer YOUR_TOKEN
```

**Example**:
```
GET /api/tickets/IT-20251219-1234/logs
```

**Response**:
```json
[
  {
    "id": 1,
    "agent_name": "Classification Agent",
    "action": "classify_issue",
    "status": "success",
    "processing_time_ms": 45.2,
    "created_at": "2025-12-19T10:30:00"
  },
  {
    "id": 2,
    "agent_name": "Decision Agent",
    "action": "make_decision",
    "status": "success",
    "processing_time_ms": 12.8,
    "created_at": "2025-12-19T10:30:01"
  }
]
```

---

## 📊 Analytics Endpoints

### Dashboard Metrics
Get comprehensive dashboard metrics (IT staff and admin only).

**Endpoint**: `GET /api/analytics/dashboard`

**Headers**:
```
Authorization: Bearer YOUR_TOKEN
```

**Response**:
```json
{
  "tickets": {
    "total_tickets": 150,
    "auto_resolved": 95,
    "escalated": 42,
    "pending": 13,
    "resolution_rate": 63.3,
    "avg_resolution_time": 45.5
  },
  "agent_performance": [
    {
      "agent_name": "Classification Agent",
      "total_actions": 150,
      "success_rate": 98.7,
      "avg_processing_time": 45.2,
      "avg_confidence": 0.87
    },
    {
      "agent_name": "Decision Agent",
      "total_actions": 150,
      "success_rate": 100.0,
      "avg_processing_time": 12.5,
      "avg_confidence": 0.0
    }
  ],
  "category_distribution": {
    "Password Reset": 45,
    "Network Connectivity": 28,
    "Email Issues": 22,
    "Hardware Issues": 18
  },
  "priority_distribution": {
    "high": 35,
    "medium": 85,
    "low": 30
  },
  "recent_tickets": [...]
}
```

**Authorization**: IT staff and admin only.

---

## ❤️ Health Check

### Health Check
Check if the application is running.

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "app": "Agentic IT Support System",
  "version": "1.0.0",
  "timestamp": "2025-12-19T10:30:00"
}
```

---

## 🌐 Web Interface Routes

### Home Page
Main IT support request submission form.

**URL**: `GET /`

### Dashboard
Admin dashboard with analytics and metrics.

**URL**: `GET /dashboard`

### Login Page
User login interface.

**URL**: `GET /login`

---

## 📋 Status Codes

- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Missing or invalid authentication
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## 🔍 Swagger Documentation

Interactive API documentation is available at:
```
http://localhost:8000/docs
```

Alternative ReDoc documentation:
```
http://localhost:8000/redoc
```

---

## 💡 Example Workflows

### Complete User Journey

1. **Register**:
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"test123","role":"user","full_name":"Test User"}'
```

2. **Login**:
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=test123"
```

3. **Submit IT Request**:
```bash
curl -X POST "http://localhost:8000/api/workflow/process" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"issue_description":"I forgot my password"}'
```

4. **Check Tickets**:
```bash
curl -X GET "http://localhost:8000/api/tickets" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

5. **View Ticket Details**:
```bash
curl -X GET "http://localhost:8000/api/tickets/IT-20251219-1234" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

6. **View Agent Logs**:
```bash
curl -X GET "http://localhost:8000/api/tickets/IT-20251219-1234/logs" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🛡️ Security Notes

- All passwords are hashed using bcrypt
- JWT tokens expire after 30 minutes (configurable)
- Role-based access control enforced on all endpoints
- Input validation using Pydantic schemas
- SQL injection protection via SQLAlchemy ORM

---

For more details, visit the interactive documentation at `/docs`.
