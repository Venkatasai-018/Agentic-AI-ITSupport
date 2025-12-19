"""
Database models using SQLAlchemy
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    """User model for authentication and authorization"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    role = Column(String(20), default="user")  # user, admin, it_staff
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    tickets = relationship("Ticket", back_populates="user")


class Ticket(Base):
    """Ticket model for IT support requests"""
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String(50), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Request details
    issue_description = Column(Text, nullable=False)
    category = Column(String(50))
    priority = Column(String(20))  # low, medium, high, critical
    
    # Status tracking
    status = Column(String(20), default="new")  # new, classified, resolved, escalated, closed
    resolution_type = Column(String(20))  # automatic, human, escalated
    
    # Resolution details
    resolution = Column(Text)
    resolution_instructions = Column(Text)
    
    # Agent processing
    confidence_score = Column(Float)
    auto_resolvable = Column(Boolean, default=False)
    requires_human = Column(Boolean, default=False)
    
    # Assignment
    assigned_to = Column(String(100))
    assigned_at = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime)
    closed_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="tickets")
    logs = relationship("AgentLog", back_populates="ticket", cascade="all, delete-orphan")


class AgentLog(Base):
    """Agent activity logs for audit trail"""
    __tablename__ = "agent_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    
    # Agent details
    agent_name = Column(String(50), nullable=False)
    action = Column(String(100), nullable=False)
    
    # Processing details
    input_data = Column(Text)
    output_data = Column(Text)
    status = Column(String(20))  # success, failed, warning
    
    # Metrics
    processing_time_ms = Column(Float)
    confidence_score = Column(Float)
    
    # Additional context
    meta_data = Column(Text)
    error_message = Column(Text)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    ticket = relationship("Ticket", back_populates="logs")


class KnowledgeBase(Base):
    """Knowledge base entries for resolution"""
    __tablename__ = "knowledge_base"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    solution = Column(Text, nullable=False)
    keywords = Column(Text)  # JSON array stored as text
    
    # Metadata
    auto_resolvable = Column(Boolean, default=True)
    priority_level = Column(String(20))
    success_rate = Column(Float, default=0.0)
    usage_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SystemMetrics(Base):
    """System-wide metrics for analytics"""
    __tablename__ = "system_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Volume metrics
    total_tickets = Column(Integer, default=0)
    auto_resolved = Column(Integer, default=0)
    escalated = Column(Integer, default=0)
    pending = Column(Integer, default=0)
    
    # Performance metrics
    avg_resolution_time_seconds = Column(Float)
    avg_confidence_score = Column(Float)
    
    # Agent metrics
    classification_accuracy = Column(Float)
    resolution_success_rate = Column(Float)
    
    # Category breakdown (JSON stored as text)
    category_distribution = Column(Text)
    priority_distribution = Column(Text)
