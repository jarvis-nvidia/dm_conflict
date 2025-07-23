"""
DevMind Database Models and Schema
MongoDB models for storing user learning data and analysis results
"""

from pymongo import MongoClient
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import os
import json
from bson import ObjectId

# MongoDB connection
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/devmind')

class DevMindDatabase:
    """Main database interface for DevMind"""
    
    def __init__(self):
        self.client = MongoClient(MONGO_URL)
        self.db = self.client.devmind
        
        # Collections
        self.users = self.db.users
        self.coding_styles = self.db.coding_styles
        self.commit_patterns = self.db.commit_patterns
        self.bug_patterns = self.db.bug_patterns
        self.code_analysis = self.db.code_analysis
        self.dependency_analysis = self.db.dependency_analysis
        self.interaction_events = self.db.interaction_events
        self.project_metadata = self.db.project_metadata
        self.code_smells = self.db.code_smells
        self.learning_sessions = self.db.learning_sessions
        
        # Create indexes for performance
        self._create_indexes()
    
    def _create_indexes(self):
        """Create database indexes for optimal performance"""
        
        # User-related indexes
        self.users.create_index("user_id", unique=True)
        self.coding_styles.create_index([("user_id", 1), ("language", 1)])
        self.commit_patterns.create_index("user_id")
        self.bug_patterns.create_index("user_id")
        
        # Analysis-related indexes
        self.code_analysis.create_index([("file_path", 1), ("analysis_date", -1)])
        self.dependency_analysis.create_index([("project_path", 1), ("analysis_date", -1)])
        self.code_smells.create_index([("file_path", 1), ("severity", 1)])
        
        # Interaction tracking indexes
        self.interaction_events.create_index([("user_id", 1), ("timestamp", -1)])
        self.interaction_events.create_index([("event_type", 1), ("timestamp", -1)])
        
        # Learning session indexes
        self.learning_sessions.create_index([("user_id", 1), ("session_date", -1)])
        
        print("✅ Database indexes created")
    
    # User Management
    def create_user(self, user_id: str, user_data: Dict[str, Any]) -> bool:
        """Create a new user"""
        try:
            user_doc = {
                "user_id": user_id,
                "created_at": datetime.now(),
                "last_active": datetime.now(),
                "preferences": user_data.get("preferences", {}),
                "subscription_type": user_data.get("subscription_type", "free"),
                "total_analyses": 0,
                "total_reviews": 0,
                "total_debug_sessions": 0
            }
            
            result = self.users.insert_one(user_doc)
            return bool(result.inserted_id)
        except Exception as e:
            print(f"❌ Error creating user: {e}")
            return False
    
    def update_user_activity(self, user_id: str):
        """Update user's last active timestamp"""
        self.users.update_one(
            {"user_id": user_id},
            {"$set": {"last_active": datetime.now()}}
        )
    
    # Coding Style Management
    def save_coding_style(self, user_id: str, language: str, style_data: Dict[str, Any]) -> bool:
        """Save or update user's coding style profile"""
        try:
            style_doc = {
                "user_id": user_id,
                "language": language,
                "style_data": style_data,
                "confidence_scores": style_data.get("confidence_scores", {}),
                "samples_analyzed": style_data.get("samples_analyzed", 0),
                "last_updated": datetime.now(),
                "created_at": datetime.now()
            }
            
            result = self.coding_styles.replace_one(
                {"user_id": user_id, "language": language},
                style_doc,
                upsert=True
            )
            return bool(result.upserted_id or result.modified_count)
        except Exception as e:
            print(f"❌ Error saving coding style: {e}")
            return False
    
    def get_coding_style(self, user_id: str, language: str) -> Optional[Dict[str, Any]]:
        """Get user's coding style profile"""
        return self.coding_styles.find_one({"user_id": user_id, "language": language})
    
    # Commit Pattern Management
    def save_commit_pattern(self, user_id: str, pattern_data: Dict[str, Any]) -> bool:
        """Save user's commit patterns"""
        try:
            pattern_doc = {
                "user_id": user_id,
                "pattern_data": pattern_data,
                "total_commits_analyzed": pattern_data.get("total_commits_analyzed", 0),
                "last_updated": datetime.now(),
                "created_at": datetime.now()
            }
            
            result = self.commit_patterns.replace_one(
                {"user_id": user_id},
                pattern_doc,
                upsert=True
            )
            return bool(result.upserted_id or result.modified_count)
        except Exception as e:
            print(f"❌ Error saving commit pattern: {e}")
            return False
    
    def get_commit_pattern(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user's commit patterns"""
        return self.commit_patterns.find_one({"user_id": user_id})
    
    # Bug Pattern Management
    def save_bug_pattern(self, user_id: str, bug_data: Dict[str, Any]) -> bool:
        """Save user's bug patterns"""
        try:
            bug_doc = {
                "user_id": user_id,
                "bug_data": bug_data,
                "bugs_analyzed": bug_data.get("bugs_analyzed", 0),
                "last_updated": datetime.now(),
                "created_at": datetime.now()
            }
            
            result = self.bug_patterns.replace_one(
                {"user_id": user_id},
                bug_doc,
                upsert=True
            )
            return bool(result.upserted_id or result.modified_count)
        except Exception as e:
            print(f"❌ Error saving bug pattern: {e}")
            return False
    
    def get_bug_pattern(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user's bug patterns"""
        return self.bug_patterns.find_one({"user_id": user_id})
    
    # Code Analysis Management
    def save_code_analysis(self, analysis_data: Dict[str, Any]) -> Optional[str]:
        """Save code analysis results"""
        try:
            analysis_doc = {
                "file_path": analysis_data.get("file_path"),
                "language": analysis_data.get("language"),
                "analysis_type": analysis_data.get("analysis_type", "comprehensive"),
                "metrics": analysis_data.get("metrics", {}),
                "ast_nodes": analysis_data.get("ast_nodes", []),
                "dependencies": analysis_data.get("dependencies", {}),
                "complexity_scores": analysis_data.get("complexity_scores", {}),
                "analysis_date": datetime.now(),
                "user_id": analysis_data.get("user_id"),
                "project_id": analysis_data.get("project_id")
            }
            
            result = self.code_analysis.insert_one(analysis_doc)
            return str(result.inserted_id)
        except Exception as e:
            print(f"❌ Error saving code analysis: {e}")
            return None
    
    def get_code_analysis_history(self, file_path: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get analysis history for a file"""
        return list(self.code_analysis.find(
            {"file_path": file_path}
        ).sort("analysis_date", -1).limit(limit))
    
    # Code Smells Management
    def save_code_smells(self, file_path: str, smells: List[Dict[str, Any]], user_id: str = None) -> bool:
        """Save detected code smells"""
        try:
            # Remove existing smells for this file
            self.code_smells.delete_many({"file_path": file_path})
            
            # Insert new smells
            if smells:
                smell_docs = []
                for smell in smells:
                    smell_doc = {
                        "file_path": file_path,
                        "smell_type": smell.get("smell_type"),
                        "severity": smell.get("severity"),
                        "description": smell.get("description"),
                        "line_number": smell.get("line_number"),
                        "suggestion": smell.get("suggestion"),
                        "rule_id": smell.get("rule_id"),
                        "category": smell.get("category"),
                        "confidence": smell.get("confidence", 1.0),
                        "detected_at": datetime.now(),
                        "user_id": user_id,
                        "resolved": False
                    }
                    smell_docs.append(smell_doc)
                
                result = self.code_smells.insert_many(smell_docs)
                return len(result.inserted_ids) == len(smells)
            
            return True
        except Exception as e:
            print(f"❌ Error saving code smells: {e}")
            return False
    
    def get_code_smells(self, file_path: str = None, severity: str = None) -> List[Dict[str, Any]]:
        """Get code smells with optional filtering"""
        query = {}
        if file_path:
            query["file_path"] = file_path
        if severity:
            query["severity"] = severity
        
        return list(self.code_smells.find(query).sort("severity", 1))
    
    def mark_smell_resolved(self, smell_id: str) -> bool:
        """Mark a code smell as resolved"""
        try:
            result = self.code_smells.update_one(
                {"_id": ObjectId(smell_id)},
                {"$set": {"resolved": True, "resolved_at": datetime.now()}}
            )
            return bool(result.modified_count)
        except Exception as e:
            print(f"❌ Error marking smell as resolved: {e}")
            return False
    
    # Dependency Analysis Management
    def save_dependency_analysis(self, project_path: str, analysis_data: Dict[str, Any], user_id: str = None) -> Optional[str]:
        """Save dependency analysis results"""
        try:
            dep_doc = {
                "project_path": project_path,
                "analysis_data": analysis_data,
                "summary": analysis_data.get("summary", {}),
                "circular_dependencies": analysis_data.get("circular_dependencies", []),
                "unused_imports": analysis_data.get("unused_imports", []),
                "coupling_metrics": analysis_data.get("coupling_metrics", {}),
                "hotspots": analysis_data.get("hotspots", []),
                "analysis_date": datetime.now(),
                "user_id": user_id
            }
            
            result = self.dependency_analysis.insert_one(dep_doc)
            return str(result.inserted_id)
        except Exception as e:
            print(f"❌ Error saving dependency analysis: {e}")
            return None
    
    def get_latest_dependency_analysis(self, project_path: str) -> Optional[Dict[str, Any]]:
        """Get latest dependency analysis for a project"""
        return self.dependency_analysis.find_one(
            {"project_path": project_path},
            sort=[("analysis_date", -1)]
        )
    
    # Interaction Tracking
    def record_interaction(self, user_id: str, event_type: str, context: Dict[str, Any], 
                          outcome: Dict[str, Any], satisfaction_score: float = None) -> bool:
        """Record user interaction"""
        try:
            interaction_doc = {
                "user_id": user_id,
                "event_type": event_type,
                "context": context,
                "outcome": outcome,
                "satisfaction_score": satisfaction_score,
                "timestamp": datetime.now(),
                "session_id": context.get("session_id"),
                "duration_ms": context.get("duration_ms"),
                "success": outcome.get("success", True)
            }
            
            result = self.interaction_events.insert_one(interaction_doc)
            
            # Update user activity
            self.update_user_activity(user_id)
            
            return bool(result.inserted_id)
        except Exception as e:
            print(f"❌ Error recording interaction: {e}")
            return False
    
    def get_user_interactions(self, user_id: str, event_type: str = None, days: int = 30) -> List[Dict[str, Any]]:
        """Get user interactions within specified days"""
        query = {
            "user_id": user_id,
            "timestamp": {"$gte": datetime.now() - datetime.timedelta(days=days)}
        }
        
        if event_type:
            query["event_type"] = event_type
        
        return list(self.interaction_events.find(query).sort("timestamp", -1))
    
    # Learning Sessions
    def create_learning_session(self, user_id: str, session_data: Dict[str, Any]) -> Optional[str]:
        """Create a new learning session"""
        try:
            session_doc = {
                "user_id": user_id,
                "session_type": session_data.get("session_type", "general"),
                "language": session_data.get("language"),
                "files_analyzed": session_data.get("files_analyzed", []),
                "insights_learned": session_data.get("insights_learned", []),
                "style_improvements": session_data.get("style_improvements", []),
                "patterns_identified": session_data.get("patterns_identified", []),
                "session_date": datetime.now(),
                "duration_minutes": session_data.get("duration_minutes", 0),
                "quality_score": session_data.get("quality_score", 0.0)
            }
            
            result = self.learning_sessions.insert_one(session_doc)
            return str(result.inserted_id)
        except Exception as e:
            print(f"❌ Error creating learning session: {e}")
            return None
    
    def get_learning_progress(self, user_id: str) -> Dict[str, Any]:
        """Get user's learning progress summary"""
        try:
            # Get overall stats
            total_sessions = self.learning_sessions.count_documents({"user_id": user_id})
            
            # Get recent sessions
            recent_sessions = list(self.learning_sessions.find(
                {"user_id": user_id}
            ).sort("session_date", -1).limit(10))
            
            # Calculate averages
            avg_quality = 0.0
            total_duration = 0
            
            if recent_sessions:
                avg_quality = sum(s.get("quality_score", 0) for s in recent_sessions) / len(recent_sessions)
                total_duration = sum(s.get("duration_minutes", 0) for s in recent_sessions)
            
            # Get language breakdown
            language_pipeline = [
                {"$match": {"user_id": user_id}},
                {"$group": {"_id": "$language", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ]
            
            languages = list(self.learning_sessions.aggregate(language_pipeline))
            
            return {
                "total_sessions": total_sessions,
                "recent_sessions": recent_sessions,
                "average_quality_score": round(avg_quality, 2),
                "total_learning_time": total_duration,
                "languages_practiced": languages,
                "learning_streak": self._calculate_learning_streak(user_id)
            }
        except Exception as e:
            print(f"❌ Error getting learning progress: {e}")
            return {}
    
    def _calculate_learning_streak(self, user_id: str) -> int:
        """Calculate user's learning streak (consecutive days)"""
        try:
            # Get sessions from last 30 days, grouped by date
            pipeline = [
                {
                    "$match": {
                        "user_id": user_id,
                        "session_date": {"$gte": datetime.now() - datetime.timedelta(days=30)}
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "$dateToString": {
                                "format": "%Y-%m-%d",
                                "date": "$session_date"
                            }
                        }
                    }
                },
                {"$sort": {"_id": -1}}
            ]
            
            session_dates = [doc["_id"] for doc in self.learning_sessions.aggregate(pipeline)]
            
            if not session_dates:
                return 0
            
            streak = 0
            current_date = datetime.now().date()
            
            for date_str in session_dates:
                session_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                
                if (current_date - session_date).days == streak:
                    streak += 1
                    current_date = session_date
                else:
                    break
            
            return streak
        except Exception as e:
            print(f"❌ Error calculating learning streak: {e}")
            return 0
    
    # Analytics and Reporting
    def get_user_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive user analytics"""
        try:
            analytics = {
                "coding_style_evolution": self._get_style_evolution(user_id),
                "bug_pattern_trends": self._get_bug_trends(user_id),
                "commit_pattern_analysis": self._get_commit_trends(user_id),
                "interaction_heatmap": self._get_interaction_heatmap(user_id),
                "quality_improvement": self._get_quality_trends(user_id)
            }
            
            return analytics
        except Exception as e:
            print(f"❌ Error getting user analytics: {e}")
            return {}
    
    def _get_style_evolution(self, user_id: str) -> List[Dict[str, Any]]:
        """Track how user's coding style has evolved"""
        styles = list(self.coding_styles.find({"user_id": user_id}).sort("created_at", 1))
        
        evolution = []
        for style in styles:
            evolution.append({
                "date": style.get("last_updated"),
                "language": style.get("language"),
                "confidence": style.get("style_data", {}).get("confidence_scores", {}),
                "samples_analyzed": style.get("samples_analyzed", 0)
            })
        
        return evolution
    
    def _get_bug_trends(self, user_id: str) -> Dict[str, Any]:
        """Analyze user's bug resolution trends"""
        interactions = self.get_user_interactions(user_id, "debug_request", days=90)
        
        if not interactions:
            return {}
        
        # Group by week
        weekly_bugs = {}
        weekly_resolutions = {}
        
        for interaction in interactions:
            week = interaction["timestamp"].strftime("%Y-W%U")
            weekly_bugs[week] = weekly_bugs.get(week, 0) + 1
            
            if interaction.get("success", False):
                weekly_resolutions[week] = weekly_resolutions.get(week, 0) + 1
        
        return {
            "weekly_bug_count": weekly_bugs,
            "weekly_resolution_rate": {
                week: weekly_resolutions.get(week, 0) / count
                for week, count in weekly_bugs.items()
            },
            "improvement_trend": len(weekly_bugs) > 4  # Simplified trend detection
        }
    
    def _get_commit_trends(self, user_id: str) -> Dict[str, Any]:
        """Analyze commit pattern trends"""
        pattern = self.get_commit_pattern(user_id)
        
        if not pattern:
            return {}
        
        return {
            "message_quality_trend": "improving",  # Simplified
            "consistency_score": 0.8,  # Placeholder
            "preferred_commit_times": pattern.get("pattern_data", {}).get("preferred_commit_times", [])
        }
    
    def _get_interaction_heatmap(self, user_id: str) -> Dict[str, Any]:
        """Generate interaction heatmap data"""
        interactions = self.get_user_interactions(user_id, days=30)
        
        # Group by hour and day of week
        heatmap = {}
        
        for interaction in interactions:
            hour = interaction["timestamp"].hour
            day = interaction["timestamp"].weekday()
            
            key = f"{day}-{hour}"
            heatmap[key] = heatmap.get(key, 0) + 1
        
        return heatmap
    
    def _get_quality_trends(self, user_id: str) -> Dict[str, Any]:
        """Track code quality improvement trends"""
        sessions = list(self.learning_sessions.find(
            {"user_id": user_id}
        ).sort("session_date", 1).limit(30))
        
        if len(sessions) < 2:
            return {}
        
        quality_scores = [s.get("quality_score", 0) for s in sessions]
        
        # Simple trend calculation
        recent_avg = sum(quality_scores[-5:]) / min(5, len(quality_scores))
        older_avg = sum(quality_scores[:5]) / min(5, len(quality_scores))
        
        return {
            "trend": "improving" if recent_avg > older_avg else "stable",
            "current_score": quality_scores[-1] if quality_scores else 0,
            "improvement_rate": (recent_avg - older_avg) if older_avg > 0 else 0,
            "quality_history": quality_scores
        }
    
    def get_project_insights(self, project_path: str) -> Dict[str, Any]:
        """Get comprehensive project insights"""
        try:
            # Get latest dependency analysis
            dep_analysis = self.get_latest_dependency_analysis(project_path)
            
            # Get code smells summary
            smells = self.code_smells.aggregate([
                {"$match": {"file_path": {"$regex": f"^{project_path}"}}},
                {"$group": {
                    "_id": "$severity",
                    "count": {"$sum": 1}
                }}
            ])
            
            smells_summary = {doc["_id"]: doc["count"] for doc in smells}
            
            # Get analysis history
            analyses = list(self.code_analysis.find(
                {"file_path": {"$regex": f"^{project_path}"}}
            ).sort("analysis_date", -1).limit(10))
            
            return {
                "dependency_health": dep_analysis.get("summary", {}) if dep_analysis else {},
                "code_quality_summary": smells_summary,
                "recent_analyses": analyses,
                "total_files_analyzed": len(set(a["file_path"] for a in analyses)),
                "last_analysis_date": analyses[0]["analysis_date"] if analyses else None
            }
        except Exception as e:
            print(f"❌ Error getting project insights: {e}")
            return {}
    
    def cleanup_old_data(self, days_to_keep: int = 90):
        """Clean up old data to maintain performance"""
        try:
            cutoff_date = datetime.now() - datetime.timedelta(days=days_to_keep)
            
            # Clean old interaction events
            result1 = self.interaction_events.delete_many({"timestamp": {"$lt": cutoff_date}})
            
            # Clean old code analyses
            result2 = self.code_analysis.delete_many({"analysis_date": {"$lt": cutoff_date}})
            
            print(f"🧹 Cleaned up {result1.deleted_count} interactions and {result2.deleted_count} analyses")
            
        except Exception as e:
            print(f"❌ Error during cleanup: {e}")

# Global database instance
devmind_db = DevMindDatabase()