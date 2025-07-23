import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { 
  CheckCircle, 
  AlertTriangle, 
  XCircle, 
  Info, 
  TrendingUp, 
  Target,
  Code2,
  GitBranch,
  Layers
} from 'lucide-react';

const AnalysisResults = ({ results }) => {
  if (!results) return null;

  const {
    ast_analysis = {},
    code_smells = [],
    smell_summary = {},
    success = true,
    language = 'unknown',
    file_path = ''
  } = results;

  // Process code smells for visualization
  const smellsByCategory = code_smells.reduce((acc, smell) => {
    const category = smell.category || 'other';
    acc[category] = (acc[category] || 0) + 1;
    return acc;
  }, {});

  const smellsBySeverity = code_smells.reduce((acc, smell) => {
    const severity = smell.severity || 'low';
    acc[severity] = (acc[severity] || 0) + 1;
    return acc;
  }, {});

  const categoryChartData = Object.entries(smellsByCategory).map(([category, count]) => ({
    name: category,
    value: count,
    color: getCategoryColor(category)
  }));

  const severityChartData = Object.entries(smellsBySeverity).map(([severity, count]) => ({
    name: severity,
    count,
    color: getSeverityColor(severity)
  }));

  const qualityScore = smell_summary.quality_score || 0;
  const totalSmells = code_smells.length;

  return (
    <div className="space-y-6">
      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-gradient-to-r from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-blue-700 dark:text-blue-300">Quality Score</p>
              <p className="text-2xl font-bold text-blue-900 dark:text-blue-100">{qualityScore}/100</p>
            </div>
            <Target className="w-8 h-8 text-blue-500" />
          </div>
        </div>

        <div className="bg-gradient-to-r from-orange-50 to-orange-100 dark:from-orange-900/20 dark:to-orange-800/20 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-orange-700 dark:text-orange-300">Total Issues</p>
              <p className="text-2xl font-bold text-orange-900 dark:text-orange-100">{totalSmells}</p>
            </div>
            <AlertTriangle className="w-8 h-8 text-orange-500" />
          </div>
        </div>

        <div className="bg-gradient-to-r from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-green-700 dark:text-green-300">Language</p>
              <p className="text-2xl font-bold text-green-900 dark:text-green-100">{language}</p>
            </div>
            <Code2 className="w-8 h-8 text-green-500" />
          </div>
        </div>
      </div>

      {/* AST Analysis */}
      {ast_analysis && Object.keys(ast_analysis).length > 0 && (
        <div className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center space-x-2">
            <GitBranch className="w-5 h-5" />
            <span>Code Structure Analysis</span>
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {ast_analysis.functions && (
              <div className="bg-white dark:bg-gray-800 rounded-lg p-4">
                <h4 className="font-medium text-gray-900 dark:text-white mb-2">Functions</h4>
                <p className="text-2xl font-bold text-blue-600">{ast_analysis.functions.length}</p>
              </div>
            )}
            
            {ast_analysis.classes && (
              <div className="bg-white dark:bg-gray-800 rounded-lg p-4">
                <h4 className="font-medium text-gray-900 dark:text-white mb-2">Classes</h4>
                <p className="text-2xl font-bold text-purple-600">{ast_analysis.classes.length}</p>
              </div>
            )}
            
            {ast_analysis.complexity && (
              <div className="bg-white dark:bg-gray-800 rounded-lg p-4">
                <h4 className="font-medium text-gray-900 dark:text-white mb-2">Complexity</h4>
                <p className="text-2xl font-bold text-orange-600">{ast_analysis.complexity}</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Code Smells Visualization */}
      {totalSmells > 0 && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Severity Distribution */}
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Issues by Severity
            </h3>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={severityChartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#3B82F6" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Category Distribution */}
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Issues by Category
            </h3>
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie
                  data={categoryChartData}
                  cx="50%"
                  cy="50%"
                  innerRadius={40}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {categoryChartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Code Smells List */}
      {totalSmells > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center space-x-2">
            <Layers className="w-5 h-5" />
            <span>Detected Issues</span>
          </h3>
          
          <div className="space-y-3">
            {code_smells.map((smell, index) => (
              <div key={index} className="border border-gray-200 dark:border-gray-600 rounded-lg p-4">
                <div className="flex items-start space-x-3">
                  <div className={`p-1 rounded-full ${getSeverityBgColor(smell.severity)}`}>
                    {getSeverityIcon(smell.severity)}
                  </div>
                  
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <h4 className="font-medium text-gray-900 dark:text-white">
                        {smell.smell_type || 'Code Issue'}
                      </h4>
                      <span className={`px-2 py-1 text-xs rounded-full ${getSeverityBadgeColor(smell.severity)}`}>
                        {smell.severity}
                      </span>
                    </div>
                    
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                      {smell.description}
                    </p>
                    
                    <div className="flex items-center space-x-4 mt-2 text-xs text-gray-500 dark:text-gray-400">
                      <span>Line: {smell.line_number}</span>
                      <span>Category: {smell.category}</span>
                      {smell.confidence && (
                        <span>Confidence: {(smell.confidence * 100).toFixed(0)}%</span>
                      )}
                    </div>
                    
                    {smell.suggestion && (
                      <div className="mt-3 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                        <p className="text-sm text-blue-800 dark:text-blue-200">
                          <strong>Suggestion:</strong> {smell.suggestion}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* No Issues Found */}
      {totalSmells === 0 && success && (
        <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-6 text-center">
          <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-green-800 dark:text-green-200 mb-2">
            Great Job!
          </h3>
          <p className="text-green-600 dark:text-green-400">
            No code issues detected in your analysis. Your code looks clean!
          </p>
        </div>
      )}
    </div>
  );
};

// Helper functions
const getCategoryColor = (category) => {
  const colors = {
    security: '#EF4444',
    complexity: '#F59E0B',
    maintainability: '#8B5CF6',
    performance: '#10B981',
    style: '#3B82F6',
    other: '#6B7280'
  };
  return colors[category] || colors.other;
};

const getSeverityColor = (severity) => {
  const colors = {
    critical: '#DC2626',
    high: '#EA580C',
    medium: '#D97706',
    low: '#65A30D'
  };
  return colors[severity] || colors.low;
};

const getSeverityIcon = (severity) => {
  const iconProps = { className: 'w-4 h-4 text-white' };
  
  switch (severity) {
    case 'critical':
      return <XCircle {...iconProps} />;
    case 'high':
      return <AlertTriangle {...iconProps} />;
    case 'medium':
      return <AlertTriangle {...iconProps} />;
    case 'low':
      return <Info {...iconProps} />;
    default:
      return <Info {...iconProps} />;
  }
};

const getSeverityBgColor = (severity) => {
  const colors = {
    critical: 'bg-red-500',
    high: 'bg-orange-500',
    medium: 'bg-yellow-500',
    low: 'bg-blue-500'
  };
  return colors[severity] || colors.low;
};

const getSeverityBadgeColor = (severity) => {
  const colors = {
    critical: 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-300',
    high: 'bg-orange-100 text-orange-800 dark:bg-orange-900/20 dark:text-orange-300',
    medium: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-300',
    low: 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-300'
  };
  return colors[severity] || colors.low;
};

export default AnalysisResults;