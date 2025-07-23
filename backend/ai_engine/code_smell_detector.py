"""
DevMind Code Smell Detector
Comprehensive code smell detection engine with multi-language support
"""

import ast
import re
import json
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from collections import defaultdict, Counter
import keyword
import builtins

@dataclass
class CodeSmell:
    """Represents a detected code smell"""
    smell_type: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    description: str
    file_path: str
    line_number: int
    column: int = 0
    suggestion: str = ""
    rule_id: str = ""
    category: str = ""
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SmellRule:
    """Defines a code smell detection rule"""
    rule_id: str
    name: str
    description: str
    category: str
    severity: str
    languages: List[str]
    detector_class: str
    config: Dict[str, Any] = field(default_factory=dict)

class BaseSmellDetector(ABC):
    """Base class for all smell detectors"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
    
    @abstractmethod
    def detect(self, content: str, file_path: str, ast_nodes: List[Any] = None) -> List[CodeSmell]:
        """Detect code smells in the given content"""
        pass

class NamingConventionDetector(BaseSmellDetector):
    """Detector for naming convention violations"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.naming_patterns = {
            'python': {
                'function': r'^[a-z_][a-z0-9_]*$',
                'class': r'^[A-Z][a-zA-Z0-9]*$',
                'variable': r'^[a-z_][a-z0-9_]*$',
                'constant': r'^[A-Z_][A-Z0-9_]*$',
                'private': r'^_[a-z_][a-z0-9_]*$'
            },
            'javascript': {
                'function': r'^[a-z][a-zA-Z0-9]*$',
                'class': r'^[A-Z][a-zA-Z0-9]*$',
                'variable': r'^[a-z][a-zA-Z0-9]*$',
                'constant': r'^[A-Z_][A-Z0-9_]*$'
            },
            'java': {
                'method': r'^[a-z][a-zA-Z0-9]*$',
                'class': r'^[A-Z][a-zA-Z0-9]*$',
                'variable': r'^[a-z][a-zA-Z0-9]*$',
                'constant': r'^[A-Z_][A-Z0-9_]*$'
            }
        }
    
    def detect(self, content: str, file_path: str, ast_nodes: List[Any] = None) -> List[CodeSmell]:
        smells = []
        language = self._detect_language(file_path)
        
        if language not in self.naming_patterns:
            return smells
        
        patterns = self.naming_patterns[language]
        
        if language == 'python':
            smells.extend(self._check_python_naming(content, file_path, patterns))
        elif language in ['javascript', 'typescript']:
            smells.extend(self._check_js_naming(content, file_path, patterns))
        elif language == 'java':
            smells.extend(self._check_java_naming(content, file_path, patterns))
        
        return smells
    
    def _check_python_naming(self, content: str, file_path: str, patterns: Dict[str, str]) -> List[CodeSmell]:
        smells = []
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if not re.match(patterns['function'], node.name):
                        smells.append(CodeSmell(
                            smell_type="naming_convention_violation",
                            severity="medium",
                            description=f"Function '{node.name}' doesn't follow Python naming convention",
                            file_path=file_path,
                            line_number=node.lineno,
                            suggestion="Use snake_case for function names (e.g., my_function)",
                            rule_id="PY_FUNC_NAMING",
                            category="naming_conventions"
                        ))
                
                elif isinstance(node, ast.ClassDef):
                    if not re.match(patterns['class'], node.name):
                        smells.append(CodeSmell(
                            smell_type="naming_convention_violation",
                            severity="medium",
                            description=f"Class '{node.name}' doesn't follow Python naming convention",
                            file_path=file_path,
                            line_number=node.lineno,
                            suggestion="Use PascalCase for class names (e.g., MyClass)",
                            rule_id="PY_CLASS_NAMING",
                            category="naming_conventions"
                        ))
                
                elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                    # Variable assignment
                    if node.id.isupper():
                        if not re.match(patterns['constant'], node.id):
                            smells.append(CodeSmell(
                                smell_type="naming_convention_violation",
                                severity="low",
                                description=f"Constant '{node.id}' doesn't follow naming convention",
                                file_path=file_path,
                                line_number=node.lineno,
                                suggestion="Use UPPER_SNAKE_CASE for constants",
                                rule_id="PY_CONST_NAMING",
                                category="naming_conventions"
                            ))
                    else:
                        if not re.match(patterns['variable'], node.id):
                            smells.append(CodeSmell(
                                smell_type="naming_convention_violation",
                                severity="low",
                                description=f"Variable '{node.id}' doesn't follow naming convention",
                                file_path=file_path,
                                line_number=node.lineno,
                                suggestion="Use snake_case for variable names",
                                rule_id="PY_VAR_NAMING",
                                category="naming_conventions"
                            ))
        
        except SyntaxError:
            pass
        
        return smells
    
    def _detect_language(self, file_path: str) -> str:
        extension_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'javascript',
            '.tsx': 'typescript',
            '.java': 'java'
        }
        
        for ext, lang in extension_map.items():
            if file_path.endswith(ext):
                return lang
        
        return 'unknown'

class ComplexityDetector(BaseSmellDetector):
    """Detector for complexity-related code smells"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.thresholds = {
            'cyclomatic_complexity': config.get('cyclomatic_threshold', 10) if config else 10,
            'cognitive_complexity': config.get('cognitive_threshold', 15) if config else 15,
            'nesting_depth': config.get('nesting_threshold', 4) if config else 4,
            'function_length': config.get('function_length_threshold', 50) if config else 50,
            'class_length': config.get('class_length_threshold', 200) if config else 200,
            'parameter_count': config.get('parameter_threshold', 5) if config else 5
        }
    
    def detect(self, content: str, file_path: str, ast_nodes: List[Any] = None) -> List[CodeSmell]:
        smells = []
        language = self._detect_language(file_path)
        
        if language == 'python':
            smells.extend(self._check_python_complexity(content, file_path))
        elif language in ['javascript', 'typescript']:
            smells.extend(self._check_js_complexity(content, file_path))
        
        return smells
    
    def _check_python_complexity(self, content: str, file_path: str) -> List[CodeSmell]:
        smells = []
        try:
            tree = ast.parse(content)
            lines = content.split('\n')
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    # Check function length
                    func_length = (node.end_lineno or node.lineno) - node.lineno + 1
                    if func_length > self.thresholds['function_length']:
                        smells.append(CodeSmell(
                            smell_type="long_function",
                            severity="medium",
                            description=f"Function '{node.name}' is too long ({func_length} lines)",
                            file_path=file_path,
                            line_number=node.lineno,
                            suggestion=f"Consider breaking down function into smaller functions (current: {func_length}, recommended: <{self.thresholds['function_length']})",
                            rule_id="LONG_FUNCTION",
                            category="complexity"
                        ))
                    
                    # Check parameter count
                    param_count = len(node.args.args)
                    if param_count > self.thresholds['parameter_count']:
                        smells.append(CodeSmell(
                            smell_type="too_many_parameters",
                            severity="medium",
                            description=f"Function '{node.name}' has too many parameters ({param_count})",
                            file_path=file_path,
                            line_number=node.lineno,
                            suggestion=f"Consider using a parameter object or reducing parameters (current: {param_count}, recommended: <={self.thresholds['parameter_count']})",
                            rule_id="TOO_MANY_PARAMS",
                            category="complexity"
                        ))
                    
                    # Check cyclomatic complexity
                    complexity = self._calculate_cyclomatic_complexity(node)
                    if complexity > self.thresholds['cyclomatic_complexity']:
                        smells.append(CodeSmell(
                            smell_type="high_cyclomatic_complexity",
                            severity="high",
                            description=f"Function '{node.name}' has high cyclomatic complexity ({complexity})",
                            file_path=file_path,
                            line_number=node.lineno,
                            suggestion=f"Consider refactoring to reduce complexity (current: {complexity}, recommended: <={self.thresholds['cyclomatic_complexity']})",
                            rule_id="HIGH_COMPLEXITY",
                            category="complexity"
                        ))
                
                elif isinstance(node, ast.ClassDef):
                    # Check class length
                    class_length = (node.end_lineno or node.lineno) - node.lineno + 1
                    if class_length > self.thresholds['class_length']:
                        smells.append(CodeSmell(
                            smell_type="large_class",
                            severity="medium",
                            description=f"Class '{node.name}' is too large ({class_length} lines)",
                            file_path=file_path,
                            line_number=node.lineno,
                            suggestion=f"Consider splitting class into smaller classes (current: {class_length}, recommended: <{self.thresholds['class_length']})",
                            rule_id="LARGE_CLASS",
                            category="complexity"
                        ))
        
        except SyntaxError:
            pass
        
        return smells
    
    def _calculate_cyclomatic_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity for a function node"""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, (ast.And, ast.Or)):
                complexity += 1
        
        return complexity
    
    def _detect_language(self, file_path: str) -> str:
        if file_path.endswith('.py'):
            return 'python'
        elif file_path.endswith(('.js', '.ts', '.jsx', '.tsx')):
            return 'javascript'
        return 'unknown'

class DuplicationDetector(BaseSmellDetector):
    """Detector for code duplication"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.min_duplicate_lines = config.get('min_duplicate_lines', 6) if config else 6
        self.similarity_threshold = config.get('similarity_threshold', 0.8) if config else 0.8
    
    def detect(self, content: str, file_path: str, ast_nodes: List[Any] = None) -> List[CodeSmell]:
        smells = []
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        # Find duplicate blocks
        duplicates = self._find_duplicate_blocks(lines)
        
        for duplicate_info in duplicates:
            smells.append(CodeSmell(
                smell_type="code_duplication",
                severity="medium",
                description=f"Duplicate code block found ({duplicate_info['lines']} lines)",
                file_path=file_path,
                line_number=duplicate_info['start_line'],
                suggestion="Consider extracting duplicate code into a separate function",
                rule_id="CODE_DUPLICATION",
                category="duplication",
                metadata=duplicate_info
            ))
        
        return smells
    
    def _find_duplicate_blocks(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Find blocks of duplicate code"""
        duplicates = []
        n = len(lines)
        
        for i in range(n):
            for j in range(i + self.min_duplicate_lines, n):
                # Check if we have a duplicate block starting at i and j
                duplicate_length = 0
                k = 0
                
                while (i + k < n and j + k < n and 
                       i + k < j and  # Don't compare overlapping blocks
                       lines[i + k] == lines[j + k]):
                    duplicate_length += 1
                    k += 1
                
                if duplicate_length >= self.min_duplicate_lines:
                    duplicates.append({
                        'start_line': i + 1,
                        'end_line': i + duplicate_length,
                        'duplicate_start': j + 1,
                        'duplicate_end': j + duplicate_length,
                        'lines': duplicate_length
                    })
        
        return duplicates

class SecuritySmellDetector(BaseSmellDetector):
    """Detector for security-related code smells"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.security_patterns = {
            'sql_injection': [
                r'(?i)execute\s*\(\s*[\'"].*\+',
                r'(?i)query\s*\(\s*[\'"].*\+',
                r'(?i)\.format\s*\(',
                r'%s.*%'
            ],
            'hardcoded_secrets': [
                r'(?i)(password|pwd|secret|key|token)\s*=\s*[\'"][^\'"]{8,}[\'"]',
                r'(?i)(api_key|apikey)\s*=\s*[\'"][^\'"]+[\'"]'
            ],
            'dangerous_functions': [
                r'(?i)\beval\s*\(',
                r'(?i)\bexec\s*\(',
                r'(?i)\b__import__\s*\(',
                r'(?i)\bpickle\.loads?\s*\('
            ],
            'weak_crypto': [
                r'(?i)md5\s*\(',
                r'(?i)sha1\s*\(',
                r'(?i)des\s*\(',
                r'(?i)rc4\s*\('
            ]
        }
    
    def detect(self, content: str, file_path: str, ast_nodes: List[Any] = None) -> List[CodeSmell]:
        smells = []
        lines = content.split('\n')
        
        for category, patterns in self.security_patterns.items():
            for pattern in patterns:
                for line_num, line in enumerate(lines, 1):
                    if re.search(pattern, line):
                        smells.append(CodeSmell(
                            smell_type=f"security_{category}",
                            severity="high",
                            description=f"Potential {category.replace('_', ' ')} vulnerability detected",
                            file_path=file_path,
                            line_number=line_num,
                            suggestion=self._get_security_suggestion(category),
                            rule_id=f"SEC_{category.upper()}",
                            category="security"
                        ))
        
        return smells
    
    def _get_security_suggestion(self, category: str) -> str:
        suggestions = {
            'sql_injection': "Use parameterized queries or ORM instead of string concatenation",
            'hardcoded_secrets': "Use environment variables or secure configuration files",
            'dangerous_functions': "Avoid using eval(), exec(), and similar dangerous functions",
            'weak_crypto': "Use strong cryptographic algorithms (SHA-256, AES, etc.)"
        }
        return suggestions.get(category, "Review for security implications")

class CodeSmellDetectorEngine:
    """Main engine for code smell detection"""
    
    def __init__(self):
        self.detectors = {
            'naming_conventions': NamingConventionDetector(),
            'complexity': ComplexityDetector(),
            'duplication': DuplicationDetector(),
            'security': SecuritySmellDetector()
        }
        
        # Language-specific rule configurations
        self.language_rules = {
            'python': {
                'enabled_detectors': ['naming_conventions', 'complexity', 'duplication', 'security'],
                'style_guide': 'PEP8',
                'complexity_thresholds': {
                    'cyclomatic_complexity': 10,
                    'cognitive_complexity': 15,
                    'function_length': 50,
                    'class_length': 200
                }
            },
            'javascript': {
                'enabled_detectors': ['naming_conventions', 'complexity', 'duplication', 'security'],
                'style_guide': 'ESLint',
                'complexity_thresholds': {
                    'cyclomatic_complexity': 10,
                    'cognitive_complexity': 15,
                    'function_length': 40,
                    'class_length': 150
                }
            }
        }
    
    def detect_smells(self, content: str, file_path: str, language: str = None, 
                     custom_config: Dict[str, Any] = None) -> List[CodeSmell]:
        """Detect all code smells in the given content"""
        
        if not language:
            language = self._detect_language(file_path)
        
        # Get language-specific configuration
        lang_config = self.language_rules.get(language, {})
        enabled_detectors = lang_config.get('enabled_detectors', list(self.detectors.keys()))
        
        # Apply custom configuration if provided
        if custom_config:
            enabled_detectors = custom_config.get('enabled_detectors', enabled_detectors)
        
        all_smells = []
        
        # Run enabled detectors
        for detector_name in enabled_detectors:
            if detector_name in self.detectors:
                detector = self.detectors[detector_name]
                
                # Update detector configuration
                if custom_config and detector_name in custom_config:
                    detector.config.update(custom_config[detector_name])
                
                try:
                    smells = detector.detect(content, file_path)
                    all_smells.extend(smells)
                except Exception as e:
                    print(f"Error in {detector_name} detector: {e}")
        
        # Sort by severity and line number
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        all_smells.sort(key=lambda x: (severity_order.get(x.severity, 4), x.line_number))
        
        return all_smells
    
    def get_smell_summary(self, smells: List[CodeSmell]) -> Dict[str, Any]:
        """Generate summary statistics for detected smells"""
        if not smells:
            return {
                'total_smells': 0,
                'by_severity': {},
                'by_category': {},
                'by_type': {},
                'quality_score': 100.0
            }
        
        summary = {
            'total_smells': len(smells),
            'by_severity': Counter(smell.severity for smell in smells),
            'by_category': Counter(smell.category for smell in smells),
            'by_type': Counter(smell.smell_type for smell in smells),
            'unique_files': len(set(smell.file_path for smell in smells))
        }
        
        # Calculate quality score (0-100)
        severity_weights = {'critical': 10, 'high': 5, 'medium': 2, 'low': 1}
        total_weight = sum(severity_weights.get(smell.severity, 1) for smell in smells)
        
        # Base score of 100, subtract weighted smells
        quality_score = max(0, 100 - (total_weight / len(smells) * 10) if smells else 100)
        summary['quality_score'] = round(quality_score, 1)
        
        return summary
    
    def generate_report(self, smells: List[CodeSmell], format_type: str = 'json') -> str:
        """Generate a formatted report of code smells"""
        
        if format_type == 'json':
            return json.dumps([
                {
                    'smell_type': smell.smell_type,
                    'severity': smell.severity,
                    'description': smell.description,
                    'file_path': smell.file_path,
                    'line_number': smell.line_number,
                    'suggestion': smell.suggestion,
                    'rule_id': smell.rule_id,
                    'category': smell.category,
                    'confidence': smell.confidence
                }
                for smell in smells
            ], indent=2)
        
        elif format_type == 'markdown':
            report = "# Code Quality Report\n\n"
            summary = self.get_smell_summary(smells)
            
            report += f"**Quality Score: {summary['quality_score']}/100**\n\n"
            report += f"**Total Issues: {summary['total_smells']}**\n\n"
            
            if summary['by_severity']:
                report += "## Issues by Severity\n"
                for severity, count in summary['by_severity'].items():
                    report += f"- {severity.title()}: {count}\n"
                report += "\n"
            
            report += "## Detailed Issues\n\n"
            
            current_file = None
            for smell in smells:
                if smell.file_path != current_file:
                    report += f"### {smell.file_path}\n\n"
                    current_file = smell.file_path
                
                report += f"**Line {smell.line_number}** - {smell.severity.upper()}: {smell.description}\n"
                if smell.suggestion:
                    report += f"*Suggestion: {smell.suggestion}*\n"
                report += "\n"
            
            return report
        
        return str(smells)
    
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
            '.cs': 'csharp',
            '.php': 'php'
        }
        
        for ext, lang in extension_map.items():
            if file_path.endswith(ext):
                return lang
        
        return 'unknown'

# Global code smell detector engine
code_smell_detector = CodeSmellDetectorEngine()