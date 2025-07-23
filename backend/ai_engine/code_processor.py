"""
DevMind Code Processor
Handles code parsing, chunking, and preparation for vector storage
"""

import os
import ast
import re
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import hashlib

class CodeProcessor:
    """Process code files for AI analysis"""
    
    def __init__(self):
        self.supported_extensions = {
            '.py': 'python',
            '.js': 'javascript', 
            '.ts': 'typescript',
            '.jsx': 'jsx',
            '.tsx': 'tsx',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.cs': 'csharp',
            '.php': 'php',
            '.rb': 'ruby',
            '.go': 'go',
            '.rs': 'rust',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.html': 'html',
            '.css': 'css',
            '.sql': 'sql',
            '.sh': 'bash',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.json': 'json',
            '.xml': 'xml'
        }
    
    def process_repository(self, repo_path: str, exclude_patterns: List[str] = None) -> List[Dict[str, Any]]:
        """Process entire repository into code chunks"""
        if exclude_patterns is None:
            exclude_patterns = [
                'node_modules', '__pycache__', '.git', '.env', 
                'dist', 'build', 'coverage', '.vscode', '.idea'
            ]
        
        code_chunks = []
        repo_path = Path(repo_path)
        
        for file_path in repo_path.rglob('*'):
            if file_path.is_file() and self._should_process_file(file_path, exclude_patterns):
                try:
                    chunks = self.process_file(str(file_path))
                    code_chunks.extend(chunks)
                except Exception as e:
                    print(f"❌ Error processing {file_path}: {e}")
        
        print(f"✅ Processed {len(code_chunks)} code chunks from repository")
        return code_chunks
    
    def process_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Process single file into code chunks"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ Cannot read file {file_path}: {e}")
            return []
        
        if not content.strip():
            return []
        
        language = self._detect_language(file_path)
        chunks = self._chunk_code(content, language, file_path)
        
        return chunks
    
    def _should_process_file(self, file_path: Path, exclude_patterns: List[str]) -> bool:
        """Check if file should be processed"""
        # Check exclude patterns
        for pattern in exclude_patterns:
            if pattern in str(file_path):
                return False
        
        # Check file extension
        return file_path.suffix.lower() in self.supported_extensions
    
    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension"""
        extension = Path(file_path).suffix.lower()
        return self.supported_extensions.get(extension, 'text')
    
    def _chunk_code(self, content: str, language: str, file_path: str) -> List[Dict[str, Any]]:
        """Chunk code based on language-specific logic"""
        chunks = []
        
        if language == 'python':
            chunks = self._chunk_python_code(content, file_path)
        elif language in ['javascript', 'typescript', 'jsx', 'tsx']:
            chunks = self._chunk_js_code(content, file_path, language)
        else:
            chunks = self._chunk_generic_code(content, file_path, language)
        
        return chunks
    
    def _chunk_python_code(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Chunk Python code by functions and classes"""
        chunks = []
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    start_line = node.lineno
                    end_line = getattr(node, 'end_lineno', start_line)
                    
                    code_lines = content.split('\n')
                    chunk_content = '\n'.join(code_lines[start_line-1:end_line])
                    
                    chunk_type = 'class' if isinstance(node, ast.ClassDef) else 'function'
                    
                    chunks.append({
                        'content': chunk_content,
                        'language': 'python',
                        'file_path': file_path,
                        'chunk_type': chunk_type,
                        'name': node.name,
                        'start_line': start_line,
                        'end_line': end_line,
                        'embedding_text': f"Python {chunk_type} {node.name} in {file_path}:\n{chunk_content}"
                    })
            
            # If no functions/classes found, chunk by lines
            if not chunks:
                chunks = self._chunk_by_lines(content, file_path, 'python')
                
        except SyntaxError:
            # If parsing fails, fall back to line-based chunking
            chunks = self._chunk_by_lines(content, file_path, 'python')
        
        return chunks
    
    def _chunk_js_code(self, content: str, file_path: str, language: str) -> List[Dict[str, Any]]:
        """Chunk JavaScript/TypeScript code"""
        chunks = []
        
        # Simple regex-based chunking for JS/TS functions and classes
        patterns = [
            (r'function\s+(\w+)\s*\([^)]*\)\s*{', 'function'),
            (r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*{', 'arrow_function'),
            (r'class\s+(\w+)(?:\s+extends\s+\w+)?\s*{', 'class'),
            (r'export\s+(?:default\s+)?(?:function\s+(\w+)|class\s+(\w+))', 'export')
        ]
        
        lines = content.split('\n')
        
        for pattern, chunk_type in patterns:
            for match in re.finditer(pattern, content, re.MULTILINE):
                start_pos = match.start()
                name = match.group(1) or match.group(2) or 'anonymous'
                
                # Find the start line
                start_line = content[:start_pos].count('\n') + 1
                
                # Simple brace matching to find end
                end_line = self._find_js_block_end(lines, start_line - 1)
                
                chunk_content = '\n'.join(lines[start_line-1:end_line])
                
                chunks.append({
                    'content': chunk_content,
                    'language': language,
                    'file_path': file_path,
                    'chunk_type': chunk_type,
                    'name': name,
                    'start_line': start_line,
                    'end_line': end_line,
                    'embedding_text': f"{language} {chunk_type} {name} in {file_path}:\n{chunk_content}"
                })
        
        # If no functions/classes found, chunk by lines
        if not chunks:
            chunks = self._chunk_by_lines(content, file_path, language)
        
        return chunks
    
    def _find_js_block_end(self, lines: List[str], start_line: int) -> int:
        """Find the end of a JavaScript block using brace matching"""
        brace_count = 0
        in_block = False
        
        for i in range(start_line, len(lines)):
            line = lines[i]
            
            for char in line:
                if char == '{':
                    brace_count += 1
                    in_block = True
                elif char == '}':
                    brace_count -= 1
                    
                    if in_block and brace_count == 0:
                        return i + 1
        
        return min(start_line + 50, len(lines))  # Fallback
    
    def _chunk_generic_code(self, content: str, file_path: str, language: str) -> List[Dict[str, Any]]:
        """Generic code chunking for unsupported languages"""  
        return self._chunk_by_lines(content, file_path, language)
    
    def _chunk_by_lines(self, content: str, file_path: str, language: str, lines_per_chunk: int = 50) -> List[Dict[str, Any]]:
        """Chunk code by number of lines"""
        chunks = []
        lines = content.split('\n')
        
        for i in range(0, len(lines), lines_per_chunk):
            chunk_lines = lines[i:i + lines_per_chunk]
            chunk_content = '\n'.join(chunk_lines)
            
            if chunk_content.strip():
                chunks.append({
                    'content': chunk_content,
                    'language': language,
                    'file_path': file_path,
                    'chunk_type': 'block',
                    'name': f'block_{i//lines_per_chunk + 1}',
                    'start_line': i + 1,
                    'end_line': min(i + lines_per_chunk, len(lines)),
                    'embedding_text': f"{language} code block in {file_path}:\n{chunk_content}"
                })
        
        return chunks
    
    def get_file_hash(self, file_path: str) -> str:
        """Get hash of file content for change detection"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            return hashlib.md5(content).hexdigest()
        except Exception:
            return ""
    
    def extract_dependencies(self, content: str, language: str) -> List[str]:
        """Extract dependencies/imports from code"""
        dependencies = []
        
        if language == 'python':
            # Python imports
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith(('import ', 'from ')):
                    dependencies.append(line)
        
        elif language in ['javascript', 'typescript']:
            # JS/TS imports
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith(('import ', 'require(')):
                    dependencies.append(line)
        
        return dependencies
    
    def analyze_complexity(self, content: str, language: str) -> Dict[str, Any]:
        """Basic complexity analysis"""
        lines = content.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        complexity_indicators = {
            'total_lines': len(lines),
            'code_lines': len(non_empty_lines),
            'cyclomatic_complexity': self._calculate_cyclomatic_complexity(content, language),
            'nesting_depth': self._calculate_nesting_depth(content),
            'function_count': len(re.findall(r'def\s+\w+|function\s+\w+', content))
        }
        
        return complexity_indicators
    
    def _calculate_cyclomatic_complexity(self, content: str, language: str) -> int:
        """Simple cyclomatic complexity calculation"""
        # Count decision points
        decision_keywords = ['if', 'while', 'for', 'case', 'catch', '&&', '||']
        complexity = 1  # Base complexity
        
        for keyword in decision_keywords:
            complexity += len(re.findall(rf'\b{keyword}\b', content))
        
        return complexity
    
    def _calculate_nesting_depth(self, content: str) -> int:
        """Calculate maximum nesting depth"""
        max_depth = 0
        current_depth = 0
        
        for char in content:
            if char in '{([':
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif char in '})]':
                current_depth = max(0, current_depth - 1)
        
        return max_depth

# Global code processor instance
code_processor = CodeProcessor()