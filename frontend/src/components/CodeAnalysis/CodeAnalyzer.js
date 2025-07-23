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
    <div className="min-h-screen bg-[#111418] text-white">
      <div className="gap-1 px-6 flex flex-1 justify-center py-5">
        <div className="layout-content-container flex flex-col max-w-[920px] flex-1">
          <h2 className="text-white text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">Code Analysis</h2>
          
          {/* Analysis Type Selection */}
          <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
            <label className="flex flex-col min-w-40 flex-1">
              <p className="text-white text-base font-medium leading-normal pb-2">Analysis Type</p>
              <select
                value={analysisType}
                onChange={(e) => setAnalysisType(e.target.value)}
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-white focus:outline-0 focus:ring-0 border border-[#3b4754] bg-[#1b2127] focus:border-[#3b4754] h-14 placeholder:text-[#9cabba] p-[15px] text-base font-normal leading-normal"
                style={{backgroundImage: "url('data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 width=%2724px%27 height=%2724px%27 fill=%27rgb(156,171,186)%27 viewBox=%270 0 256 256%27%3e%3cpath d=%27M181.66,170.34a8,8,0,0,1,0,11.32l-48,48a8,8,0,0,1-11.32,0l-48-48a8,8,0,0,1,11.32-11.32L128,212.69l42.34-42.35A8,8,0,0,1,181.66,170.34Zm-96-84.68L128,43.31l42.34,42.35a8,8,0,0,0,11.32-11.32l-48-48a8,8,0,0,0-11.32,0l-48,48A8,8,0,0,0,85.66,85.66Z%27%3e%3c/path%3e%3c/svg%3e')", backgroundRepeat: 'no-repeat', backgroundPosition: 'right 15px center'}}
              >
                {analysisTypes.map(type => (
                  <option key={type.value} value={type.value}>{type.label}</option>
                ))}
              </select>
            </label>
          </div>

          {/* Language Selection */}
          <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
            <label className="flex flex-col min-w-40 flex-1">
              <p className="text-white text-base font-medium leading-normal pb-2">Language</p>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-white focus:outline-0 focus:ring-0 border border-[#3b4754] bg-[#1b2127] focus:border-[#3b4754] h-14 placeholder:text-[#9cabba] p-[15px] text-base font-normal leading-normal"
                style={{backgroundImage: "url('data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 width=%2724px%27 height=%2724px%27 fill=%27rgb(156,171,186)%27 viewBox=%270 0 256 256%27%3e%3cpath d=%27M181.66,170.34a8,8,0,0,1,0,11.32l-48,48a8,8,0,0,1-11.32,0l-48-48a8,8,0,0,1,11.32-11.32L128,212.69l42.34-42.35A8,8,0,0,1,181.66,170.34Zm-96-84.68L128,43.31l42.34,42.35a8,8,0,0,0,11.32-11.32l-48-48a8,8,0,0,0-11.32,0l-48,48A8,8,0,0,0,85.66,85.66Z%27%3e%3c/path%3e%3c/svg%3e')", backgroundRepeat: 'no-repeat', backgroundPosition: 'right 15px center'}}
              >
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
                <option value="java">Java</option>
                <option value="typescript">TypeScript</option>
              </select>
            </label>
          </div>

          {/* File Path */}
          <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
            <label className="flex flex-col min-w-40 flex-1">
              <p className="text-white text-base font-medium leading-normal pb-2">File Path</p>
              <input
                type="text"
                value={filePath}
                onChange={(e) => setFilePath(e.target.value)}
                placeholder="Enter file path"
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-white focus:outline-0 focus:ring-0 border border-[#3b4754] bg-[#1b2127] focus:border-[#3b4754] h-14 placeholder:text-[#9cabba] p-[15px] text-base font-normal leading-normal"
              />
            </label>
          </div>

          {/* Code Editor */}
          <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
            <label className="flex flex-col min-w-40 flex-1">
              <p className="text-white text-base font-medium leading-normal pb-2">Code Editor</p>
              <textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="Paste your code here"
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-white focus:outline-0 focus:ring-0 border border-[#3b4754] bg-[#1b2127] focus:border-[#3b4754] min-h-36 placeholder:text-[#9cabba] p-[15px] text-base font-normal leading-normal"
              />
            </label>
          </div>

          {/* Analyze Button */}
          <div className="flex px-4 py-3 justify-end">
            <button
              onClick={handleAnalyze}
              disabled={loading || !code.trim()}
              className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-12 px-5 bg-[#0c7ff2] text-white text-base font-bold leading-normal tracking-[0.015em] hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? (
                <LoadingSpinner size="sm" text="" />
              ) : (
                <span className="truncate">Analyze Code</span>
              )}
            </button>
          </div>

          {/* Error Display */}
          {error && (
            <div className="px-4 py-3">
              <ErrorMessage error={error} />
            </div>
          )}
        </div>

        {/* Results Section */}
        <div className="layout-content-container flex flex-col w-[360px]">
          <h2 className="text-white text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">Analysis Results</h2>
          <div className="flex flex-col px-4 py-6">
            {!analysisResults && !loading && (
              <div className="flex flex-col items-center gap-6">
                <div
                  className="bg-center bg-no-repeat aspect-video bg-cover rounded-lg w-full max-w-[360px]"
                  style={{backgroundImage: "url('https://images.unsplash.com/photo-1744324472890-d4cac1650e2e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzl8MHwxfHNlYXJjaHwyfHxnZW9tZXRyaWMlMjBicmFpbnxlbnwwfHx8fDE3NTMyOTA4NjF8MA&ixlib=rb-4.1.0&q=85')"}}
                />
                <div className="flex max-w-[480px] flex-col items-center gap-2">
                  <p className="text-white text-lg font-bold leading-tight tracking-[-0.015em] max-w-[480px] text-center">Ready to Analyze</p>
                  <p className="text-white text-sm font-normal leading-normal max-w-[480px] text-center">Paste your code or upload a file to start the analysis.</p>
                </div>
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