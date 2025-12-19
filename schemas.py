"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# Enums
class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    IT_STAFF = "it_staff"


class TicketStatus(str, Enum):
    NEW = "new"
    CLASSIFIED = "classified"
    PROCESSING = "processing"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    CLOSED = "closed"


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# User Schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    role: UserRole = UserRole.USER


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None


# Ticket Schemas
class TicketCreate(BaseModel):
    issue_description: str = Field(..., min_length=10, max_length=2000)
    user_details: Optional[Dict[str, Any]] = None


class TicketUpdate(BaseModel):
    status: Optional[TicketStatus] = None
    resolution: Optional[str] = None
    assigned_to: Optional[str] = None


class TicketResponse(BaseModel):
    id: int
    ticket_id: str
    user_id: int
    issue_description: str
    category: Optional[str]
    priority: Optional[str]
    status: str
    resolution_type: Optional[str]
    resolution: Optional[str]
    resolution_instructions: Optional[str]
    confidence_score: Optional[float]
    auto_resolvable: bool
    requires_human: bool
    assigned_to: Optional[str]
    created_at: datetime
    resolved_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)


# Agent Communication Schemas
class ClassificationResult(BaseModel):
    category: str
    priority: Priority
    confidence_score: float
    keywords_matched: List[str]
    auto_resolvable: bool


class DecisionResult(BaseModel):
    action: str  # "auto_resolve" or "escalate"
    reasoning: str
    confidence: float
    requires_human: bool


class ResolutionResult(BaseModel):
    status: str  # "resolved" or "failed"
    solution: Optional[str]
    instructions: Optional[str]
    success: bool


class EscalationResult(BaseModel):
    status: str
    ticket_id: str
    assigned_to: str
    priority: Priority
    estimated_response_time: str
    message: str


# Agent Log Schema
class AgentLogCreate(BaseModel):
    ticket_id: int
    agent_name: str
    action: str
    input_data: Optional[str]
    output_data: Optional[str]
    status: str
    processing_time_ms: Optional[float]
    confidence_score: Optional[float]
    meta_data: Optional[str]
    error_message: Optional[str]


class AgentLogResponse(BaseModel):
    id: int
    agent_name: str
    action: str
    status: str
    processing_time_ms: Optional[float]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Workflow Schemas
class WorkflowRequest(BaseModel):
    issue_description: str = Field(..., min_length=10)
    user_id: Optional[int] = None


class WorkflowResponse(BaseModel):
    ticket_id: str
    status: str
    category: Optional[str]
    priority: Optional[str]
    resolution_type: str
    message: str
    resolution_instructions: Optional[str]
    requires_human: bool
    estimated_resolution_time: Optional[str]


# Analytics Schemas
class TicketAnalytics(BaseModel):
    total_tickets: int
    auto_resolved: int
    escalated: int
    pending: int
    resolution_rate: float
    avg_resolution_time: Optional[float]


class AgentPerformance(BaseModel):
    agent_name: str
    total_actions: int
    success_rate: float
    avg_processing_time: float
    avg_confidence: float


class DashboardMetrics(BaseModel):
    tickets: TicketAnalytics
    agent_performance: List[AgentPerformance]
    category_distribution: Dict[str, int]
    priority_distribution: Dict[str, int]
    recent_tickets: List[TicketResponse]


# Knowledge Base Schemas
class KnowledgeBaseEntry(BaseModel):
    category: str
    title: str
    description: Optional[str]
    solution: str
    keywords: List[str]
    auto_resolvable: bool = True
    priority_level: Optional[Priority] = None


class KnowledgeBaseResponse(KnowledgeBaseEntry):
    id: int
    success_rate: float
    usage_count: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
