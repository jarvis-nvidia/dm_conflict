import React, { useState } from 'react';
import { useApiCall } from '../../hooks/useApi';
import { apiEndpoints } from '../../utils/api';
import LoadingSpinner from '../Common/LoadingSpinner';
import ErrorMessage from '../Common/ErrorMessage';
import SmellCard from './SmellCard';
import SmellVisualization from './SmellVisualization';
import { 
  Search, 
  Filter, 
  Download, 
  RefreshCw,
  AlertTriangle,
  CheckCircle,
  TrendingUp,
  BarChart3
} from 'lucide-react';

const CodeSmellDashboard = () => {
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [filePath, setFilePath] = useState('');
  const [smellResults, setSmellResults] = useState(null);
  const [filterSeverity, setFilterSeverity] = useState('all');
  const [filterCategory, setFilterCategory] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  
  const { execute: detectSmells, loading, error } = useApiCall();

  const handleDetectSmells = async () => {
    if (!code.trim()) return;

    const smellData = {
      code: code.trim(),
      file_path: filePath || `temp_file.${language}`,
      language,
      user_id: 'demo_user'
    };

    try {
      const result = await detectSmells(() => apiEndpoints.detectCodeSmells(smellData));
      setSmellResults(result);
    } catch (err) {
      console.error('Smell detection failed:', err);
    }
  };

  const filteredSmells = smellResults?.smells?.filter(smell => {
    const matchesSeverity = filterSeverity === 'all' || smell.severity === filterSeverity;
    const matchesCategory = filterCategory === 'all' || smell.category === filterCategory;
    const matchesSearch = searchTerm === '' || 
      smell.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      smell.smell_type?.toLowerCase().includes(searchTerm.toLowerCase());
    
    return matchesSeverity && matchesCategory && matchesSearch;
  }) || [];

  const smellSummary = smellResults?.summary || {};
  const totalSmells = smellResults?.smells?.length || 0;

  // Get unique categories and severities for filters
  const categories = [...new Set(smellResults?.smells?.map(s => s.category).filter(Boolean) || [])];
  const severities = [...new Set(smellResults?.smells?.map(s => s.severity).filter(Boolean) || [])];

  const exampleCode = `def calculate_fibonacci(n):
    if n <= 1:
        return n
    else:
        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

class Calculator:
    def __init__(self):
        self.result = 0
    
    def add(self, a, b):
        result = a + b
        return result
    
    def divide(self, a, b):
        return a / b  # Potential division by zero
    
    def complex_function(self, x, y, z, w, v, u):  # Too many parameters
        if x > 0:
            if y > 0:
                if z > 0:
                    if w > 0:
                        if v > 0:
                            return u  # Deep nesting
        return 0

# Hardcoded sensitive data
PASSWORD = "admin123"
API_KEY = "sk-1234567890abcdef"

def unsafe_eval(user_input):
    return eval(user_input)  # Dangerous function`;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Code Smell Detection
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Detect and analyze code smells to improve your code quality and maintainability.
        </p>
      </div>

      {/* Input Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
        <div className="lg:col-span-2">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              Code Input
            </h2>
            
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Language
                  </label>
                  <select
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="python">Python</option>
                    <option value="javascript">JavaScript</option>
                    <option value="java">Java</option>
                    <option value="typescript">TypeScript</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    File Path
                  </label>
                  <input
                    type="text"
                    value={filePath}
                    onChange={(e) => setFilePath(e.target.value)}
                    placeholder="e.g., src/main.py"
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-2">
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    Code
                  </label>
                  <button
                    onClick={() => setCode(exampleCode)}
                    className="text-sm text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300"
                  >
                    Load Example
                  </button>
                </div>
                <textarea
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  placeholder="Paste your code here..."
                  className="w-full h-64 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-mono text-sm resize-none"
                />
              </div>

              <button
                onClick={handleDetectSmells}
                disabled={loading || !code.trim()}
                className="w-full flex items-center justify-center space-x-2 px-4 py-2 bg-red-600 hover:bg-red-700 disabled:bg-gray-400 text-white rounded-lg transition-colors"
              >
                {loading ? (
                  <LoadingSpinner size="sm" text="" />
                ) : (
                  <>
                    <Search className="w-4 h-4" />
                    <span>Detect Code Smells</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Summary Card */}
        <div className="space-y-4">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Detection Summary
            </h3>
            
            {smellResults ? (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-400">Total Issues</span>
                  <span className="text-lg font-semibold text-gray-900 dark:text-white">{totalSmells}</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-400">Quality Score</span>
                  <span className="text-lg font-semibold text-gray-900 dark:text-white">
                    {smellSummary.quality_score || 'N/A'}/100
                  </span>
                </div>
                
                <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
                  <div className="flex items-center space-x-2 mb-2">
                    <TrendingUp className="w-4 h-4 text-blue-500" />
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                      Recommendations
                    </span>
                  </div>
                  <ul className="text-xs text-gray-600 dark:text-gray-400 space-y-1">
                    {smellSummary.recommendations?.slice(0, 3).map((rec, idx) => (
                      <li key={idx}>• {rec}</li>
                    )) || <li>No recommendations available</li>}
                  </ul>
                </div>
              </div>
            ) : (
              <div className="text-center py-8">
                <AlertTriangle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600 dark:text-gray-400">
                  Run detection to see results
                </p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Error Display */}
      {error && <ErrorMessage error={error} />}

      {/* Results Section */}
      {smellResults && (
        <div className="space-y-6">
          {/* Visualization */}
          <SmellVisualization smells={smellResults.smells} />

          {/* Filters */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <div className="flex flex-wrap items-center gap-4 mb-4">
              <div className="flex items-center space-x-2">
                <Filter className="w-4 h-4 text-gray-500" />
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Filters:</span>
              </div>
              
              <select
                value={filterSeverity}
                onChange={(e) => setFilterSeverity(e.target.value)}
                className="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-sm"
              >
                <option value="all">All Severities</option>
                {severities.map(severity => (
                  <option key={severity} value={severity}>{severity}</option>
                ))}
              </select>
              
              <select
                value={filterCategory}
                onChange={(e) => setFilterCategory(e.target.value)}
                className="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-sm"
              >
                <option value="all">All Categories</option>
                {categories.map(category => (
                  <option key={category} value={category}>{category}</option>
                ))}
              </select>
              
              <div className="flex-1 max-w-md">
                <input
                  type="text"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder="Search smells..."
                  className="w-full px-3 py-1 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-sm"
                />
              </div>
            </div>

            <div className="text-sm text-gray-600 dark:text-gray-400">
              Showing {filteredSmells.length} of {totalSmells} issues
            </div>
          </div>

          {/* Smells List */}
          <div className="space-y-4">
            {filteredSmells.length > 0 ? (
              filteredSmells.map((smell, index) => (
                <SmellCard key={index} smell={smell} />
              ))
            ) : (
              <div className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-8 text-center">
                <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  No Issues Found
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  {totalSmells === 0 
                    ? "Great! Your code looks clean." 
                    : "No issues match your current filters."}
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default CodeSmellDashboard;