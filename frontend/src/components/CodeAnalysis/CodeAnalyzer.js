import React, { useState } from 'react';
import CodeInput from './CodeInput';
import AnalysisResults from './AnalysisResults';
import { useApiCall } from '../../hooks/useApi';
import { apiEndpoints } from '../../utils/api';
import LoadingSpinner from '../Common/LoadingSpinner';
import ErrorMessage from '../Common/ErrorMessage';
import { Play, FileText, Zap, Brain } from 'lucide-react';

const CodeAnalyzer = () => {
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [filePath, setFilePath] = useState('');
  const [analysisResults, setAnalysisResults] = useState(null);
  const [analysisType, setAnalysisType] = useState('comprehensive');
  
  const { execute: analyzeCode, loading, error } = useApiCall();

  const handleAnalyze = async () => {
    if (!code.trim()) {
      return;
    }

    const analysisData = {
      code: code.trim(),
      language,
      file_path: filePath || `temp_file.${language}`,
      analysis_type: analysisType,
      user_id: 'demo_user',
      include_smells: true,
      include_complexity: true,
      include_dependencies: true
    };

    try {
      const result = await analyzeCode(() => apiEndpoints.analyzeCode(analysisData));
      setAnalysisResults(result);
    } catch (err) {
      console.error('Analysis failed:', err);
    }
  };

  const analysisTypes = [
    { value: 'comprehensive', label: 'Comprehensive', icon: Brain },
    { value: 'quick', label: 'Quick', icon: Zap },
    { value: 'security', label: 'Security Focus', icon: FileText },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Code Analysis
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Get AI-powered insights about your code quality, complexity, and potential improvements.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Section */}
        <div className="space-y-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              Code Input
            </h2>
            
            {/* Analysis Type Selection */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Analysis Type
              </label>
              <div className="grid grid-cols-3 gap-2">
                {analysisTypes.map((type) => {
                  const Icon = type.icon;
                  return (
                    <button
                      key={type.value}
                      onClick={() => setAnalysisType(type.value)}
                      className={`p-3 rounded-lg border-2 transition-all ${
                        analysisType === type.value
                          ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300'
                          : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                      }`}
                    >
                      <Icon className="w-4 h-4 mx-auto mb-1" />
                      <span className="text-xs font-medium">{type.label}</span>
                    </button>
                  );
                })}
              </div>
            </div>

            <CodeInput
              code={code}
              setCode={setCode}
              language={language}
              setLanguage={setLanguage}
              filePath={filePath}
              setFilePath={setFilePath}
            />

            <div className="mt-6">
              <button
                onClick={handleAnalyze}
                disabled={loading || !code.trim()}
                className="w-full flex items-center justify-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white rounded-lg transition-colors"
              >
                {loading ? (
                  <LoadingSpinner size="sm" text="" />
                ) : (
                  <>
                    <Play className="w-4 h-4" />
                    <span>Analyze Code</span>
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Error Display */}
          {error && (
            <ErrorMessage 
              error={error} 
              onClose={() => setError(null)} 
            />
          )}
        </div>

        {/* Results Section */}
        <div>
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              Analysis Results
            </h2>
            
            {!analysisResults && !loading && (
              <div className="text-center py-12">
                <Brain className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                  Ready to Analyze
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  Enter your code and click "Analyze Code" to get AI-powered insights.
                </p>
              </div>
            )}

            {loading && (
              <div className="text-center py-12">
                <LoadingSpinner size="lg" text="Analyzing your code..." />
              </div>
            )}

            {analysisResults && (
              <AnalysisResults results={analysisResults} />
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CodeAnalyzer;