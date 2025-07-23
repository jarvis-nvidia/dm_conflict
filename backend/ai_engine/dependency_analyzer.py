"""
DevMind Cross-File Dependency Analyzer
Advanced dependency analysis and call graph generation
"""

import ast
import os
import re
import json
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict, deque
from pathlib import Path
import networkx as nx
import hashlib

@dataclass
class DependencyNode:
    """Represents a node in the dependency graph"""
    name: str
    file_path: str
    node_type: str  # 'function', 'class', 'variable', 'import'
    line_number: int
    dependencies: Set[str] = field(default_factory=set)
    dependents: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CallRelation:
    """Represents a function/method call relationship"""
    caller: str
    callee: str
    caller_file: str
    callee_file: str
    line_number: int
    call_type: str  # 'function_call', 'method_call', 'constructor_call'

@dataclass
class ImportRelation:
    """Represents an import relationship"""
    importer_file: str
    imported_module: str
    imported_names: List[str]
    import_type: str  # 'module', 'from', 'relative'
    line_number: int

class CrossFileDependencyAnalyzer:
    """Advanced cross-file dependency analyzer with call graph generation"""
    
    def __init__(self):
        self.dependency_graph = nx.DiGraph()
        self.call_graph = nx.DiGraph()
        self.import_graph = nx.DiGraph()
        
        self.nodes = {}  # name -> DependencyNode
        self.file_nodes = defaultdict(list)  # file_path -> List[DependencyNode]
        self.call_relations = []
        self.import_relations = []
        
        # Cache for parsed files
        self.file_cache = {}
        
    def analyze_project(self, project_path: str, exclude_patterns: List[str] = None) -> Dict[str, Any]:
        """Analyze entire project for cross-file dependencies"""
        
        if exclude_patterns is None:
            exclude_patterns = [
                '__pycache__', '.git', '.venv', 'node_modules', 
                'dist', 'build', '.pytest_cache', '.mypy_cache'
            ]
        
        # Clear previous analysis
        self._reset_analysis()
        
        # Find all code files
        code_files = self._find_code_files(project_path, exclude_patterns)
        
        # Phase 1: Parse all files and extract nodes
        print(f"📁 Phase 1: Parsing {len(code_files)} files...")
        for file_path in code_files:
            self._parse_file_dependencies(file_path)
        
        # Phase 2: Build dependency relationships
        print("🔗 Phase 2: Building dependency relationships...")
        self._build_dependency_relationships()
        
        # Phase 3: Generate call graph
        print("📞 Phase 3: Generating call graph...")
        self._build_call_graph()
        
        # Phase 4: Analyze patterns and metrics
        print("📊 Phase 4: Analyzing patterns...")
        analysis_results = self._generate_analysis_results()
        
        return analysis_results
    
    def _reset_analysis(self):
        """Reset all analysis data"""
        self.dependency_graph.clear()
        self.call_graph.clear()
        self.import_graph.clear()
        self.nodes.clear()
        self.file_nodes.clear()
        self.call_relations.clear()
        self.import_relations.clear()
        self.file_cache.clear()
    
    def _find_code_files(self, project_path: str, exclude_patterns: List[str]) -> List[str]:
        """Find all code files in the project"""
        code_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs', '.cpp', '.cs'}
        code_files = []
        
        for root, dirs, files in os.walk(project_path):
            # Remove excluded directories
            dirs[:] = [d for d in dirs if not any(pattern in d for pattern in exclude_patterns)]
            
            for file in files:
                if any(file.endswith(ext) for ext in code_extensions):
                    file_path = os.path.join(root, file)
                    if not any(pattern in file_path for pattern in exclude_patterns):
                        code_files.append(file_path)
        
        return code_files
    
    def _parse_file_dependencies(self, file_path: str):
        """Parse a single file for dependencies"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            return
        
        # Check cache
        file_hash = hashlib.md5(content.encode()).hexdigest()
        if file_path in self.file_cache and self.file_cache[file_path]['hash'] == file_hash:
            return
        
        language = self._detect_language(file_path)
        
        if language == 'python':
            self._parse_python_dependencies(content, file_path)
        elif language in ['javascript', 'typescript']:
            self._parse_js_dependencies(content, file_path)
        elif language == 'java':
            self._parse_java_dependencies(content, file_path)
        
        # Cache the results
        self.file_cache[file_path] = {'hash': file_hash, 'parsed': True}
    
    def _parse_python_dependencies(self, content: str, file_path: str):
        """Parse Python file for dependencies"""
        try:
            tree = ast.parse(content)
            
            # Extract imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        import_rel = ImportRelation(
                            importer_file=file_path,
                            imported_module=alias.name,
                            imported_names=[alias.asname or alias.name],
                            import_type='module',
                            line_number=node.lineno
                        )
                        self.import_relations.append(import_rel)
                
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imported_names = [alias.name for alias in node.names]
                        import_rel = ImportRelation(
                            importer_file=file_path,
                            imported_module=node.module,
                            imported_names=imported_names,
                            import_type='from',
                            line_number=node.lineno
                        )
                        self.import_relations.append(import_rel)
                
                # Extract function definitions
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    func_node = DependencyNode(
                        name=node.name,
                        file_path=file_path,
                        node_type='function',
                        line_number=node.lineno,
                        metadata={
                            'args': [arg.arg for arg in node.args.args],
                            'is_async': isinstance(node, ast.AsyncFunctionDef),
                            'decorators': [self._get_decorator_name(d) for d in node.decorator_list]
                        }
                    )
                    
                    full_name = f"{file_path}::{node.name}"
                    self.nodes[full_name] = func_node
                    self.file_nodes[file_path].append(func_node)
                    
                    # Extract function calls within this function
                    self._extract_python_calls(node, file_path, node.name)
                
                # Extract class definitions
                elif isinstance(node, ast.ClassDef):
                    class_node = DependencyNode(
                        name=node.name,
                        file_path=file_path,
                        node_type='class',
                        line_number=node.lineno,
                        metadata={
                            'bases': [self._get_base_name(base) for base in node.bases],
                            'methods': []
                        }
                    )
                    
                    full_name = f"{file_path}::{node.name}"
                    self.nodes[full_name] = class_node
                    self.file_nodes[file_path].append(class_node)
                    
                    # Extract methods
                    for child in node.body:
                        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            method_name = f"{node.name}.{child.name}"
                            method_node = DependencyNode(
                                name=method_name,
                                file_path=file_path,
                                node_type='method',
                                line_number=child.lineno,
                                metadata={
                                    'class': node.name,
                                    'is_async': isinstance(child, ast.AsyncFunctionDef)
                                }
                            )
                            
                            method_full_name = f"{file_path}::{method_name}"
                            self.nodes[method_full_name] = method_node
                            self.file_nodes[file_path].append(method_node)
                            
                            # Extract method calls
                            self._extract_python_calls(child, file_path, method_name)
        
        except SyntaxError as e:
            print(f"❌ Syntax error in {file_path}: {e}")
    
    def _extract_python_calls(self, func_node: ast.AST, file_path: str, caller_name: str):
        """Extract function calls from a Python function"""
        for node in ast.walk(func_node):
            if isinstance(node, ast.Call):
                callee_name = self._get_call_name(node.func)
                if callee_name:
                    call_rel = CallRelation(
                        caller=caller_name,
                        callee=callee_name,
                        caller_file=file_path,
                        callee_file="",  # Will be resolved later
                        line_number=node.lineno,
                        call_type='function_call'
                    )
                    self.call_relations.append(call_rel)
    
    def _parse_js_dependencies(self, content: str, file_path: str):
        """Parse JavaScript/TypeScript file for dependencies"""
        lines = content.split('\n')
        
        # Extract imports (simplified regex-based parsing)
        import_patterns = [
            r'import\s+(.+?)\s+from\s+[\'"]([^\'"]+)[\'"]',
            r'import\s+[\'"]([^\'"]+)[\'"]',
            r'const\s+(.+?)\s*=\s*require\([\'"]([^\'"]+)[\'"]\)',
            r'require\([\'"]([^\'"]+)[\'"]\)'
        ]
        
        for line_num, line in enumerate(lines, 1):
            for pattern in import_patterns:
                matches = re.findall(pattern, line)
                for match in matches:
                    if len(match) == 2:
                        imported_names = [name.strip() for name in match[0].split(',')]
                        module_name = match[1]
                    else:
                        imported_names = []
                        module_name = match[0] if isinstance(match, tuple) else match
                    
                    import_rel = ImportRelation(
                        importer_file=file_path,
                        imported_module=module_name,
                        imported_names=imported_names,
                        import_type='module',
                        line_number=line_num
                    )
                    self.import_relations.append(import_rel)
        
        # Extract function definitions (simplified)
        function_patterns = [
            r'function\s+(\w+)\s*\(',
            r'const\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>',
            r'(\w+)\s*:\s*(?:async\s+)?function',
            r'(?:async\s+)?(\w+)\s*\([^)]*\)\s*{'
        ]
        
        for line_num, line in enumerate(lines, 1):
            for pattern in function_patterns:
                matches = re.findall(pattern, line)
                for func_name in matches:
                    func_node = DependencyNode(
                        name=func_name,
                        file_path=file_path,
                        node_type='function',
                        line_number=line_num,
                        metadata={'language': 'javascript'}
                    )
                    
                    full_name = f"{file_path}::{func_name}"
                    self.nodes[full_name] = func_node
                    self.file_nodes[file_path].append(func_node)
    
    def _parse_java_dependencies(self, content: str, file_path: str):
        """Parse Java file for dependencies (simplified)"""
        lines = content.split('\n')
        
        # Extract imports
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if line.startswith('import ') and not line.startswith('import static'):
                module_name = line.replace('import ', '').replace(';', '').strip()
                import_rel = ImportRelation(
                    importer_file=file_path,
                    imported_module=module_name,
                    imported_names=[module_name.split('.')[-1]],
                    import_type='module',
                    line_number=line_num
                )
                self.import_relations.append(import_rel)
        
        # Extract classes and methods (simplified)
        class_pattern = r'(?:public|private|protected)?\s*class\s+(\w+)'
        method_pattern = r'(?:public|private|protected)?\s*(?:static)?\s*[\w<>]+\s+(\w+)\s*\('
        
        current_class = None
        for line_num, line in enumerate(lines, 1):
            class_match = re.search(class_pattern, line)
            if class_match:
                current_class = class_match.group(1)
                class_node = DependencyNode(
                    name=current_class,
                    file_path=file_path,
                    node_type='class',
                    line_number=line_num,
                    metadata={'language': 'java'}
                )
                full_name = f"{file_path}::{current_class}"
                self.nodes[full_name] = class_node
                self.file_nodes[file_path].append(class_node)
            
            method_match = re.search(method_pattern, line)
            if method_match and current_class:
                method_name = method_match.group(1)
                if method_name != current_class:  # Not a constructor
                    method_node = DependencyNode(
                        name=f"{current_class}.{method_name}",
                        file_path=file_path,
                        node_type='method',
                        line_number=line_num,
                        metadata={'class': current_class, 'language': 'java'}
                    )
                    full_name = f"{file_path}::{current_class}.{method_name}"
                    self.nodes[full_name] = method_node
                    self.file_nodes[file_path].append(method_node)
    
    def _build_dependency_relationships(self):
        """Build dependency relationships between nodes"""
        # Add nodes to dependency graph
        for full_name, node in self.nodes.items():
            self.dependency_graph.add_node(full_name, **node.__dict__)
        
        # Add import relationships
        for import_rel in self.import_relations:
            self.import_graph.add_edge(
                import_rel.importer_file,
                import_rel.imported_module,
                **import_rel.__dict__
            )
        
        # Resolve call relationships
        for call_rel in self.call_relations:
            # Try to find the callee in the same file first
            caller_full = f"{call_rel.caller_file}::{call_rel.caller}"
            callee_candidates = [
                f"{call_rel.caller_file}::{call_rel.callee}",
                f"{call_rel.caller_file}::{call_rel.callee.split('.')[-1]}"  # For method calls
            ]
            
            # Look for callee in imported modules
            for import_rel in self.import_relations:
                if import_rel.importer_file == call_rel.caller_file:
                    for imported_name in import_rel.imported_names:
                        if imported_name == call_rel.callee or call_rel.callee.startswith(imported_name):
                            # Try to find in other files
                            for file_path, nodes in self.file_nodes.items():
                                for node in nodes:
                                    if node.name == call_rel.callee or node.name.endswith(f".{call_rel.callee}"):
                                        callee_candidates.append(f"{file_path}::{node.name}")
            
            # Add edges for found callees
            for callee_candidate in callee_candidates:
                if callee_candidate in self.nodes:
                    self.dependency_graph.add_edge(caller_full, callee_candidate, **call_rel.__dict__)
                    break
    
    def _build_call_graph(self):
        """Build call graph from dependency relationships"""
        for edge in self.dependency_graph.edges(data=True):
            caller, callee, data = edge
            if 'call_type' in data:
                self.call_graph.add_edge(caller, callee, **data)
    
    def _generate_analysis_results(self) -> Dict[str, Any]:
        """Generate comprehensive analysis results"""
        
        results = {
            'summary': {
                'total_files': len(self.file_nodes),
                'total_nodes': len(self.nodes),
                'total_dependencies': self.dependency_graph.number_of_edges(),
                'total_imports': len(self.import_relations),
                'total_calls': self.call_graph.number_of_edges()
            },
            'dependency_metrics': self._calculate_dependency_metrics(),
            'circular_dependencies': self._detect_circular_dependencies(),
            'unused_imports': self._detect_unused_imports(),
            'dead_code': self._detect_dead_code(),
            'coupling_metrics': self._calculate_coupling_metrics(),
            'hotspots': self._identify_hotspots(),
            'architectural_violations': self._detect_architectural_violations()
        }
        
        return results
    
    def _calculate_dependency_metrics(self) -> Dict[str, Any]:
        """Calculate various dependency metrics"""
        metrics = {}
        
        if self.dependency_graph.number_of_nodes() > 0:
            # Network metrics
            metrics['density'] = nx.density(self.dependency_graph)
            
            # Node metrics
            in_degrees = dict(self.dependency_graph.in_degree())
            out_degrees = dict(self.dependency_graph.out_degree())
            
            metrics['average_in_degree'] = sum(in_degrees.values()) / len(in_degrees)
            metrics['average_out_degree'] = sum(out_degrees.values()) / len(out_degrees)
            metrics['max_in_degree'] = max(in_degrees.values()) if in_degrees else 0
            metrics['max_out_degree'] = max(out_degrees.values()) if out_degrees else 0
            
            # Find most connected nodes
            metrics['most_dependent_nodes'] = sorted(in_degrees.items(), key=lambda x: x[1], reverse=True)[:10]
            metrics['most_depended_upon_nodes'] = sorted(out_degrees.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return metrics
    
    def _detect_circular_dependencies(self) -> List[List[str]]:
        """Detect circular dependencies"""
        try:
            cycles = list(nx.simple_cycles(self.dependency_graph))
            return cycles
        except nx.NetworkXError:
            return []
    
    def _detect_unused_imports(self) -> List[Dict[str, Any]]:
        """Detect unused imports"""
        unused_imports = []
        
        for import_rel in self.import_relations:
            file_path = import_rel.importer_file
            
            # Check if any imported name is used in function calls
            is_used = False
            for call_rel in self.call_relations:
                if call_rel.caller_file == file_path:
                    for imported_name in import_rel.imported_names:
                        if imported_name in call_rel.callee:
                            is_used = True
                            break
                if is_used:
                    break
            
            if not is_used:
                unused_imports.append({
                    'file': file_path,
                    'module': import_rel.imported_module,
                    'names': import_rel.imported_names,
                    'line': import_rel.line_number
                })
        
        return unused_imports
    
    def _detect_dead_code(self) -> List[Dict[str, Any]]:
        """Detect potentially dead code (unreachable functions/methods)"""
        dead_code = []
        
        # Find nodes with no incoming edges (not called by anyone)
        for node_name, node in self.nodes.items():
            if node.node_type in ['function', 'method']:
                in_degree = self.dependency_graph.in_degree(node_name)
                if in_degree == 0:
                    # Check if it's a main function or entry point
                    if not (node.name in ['main', '__main__', 'index'] or 
                           node.name.startswith('test_') or
                           'main' in node.metadata.get('decorators', [])):
                        dead_code.append({
                            'name': node.name,
                            'file': node.file_path,
                            'line': node.line_number,
                            'type': node.node_type
                        })
        
        return dead_code
    
    def _calculate_coupling_metrics(self) -> Dict[str, Any]:
        """Calculate coupling metrics between files"""
        coupling_metrics = {}
        
        file_coupling = defaultdict(set)
        
        # Calculate file-to-file coupling
        for import_rel in self.import_relations:
            file_coupling[import_rel.importer_file].add(import_rel.imported_module)
        
        for file_path in self.file_nodes.keys():
            efferent_coupling = len(file_coupling[file_path])  # Files this file depends on
            afferent_coupling = sum(1 for deps in file_coupling.values() if file_path in deps)  # Files that depend on this
            
            # Calculate instability (I = Ce / (Ca + Ce))
            total_coupling = afferent_coupling + efferent_coupling
            instability = efferent_coupling / total_coupling if total_coupling > 0 else 0
            
            coupling_metrics[file_path] = {
                'efferent_coupling': efferent_coupling,
                'afferent_coupling': afferent_coupling,
                'instability': instability
            }
        
        return coupling_metrics
    
    def _identify_hotspots(self) -> List[Dict[str, Any]]:
        """Identify architectural hotspots (highly coupled or complex areas)"""
        hotspots = []
        
        # Find files with high coupling
        coupling_metrics = self._calculate_coupling_metrics()
        
        for file_path, metrics in coupling_metrics.items():
            total_coupling = metrics['efferent_coupling'] + metrics['afferent_coupling']
            
            if total_coupling > 10:  # Threshold for high coupling
                hotspots.append({
                    'type': 'high_coupling',
                    'file': file_path,
                    'coupling_score': total_coupling,
                    'instability': metrics['instability'],
                    'severity': 'high' if total_coupling > 20 else 'medium'
                })
        
        # Find files with many functions (potential god objects)
        for file_path, nodes in self.file_nodes.items():
            function_count = len([n for n in nodes if n.node_type in ['function', 'method']])
            
            if function_count > 20:  # Threshold for too many functions
                hotspots.append({
                    'type': 'god_object',
                    'file': file_path,
                    'function_count': function_count,
                    'severity': 'high' if function_count > 50 else 'medium'
                })
        
        return hotspots
    
    def _detect_architectural_violations(self) -> List[Dict[str, Any]]:
        """Detect architectural violations"""
        violations = []
        
        # Detect circular dependencies at file level
        file_import_graph = nx.DiGraph()
        for import_rel in self.import_relations:
            file_import_graph.add_edge(import_rel.importer_file, import_rel.imported_module)
        
        try:
            file_cycles = list(nx.simple_cycles(file_import_graph))
            for cycle in file_cycles:
                violations.append({
                    'type': 'circular_file_dependency',
                    'description': f"Circular dependency detected: {' -> '.join(cycle)}",
                    'files': cycle,
                    'severity': 'high'
                })
        except nx.NetworkXError:
            pass
        
        return violations
    
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
            '.cs': 'csharp'
        }
        
        for ext, lang in extension_map.items():
            if file_path.endswith(ext):
                return lang
        
        return 'unknown'
    
    def _get_decorator_name(self, decorator) -> str:
        """Extract decorator name from AST node"""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return f"{decorator.value.id}.{decorator.attr}"
        return str(decorator)
    
    def _get_base_name(self, base) -> str:
        """Extract base class name from AST node"""
        if isinstance(base, ast.Name):
            return base.id
        elif isinstance(base, ast.Attribute):
            return f"{base.value.id}.{base.attr}"
        return str(base)
    
    def _get_call_name(self, func_node) -> Optional[str]:
        """Extract function call name from AST node"""
        if isinstance(func_node, ast.Name):
            return func_node.id
        elif isinstance(func_node, ast.Attribute):
            if isinstance(func_node.value, ast.Name):
                return f"{func_node.value.id}.{func_node.attr}"
            else:
                return func_node.attr
        return None
    
    def export_graphs(self, output_dir: str):
        """Export dependency graphs to files"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Export as JSON
        dependency_data = {
            'nodes': [{'id': node, **data} for node, data in self.dependency_graph.nodes(data=True)],
            'edges': [{'source': u, 'target': v, **data} for u, v, data in self.dependency_graph.edges(data=True)]
        }
        
        with open(os.path.join(output_dir, 'dependency_graph.json'), 'w') as f:
            json.dump(dependency_data, f, indent=2, default=str)
        
        # Export call graph
        call_data = {
            'nodes': [{'id': node} for node in self.call_graph.nodes()],
            'edges': [{'source': u, 'target': v, **data} for u, v, data in self.call_graph.edges(data=True)]
        }
        
        with open(os.path.join(output_dir, 'call_graph.json'), 'w') as f:
            json.dump(call_data, f, indent=2, default=str)
        
        print(f"📊 Graphs exported to {output_dir}")

# Global dependency analyzer instance
dependency_analyzer = CrossFileDependencyAnalyzer()