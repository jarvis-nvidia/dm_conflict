"""
DevMind Learning System
Advanced user pattern learning and personalization engine
"""

import json
import re
import ast
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict, Counter
from datetime import datetime, timedelta
import hashlib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

@dataclass
class CodingStyleProfile:
    """User's coding style profile"""
    user_id: str
    language: str
    
    # Naming conventions
    function_naming: str = "snake_case"  # snake_case, camelCase, PascalCase
    variable_naming: str = "snake_case"
    class_naming: str = "PascalCase"
    constant_naming: str = "UPPER_SNAKE_CASE"
    
    # Formatting preferences
    indentation: str = "4_spaces"  # 4_spaces, 2_spaces, tabs
    line_length: int = 79
    blank_lines_after_class: int = 2
    blank_lines_after_function: int = 1
    
    # Code structure preferences
    max_function_length: int = 50
    max_class_length: int = 200
    max_parameters: int = 5
    
    # Documentation preferences
    docstring_style: str = "google"  # google, sphinx, numpy
    comment_frequency: float = 0.1  # Comments per line of code
    type_hints_usage: bool = True
    
    # Error handling preferences
    error_handling_style: str = "specific"  # specific, generic, minimal
    logging_usage: bool = True
    
    # Testing preferences
    test_coverage_target: float = 0.8
    test_naming_pattern: str = "test_*"
    
    # Framework/Library preferences
    preferred_libraries: List[str] = field(default_factory=list)
    coding_patterns: List[str] = field(default_factory=list)
    
    # Confidence scores
    confidence_scores: Dict[str, float] = field(default_factory=dict)
    
    # Learning metadata
    samples_analyzed: int = 0
    last_updated: datetime = field(default_factory=datetime.now)
    creation_date: datetime = field(default_factory=datetime.now)

@dataclass
class CommitPattern:
    """User's commit message patterns"""
    user_id: str
    
    # Commit message structure
    message_format: str = "conventional"  # conventional, traditional, custom
    average_length: int = 50
    uses_emoji: bool = False
    uses_scope: bool = True
    
    # Common patterns
    common_prefixes: List[str] = field(default_factory=list)
    common_keywords: List[str] = field(default_factory=list)
    
    # Commit frequency patterns
    commits_per_day: float = 3.0
    preferred_commit_times: List[int] = field(default_factory=list)  # Hours of day
    
    # File change patterns
    files_per_commit: float = 2.5
    lines_per_commit: float = 25.0
    
    # Metadata
    total_commits_analyzed: int = 0
    last_updated: datetime = field(default_factory=datetime.now)

@dataclass
class BugPattern:
    """User's bug patterns and debugging preferences"""
    user_id: str
    
    # Common bug types
    frequent_bug_types: List[str] = field(default_factory=list)
    bug_categories: Dict[str, int] = field(default_factory=dict)
    
    # Debugging preferences
    preferred_debugging_tools: List[str] = field(default_factory=list)
    debug_strategy: str = "systematic"  # systematic, exploratory, minimal
    
    # Error patterns
    common_error_messages: List[str] = field(default_factory=list)
    resolution_patterns: List[str] = field(default_factory=list)
    
    # Learning from fixes
    fix_patterns: Dict[str, List[str]] = field(default_factory=dict)
    
    # Metadata
    bugs_analyzed: int = 0
    last_updated: datetime = field(default_factory=datetime.now)

@dataclass
class InteractionEvent:
    """User interaction event for learning"""
    user_id: str
    event_type: str  # 'code_analysis', 'debug_request', 'code_review', 'commit_gen'
    timestamp: datetime
    context: Dict[str, Any]
    outcome: Dict[str, Any]
    satisfaction_score: Optional[float] = None
    feedback: Optional[str] = None

class CodingStyleAnalyzer:
    """Analyzes user's coding style from code samples"""
    
    def __init__(self):
        self.style_patterns = {
            'naming_conventions': {
                'snake_case': r'^[a-z_][a-z0-9_]*$',
                'camelCase': r'^[a-z][a-zA-Z0-9]*$',
                'PascalCase': r'^[A-Z][a-zA-Z0-9]*$',
                'UPPER_SNAKE_CASE': r'^[A-Z_][A-Z0-9_]*$'
            },
            'indentation': {
                '2_spaces': r'^  [^ ]',
                '4_spaces': r'^    [^ ]',
                'tabs': r'^\t[^\t]'
            }
        }
    
    def analyze_python_style(self, code: str, file_path: str) -> Dict[str, Any]:
        """Analyze Python coding style"""
        try:
            tree = ast.parse(code)
            analysis = {
                'naming_patterns': defaultdict(list),
                'structure_metrics': {},
                'formatting_patterns': {},
                'documentation_patterns': {}
            }
            
            lines = code.split('\n')
            
            # Analyze naming conventions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis['naming_patterns']['functions'].append(node.name)
                elif isinstance(node, ast.ClassDef):
                    analysis['naming_patterns']['classes'].append(node.name)
                elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                    analysis['naming_patterns']['variables'].append(node.id)
            
            # Analyze indentation
            indented_lines = [line for line in lines if line.startswith((' ', '\t'))]
            if indented_lines:
                if most_common_indent := self._detect_indentation(indented_lines):
                    analysis['formatting_patterns']['indentation'] = most_common_indent
            
            # Analyze line length
            line_lengths = [len(line) for line in lines if line.strip()]
            if line_lengths:
                analysis['formatting_patterns']['average_line_length'] = np.mean(line_lengths)
                analysis['formatting_patterns']['max_line_length'] = max(line_lengths)
            
            # Analyze documentation
            docstring_count = 0
            total_functions = 0
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    total_functions += 1
                    if ast.get_docstring(node):
                        docstring_count += 1
            
            if total_functions > 0:
                analysis['documentation_patterns']['docstring_ratio'] = docstring_count / total_functions
            
            # Analyze comments
            comment_lines = [line for line in lines if line.strip().startswith('#')]
            code_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
            
            if code_lines:
                analysis['documentation_patterns']['comment_ratio'] = len(comment_lines) / len(code_lines)
            
            return analysis
            
        except SyntaxError:
            return {}
    
    def _detect_indentation(self, indented_lines: List[str]) -> str:
        """Detect most common indentation style"""
        indent_counts = Counter()
        
        for line in indented_lines:
            if line.startswith('    '):
                indent_counts['4_spaces'] += 1
            elif line.startswith('  '):
                indent_counts['2_spaces'] += 1
            elif line.startswith('\t'):
                indent_counts['tabs'] += 1
        
        return indent_counts.most_common(1)[0][0] if indent_counts else '4_spaces'
    
    def _detect_naming_pattern(self, names: List[str]) -> str:
        """Detect most common naming pattern"""
        pattern_counts = Counter()
        
        for name in names:
            for pattern_name, pattern_regex in self.style_patterns['naming_conventions'].items():
                if re.match(pattern_regex, name):
                    pattern_counts[pattern_name] += 1
                    break
        
        return pattern_counts.most_common(1)[0][0] if pattern_counts else 'snake_case'

class CommitPatternAnalyzer:
    """Analyzes user's commit message patterns"""
    
    def __init__(self):
        self.conventional_prefixes = [
            'feat', 'fix', 'docs', 'style', 'refactor', 
            'test', 'chore', 'perf', 'ci', 'build'
        ]
    
    def analyze_commit_messages(self, commits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns in commit messages"""
        if not commits:
            return {}
        
        messages = [commit.get('message', '') for commit in commits]
        analysis = {
            'message_patterns': {},
            'structural_patterns': {},
            'temporal_patterns': {},
            'change_patterns': {}
        }
        
        # Analyze message structure
        analysis['message_patterns'] = self._analyze_message_structure(messages)
        
        # Analyze temporal patterns
        if timestamps := [commit.get('timestamp') for commit in commits if commit.get('timestamp')]:
            analysis['temporal_patterns'] = self._analyze_commit_timing(timestamps)
        
        # Analyze change patterns
        if file_changes := [commit.get('files_changed', []) for commit in commits]:
            analysis['change_patterns'] = self._analyze_change_patterns(file_changes)
        
        return analysis
    
    def _analyze_message_structure(self, messages: List[str]) -> Dict[str, Any]:
        """Analyze commit message structure patterns"""
        patterns = {
            'average_length': np.mean([len(msg) for msg in messages]),
            'uses_conventional': 0,
            'uses_scope': 0,
            'uses_emoji': 0,
            'common_prefixes': Counter(),
            'common_keywords': Counter()
        }
        
        for message in messages:
            # Check conventional commits
            if any(message.lower().startswith(f"{prefix}:") or message.lower().startswith(f"{prefix}(") 
                   for prefix in self.conventional_prefixes):
                patterns['uses_conventional'] += 1
            
            # Check scope usage
            if re.match(r'^\w+\([^)]+\):', message):
                patterns['uses_scope'] += 1
            
            # Check emoji usage
            if re.search(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]', message):
                patterns['uses_emoji'] += 1
            
            # Extract common prefixes (first word)
            first_word = message.split()[0].lower() if message.split() else ''
            if first_word:
                patterns['common_prefixes'][first_word] += 1
            
            # Extract keywords
            words = re.findall(r'\b\w+\b', message.lower())
            for word in words:
                if len(word) > 3:  # Filter out short words
                    patterns['common_keywords'][word] += 1
        
        # Convert to percentages
        total_messages = len(messages)
        patterns['conventional_ratio'] = patterns['uses_conventional'] / total_messages
        patterns['scope_ratio'] = patterns['uses_scope'] / total_messages
        patterns['emoji_ratio'] = patterns['uses_emoji'] / total_messages
        
        return patterns
    
    def _analyze_commit_timing(self, timestamps: List[datetime]) -> Dict[str, Any]:
        """Analyze temporal patterns in commits"""
        hours = [ts.hour for ts in timestamps]
        days = [ts.weekday() for ts in timestamps]
        
        return {
            'preferred_hours': Counter(hours).most_common(5),
            'preferred_days': Counter(days).most_common(7),
            'commits_per_day': len(timestamps) / max(1, (max(timestamps) - min(timestamps)).days),
            'most_active_hour': Counter(hours).most_common(1)[0][0] if hours else 9
        }
    
    def _analyze_change_patterns(self, file_changes: List[List[str]]) -> Dict[str, Any]:
        """Analyze patterns in file changes"""
        all_files = [file for changes in file_changes for file in changes]
        file_extensions = [os.path.splitext(file)[1] for file in all_files if '.' in file]
        
        return {
            'files_per_commit': np.mean([len(changes) for changes in file_changes]),
            'common_file_types': Counter(file_extensions).most_common(10),
            'average_files_changed': len(all_files) / len(file_changes) if file_changes else 0
        }

class BugPatternLearner:
    """Learns from user's bug patterns and debugging behavior"""
    
    def __init__(self):
        self.bug_categories = [
            'syntax_error', 'type_error', 'name_error', 'attribute_error',
            'index_error', 'key_error', 'import_error', 'logic_error',
            'performance_issue', 'memory_issue', 'concurrency_issue'
        ]
    
    def analyze_debug_sessions(self, debug_sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze user's debugging sessions to learn patterns"""
        if not debug_sessions:
            return {}
        
        analysis = {
            'error_patterns': self._analyze_error_patterns(debug_sessions),
            'resolution_patterns': self._analyze_resolution_patterns(debug_sessions),
            'debugging_behavior': self._analyze_debugging_behavior(debug_sessions)
        }
        
        return analysis
    
    def _analyze_error_patterns(self, sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze common error patterns"""
        error_messages = []
        error_types = []
        
        for session in sessions:
            if error_msg := session.get('error_message'):
                error_messages.append(error_msg)
                error_types.append(self._categorize_error(error_msg))
        
        # Use TF-IDF to find common error patterns
        if error_messages:
            vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(error_messages)
            
            # Cluster similar errors
            n_clusters = min(10, len(error_messages))
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(tfidf_matrix)
            
            return {
                'common_error_types': Counter(error_types).most_common(10),
                'error_clusters': self._group_errors_by_cluster(error_messages, clusters),
                'total_errors_analyzed': len(error_messages)
            }
        
        return {}
    
    def _analyze_resolution_patterns(self, sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze how user typically resolves issues"""
        resolution_methods = []
        time_to_resolve = []
        
        for session in sessions:
            if resolution := session.get('resolution_method'):
                resolution_methods.append(resolution)
            
            if start_time := session.get('start_time'):
                if end_time := session.get('end_time'):
                    duration = (end_time - start_time).total_seconds() / 60  # minutes
                    time_to_resolve.append(duration)
        
        return {
            'common_resolution_methods': Counter(resolution_methods).most_common(10),
            'average_resolution_time': np.mean(time_to_resolve) if time_to_resolve else 0,
            'median_resolution_time': np.median(time_to_resolve) if time_to_resolve else 0
        }
    
    def _analyze_debugging_behavior(self, sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze user's debugging behavior patterns"""
        debugging_approaches = []
        tools_used = []
        
        for session in sessions:
            if approach := session.get('debugging_approach'):
                debugging_approaches.append(approach)
            
            if tools := session.get('tools_used'):
                tools_used.extend(tools)
        
        return {
            'preferred_debugging_approaches': Counter(debugging_approaches).most_common(5),
            'commonly_used_tools': Counter(tools_used).most_common(10),
            'debugging_sessions_count': len(sessions)
        }
    
    def _categorize_error(self, error_message: str) -> str:
        """Categorize error message into predefined categories"""
        error_lower = error_message.lower()
        
        if 'syntaxerror' in error_lower or 'invalid syntax' in error_lower:
            return 'syntax_error'
        elif 'typeerror' in error_lower:
            return 'type_error'
        elif 'nameerror' in error_lower:
            return 'name_error'
        elif 'attributeerror' in error_lower:
            return 'attribute_error'
        elif 'indexerror' in error_lower:
            return 'index_error'
        elif 'keyerror' in error_lower:
            return 'key_error'
        elif 'importerror' in error_lower or 'modulenotfounderror' in error_lower:
            return 'import_error'
        elif 'performance' in error_lower or 'slow' in error_lower:
            return 'performance_issue'
        elif 'memory' in error_lower:
            return 'memory_issue'
        else:
            return 'other'
    
    def _group_errors_by_cluster(self, error_messages: List[str], clusters: List[int]) -> Dict[int, List[str]]:
        """Group errors by their cluster assignments"""
        clustered_errors = defaultdict(list)
        
        for message, cluster in zip(error_messages, clusters):
            clustered_errors[cluster].append(message)
        
        return dict(clustered_errors)

class PersonalizationEngine:
    """Main personalization engine that learns from user interactions"""
    
    def __init__(self, storage_path: str = "/app/backend/user_profiles"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        
        self.style_analyzer = CodingStyleAnalyzer()
        self.commit_analyzer = CommitPatternAnalyzer()
        self.bug_learner = BugPatternLearner()
        
        # In-memory caches
        self.user_profiles = {}
        self.interaction_history = defaultdict(list)
    
    def learn_from_code_sample(self, user_id: str, code: str, file_path: str, language: str):
        """Learn user's coding style from a code sample"""
        profile = self._get_or_create_style_profile(user_id, language)
        
        if language == 'python':
            style_analysis = self.style_analyzer.analyze_python_style(code, file_path)
            self._update_style_profile(profile, style_analysis)
        
        profile.samples_analyzed += 1
        profile.last_updated = datetime.now()
        
        self._save_user_profile(user_id, profile)
    
    def learn_from_commits(self, user_id: str, commits: List[Dict[str, Any]]):
        """Learn user's commit patterns"""
        commit_pattern = self._get_or_create_commit_pattern(user_id)
        
        commit_analysis = self.commit_analyzer.analyze_commit_messages(commits)
        self._update_commit_pattern(commit_pattern, commit_analysis)
        
        commit_pattern.total_commits_analyzed += len(commits)
        commit_pattern.last_updated = datetime.now()
        
        self._save_commit_pattern(user_id, commit_pattern)
    
    def learn_from_debug_session(self, user_id: str, debug_session: Dict[str, Any]):
        """Learn from a debugging session"""
        bug_pattern = self._get_or_create_bug_pattern(user_id)
        
        # Extract learning insights from debug session
        if error_msg := debug_session.get('error_message'):
            error_type = self.bug_learner._categorize_error(error_msg)
            bug_pattern.frequent_bug_types.append(error_type)
            bug_pattern.common_error_messages.append(error_msg[:200])  # Truncate
        
        if resolution := debug_session.get('resolution'):
            bug_pattern.resolution_patterns.append(resolution)
        
        bug_pattern.bugs_analyzed += 1
        bug_pattern.last_updated = datetime.now()
        
        self._save_bug_pattern(user_id, bug_pattern)
    
    def record_interaction(self, user_id: str, event_type: str, context: Dict[str, Any], 
                          outcome: Dict[str, Any], satisfaction_score: Optional[float] = None):
        """Record user interaction for learning"""
        interaction = InteractionEvent(
            user_id=user_id,
            event_type=event_type,
            timestamp=datetime.now(),
            context=context,
            outcome=outcome,
            satisfaction_score=satisfaction_score
        )
        
        self.interaction_history[user_id].append(interaction)
        
        # Learn from the interaction
        self._learn_from_interaction(interaction)
    
    def get_personalized_recommendations(self, user_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get personalized recommendations based on user profile"""
        recommendations = {
            'style_suggestions': [],
            'debugging_hints': [],
            'commit_template': '',
            'preferred_patterns': [],
            'custom_rules': []
        }
        
        # Get user profiles
        style_profile = self._load_style_profile(user_id, context.get('language', 'python'))
        commit_pattern = self._load_commit_pattern(user_id)
        bug_pattern = self._load_bug_pattern(user_id)
        
        if style_profile:
            recommendations['style_suggestions'] = self._generate_style_suggestions(style_profile, context)
            recommendations['preferred_patterns'] = style_profile.coding_patterns
        
        if commit_pattern:
            recommendations['commit_template'] = self._generate_commit_template(commit_pattern)
        
        if bug_pattern:
            recommendations['debugging_hints'] = self._generate_debugging_hints(bug_pattern, context)
        
        return recommendations
    
    def _get_or_create_style_profile(self, user_id: str, language: str) -> CodingStyleProfile:
        """Get or create user's coding style profile"""
        profile_key = f"{user_id}_{language}"
        
        if profile_key not in self.user_profiles:
            # Try to load from disk
            profile = self._load_style_profile(user_id, language)
            if not profile:
                profile = CodingStyleProfile(user_id=user_id, language=language)
            self.user_profiles[profile_key] = profile
        
        return self.user_profiles[profile_key]
    
    def _update_style_profile(self, profile: CodingStyleProfile, analysis: Dict[str, Any]):
        """Update style profile based on analysis"""
        if not analysis:
            return
        
        # Update naming conventions
        if naming_patterns := analysis.get('naming_patterns'):
            if functions := naming_patterns.get('functions'):
                profile.function_naming = self.style_analyzer._detect_naming_pattern(functions)
            if classes := naming_patterns.get('classes'):
                profile.class_naming = self.style_analyzer._detect_naming_pattern(classes)
            if variables := naming_patterns.get('variables'):
                profile.variable_naming = self.style_analyzer._detect_naming_pattern(variables)
        
        # Update formatting preferences
        if formatting := analysis.get('formatting_patterns'):
            if indentation := formatting.get('indentation'):
                profile.indentation = indentation
            if avg_line_length := formatting.get('average_line_length'):
                profile.line_length = int(avg_line_length)
        
        # Update documentation patterns
        if docs := analysis.get('documentation_patterns'):
            if comment_ratio := docs.get('comment_ratio'):
                profile.comment_frequency = comment_ratio
        
        # Update confidence scores
        profile.confidence_scores['naming'] = min(1.0, profile.samples_analyzed / 10)
        profile.confidence_scores['formatting'] = min(1.0, profile.samples_analyzed / 5)
    
    def _generate_style_suggestions(self, profile: CodingStyleProfile, context: Dict[str, Any]) -> List[str]:
        """Generate personalized style suggestions"""
        suggestions = []
        
        code = context.get('code', '')
        if not code:
            return suggestions
        
        # Check naming conventions
        if profile.function_naming == 'snake_case':
            if re.search(r'def\s+[a-z][a-zA-Z0-9]*\s*\(', code):
                suggestions.append(f"Consider using {profile.function_naming} for function names")
        
        # Check indentation
        if profile.indentation == '4_spaces':
            if re.search(r'^\s{2}[^ ]', code, re.MULTILINE):
                suggestions.append(f"Your preferred indentation is {profile.indentation}")
        
        # Check line length
        long_lines = [line for line in code.split('\n') if len(line) > profile.line_length]
        if long_lines:
            suggestions.append(f"Consider breaking lines longer than {profile.line_length} characters")
        
        return suggestions
    
    def _generate_commit_template(self, pattern: CommitPattern) -> str:
        """Generate personalized commit message template"""
        if pattern.message_format == 'conventional':
            most_common_prefix = pattern.common_prefixes[0] if pattern.common_prefixes else 'feat'
            
            if pattern.uses_scope:
                return f"{most_common_prefix}(scope): description"
            else:
                return f"{most_common_prefix}: description"
        
        return "Brief description of changes"
    
    def _generate_debugging_hints(self, pattern: BugPattern, context: Dict[str, Any]) -> List[str]:
        """Generate personalized debugging hints"""
        hints = []
        
        error_msg = context.get('error_message', '').lower()
        
        # Check against user's common error patterns
        for bug_type in pattern.frequent_bug_types[-5:]:  # Last 5 types
            if bug_type in error_msg:
                hints.append(f"You've encountered {bug_type} before. Check your recent solutions.")
        
        # Suggest preferred debugging tools
        if pattern.preferred_debugging_tools:
            tools = ', '.join(pattern.preferred_debugging_tools[:3])
            hints.append(f"Consider using your preferred tools: {tools}")
        
        return hints
    
    def _save_user_profile(self, user_id: str, profile: CodingStyleProfile):
        """Save user profile to disk"""
        filename = os.path.join(self.storage_path, f"{user_id}_{profile.language}_style.pkl")
        with open(filename, 'wb') as f:
            pickle.dump(profile, f)
    
    def _load_style_profile(self, user_id: str, language: str) -> Optional[CodingStyleProfile]:
        """Load user profile from disk"""
        filename = os.path.join(self.storage_path, f"{user_id}_{language}_style.pkl")
        try:
            with open(filename, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return None
    
    def _save_commit_pattern(self, user_id: str, pattern: CommitPattern):
        """Save commit pattern to disk"""
        filename = os.path.join(self.storage_path, f"{user_id}_commits.pkl")
        with open(filename, 'wb') as f:
            pickle.dump(pattern, f)
    
    def _load_commit_pattern(self, user_id: str) -> Optional[CommitPattern]:
        """Load commit pattern from disk"""
        filename = os.path.join(self.storage_path, f"{user_id}_commits.pkl")
        try:
            with open(filename, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return None
    
    def _save_bug_pattern(self, user_id: str, pattern: BugPattern):
        """Save bug pattern to disk"""
        filename = os.path.join(self.storage_path, f"{user_id}_bugs.pkl")
        with open(filename, 'wb') as f:
            pickle.dump(pattern, f)
    
    def _load_bug_pattern(self, user_id: str) -> Optional[BugPattern]:
        """Load bug pattern from disk"""
        filename = os.path.join(self.storage_path, f"{user_id}_bugs.pkl")
        try:
            with open(filename, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return None
    
    def _get_or_create_commit_pattern(self, user_id: str) -> CommitPattern:
        """Get or create commit pattern"""
        pattern = self._load_commit_pattern(user_id)
        if not pattern:
            pattern = CommitPattern(user_id=user_id)
        return pattern
    
    def _get_or_create_bug_pattern(self, user_id: str) -> BugPattern:
        """Get or create bug pattern"""
        pattern = self._load_bug_pattern(user_id)
        if not pattern:
            pattern = BugPattern(user_id=user_id)
        return pattern
    
    def _update_commit_pattern(self, pattern: CommitPattern, analysis: Dict[str, Any]):
        """Update commit pattern based on analysis"""
        if not analysis:
            return
        
        if msg_patterns := analysis.get('message_patterns'):
            pattern.average_length = int(msg_patterns.get('average_length', pattern.average_length))
            pattern.uses_emoji = msg_patterns.get('emoji_ratio', 0) > 0.1
            pattern.uses_scope = msg_patterns.get('scope_ratio', 0) > 0.5
            
            if msg_patterns.get('conventional_ratio', 0) > 0.5:
                pattern.message_format = 'conventional'
            
            # Update common prefixes and keywords
            if common_prefixes := msg_patterns.get('common_prefixes'):
                pattern.common_prefixes = [prefix for prefix, count in common_prefixes.most_common(5)]
            
            if common_keywords := msg_patterns.get('common_keywords'):
                pattern.common_keywords = [keyword for keyword, count in common_keywords.most_common(10)]
        
        if temporal_patterns := analysis.get('temporal_patterns'):
            pattern.commits_per_day = temporal_patterns.get('commits_per_day', pattern.commits_per_day)
            if preferred_hours := temporal_patterns.get('preferred_hours'):
                pattern.preferred_commit_times = [hour for hour, count in preferred_hours]
        
        if change_patterns := analysis.get('change_patterns'):
            pattern.files_per_commit = change_patterns.get('files_per_commit', pattern.files_per_commit)
    
    def _learn_from_interaction(self, interaction: InteractionEvent):
        """Learn from user interaction"""
        # Update preferences based on positive/negative feedback
        if interaction.satisfaction_score and interaction.satisfaction_score > 0.7:
            # Positive feedback - reinforce patterns
            if interaction.event_type == 'code_review':
                # User liked the review style
                pass
            elif interaction.event_type == 'debug_request':
                # User found debugging helpful
                pass
        elif interaction.satisfaction_score and interaction.satisfaction_score < 0.3:
            # Negative feedback - adjust patterns
            pass

# Global personalization engine
personalization_engine = PersonalizationEngine()