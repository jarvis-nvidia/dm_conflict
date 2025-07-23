"""
DevMind RAG (Retrieval Augmented Generation) System
Combines vector search with LLM generation for contextual code understanding
"""

import asyncio
from typing import List, Dict, Optional, Any, Tuple
import json
import re

from .llm_client import llm_client, LLMResponse
from .vector_store import vector_store
from .embedding_service import embedding_service

class RAGSystem:
    """RAG system for contextual code analysis and generation"""
    
    def __init__(self):
        self.max_context_tokens = 3000
        self.similarity_threshold = 0.7
    
    async def query_codebase(
        self, 
        query: str,
        context_type: str = "general",
        max_results: int = 5,
        file_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        """Query codebase with RAG approach"""
        
        # Step 1: Retrieve relevant code chunks
        filter_dict = {"file_path": {"$regex": file_filter}} if file_filter else None
        
        relevant_chunks = await vector_store.similarity_search(
            query=query,
            top_k=max_results * 2,  # Get more for filtering
            filter_dict=filter_dict
        )
        
        # Step 2: Filter by similarity threshold
        high_quality_chunks = [
            chunk for chunk in relevant_chunks 
            if chunk["score"] >= self.similarity_threshold
        ][:max_results]
        
        # Step 3: Build context from retrieved chunks
        context = self._build_context(high_quality_chunks, context_type)
        
        # Step 4: Generate response using LLM
        system_prompt = self._get_system_prompt(context_type)
        
        llm_response = await llm_client.generate_response(
            prompt=f"Context:\n{context}\n\nQuery: {query}",
            system_prompt=system_prompt,
            max_tokens=1000,
            temperature=0.3
        )
        
        return {
            "response": llm_response.content,
            "relevant_chunks": high_quality_chunks,
            "context_used": context,
            "model_info": {
                "provider": llm_response.provider,
                "model": llm_response.model
            },
            "error": llm_response.error
        }
    
    async def debug_code(
        self, 
        code: str, 
        error_message: str,
        language: str,
        file_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Debug code using RAG approach"""
        
        # Create search query for similar issues
        debug_query = f"error debugging {language} {error_message} {code[:200]}"
        
        # Search for similar debugging scenarios
        similar_cases = await vector_store.similarity_search(
            query=debug_query,
            top_k=3,
            filter_dict={"language": language} if language else None
        )
        
        # Build debugging context
        context = self._build_debug_context(code, error_message, similar_cases)
        
        # Generate debugging suggestions
        system_prompt = """You are an expert code debugger. Analyze the provided code and error message.
        Use the similar cases from the codebase to provide specific, actionable debugging suggestions.
        Focus on:
        1. Identifying the root cause
        2. Providing step-by-step fix instructions
        3. Explaining why the error occurred
        4. Suggesting preventive measures"""
        
        llm_response = await llm_client.generate_response(
            prompt=context,
            system_prompt=system_prompt,
            max_tokens=1500,
            temperature=0.2
        )
        
        return {
            "debug_suggestions": llm_response.content,
            "similar_cases": similar_cases,
            "confidence_score": self._calculate_confidence(similar_cases),
            "model_info": {
                "provider": llm_response.provider,
                "model": llm_response.model
            }
        }
    
    async def review_code(
        self, 
        code: str,
        language: str,
        file_path: str,
        review_type: str = "comprehensive"
    ) -> Dict[str, Any]:
        """Review code using RAG approach"""
        
        # Search for similar code patterns and best practices
        review_query = f"code review best practices {language} {self._extract_code_features(code)}"
        
        similar_patterns = await vector_store.similarity_search(
            query=review_query,
            top_k=5,
            filter_dict={"language": language}
        )
        
        # Build review context
        context = self._build_review_context(code, language, similar_patterns, review_type)
        
        # Generate review
        system_prompt = self._get_review_system_prompt(review_type)
        
        llm_response = await llm_client.generate_response(
            prompt=context,
            system_prompt=system_prompt,
            max_tokens=2000,
            temperature=0.4
        )
        
        return {
            "review": llm_response.content,
            "similar_patterns": similar_patterns,
            "review_type": review_type,
            "recommendations": self._extract_recommendations(llm_response.content),
            "model_info": {
                "provider": llm_response.provider,
                "model": llm_response.model
            }
        }
    
    async def generate_commit_message(
        self, 
        changes: List[Dict[str, Any]],
        commit_style: str = "conventional"
    ) -> Dict[str, Any]:
        """Generate commit message using RAG approach"""
        
        # Analyze changes to understand the impact
        change_summary = self._analyze_changes(changes)
        
        # Search for similar commit patterns
        commit_query = f"commit message {change_summary['type']} {change_summary['scope']}"
        
        similar_commits = await vector_store.similarity_search(
            query=commit_query,
            top_k=3
        )
        
        # Build commit context
        context = self._build_commit_context(changes, change_summary, similar_commits, commit_style)
        
        # Generate commit message
        system_prompt = f"""You are an expert at writing {commit_style} commit messages.
        Generate a clear, descriptive commit message that follows {commit_style} conventions.
        Focus on what changed and why it matters."""
        
        llm_response = await llm_client.generate_response(
            prompt=context,
            system_prompt=system_prompt,
            max_tokens=500,
            temperature=0.3
        )
        
        return {
            "commit_message": llm_response.content.strip(),
            "change_summary": change_summary,
            "similar_commits": similar_commits,
            "commit_style": commit_style
        }
    
    def _build_context(self, chunks: List[Dict], context_type: str) -> str:
        """Build context string from retrieved chunks"""
        context_parts = []
        
        for i, chunk in enumerate(chunks):
            context_parts.append(f"## Code Context {i+1}")
            context_parts.append(f"File: {chunk['file_path']}")
            context_parts.append(f"Language: {chunk['language']}")
            context_parts.append(f"Relevance Score: {chunk['score']:.3f}")
            context_parts.append(f"Code:\n```{chunk['language']}\n{chunk['content']}\n```")
            context_parts.append("")
        
        return "\n".join(context_parts)
    
    def _build_debug_context(self, code: str, error: str, similar_cases: List[Dict]) -> str:
        """Build debugging context"""
        context = f"""DEBUG REQUEST:
        
Current Code:
```
{code}
```

Error Message:
{error}

Similar Cases from Codebase:
"""
        
        for case in similar_cases:
            context += f"""
File: {case['file_path']}
Similarity: {case['score']:.3f}
Code: {case['content'][:300]}...
---"""
        
        return context
    
    def _build_review_context(self, code: str, language: str, patterns: List[Dict], review_type: str) -> str:
        """Build code review context"""
        context = f"""CODE REVIEW REQUEST ({review_type}):

Code to Review ({language}):
```{language}
{code}
```

Similar Patterns Found:
"""
        
        for pattern in patterns:
            context += f"""
File: {pattern['file_path']}
Similarity: {pattern['score']:.3f}
Pattern: {pattern['content'][:200]}...
---"""
        
        return context
    
    def _build_commit_context(self, changes: List[Dict], summary: Dict, similar_commits: List[Dict], style: str) -> str:
        """Build commit message context"""
        context = f"""COMMIT MESSAGE GENERATION ({style} style):

Changes Summary:
- Type: {summary['type']}
- Scope: {summary['scope']}  
- Files Changed: {summary['files_count']}
- Lines Added: {summary.get('additions', 0)}
- Lines Removed: {summary.get('deletions', 0)}

Detailed Changes:
"""
        
        for change in changes[:5]:  # Limit to first 5 changes
            context += f"- {change.get('file', 'unknown')}: {change.get('description', 'modified')}\n"
        
        if similar_commits:
            context += "\nSimilar Commit Patterns:\n"
            for commit in similar_commits:
                context += f"- {commit['content'][:100]}...\n"
        
        return context
    
    def _get_system_prompt(self, context_type: str) -> str:
        """Get system prompt based on context type"""
        prompts = {
            "general": "You are DevMind, an intelligent code assistant. Provide helpful, accurate responses based on the codebase context.",
            "debugging": "You are a debugging expert. Analyze code issues and provide specific solutions.",
            "review": "You are a code review expert. Provide constructive feedback to improve code quality.",
            "documentation": "You are a documentation expert. Help explain and document code clearly."
        }
        return prompts.get(context_type, prompts["general"])
    
    def _get_review_system_prompt(self, review_type: str) -> str:
        """Get system prompt for code review"""
        prompts = {
            "comprehensive": """You are an expert code reviewer. Provide a comprehensive review covering:
                1. Code quality and maintainability
                2. Performance considerations  
                3. Security issues
                4. Best practices adherence
                5. Testing recommendations""",
            "security": "You are a security expert. Focus on identifying potential security vulnerabilities and risks.",
            "performance": "You are a performance expert. Focus on optimization opportunities and efficiency improvements.",
            "style": "You are a code style expert. Focus on code formatting, naming conventions, and consistency."
        }
        return prompts.get(review_type, prompts["comprehensive"])
    
    def _extract_code_features(self, code: str) -> str:
        """Extract key features from code for search"""
        features = []
        
        # Extract function names
        func_matches = re.findall(r'def\s+(\w+)', code)
        if func_matches:
            features.extend(func_matches[:3])
        
        # Extract class names
        class_matches = re.findall(r'class\s+(\w+)', code)
        if class_matches:
            features.extend(class_matches[:2])
        
        # Extract imports
        import_matches = re.findall(r'import\s+(\w+)', code)
        if import_matches:
            features.extend(import_matches[:3])
        
        return " ".join(features)
    
    def _analyze_changes(self, changes: List[Dict]) -> Dict[str, Any]:
        """Analyze changes to determine commit type and scope"""
        change_types = []
        scopes = set()
        files_count = len(changes)
        
        for change in changes:
            file_path = change.get('file', '')
            
            # Determine change type
            if 'test' in file_path.lower():
                change_types.append('test')
            elif 'doc' in file_path.lower() or 'readme' in file_path.lower():
                change_types.append('docs')
            elif change.get('status') == 'added':
                change_types.append('feat')
            elif change.get('status') == 'deleted':
                change_types.append('remove')
            else:
                change_types.append('fix')
            
            # Determine scope
            if '/' in file_path:
                scope = file_path.split('/')[0]
                scopes.add(scope)
        
        # Determine primary type
        primary_type = max(set(change_types), key=change_types.count) if change_types else 'feat'
        
        # Determine primary scope
        primary_scope = list(scopes)[0] if len(scopes) == 1 else 'multiple' if scopes else 'general'
        
        return {
            'type': primary_type,
            'scope': primary_scope,
            'files_count': files_count,
            'change_types': change_types
        }
    
    def _extract_recommendations(self, review_content: str) -> List[str]:
        """Extract actionable recommendations from review"""
        recommendations = []
        
        # Look for numbered lists or bullet points
        lines = review_content.split('\n')
        for line in lines:
            line = line.strip()
            if (line.startswith(('1.', '2.', '3.', '4.', '5.')) or 
                line.startswith(('- ', '* ')) or
                'recommend' in line.lower() or
                'should' in line.lower()):
                recommendations.append(line)
        
        return recommendations[:5]  # Limit to top 5
    
    def _calculate_confidence(self, chunks: List[Dict]) -> float:
        """Calculate confidence score based on retrieval results"""
        if not chunks:
            return 0.0
        
        avg_score = sum(chunk['score'] for chunk in chunks) / len(chunks)
        return min(avg_score * 100, 100)  # Convert to percentage

# Global RAG system instance
rag_system = RAGSystem()