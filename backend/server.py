"""
DevMind Backend Server
FastAPI server with advanced AI-powered code analysis endpoints
"""

import os
import asyncio
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Import AI Engine components
from ai_engine import (
    llm_client, 
    vector_store, 
    embedding_service, 
    rag_system
)
from ai_engine.code_processor import code_processor
from ai_engine.agent_framework import AgentTask, AgentMessage, agent_framework
from ai_engine.advanced_ast_parser import advanced_ast_parser
from ai_engine.code_smell_detector import code_smell_detector
from ai_engine.dependency_analyzer import dependency_analyzer
from ai_engine.learning_system import personalization_engine
from ai_engine.database import devmind_db

app = FastAPI(
    title="DevMind AI Engine",
    description="Advanced AI-powered debugging and code review assistant",
    version="2.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enhanced Request/Response Models
class AdvancedCodeAnalysisRequest(BaseModel):
    code: str
    language: str
    file_path: Optional[str] = None
    analysis_type: str = "comprehensive"
    user_id: Optional[str] = None
    include_smells: bool = True
    include_complexity: bool = True
    include_dependencies: bool = True

class CodeSmellAnalysisRequest(BaseModel):
    code: str
    file_path: str
    language: str
    user_id: Optional[str] = None
    custom_rules: Optional[Dict[str, Any]] = None

class ProjectAnalysisRequest(BaseModel):
    project_path: str
    user_id: Optional[str] = None
    exclude_patterns: Optional[List[str]] = None
    analysis_depth: str = "full"  # full, medium, quick

class LearningRequest(BaseModel):
    user_id: str
    learning_type: str  # "code_style", "commit_pattern", "debug_session"
    data: Dict[str, Any]

class PersonalizationRequest(BaseModel):
    user_id: str
    context: Dict[str, Any]

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize AI Engine on startup"""
    print("🚀 Starting DevMind AI Engine v2.0...")
    
    # Start agent framework
    await agent_framework.start()
    
    # Initialize database
    try:
        devmind_db._create_indexes()
    except Exception as e:
        print(f"⚠️ Database initialization warning: {e}")
    
    print("✅ DevMind AI Engine v2.0 initialized successfully!")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    await agent_framework.stop()
    print("🛑 DevMind AI Engine shutdown complete")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Enhanced health check endpoint"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "ai_engine": "operational",
        "agents": agent_framework.get_agent_status(),
        "database": "connected",
        "features": [
            "advanced_ast_parsing",
            "code_smell_detection", 
            "dependency_analysis",
            "personalized_learning",
            "multi_language_support"
        ]
    }

# ===== PHASE 2: ADVANCED ANALYSIS ENDPOINTS =====

@app.post("/api/v2/analyze-code-advanced")
async def analyze_code_advanced(request: AdvancedCodeAnalysisRequest):
    """Advanced code analysis with AST parsing, complexity metrics, and smells"""
    try:
        results = {
            "success": True,
            "file_path": request.file_path,
            "language": request.language,
            "analysis_timestamp": asyncio.get_event_loop().time()
        }
        
        # 1. Advanced AST Analysis
        if request.include_dependencies or request.analysis_type == "comprehensive":
            ast_analysis = advanced_ast_parser.parse_file(
                request.file_path or "temp_file.py", 
                request.code
            )
            results["ast_analysis"] = ast_analysis
        
        # 2. Code Smell Detection
        if request.include_smells:
            smells = code_smell_detector.detect_smells(
                request.code, 
                request.file_path or "temp_file",
                request.language,
                request.custom_rules if hasattr(request, 'custom_rules') else None
            )
            
            results["code_smells"] = [
                {
                    "type": smell.smell_type,
                    "severity": smell.severity,
                    "description": smell.description,
                    "line": smell.line_number,
                    "suggestion": smell.suggestion,
                    "rule_id": smell.rule_id,
                    "category": smell.category
                }
                for smell in smells
            ]
            
            results["smell_summary"] = code_smell_detector.get_smell_summary(smells)
            
            # Save smells to database
            if request.file_path and request.user_id:
                devmind_db.save_code_smells(
                    request.file_path, 
                    [smell.__dict__ for smell in smells],
                    request.user_id
                )
        
        # 3. Save analysis to database
        if request.user_id:
            analysis_id = devmind_db.save_code_analysis({
                "file_path": request.file_path,
                "language": request.language,
                "analysis_type": request.analysis_type,
                "metrics": results.get("ast_analysis", {}).get("metrics", {}),
                "user_id": request.user_id
            })
            results["analysis_id"] = analysis_id
            
            # Learn from user's code for personalization
            if request.code and request.language:
                personalization_engine.learn_from_code_sample(
                    request.user_id,
                    request.code,
                    request.file_path or "temp_file",
                    request.language
                )
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Advanced analysis failed: {str(e)}")

@app.post("/api/v2/analyze-project")
async def analyze_project(request: ProjectAnalysisRequest, background_tasks: BackgroundTasks):
    """Comprehensive project-wide analysis"""
    try:
        def run_project_analysis():
            """Background task for project analysis"""
            try:
                # 1. Dependency Analysis
                dep_analysis = dependency_analyzer.analyze_project(
                    request.project_path,
                    request.exclude_patterns
                )
                
                # 2. Save results to database
                if request.user_id:
                    analysis_id = devmind_db.save_dependency_analysis(
                        request.project_path,
                        dep_analysis,
                        request.user_id
                    )
                    print(f"✅ Project analysis saved with ID: {analysis_id}")
                
                return dep_analysis
                
            except Exception as e:
                print(f"❌ Project analysis error: {e}")
                return {"error": str(e)}
        
        # Start background analysis
        background_tasks.add_task(run_project_analysis)
        
        return {
            "success": True,
            "message": "Project analysis started",
            "project_path": request.project_path,
            "analysis_depth": request.analysis_depth,
            "estimated_completion": "2-5 minutes"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Project analysis failed: {str(e)}")

@app.get("/api/v2/project-analysis-status/{project_path:path}")
async def get_project_analysis_status(project_path: str):
    """Get status of project analysis"""
    try:
        analysis = devmind_db.get_latest_dependency_analysis(project_path)
        
        if analysis:
            return {
                "success": True,
                "status": "completed",
                "analysis_date": analysis["analysis_date"],
                "summary": analysis["analysis_data"].get("summary", {}),
                "analysis_id": str(analysis["_id"])
            }
        else:
            return {
                "success": True,
                "status": "not_found",
                "message": "No analysis found for this project"
            }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v2/project-insights/{project_path:path}")
async def get_project_insights(project_path: str):
    """Get comprehensive project insights"""
    try:
        insights = devmind_db.get_project_insights(project_path)
        
        return {
            "success": True,
            "project_path": project_path,
            "insights": insights
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== LEARNING AND PERSONALIZATION ENDPOINTS =====

@app.post("/api/v2/learn-user-pattern")
async def learn_user_pattern(request: LearningRequest):
    """Learn from user patterns for personalization"""
    try:
        if request.learning_type == "code_style":
            personalization_engine.learn_from_code_sample(
                request.user_id,
                request.data.get("code", ""),
                request.data.get("file_path", ""),
                request.data.get("language", "python")
            )
        
        elif request.learning_type == "commit_pattern":
            personalization_engine.learn_from_commits(
                request.user_id,
                request.data.get("commits", [])
            )
        
        elif request.learning_type == "debug_session":
            personalization_engine.learn_from_debug_session(
                request.user_id,
                request.data
            )
        
        return {
            "success": True,
            "learning_type": request.learning_type,
            "message": "Pattern learned successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Learning failed: {str(e)}")

@app.post("/api/v2/get-personalized-recommendations")
async def get_personalized_recommendations(request: PersonalizationRequest):
    """Get personalized recommendations based on user profile"""
    try:
        recommendations = personalization_engine.get_personalized_recommendations(
            request.user_id,
            request.context
        )
        
        return {
            "success": True,
            "user_id": request.user_id,
            "recommendations": recommendations,
            "personalized": len(recommendations.get("style_suggestions", [])) > 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Personalization failed: {str(e)}")

@app.get("/api/v2/user-learning-progress/{user_id}")
async def get_user_learning_progress(user_id: str):
    """Get user's learning progress and analytics"""
    try:
        progress = devmind_db.get_learning_progress(user_id)
        analytics = devmind_db.get_user_analytics(user_id)
        
        return {
            "success": True,
            "user_id": user_id,
            "progress": progress,
            "analytics": analytics
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== CODE SMELL MANAGEMENT ENDPOINTS =====

@app.post("/api/v2/detect-code-smells")
async def detect_code_smells(request: CodeSmellAnalysisRequest):
    """Detect code smells with customizable rules"""
    try:
        smells = code_smell_detector.detect_smells(
            request.code,
            request.file_path,
            request.language,
            request.custom_rules
        )
        
        # Save to database
        if request.user_id:
            devmind_db.save_code_smells(
                request.file_path,
                [smell.__dict__ for smell in smells],
                request.user_id
            )
        
        smell_summary = code_smell_detector.get_smell_summary(smells)
        
        return {
            "success": True,
            "file_path": request.file_path,
            "language": request.language,
            "smells": [
                {
                    "type": smell.smell_type,
                    "severity": smell.severity,
                    "description": smell.description,
                    "line": smell.line_number,
                    "suggestion": smell.suggestion,
                    "rule_id": smell.rule_id,
                    "category": smell.category,
                    "confidence": smell.confidence
                }
                for smell in smells
            ],
            "summary": smell_summary,
            "report": code_smell_detector.generate_report(smells, "json")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Smell detection failed: {str(e)}")

@app.get("/api/v2/code-smells")
async def get_code_smells(
    file_path: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    resolved: Optional[bool] = Query(None)
):
    """Get code smells with filtering options"""
    try:
        smells = devmind_db.get_code_smells(file_path, severity)
        
        # Filter by resolved status if specified
        if resolved is not None:
            smells = [s for s in smells if s.get("resolved", False) == resolved]
        
        return {
            "success": True,
            "smells": smells,
            "total": len(smells)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/v2/code-smells/{smell_id}/resolve")
async def resolve_code_smell(smell_id: str):
    """Mark a code smell as resolved"""
    try:
        success = devmind_db.mark_smell_resolved(smell_id)
        
        return {
            "success": success,
            "smell_id": smell_id,
            "message": "Code smell marked as resolved" if success else "Failed to resolve"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== USER MANAGEMENT ENDPOINTS =====

@app.post("/api/v2/users")
async def create_user(user_data: Dict[str, Any]):
    """Create a new user"""
    try:
        user_id = user_data.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")
        
        success = devmind_db.create_user(user_id, user_data)
        
        return {
            "success": success,
            "user_id": user_id,
            "message": "User created successfully" if success else "Failed to create user"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v2/users/{user_id}/interaction")
async def record_user_interaction(
    user_id: str,
    event_type: str,
    context: Dict[str, Any],
    outcome: Dict[str, Any],
    satisfaction_score: Optional[float] = None
):
    """Record user interaction for learning"""
    try:
        success = devmind_db.record_interaction(
            user_id, event_type, context, outcome, satisfaction_score
        )
        
        # Also record in personalization engine
        personalization_engine.record_interaction(
            user_id, event_type, context, outcome, satisfaction_score
        )
        
        return {
            "success": success,
            "message": "Interaction recorded successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== EXISTING ENDPOINTS (Enhanced) =====

@app.post("/api/debug-code")
async def debug_code(request):
    """Enhanced debug code with personalization"""
    try:
        # Get personalized debugging hints if user_id provided
        personalized_hints = []
        if hasattr(request, 'user_id') and request.user_id:
            recommendations = personalization_engine.get_personalized_recommendations(
                request.user_id,
                {
                    "error_message": request.error_message,
                    "language": request.language,
                    "code": request.code[:200]  # First 200 chars for context
                }
            )
            personalized_hints = recommendations.get("debugging_hints", [])
        
        # Original debug logic
        task = agent_framework.AgentTask(
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
            debug_result = result["result"]
            debug_result["personalized_hints"] = personalized_hints
            
            return {
                "success": True,
                "debug_result": debug_result,
                "task_id": task_id
            }
        else:
            raise HTTPException(status_code=500, detail="Debugging failed")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== UTILITY ENDPOINTS =====

@app.get("/api/v2/supported-languages")
async def get_supported_languages():
    """Get list of supported programming languages"""
    return {
        "success": True,
        "languages": [
            {
                "name": "Python",
                "code": "python",
                "extensions": [".py"],
                "features": ["ast_parsing", "code_smells", "complexity_analysis"]
            },
            {
                "name": "JavaScript",
                "code": "javascript", 
                "extensions": [".js", ".jsx"],
                "features": ["ast_parsing", "code_smells", "dependency_analysis"]
            },
            {
                "name": "TypeScript",
                "code": "typescript",
                "extensions": [".ts", ".tsx"],
                "features": ["ast_parsing", "code_smells", "dependency_analysis"]
            },
            {
                "name": "Java",
                "code": "java",
                "extensions": [".java"],
                "features": ["basic_parsing", "code_smells"]
            }
        ]
    }

@app.get("/api/v2/analysis-history/{file_path:path}")
async def get_analysis_history(file_path: str, limit: int = Query(10)):
    """Get analysis history for a file"""
    try:
        history = devmind_db.get_code_analysis_history(file_path, limit)
        
        return {
            "success": True,
            "file_path": file_path,
            "history": history,
            "total": len(history)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v2/cleanup-data")
async def cleanup_old_data(days_to_keep: int = Query(90)):
    """Clean up old data to maintain performance"""
    try:
        devmind_db.cleanup_old_data(days_to_keep)
        
        return {
            "success": True,
            "message": f"Cleaned up data older than {days_to_keep} days"
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