"""
DevMind Advanced AST Parser
Multi-language Abstract Syntax Tree parser with deep code analysis
"""

import ast
import os
import re
import json
from typing import Dict, List, Any, Optional, Set, Tuple, Union
from dataclasses import dataclass, field
from pathlib import Path
import hashlib
from collections import defaultdict, deque
import esprima  # For JavaScript parsing
import javalang  # For Java parsing

@dataclass
class ASTNode:
    """Standardized AST node representation"""
    node_type: str
    name: str
    start_line: int
    end_line: int
    children: List['ASTNode'] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    complexity: int = 0
    dependencies: List[str] = field(default_factory=list)

@dataclass
class CodeMetrics:
    """Comprehensive code metrics"""
    cyclomatic_complexity: int = 0
    cognitive_complexity: int = 0
    maintainability_index: float = 0.0
    lines_of_code: int = 0
    comment_ratio: float = 0.0
    function_count: int = 0
    class_count: int = 0
    max_nesting_depth: int = 0
    duplicate_code_ratio: float = 0.0
    test_coverage: float = 0.0

@dataclass
class DependencyInfo:
    """Cross-file dependency information"""
    imports: List[str] = field(default_factory=list)
    exports: List[str] = field(default_factory=list)
    function_calls: List[str] = field(default_factory=list)
    class_usage: List[str] = field(default_factory=list)
    file_dependencies: Set[str] = field(default_factory=set)

class AdvancedASTParser:
    """Advanced multi-language AST parser with deep analysis"""
    
    def __init__(self):
        self.language_parsers = {
            'python': self._parse_python,
            'javascript': self._parse_javascript,
            'typescript': self._parse_typescript,
            'java': self._parse_java
        }
        
        # Language-specific complexity rules
        self.complexity_rules = {
            'python': {
                'decision_points': ['if', 'elif', 'while', 'for', 'except', 'with', 'and', 'or'],
                'cognitive_incrementors': ['if', 'elif', 'else', 'while', 'for', 'except', 'finally', 'with'],
                'nesting_incrementors': ['def', 'class', 'if', 'while', 'for', 'try', 'with']
            },
            'javascript': {
                'decision_points': ['if', 'else', 'while', 'for', 'switch', 'case', 'catch', '&&', '||', '?:'],
                'cognitive_incrementors': ['if', 'else', 'while', 'for', 'switch', 'case', 'catch', 'finally'],
                'nesting_incrementors': ['function', 'if', 'while', 'for', 'try', 'switch', 'class']
            }
        }
        
        # Cache for parsed files
        self.parse_cache = {}
        self.dependency_graph = defaultdict(set)
    
    def parse_file(self, file_path: str, content: Optional[str] = None) -> Dict[str, Any]:
        """Parse a single file and return comprehensive analysis"""
        
        # Check cache first
        file_hash = self._get_file_hash(file_path, content)
        if file_hash in self.parse_cache:
            return self.parse_cache[file_hash]
        
        if content is None:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except Exception as e:
                return {"error": f"Cannot read file: {e}"}
        
        language = self._detect_language(file_path)
        
        # Parse based on language
        if language in self.language_parsers:
            result = self.language_parsers[language](content, file_path)
        else:
            result = self._parse_generic(content, file_path, language)
        
        # Add comprehensive metrics
        result['metrics'] = self._calculate_metrics(content, result.get('ast_nodes', []), language)
        result['dependencies'] = self._extract_dependencies(content, language, file_path)
        result['file_hash'] = file_hash
        result['language'] = language
        
        # Cache result
        self.parse_cache[file_hash] = result
        
        return result
    
    def _parse_python(self, content: str, file_path: str) -> Dict[str, Any]:
        """Parse Python code using AST"""
        try:
            tree = ast.parse(content)
            ast_nodes = []
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    ast_node = ASTNode(
                        node_type=type(node).__name__,
                        name=node.name,
                        start_line=getattr(node, 'lineno', 0),
                        end_line=getattr(node, 'end_lineno', 0),
                        complexity=self._calculate_node_complexity(node, 'python'),
                        metadata={
                            'decorators': [d.id if isinstance(d, ast.Name) else str(d) for d in getattr(node, 'decorator_list', [])],
                            'args': [arg.arg for arg in getattr(node, 'args', ast.arguments()).args] if hasattr(node, 'args') else [],
                            'docstring': ast.get_docstring(node),
                            'is_async': isinstance(node, ast.AsyncFunctionDef),
                            'is_private': node.name.startswith('_'),
                            'return_type': self._extract_return_type(node)
                        }
                    )
                    ast_nodes.append(ast_node)
            
            return {
                'ast_nodes': ast_nodes,
                'imports': self._extract_python_imports(tree),
                'globals': self._extract_python_globals(tree),
                'classes': [n for n in ast_nodes if n.node_type == 'ClassDef'],
                'functions': [n for n in ast_nodes if n.node_type in ['FunctionDef', 'AsyncFunctionDef']],
                'syntax_errors': []
            }
            
        except SyntaxError as e:
            return {
                'ast_nodes': [],
                'syntax_errors': [{'line': e.lineno, 'message': str(e), 'type': 'SyntaxError'}],
                'error': str(e)
            }
    
    def _calculate_node_complexity(self, node: ast.AST, language: str) -> int:
        """Calculate complexity for a specific AST node"""
        complexity = 1  # Base complexity
        
        if language == 'python':
            # Add complexity for control flow statements
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.Try):
                complexity += len(getattr(node, 'handlers', []))
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Add complexity for nested conditions and loops
                for child in ast.walk(node):
                    if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                        complexity += 1
                    elif isinstance(child, (ast.And, ast.Or)):
                        complexity += 1
        
        return complexity
    
    def _extract_return_type(self, node: ast.AST) -> Optional[str]:
        """Extract return type annotation from function node"""
        if hasattr(node, 'returns') and node.returns:
            if isinstance(node.returns, ast.Name):
                return node.returns.id
            elif isinstance(node.returns, ast.Constant):
                return str(node.returns.value)
            elif hasattr(node.returns, 'id'):
                return node.returns.id
            else:
                return str(node.returns)
        return None
    
    def _parse_javascript(self, content: str, file_path: str) -> Dict[str, Any]:
        """Parse JavaScript/TypeScript code"""
        try:
            # Use esprima for JavaScript parsing
            tree = esprima.parseScript(content, {'loc': True, 'range': True})
            ast_nodes = []
            
            def extract_nodes(node, parent_name=""):
                if node.type == 'FunctionDeclaration':
                    ast_node = ASTNode(
                        node_type='Function',
                        name=node.id.name if node.id else 'anonymous',
                        start_line=node.loc.start.line,
                        end_line=node.loc.end.line,
                        complexity=self._calculate_js_complexity(node),
                        metadata={
                            'params': [p.name for p in node.params if hasattr(p, 'name')],
                            'is_async': getattr(node, 'async', False),
                            'is_generator': getattr(node, 'generator', False),
                            'parent': parent_name
                        }
                    )
                    ast_nodes.append(ast_node)
                
                elif node.type == 'ClassDeclaration':
                    ast_node = ASTNode(
                        node_type='Class',
                        name=node.id.name if node.id else 'anonymous',
                        start_line=node.loc.start.line,
                        end_line=node.loc.end.line,
                        metadata={
                            'superclass': node.superClass.name if node.superClass and hasattr(node.superClass, 'name') else None,
                            'methods': []
                        }
                    )
                    ast_nodes.append(ast_node)
                
                # Recursively process child nodes
                for key, value in node.__dict__.items():
                    if isinstance(value, list):
                        for item in value:
                            if hasattr(item, 'type'):
                                extract_nodes(item, parent_name)
                    elif hasattr(value, 'type'):
                        extract_nodes(value, parent_name)
            
            extract_nodes(tree)
            
            return {
                'ast_nodes': ast_nodes,
                'imports': self._extract_js_imports(content),
                'exports': self._extract_js_exports(content),
                'functions': [n for n in ast_nodes if n.node_type == 'Function'],
                'classes': [n for n in ast_nodes if n.node_type == 'Class'],
                'syntax_errors': []
            }
            
        except Exception as e:
            return {
                'ast_nodes': [],
                'syntax_errors': [{'message': str(e), 'type': 'ParseError'}],
                'error': str(e)
            }
    
    def _parse_typescript(self, content: str, file_path: str) -> Dict[str, Any]:
        """Parse TypeScript code (similar to JavaScript with type info)"""
        # For now, treat TypeScript like JavaScript
        # In production, you'd use a TypeScript-specific parser
        result = self._parse_javascript(content, file_path)
        result['types'] = self._extract_typescript_types(content)
        return result
    
    def _parse_java(self, content: str, file_path: str) -> Dict[str, Any]:
        """Parse Java code"""
        try:
            tree = javalang.parse.parse(content)
            ast_nodes = []
            
            # Extract classes
            for _, class_decl in tree.filter(javalang.tree.ClassDeclaration):
                ast_node = ASTNode(
                    node_type='Class',
                    name=class_decl.name,
                    start_line=getattr(class_decl, 'position', {}).get('line', 0),
                    end_line=0,  # Java parser doesn't provide end lines easily
                    metadata={
                        'modifiers': class_decl.modifiers if hasattr(class_decl, 'modifiers') else [],
                        'extends': class_decl.extends.name if class_decl.extends else None,
                        'implements': [impl.name for impl in class_decl.implements] if class_decl.implements else []
                    }
                )
                ast_nodes.append(ast_node)
            
            # Extract methods
            for _, method_decl in tree.filter(javalang.tree.MethodDeclaration):
                ast_node = ASTNode(
                    node_type='Method',
                    name=method_decl.name,
                    start_line=getattr(method_decl, 'position', {}).get('line', 0),
                    end_line=0,
                    metadata={
                        'modifiers': method_decl.modifiers if hasattr(method_decl, 'modifiers') else [],
                        'return_type': method_decl.return_type.name if method_decl.return_type else 'void',
                        'parameters': [p.name for p in method_decl.parameters] if method_decl.parameters else []
                    }
                )
                ast_nodes.append(ast_node)
            
            return {
                'ast_nodes': ast_nodes,
                'imports': self._extract_java_imports(tree),
                'package': getattr(tree, 'package', {}).name if hasattr(tree, 'package') and tree.package else None,
                'classes': [n for n in ast_nodes if n.node_type == 'Class'],
                'methods': [n for n in ast_nodes if n.node_type == 'Method'],
                'syntax_errors': []
            }
            
        except Exception as e:
            return {
                'ast_nodes': [],
                'syntax_errors': [{'message': str(e), 'type': 'ParseError'}],
                'error': str(e)
            }
    
    def _parse_generic(self, content: str, file_path: str, language: str) -> Dict[str, Any]:
        """Generic parsing for unsupported languages"""
        lines = content.split('\n')
        ast_nodes = []
        
        # Simple regex-based parsing for functions and classes
        function_patterns = {
            'go': r'func\s+(\w+)\s*\(',
            'rust': r'fn\s+(\w+)\s*\(',
            'cpp': r'(?:[\w:]+\s+)?(\w+)\s*\([^)]*\)\s*{',
            'csharp': r'(?:public|private|protected|internal)?\s*(?:static)?\s*(?:[\w<>]+\s+)?(\w+)\s*\([^)]*\)\s*{'
        }
        
        class_patterns = {
            'go': r'type\s+(\w+)\s+struct',
            'rust': r'struct\s+(\w+)',
            'cpp': r'class\s+(\w+)',
            'csharp': r'(?:public|private|protected|internal)?\s*class\s+(\w+)'
        }
        
        # Extract functions
        if language in function_patterns:
            for i, line in enumerate(lines):
                match = re.search(function_patterns[language], line)
                if match:
                    ast_nodes.append(ASTNode(
                        node_type='Function',
                        name=match.group(1),
                        start_line=i + 1,
                        end_line=i + 1,  # Simplified
                        metadata={'language': language}
                    ))
        
        # Extract classes
        if language in class_patterns:
            for i, line in enumerate(lines):
                match = re.search(class_patterns[language], line)
                if match:
                    ast_nodes.append(ASTNode(
                        node_type='Class',
                        name=match.group(1),
                        start_line=i + 1,
                        end_line=i + 1,  # Simplified
                        metadata={'language': language}
                    ))
        
        return {
            'ast_nodes': ast_nodes,
            'functions': [n for n in ast_nodes if n.node_type == 'Function'],
            'classes': [n for n in ast_nodes if n.node_type == 'Class'],
            'syntax_errors': [],
            'note': 'Generic parsing - limited functionality'
        }
    
    def _calculate_metrics(self, content: str, ast_nodes: List[ASTNode], language: str) -> CodeMetrics:
        """Calculate comprehensive code metrics"""
        lines = content.split('\n')
        code_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
        comment_lines = [line for line in lines if line.strip().startswith('#')]
        
        metrics = CodeMetrics(
            lines_of_code=len(code_lines),
            comment_ratio=len(comment_lines) / len(lines) if lines else 0,
            function_count=len([n for n in ast_nodes if 'Function' in n.node_type or 'Method' in n.node_type]),
            class_count=len([n for n in ast_nodes if n.node_type == 'Class']),
            cyclomatic_complexity=self._calculate_cyclomatic_complexity(content, language),
            cognitive_complexity=self._calculate_cognitive_complexity(content, language),
            max_nesting_depth=self._calculate_nesting_depth(content)
        )
        
        # Calculate maintainability index
        metrics.maintainability_index = self._calculate_maintainability_index(metrics, content)
        
        return metrics
    
    def _calculate_cyclomatic_complexity(self, content: str, language: str) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1  # Base complexity
        
        if language in self.complexity_rules:
            decision_points = self.complexity_rules[language]['decision_points']
            
            for keyword in decision_points:
                if keyword in ['&&', '||', '?:']:
                    complexity += content.count(keyword)
                else:
                    # Use word boundaries for keywords
                    pattern = rf'\b{re.escape(keyword)}\b'
                    complexity += len(re.findall(pattern, content))
        
        return complexity
    
    def _calculate_cognitive_complexity(self, content: str, language: str) -> int:
        """Calculate cognitive complexity (more sophisticated than cyclomatic)"""
        complexity = 0
        nesting_level = 0
        
        lines = content.split('\n')
        
        if language in self.complexity_rules:
            incrementors = self.complexity_rules[language]['cognitive_incrementors']
            nesting_incrementors = self.complexity_rules[language]['nesting_incrementors']
            
            for line in lines:
                line = line.strip()
                
                # Track nesting level
                for keyword in nesting_incrementors:
                    if re.search(rf'\b{re.escape(keyword)}\b', line):
                        if keyword in ['def', 'function', 'class']:
                            nesting_level = 1  # Reset for new function/class
                        else:
                            nesting_level += 1
                
                # Add complexity based on nesting
                for keyword in incrementors:
                    if re.search(rf'\b{re.escape(keyword)}\b', line):
                        complexity += nesting_level
        
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
    
    def _calculate_maintainability_index(self, metrics: CodeMetrics, content: str) -> float:
        """Calculate maintainability index (0-100 scale)"""
        # Simplified maintainability index calculation
        # Based on Halstead volume, cyclomatic complexity, and lines of code
        
        halstead_volume = len(set(content.split())) * 4.7  # Simplified
        
        try:
            mi = 171 - 5.2 * (halstead_volume ** 0.23) - 0.23 * metrics.cyclomatic_complexity - 16.2 * (metrics.lines_of_code ** 0.5)
            return max(0, min(100, mi))
        except:
            return 50.0  # Default moderate maintainability
    
    def _extract_dependencies(self, content: str, language: str, file_path: str) -> DependencyInfo:
        """Extract comprehensive dependency information"""
        deps = DependencyInfo()
        
        if language == 'python':
            deps.imports = self._extract_python_imports_from_content(content)
        elif language in ['javascript', 'typescript']:
            deps.imports = self._extract_js_imports(content)
            deps.exports = self._extract_js_exports(content)
        
        # Add to dependency graph
        self.dependency_graph[file_path].update(deps.imports)
        
        return deps
    
    def _extract_python_imports_from_content(self, content: str) -> List[str]:
        """Extract Python imports from content"""
        imports = []
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('import ') or line.startswith('from '):
                imports.append(line)
        return imports
    
    def _extract_js_imports(self, content: str) -> List[str]:
        """Extract JavaScript/TypeScript imports"""
        imports = []
        import_pattern = r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]'
        require_pattern = r'require\([\'"]([^\'"]+)[\'"]\)'
        
        imports.extend(re.findall(import_pattern, content))
        imports.extend(re.findall(require_pattern, content))
        
        return imports
    
    def _extract_js_exports(self, content: str) -> List[str]:
        """Extract JavaScript/TypeScript exports"""
        exports = []
        export_patterns = [
            r'export\s+(?:default\s+)?(?:function|class|const|let|var)\s+(\w+)',
            r'export\s*{\s*([^}]+)\s*}',
            r'module\.exports\s*=\s*(\w+)'
        ]
        
        for pattern in export_patterns:
            matches = re.findall(pattern, content)
            exports.extend(matches)
        
        return exports
    
    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension"""
        extension_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'javascript',
            '.tsx': 'typescript',
            '.java': 'java',
            '.go': 'go',
            '.rs': 'rust',
            '.cpp': 'cpp',
            '.cc': 'cpp',
            '.cxx': 'cpp',
            '.cs': 'csharp',
            '.php': 'php',
            '.rb': 'ruby',
            '.swift': 'swift',
            '.kt': 'kotlin'
        }
        
        ext = Path(file_path).suffix.lower()
        return extension_map.get(ext, 'unknown')
    
    def _get_file_hash(self, file_path: str, content: Optional[str] = None) -> str:
        """Get hash for caching"""
        if content:
            return hashlib.md5(content.encode()).hexdigest()
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return hashlib.md5(file_path.encode()).hexdigest()
    
    def get_dependency_graph(self) -> Dict[str, Set[str]]:
        """Get the complete dependency graph"""
        return dict(self.dependency_graph)
    
    def analyze_cross_file_dependencies(self, project_path: str) -> Dict[str, Any]:
        """Analyze cross-file dependencies for entire project"""
        dependency_analysis = {
            'circular_dependencies': [],
            'unused_imports': [],
            'missing_dependencies': [],
            'dependency_tree': {},
            'coupling_metrics': {}
        }
        
        # Build complete dependency graph
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if any(file.endswith(ext) for ext in ['.py', '.js', '.ts', '.java']):
                    file_path = os.path.join(root, file)
                    self.parse_file(file_path)
        
        # Detect circular dependencies
        dependency_analysis['circular_dependencies'] = self._detect_circular_dependencies()
        
        # Calculate coupling metrics
        dependency_analysis['coupling_metrics'] = self._calculate_coupling_metrics()
        
        return dependency_analysis
    
    def _detect_circular_dependencies(self) -> List[List[str]]:
        """Detect circular dependencies using DFS"""
        visited = set()
        rec_stack = set()
        cycles = []
        
        def dfs(node, path):
            if node in rec_stack:
                # Found cycle
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:] + [node])
                return
            
            if node in visited:
                return
            
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in self.dependency_graph.get(node, []):
                dfs(neighbor, path + [node])
            
            rec_stack.remove(node)
        
        for node in self.dependency_graph:
            if node not in visited:
                dfs(node, [])
        
        return cycles
    
    def _calculate_coupling_metrics(self) -> Dict[str, float]:
        """Calculate coupling metrics for the project"""
        total_files = len(self.dependency_graph)
        if total_files == 0:
            return {}
        
        # Afferent coupling (Ca) - number of classes that depend on this class
        # Efferent coupling (Ce) - number of classes this class depends on
        coupling_metrics = {}
        
        for file_path in self.dependency_graph:
            efferent = len(self.dependency_graph[file_path])
            afferent = sum(1 for deps in self.dependency_graph.values() if file_path in deps)
            
            # Instability (I) = Ce / (Ca + Ce)
            instability = efferent / (afferent + efferent) if (afferent + efferent) > 0 else 0
            
            coupling_metrics[file_path] = {
                'afferent_coupling': afferent,
                'efferent_coupling': efferent,
                'instability': instability
            }
        
        return coupling_metrics

# Global advanced AST parser instance
advanced_ast_parser = AdvancedASTParser()