"""
DevMind Backend Server
FastAPI server with AI-powered code analysis endpoints
"""

import os
import asyncio
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Import AI Engine components
from ai_engine import (
    llm_client, 
    vector_store, 
    embedding_service, 
    rag_system, 
    agent_framework
)
from ai_engine.code_processor import code_processor
from ai_engine.agent_framework import AgentTask, AgentMessage

app = FastAPI(
    title="DevMind AI Engine",
    description="AI-powered debugging and code review assistant",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class CodeAnalysisRequest(BaseModel):
    code: str
    language: str
    file_path: Optional[str] = None
    analysis_type: str = "general"

class DebugRequest(BaseModel):
    code: str
    error_message: str
    language: str
    file_path: Optional[str] = None

class ReviewRequest(BaseModel):
    code: str
    language: str
    file_path: str
    review_type: str = "comprehensive"

class CommitRequest(BaseModel):
    changes: List[Dict[str, Any]]
    commit_style: str = "conventional"

class RepositoryRequest(BaseModel):
    repo_path: str
    exclude_patterns: Optional[List[str]] = None

class QueryRequest(BaseModel):
    query: str
    context_type: str = "general"
    max_results: int = 5
    file_filter: Optional[str] = None

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize AI Engine on startup"""
    print("🚀 Starting DevMind AI Engine...")
    
    # Start agent framework
    await agent_framework.start()
    
    print("✅ DevMind AI Engine initialized successfully!")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    await agent_framework.stop()
    print("🛑 DevMind AI Engine shutdown complete")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ai_engine": "operational",
        "agents": agent_framework.get_agent_status()
    }

# AI Engine Endpoints
@app.post("/api/analyze-code")
async def analyze_code(request: CodeAnalysisRequest):
    """Analyze code using AI agents"""
    try:
        task = AgentTask(
            task_type="analyze",
            input_data={
                "code": request.code,
                "language": request.language,
                "file_path": request.file_path,
                "analysis_type": request.analysis_type
            }
        )
        
        task_id = await agent_framework.submit_task(task)
        
        # Wait for result (in production, this would be async)
        result = await agent_framework.get_task_result(task_id, timeout=30)
        
        if result and result.get("status") == "success":
            return {
                "success": True,
                "analysis": result["result"],
                "task_id": task_id
            }
        else:
            raise HTTPException(status_code=500, detail="Analysis failed")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/debug-code") 
async def debug_code(request: DebugRequest):
    """Debug code using AI agents"""
    try:
        task = AgentTask(
            task_type="debug",
            input_data={
                "code": request.code,
                "error_message": request.error_message,
                "language": request.language,
                "file_path": request.file_path
            }
        )
        
        task_id = await agent_framework.submit_task(task)
        result = await agent_framework.get_task_result(task_id, timeout=30)
        
        if result and result.get("status") == "success":
            return {
                "success": True,
                "debug_result": result["result"],
                "task_id": task_id
            }
        else:
            raise HTTPException(status_code=500, detail="Debugging failed")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/review-code")
async def review_code(request: ReviewRequest):
    """Review code using AI agents"""
    try:
        task = AgentTask(
            task_type="review",
            input_data={
                "code": request.code,
                "language": request.language,
                "file_path": request.file_path,
                "review_type": request.review_type
            }
        )
        
        task_id = await agent_framework.submit_task(task)
        result = await agent_framework.get_task_result(task_id, timeout=30)
        
        if result and result.get("status") == "success":
            return {
                "success": True,
                "review": result["result"],
                "task_id": task_id
            }
        else:
            raise HTTPException(status_code=500, detail="Review failed")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-commit")
async def generate_commit(request: CommitRequest):
    """Generate commit message using AI"""
    try:
        task = AgentTask(
            task_type="generate",
            input_data={
                "generation_type": "commit_message",
                "changes": request.changes,
                "commit_style": request.commit_style
            }
        )
        
        task_id = await agent_framework.submit_task(task)
        result = await agent_framework.get_task_result(task_id, timeout=30)
        
        if result and result.get("status") == "success":
            return {
                "success": True,
                "commit_message": result["result"],
                "task_id": task_id
            }
        else:
            raise HTTPException(status_code=500, detail="Commit generation failed")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/query-codebase")
async def query_codebase(request: QueryRequest):
    """Query codebase using RAG system"""
    try:
        result = await rag_system.query_codebase(
            query=request.query,
            context_type=request.context_type,
            max_results=request.max_results,
            file_filter=request.file_filter
        )
        
        return {
            "success": True,
            "response": result["response"],
            "relevant_chunks": result["relevant_chunks"],
            "model_info": result["model_info"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/process-repository")
async def process_repository(request: RepositoryRequest, background_tasks: BackgroundTasks):
    """Process repository and store in vector database"""
    try:
        # Process repository in background
        def process_repo():
            chunks = code_processor.process_repository(
                repo_path=request.repo_path,
                exclude_patterns=request.exclude_patterns
            )
            
            # Store in vector database
            asyncio.create_task(vector_store.upsert_code_chunks(chunks))
        
        background_tasks.add_task(process_repo)
        
        return {
            "success": True,
            "message": "Repository processing started",
            "repo_path": request.repo_path
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/agent-status")
async def get_agent_status():
    """Get status of all AI agents"""
    try:
        return {
            "success": True,
            "agents": agent_framework.get_agent_status(),
            "framework_running": agent_framework.is_running
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/learn-interaction")
async def learn_interaction(user_id: str, interaction_data: Dict[str, Any]):
    """Learn from user interaction"""
    try:
        task = AgentTask(
            task_type="learn",
            input_data={
                "user_id": user_id,
                **interaction_data
            }
        )
        
        task_id = await agent_framework.submit_task(task)
        result = await agent_framework.get_task_result(task_id, timeout=10)
        
        return {
            "success": True,
            "learning_result": result["result"] if result else None,
            "task_id": task_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Test endpoints for development
@app.post("/api/test-llm")
async def test_llm(prompt: str, provider: Optional[str] = None):
    """Test LLM connectivity"""
    try:
        response = await llm_client.generate_response(
            prompt=prompt,
            provider=provider,
            max_tokens=500
        )
        
        return {
            "success": True,
            "response": response.content,
            "provider": response.provider,
            "model": response.model,
            "error": response.error
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/test-embeddings")
async def test_embeddings(texts: List[str]):
    """Test embedding generation"""
    try:
        embeddings = await embedding_service.generate_embeddings(texts)
        
        return {
            "success": True,
            "embeddings_count": len(embeddings),
            "dimension": len(embeddings[0]) if embeddings else 0,
            "sample_embedding": embeddings[0][:5] if embeddings else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Development server
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8001)),
        reload=True
    )