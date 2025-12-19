"""
AI Agents for IT Support System with RAG Integration
Each agent is autonomous and communicates via structured data
"""
import json
import time
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import logging
from rag_system import RAGSystem

logger = logging.getLogger(__name__)


class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"Agent.{name}")
    
    def log_action(self, action: str, status: str, **kwargs):
        """Log agent action"""
        self.logger.info(f"[{self.name}] {action} - Status: {status}")


class UIAgent(BaseAgent):
    """
    UI Agent - Captures and validates user input
    First point of contact in the workflow
    """
    
    def __init__(self):
        super().__init__("UI Agent")
    
    def capture_request(self, issue_description: str, user_id: int, user_details: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Capture and structure user request
        
        Args:
            issue_description: User's issue description
            user_id: User identifier
            user_details: Additional user information
            
        Returns:
            Structured request data
        """
        start_time = time.time()
        
        self.log_action("Capturing user request", "processing")
        
        # Validate input
        if not issue_description or len(issue_description) < 10:
            self.log_action("Input validation", "failed")
            return {
                "success": False,
                "error": "Issue description must be at least 10 characters"
            }
        
        # Structure the request
        request_data = {
            "success": True,
            "issue_description": issue_description.strip(),
            "user_id": user_id,
            "user_details": user_details or {},
            "timestamp": datetime.utcnow().isoformat(),
            "processing_time_ms": (time.time() - start_time) * 1000
        }
        
        self.log_action("Request captured successfully", "success")
        return request_data


class ClassificationAgent(BaseAgent):
    """
    Classification Agent - Uses RAG to classify IT issues
    Performs semantic search to identify issue category
    """
    
    def __init__(self, rag_system: RAGSystem):
        super().__init__("Classification Agent")
        self.rag = rag_system
        self.confidence_threshold = 0.6
    
    def classify(self, issue_description: str) -> Dict[str, Any]:
        """
        Classify IT issue using RAG-based semantic search
        
        Args:
            issue_description: User's issue description
            
        Returns:
            Classification result with category, priority, and confidence
        """
        start_time = time.time()
        
        self.log_action(f"Classifying issue: '{issue_description[:50]}...'", "processing")
        
        try:
            # Use RAG to find best matching knowledge base entry
            best_match = self.rag.get_best_match(issue_description)
            
            if not best_match:
                self.log_action("Classification", "failed - no match found")
                return {
                    "success": False,
                    "category": "Unknown",
                    "priority": "medium",
                    "confidence_score": 0.0,
                    "auto_resolvable": False,
                    "keywords_matched": [],
                    "rag_solution": None,
                    "error": "No matching knowledge base entry found"
                }
            
            # Calculate confidence based on relevance score
            relevance_score = best_match.get('relevance_score', 0.0)
            confidence_level = "high" if relevance_score > 0.7 else "medium" if relevance_score > 0.5 else "low"
            
            classification = {
                "success": True,
                "category": best_match['category'],
                "title": best_match.get('title', best_match['category']),
                "priority": best_match['priority'],
                "confidence_score": relevance_score,
                "confidence_level": confidence_level,
                "auto_resolvable": best_match['auto_resolvable'] and relevance_score > self.confidence_threshold,
                "keywords_matched": best_match['keywords'],
                "rag_solution": best_match['solution'],
                "description": best_match.get('description', ''),
                "processing_time_ms": (time.time() - start_time) * 1000
            }
            
            self.log_action(
                f"Classified as '{classification['category']}' with {confidence_level} confidence ({relevance_score:.3f})",
                "success"
            )
            
            return classification
            
        except Exception as e:
            self.logger.error(f"Classification error: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "category": "Unknown",
                "priority": "medium",
                "confidence_score": 0.0,
                "auto_resolvable": False
            }


class DecisionAgent(BaseAgent):
    """
    Decision Agent - Decides resolution path
    Determines whether issue can be auto-resolved or needs escalation
    """
    
    def __init__(self):
        super().__init__("Decision Agent")
        self.auto_resolve_threshold = 0.7
    
    def decide(self, classification: Dict[str, Any]) -> Dict[str, Any]:
        """
        Decide resolution path based on classification
        
        Args:
            classification: Classification result from ClassificationAgent
            
        Returns:
            Decision with action (auto_resolve/escalate) and reasoning
        """
        start_time = time.time()
        
        self.log_action("Evaluating resolution path", "processing")
        
        confidence_score = classification.get('confidence_score', 0.0)
        auto_resolvable = classification.get('auto_resolvable', False)
        priority = classification.get('priority', 'medium')
        
        # Decision logic
        if auto_resolvable and confidence_score >= self.auto_resolve_threshold:
            action = "auto_resolve"
            reasoning = f"Issue classified as '{classification['category']}' with high confidence ({confidence_score:.2f}) and marked as auto-resolvable"
            requires_human = False
            
        elif priority == "critical":
            action = "escalate"
            reasoning = "Critical priority issues always require immediate human attention"
            requires_human = True
            
        elif confidence_score < 0.5:
            action = "escalate"
            reasoning = f"Low confidence score ({confidence_score:.2f}) - human review needed"
            requires_human = True
            
        else:
            action = "escalate"
            reasoning = "Issue complexity or policy requires human IT staff involvement"
            requires_human = True
        
        decision = {
            "success": True,
            "action": action,
            "reasoning": reasoning,
            "confidence": confidence_score,
            "requires_human": requires_human,
            "processing_time_ms": (time.time() - start_time) * 1000
        }
        
        self.log_action(f"Decision: {action.upper()}", "success")
        
        return decision


class ResolutionAgent(BaseAgent):
    """
    Resolution Agent - Handles automatic resolution
    Provides step-by-step instructions from RAG knowledge base
    """
    
    def __init__(self):
        super().__init__("Resolution Agent")
    
    def resolve(self, classification: Dict[str, Any], issue_description: str) -> Dict[str, Any]:
        """
        Attempt automatic resolution of the issue
        
        Args:
            classification: Classification result
            issue_description: Original issue description
            
        Returns:
            Resolution result with solution and instructions
        """
        start_time = time.time()
        
        self.log_action("Attempting automatic resolution", "processing")
        
        solution = classification.get('rag_solution')
        category = classification.get('category', 'Unknown')
        title = classification.get('title', category)
        
        if not solution:
            self.log_action("Resolution failed - no solution available", "failed")
            return {
                "success": False,
                "status": "failed",
                "error": "No solution available for this issue type",
                "processing_time_ms": (time.time() - start_time) * 1000
            }
        
        # Format resolution message
        resolution_message = f"""
✅ Automatic Resolution - {title}

{solution}

---
If this solution doesn't resolve your issue, please reply to this ticket or contact IT support directly.

Category: {category}
Confidence: {classification.get('confidence_score', 0):.1%}
        """.strip()
        
        resolution = {
            "success": True,
            "status": "resolved",
            "solution": solution,
            "instructions": resolution_message,
            "category": category,
            "title": title,
            "resolved_at": datetime.utcnow().isoformat(),
            "processing_time_ms": (time.time() - start_time) * 1000
        }
        
        self.log_action(f"Issue resolved automatically - {category}", "success")
        
        return resolution


class EscalationAgent(BaseAgent):
    """
    Escalation Agent - Handles escalation to human IT staff
    Packages all context for human review
    """
    
    def __init__(self):
        super().__init__("Escalation Agent")
    
    def escalate(
        self, 
        issue_description: str, 
        classification: Dict[str, Any], 
        ticket_id: str
    ) -> Dict[str, Any]:
        """
        Escalate issue to human IT support
        
        Args:
            issue_description: Original issue description
            classification: Classification result
            ticket_id: Ticket identifier
            
        Returns:
            Escalation result with assignment details
        """
        start_time = time.time()
        
        self.log_action(f"Escalating ticket {ticket_id}", "processing")
        
        priority = classification.get('priority', 'medium')
        category = classification.get('category', 'Unknown')
        
        # Determine response time based on priority
        response_times = {
            'critical': '15 minutes',
            'high': '2-4 hours',
            'medium': '24 hours',
            'low': '48 hours'
        }
        
        estimated_response = response_times.get(priority, '24 hours')
        
        # Create escalation message
        escalation_message = f"""
📨 Your request has been escalated to our IT support team.

Ticket ID: {ticket_id}
Category: {category}
Priority: {priority.upper()}

Your request requires attention from our IT specialists. A team member will contact you soon.

Expected Response Time: {estimated_response}

What happens next:
1. An IT support specialist will review your request
2. You'll receive an email when someone is assigned
3. The specialist may contact you for additional information
4. You'll be notified when the issue is resolved

You can check your ticket status anytime using Ticket ID: {ticket_id}

If this is urgent, please call IT Support at ext. 2222
        """.strip()
        
        escalation = {
            "success": True,
            "status": "escalated",
            "ticket_id": ticket_id,
            "assigned_to": "IT Support Team",
            "escalated_at": datetime.utcnow().isoformat(),
            "priority": priority,
            "category": category,
            "estimated_response_time": estimated_response,
            "message": escalation_message,
            "requires_human": True,
            "context": {
                "original_issue": issue_description,
                "classification": category,
                "confidence": classification.get('confidence_score', 0),
                "rag_insights": classification.get('description', '')
            },
            "processing_time_ms": (time.time() - start_time) * 1000
        }
        
        self.log_action(f"Ticket {ticket_id} escalated - Priority: {priority}", "success")
        
        return escalation


class LoggingAgent(BaseAgent):
    """
    Logging Agent - Maintains audit trail
    Logs all agent actions and ticket updates
    """
    
    def __init__(self, db_session):
        super().__init__("Logging Agent")
        self.db = db_session
    
    async def create_ticket(self, issue_description: str, user_id: int) -> str:
        """Create a new ticket"""
        from models import Ticket
        import random
        
        ticket_id = f"IT-{datetime.utcnow().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        
        ticket = Ticket(
            ticket_id=ticket_id,
            user_id=user_id,
            issue_description=issue_description,
            status="new",
            created_at=datetime.utcnow()
        )
        
        self.db.add(ticket)
        await self.db.commit()
        await self.db.refresh(ticket)
        
        self.log_action(f"Created ticket: {ticket_id}", "success")
        return ticket_id
    
    async def log_agent_action(
        self,
        ticket_id: int,
        agent_name: str,
        action: str,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        status: str,
        processing_time_ms: float,
        confidence_score: Optional[float] = None
    ):
        """Log agent action to database"""
        from models import AgentLog
        
        log_entry = AgentLog(
            ticket_id=ticket_id,
            agent_name=agent_name,
            action=action,
            input_data=json.dumps(input_data),
            output_data=json.dumps(output_data),
            status=status,
            processing_time_ms=processing_time_ms,
            confidence_score=confidence_score,
            created_at=datetime.utcnow()
        )
        
        self.db.add(log_entry)
        await self.db.commit()
        
        self.logger.debug(f"Logged action: {agent_name} - {action}")
    
    async def update_ticket(
        self,
        ticket_id: str,
        **updates
    ):
        """Update ticket with new information"""
        from models import Ticket
        from sqlalchemy import select
        
        result = await self.db.execute(
            select(Ticket).where(Ticket.ticket_id == ticket_id)
        )
        ticket = result.scalar_one_or_none()
        
        if ticket:
            for key, value in updates.items():
                if hasattr(ticket, key):
                    setattr(ticket, key, value)
            
            ticket.updated_at = datetime.utcnow()
            await self.db.commit()
            await self.db.refresh(ticket)
            
            self.log_action(f"Updated ticket {ticket_id}", "success")
            return ticket
        
        return None


def create_agents(db_session, rag_system: RAGSystem) -> Dict[str, BaseAgent]:
    """
    Factory function to create all agents
    
    Args:
        db_session: Database session
        rag_system: RAG system instance
        
    Returns:
        Dictionary of agent instances
    """
    return {
        "ui": UIAgent(),
        "classification": ClassificationAgent(rag_system),
        "decision": DecisionAgent(),
        "resolution": ResolutionAgent(),
        "escalation": EscalationAgent(),
        "logging": LoggingAgent(db_session)
    }
