"""
DevMind Agent Framework
Multi-agent system for specialized code analysis tasks using Google's approach
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import uuid
from datetime import datetime

from .rag_system import rag_system
from .llm_client import llm_client

class AgentRole(Enum):
    """Predefined agent roles"""
    DEBUGGER = "debugger"
    REVIEWER = "reviewer" 
    GENERATOR = "generator"
    ANALYZER = "analyzer"
    LEARNER = "learner"
    COORDINATOR = "coordinator"

@dataclass
class AgentMessage:
    """Message structure for inter-agent communication"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender: str = ""
    receiver: str = ""
    content: str = ""
    message_type: str = "info"  # info, request, response, error
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class AgentTask:
    """Task structure for agent processing"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    task_type: str = ""
    input_data: Dict[str, Any] = field(default_factory=dict)
    priority: int = 1  # 1 = high, 5 = low
    assigned_agent: Optional[str] = None
    status: str = "pending"  # pending, processing, completed, failed
    result: Optional[Dict[str, Any]] = None
    created_at: datetime = field(default_factory=datetime.now)

class BaseAgent:
    """Base class for all DevMind agents"""
    
    def __init__(self, name: str, role: AgentRole, capabilities: List[str]):
        self.name = name
        self.role = role
        self.capabilities = capabilities
        self.memory = []  # Agent memory for learning
        self.message_queue = asyncio.Queue()
        self.is_active = False
        
    async def process_task(self, task: AgentTask) -> Dict[str, Any]:
        """Process a task assigned to this agent"""
        raise NotImplementedError("Subclasses must implement process_task")
    
    async def send_message(self, message: AgentMessage, agent_framework: 'AgentFramework'):
        """Send message to another agent"""
        await agent_framework.route_message(message)
    
    async def receive_message(self, message: AgentMessage):
        """Receive and queue message"""
        await self.message_queue.put(message)
    
    def add_to_memory(self, experience: Dict[str, Any]):
        """Add experience to agent memory"""
        self.memory.append({
            **experience,
            "timestamp": datetime.now(),
            "agent": self.name
        })
        
        # Keep memory size manageable
        if len(self.memory) > 100:
            self.memory = self.memory[-50:]  # Keep last 50 entries

class DebuggerAgent(BaseAgent):
    """Specialized agent for code debugging"""
    
    def __init__(self):
        super().__init__(
            name="debugger_agent",
            role=AgentRole.DEBUGGER,
            capabilities=["debug_code", "analyze_errors", "suggest_fixes"]
        )
    
    async def process_task(self, task: AgentTask) -> Dict[str, Any]:
        """Process debugging task"""
        try:
            task_data = task.input_data
            
            result = await rag_system.debug_code(
                code=task_data.get("code", ""),
                error_message=task_data.get("error_message", ""),
                language=task_data.get("language", ""),
                file_path=task_data.get("file_path")
            )
            
            # Add to memory for learning
            self.add_to_memory({
                "task_type": "debug",
                "error_pattern": task_data.get("error_message", "")[:100],
                "solution_found": bool(result.get("debug_suggestions")),
                "confidence": result.get("confidence_score", 0)
            })
            
            return {
                "status": "success",
                "result": result,
                "agent": self.name
            }
            
        except Exception as e:
            return {
                "status": "error", 
                "error": str(e),
                "agent": self.name
            }

class ReviewerAgent(BaseAgent):
    """Specialized agent for code review"""
    
    def __init__(self):
        super().__init__(
            name="reviewer_agent",
            role=AgentRole.REVIEWER,
            capabilities=["review_code", "check_quality", "suggest_improvements"]
        )
    
    async def process_task(self, task: AgentTask) -> Dict[str, Any]:
        """Process code review task"""
        try:
            task_data = task.input_data
            
            result = await rag_system.review_code(
                code=task_data.get("code", ""),
                language=task_data.get("language", ""),
                file_path=task_data.get("file_path", ""),
                review_type=task_data.get("review_type", "comprehensive")
            )
            
            # Add to memory
            self.add_to_memory({
                "task_type": "review",
                "language": task_data.get("language", ""),
                "review_type": task_data.get("review_type", ""),
                "recommendations_count": len(result.get("recommendations", []))
            })
            
            return {
                "status": "success",
                "result": result,
                "agent": self.name
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "agent": self.name
            }

class GeneratorAgent(BaseAgent):
    """Specialized agent for code generation"""
    
    def __init__(self):
        super().__init__(
            name="generator_agent",
            role=AgentRole.GENERATOR,
            capabilities=["generate_commit_messages", "generate_documentation", "generate_tests"]
        )
    
    async def process_task(self, task: AgentTask) -> Dict[str, Any]:
        """Process generation task"""
        try:
            task_data = task.input_data
            task_type = task_data.get("generation_type", "commit_message")
            
            if task_type == "commit_message":
                result = await rag_system.generate_commit_message(
                    changes=task_data.get("changes", []),
                    commit_style=task_data.get("commit_style", "conventional")
                )
            else:
                # Handle other generation types
                result = await self._generate_content(task_data, task_type)
            
            # Add to memory
            self.add_to_memory({
                "task_type": "generate",
                "generation_type": task_type,
                "input_size": len(str(task_data)),
                "success": True
            })
            
            return {
                "status": "success",
                "result": result,
                "agent": self.name
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "agent": self.name
            }
    
    async def _generate_content(self, task_data: Dict, content_type: str) -> Dict[str, Any]:
        """Generate content based on type"""
        prompt = f"Generate {content_type} for: {json.dumps(task_data, indent=2)}"
        
        response = await llm_client.generate_response(
            prompt=prompt,
            system_prompt=f"You are an expert at generating {content_type}. Be concise and helpful.",
            max_tokens=1000
        )
        
        return {
            "generated_content": response.content,
            "content_type": content_type,
            "model_info": {
                "provider": response.provider,
                "model": response.model
            }
        }

class AnalyzerAgent(BaseAgent):
    """Specialized agent for code analysis"""
    
    def __init__(self):
        super().__init__(
            name="analyzer_agent",
            role=AgentRole.ANALYZER,
            capabilities=["analyze_complexity", "analyze_dependencies", "analyze_patterns"]
        )
    
    async def process_task(self, task: AgentTask) -> Dict[str, Any]:
        """Process analysis task"""
        try:
            task_data = task.input_data
            
            # Use RAG system for contextual analysis
            result = await rag_system.query_codebase(
                query=f"analyze {task_data.get('analysis_type', 'general')} {task_data.get('code', '')[:200]}",
                context_type="general",
                file_filter=task_data.get("file_filter")
            )
            
            # Add to memory
            self.add_to_memory({
                "task_type": "analyze",
                "analysis_type": task_data.get("analysis_type", "general"),
                "codebase_context_used": len(result.get("relevant_chunks", []))
            })
            
            return {
                "status": "success",
                "result": result,
                "agent": self.name
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "agent": self.name
            }

class LearnerAgent(BaseAgent):
    """Specialized agent for learning user patterns"""
    
    def __init__(self):
        super().__init__(
            name="learner_agent",
            role=AgentRole.LEARNER,
            capabilities=["learn_patterns", "adapt_responses", "personalize"]
        )
        self.user_patterns = {}
    
    async def process_task(self, task: AgentTask) -> Dict[str, Any]:
        """Process learning task"""
        try:
            task_data = task.input_data
            user_id = task_data.get("user_id", "default")
            
            # Learn from user interactions
            interaction = {
                "action": task_data.get("action"),
                "context": task_data.get("context"),
                "outcome": task_data.get("outcome"),
                "timestamp": datetime.now()
            }
            
            if user_id not in self.user_patterns:
                self.user_patterns[user_id] = []
            
            self.user_patterns[user_id].append(interaction)
            
            # Analyze patterns
            patterns = self._analyze_user_patterns(user_id)
            
            return {
                "status": "success",
                "result": {
                    "patterns_learned": patterns,
                    "interaction_count": len(self.user_patterns[user_id])
                },
                "agent": self.name
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "agent": self.name
            }
    
    def _analyze_user_patterns(self, user_id: str) -> Dict[str, Any]:
        """Analyze user patterns to personalize experience"""
        interactions = self.user_patterns.get(user_id, [])
        
        if not interactions:
            return {}
        
        # Analyze common actions
        actions = [i.get("action") for i in interactions if i.get("action")]
        action_counts = {action: actions.count(action) for action in set(actions)}
        
        # Analyze preferred contexts
        contexts = [i.get("context") for i in interactions if i.get("context")]
        
        return {
            "preferred_actions": action_counts,
            "total_interactions": len(interactions),
            "most_common_action": max(action_counts, key=action_counts.get) if action_counts else None,
            "active_contexts": len(set(contexts))
        }

class AgentFramework:
    """Main agent coordination framework"""
    
    def __init__(self):
        self.agents = {}
        self.task_queue = asyncio.Queue()
        self.message_router = {}
        self.is_running = False
        
        # Initialize agents
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all agent instances"""
        agents = [
            DebuggerAgent(),
            ReviewerAgent(), 
            GeneratorAgent(),
            AnalyzerAgent(),
            LearnerAgent()
        ]
        
        for agent in agents:
            self.agents[agent.name] = agent
            print(f"✅ Agent initialized: {agent.name} ({agent.role.value})")
    
    async def start(self):
        """Start the agent framework"""
        self.is_running = True
        print("🚀 DevMind Agent Framework started")
        
        # Start task processing
        asyncio.create_task(self._process_tasks())
    
    async def stop(self):
        """Stop the agent framework"""
        self.is_running = False
        print("🛑 DevMind Agent Framework stopped")
    
    async def submit_task(self, task: AgentTask) -> str:
        """Submit task to appropriate agent"""
        # Auto-assign agent based on task type
        if not task.assigned_agent:
            task.assigned_agent = self._assign_agent(task)
        
        await self.task_queue.put(task)
        print(f"📋 Task {task.id} submitted to {task.assigned_agent}")
        return task.id
    
    async def get_task_result(self, task_id: str, timeout: int = 30) -> Optional[Dict[str, Any]]:
        """Get result for a completed task"""
        # In a real implementation, this would check a results store
        # For now, we'll implement a simple polling mechanism
        for _ in range(timeout):
            await asyncio.sleep(1)
            # Check if task is completed (simplified)
        
        return None
    
    async def route_message(self, message: AgentMessage):
        """Route message between agents"""
        if message.receiver in self.agents:
            await self.agents[message.receiver].receive_message(message)
        else:
            print(f"❌ Unknown agent: {message.receiver}")
    
    async def _process_tasks(self):
        """Main task processing loop"""
        while self.is_running:
            try:
                # Get task from queue with timeout
                task = await asyncio.wait_for(self.task_queue.get(), timeout=1.0)
                
                # Process task
                if task.assigned_agent in self.agents:
                    agent = self.agents[task.assigned_agent]
                    result = await agent.process_task(task)
                    task.result = result
                    task.status = "completed"
                    print(f"✅ Task {task.id} completed by {task.assigned_agent}")
                else:
                    print(f"❌ Unknown agent for task {task.id}: {task.assigned_agent}")
                    task.status = "failed"
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"❌ Task processing error: {e}")
    
    def _assign_agent(self, task: AgentTask) -> str:
        """Assign appropriate agent based on task type"""
        task_type = task.task_type.lower()
        
        assignment_rules = {
            "debug": "debugger_agent",
            "review": "reviewer_agent", 
            "generate": "generator_agent",
            "analyze": "analyzer_agent",
            "learn": "learner_agent"
        }
        
        for keyword, agent_name in assignment_rules.items():
            if keyword in task_type:
                return agent_name
        
        # Default to analyzer for unknown tasks
        return "analyzer_agent"
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        status = {}
        for name, agent in self.agents.items():
            status[name] = {
                "role": agent.role.value,
                "capabilities": agent.capabilities,
                "memory_size": len(agent.memory),
                "is_active": agent.is_active
            }
        return status

# Global agent framework instance  
agent_framework = AgentFramework()