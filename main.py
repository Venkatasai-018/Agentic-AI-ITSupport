"""
Main FastAPI Application
Central orchestration for the Agentic AI IT Support System
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta
from typing import List, Optional

from config import settings
from database import init_db, get_db
from models import Ticket, AgentLog, SystemMetrics
from schemas import (
    TicketCreate, TicketResponse, TicketUpdate,
    WorkflowRequest, WorkflowResponse,
    AgentLogResponse, DashboardMetrics, TicketAnalytics
)
from rag_system import get_rag_system
from agents import create_agents
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting Agentic AI IT Support System...")
    await init_db()
    
    # Initialize RAG system
    rag = get_rag_system()
    logger.info("RAG system initialized")
    
    logger.info(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} is ready!")
    logger.info(f"📚 API Documentation: http://{settings.HOST}:{settings.PORT}/docs")
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Agentic AI-powered IT Support System with RAG and multi-agent architecture",
    lifespan=lifespan
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ==================== Workflow Orchestration Endpoint ====================

@app.post("/api/workflow/process", response_model=WorkflowResponse)
async def process_workflow(
    request: WorkflowRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Main workflow endpoint - Orchestrates all agents
    
    Process:
    1. UI Agent captures request
    2. Classification Agent (RAG) identifies issue
    3. Decision Agent determines resolution path
    4. Resolution/Escalation Agent handles the issue
    5. Logging Agent records everything
    """
    logger.info(f"Processing new workflow request")
    
    # Initialize RAG system and agents
    rag = get_rag_system()
    agents = create_agents(db, rag)
    
    # Step 1: UI Agent - Capture request
    ui_result = agents["ui"].capture_request(
        issue_description=request.issue_description,
        user_id=1,  # Default user ID
        user_details={"email": "user@company.com", "full_name": "Anonymous User"}
    )
    
    if not ui_result["success"]:
        raise HTTPException(status_code=400, detail=ui_result.get("error", "Invalid request"))
    
    # Step 2: Create ticket
    ticket_id = await agents["logging"].create_ticket(
        issue_description=request.issue_description,
        user_id=1  # Default user ID
    )
    
    # Get ticket object
    result = await db.execute(select(Ticket).where(Ticket.ticket_id == ticket_id))
    ticket = result.scalar_one()
    
    # Step 3: Classification Agent (RAG-powered)
    classification = agents["classification"].classify(request.issue_description)
    
    await agents["logging"].log_agent_action(
        ticket_id=ticket.id,
        agent_name="Classification Agent",
        action="classify_issue",
        input_data={"issue": request.issue_description},
        output_data=classification,
        status="success" if classification["success"] else "failed",
        processing_time_ms=classification.get("processing_time_ms", 0),
        confidence_score=classification.get("confidence_score")
    )
    
    # Update ticket with classification
    await agents["logging"].update_ticket(
        ticket_id=ticket_id,
        category=classification.get("category"),
        priority=classification.get("priority"),
        confidence_score=classification.get("confidence_score"),
        auto_resolvable=classification.get("auto_resolvable", False),
        status="classified"
    )
    
    # Step 4: Decision Agent
    decision = agents["decision"].decide(classification)
    
    await agents["logging"].log_agent_action(
        ticket_id=ticket.id,
        agent_name="Decision Agent",
        action="make_decision",
        input_data=classification,
        output_data=decision,
        status="success",
        processing_time_ms=decision.get("processing_time_ms", 0)
    )
    
    # Step 5: Resolution or Escalation
    if decision["action"] == "auto_resolve":
        # Resolution Agent
        resolution = agents["resolution"].resolve(classification, request.issue_description)
        
        await agents["logging"].log_agent_action(
            ticket_id=ticket.id,
            agent_name="Resolution Agent",
            action="auto_resolve",
            input_data=classification,
            output_data=resolution,
            status=resolution["status"],
            processing_time_ms=resolution.get("processing_time_ms", 0)
        )
        
        # Update ticket
        await agents["logging"].update_ticket(
            ticket_id=ticket_id,
            status="resolved",
            resolution_type="automatic",
            resolution=resolution.get("solution"),
            resolution_instructions=resolution.get("instructions"),
            resolved_at=datetime.utcnow(),
            requires_human=False
        )
        
        response = WorkflowResponse(
            ticket_id=ticket_id,
            status="resolved",
            category=classification.get("category"),
            priority=classification.get("priority"),
            resolution_type="automatic",
            message=resolution.get("instructions", "Issue resolved automatically"),
            resolution_instructions=resolution.get("instructions"),
            requires_human=False,
            estimated_resolution_time="Immediate"
        )
        
    else:
        # Escalation Agent
        escalation = agents["escalation"].escalate(
            issue_description=request.issue_description,
            classification=classification,
            ticket_id=ticket_id
        )
        
        await agents["logging"].log_agent_action(
            ticket_id=ticket.id,
            agent_name="Escalation Agent",
            action="escalate_to_human",
            input_data=classification,
            output_data=escalation,
            status="escalated",
            processing_time_ms=escalation.get("processing_time_ms", 0)
        )
        
        # Update ticket
        await agents["logging"].update_ticket(
            ticket_id=ticket_id,
            status="escalated",
            resolution_type="escalated",
            assigned_to=escalation.get("assigned_to"),
            assigned_at=datetime.utcnow(),
            requires_human=True
        )
        
        response = WorkflowResponse(
            ticket_id=ticket_id,
            status="escalated",
            category=classification.get("category"),
            priority=classification.get("priority"),
            resolution_type="escalated",
            message=escalation.get("message", "Issue escalated to IT support"),
            resolution_instructions=None,
            requires_human=True,
            estimated_resolution_time=escalation.get("estimated_response_time")
        )
    
    logger.info(f"Workflow completed for ticket {ticket_id}: {response.status}")
    return response


# ==================== Ticket Management Endpoints ====================

@app.get("/api/tickets", response_model=List[TicketResponse])
async def get_tickets(
    skip: int = 0,
    limit: int = 50,
    status_filter: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all tickets"""
    query = select(Ticket).order_by(Ticket.created_at.desc())
    
    if status_filter:
        query = query.where(Ticket.status == status_filter)
    
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    tickets = result.scalars().all()
    
    return tickets


@app.get("/api/tickets/{ticket_id}", response_model=TicketResponse)
async def get_ticket(
    ticket_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get specific ticket details"""
    result = await db.execute(select(Ticket).where(Ticket.ticket_id == ticket_id))
    ticket = result.scalar_one_or_none()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return ticket


@app.patch("/api/tickets/{ticket_id}", response_model=TicketResponse)
async def update_ticket(
    ticket_id: str,
    update_data: TicketUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update ticket"""
    result = await db.execute(select(Ticket).where(Ticket.ticket_id == ticket_id))
    ticket = result.scalar_one_or_none()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Update fields
    if update_data.status:
        ticket.status = update_data.status
    if update_data.resolution:
        ticket.resolution = update_data.resolution
        ticket.resolved_at = datetime.utcnow()
    if update_data.assigned_to:
        ticket.assigned_to = update_data.assigned_to
        ticket.assigned_at = datetime.utcnow()
    
    ticket.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(ticket)
    
    logger.info(f"Ticket {ticket_id} updated")
    return ticket


@app.get("/api/tickets/{ticket_id}/logs", response_model=List[AgentLogResponse])
async def get_ticket_logs(
    ticket_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get agent logs for a ticket"""
    # Get ticket first
    result = await db.execute(select(Ticket).where(Ticket.ticket_id == ticket_id))
    ticket = result.scalar_one_or_none()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Get logs
    result = await db.execute(
        select(AgentLog)
        .where(AgentLog.ticket_id == ticket.id)
        .order_by(AgentLog.created_at)
    )
    logs = result.scalars().all()
    
    return logs


# ==================== Analytics Endpoints ====================

@app.get("/api/analytics/dashboard", response_model=DashboardMetrics)
async def get_dashboard_metrics(
    db: AsyncSession = Depends(get_db)
):
    """Get dashboard metrics"""
    # Ticket analytics
    total_result = await db.execute(select(func.count(Ticket.id)))
    total_tickets = total_result.scalar()
    
    resolved_result = await db.execute(
        select(func.count(Ticket.id)).where(Ticket.status == "resolved")
    )
    auto_resolved = resolved_result.scalar()
    
    escalated_result = await db.execute(
        select(func.count(Ticket.id)).where(Ticket.status == "escalated")
    )
    escalated = escalated_result.scalar()
    
    pending_result = await db.execute(
        select(func.count(Ticket.id)).where(Ticket.status.in_(["new", "classified", "processing"]))
    )
    pending = pending_result.scalar()
    
    resolution_rate = (auto_resolved / total_tickets * 100) if total_tickets > 0 else 0
    
    # Category distribution
    category_result = await db.execute(
        select(Ticket.category, func.count(Ticket.id))
        .where(Ticket.category.isnot(None))
        .group_by(Ticket.category)
    )
    category_dist = {row[0]: row[1] for row in category_result}
    
    # Priority distribution
    priority_result = await db.execute(
        select(Ticket.priority, func.count(Ticket.id))
        .where(Ticket.priority.isnot(None))
        .group_by(Ticket.priority)
    )
    priority_dist = {row[0]: row[1] for row in priority_result}
    
    # Recent tickets
    recent_result = await db.execute(
        select(Ticket).order_by(Ticket.created_at.desc()).limit(10)
    )
    recent_tickets = recent_result.scalars().all()
    
    # Agent performance (simplified)
    agent_performance = []
    agents_list = ["Classification Agent", "Decision Agent", "Resolution Agent", "Escalation Agent"]
    
    for agent_name in agents_list:
        log_result = await db.execute(
            select(
                func.count(AgentLog.id),
                func.avg(AgentLog.processing_time_ms),
                func.avg(AgentLog.confidence_score)
            )
            .where(AgentLog.agent_name == agent_name)
        )
        row = log_result.first()
        
        if row and row[0] > 0:
            success_result = await db.execute(
                select(func.count(AgentLog.id))
                .where(AgentLog.agent_name == agent_name, AgentLog.status == "success")
            )
            success_count = success_result.scalar()
            
            agent_performance.append({
                "agent_name": agent_name,
                "total_actions": row[0],
                "success_rate": (success_count / row[0] * 100) if row[0] > 0 else 0,
                "avg_processing_time": row[1] or 0,
                "avg_confidence": row[2] or 0
            })
    
    return DashboardMetrics(
        tickets=TicketAnalytics(
            total_tickets=total_tickets,
            auto_resolved=auto_resolved,
            escalated=escalated,
            pending=pending,
            resolution_rate=resolution_rate,
            avg_resolution_time=None
        ),
        agent_performance=agent_performance,
        category_distribution=category_dist,
        priority_distribution=priority_dist,
        recent_tickets=recent_tickets
    )


# ==================== Web Interface Routes ====================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page - IT support request form"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Admin dashboard"""
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse("login.html", {"request": request})


# ==================== Health Check ====================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
