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

  const loadExampleCode = () => {
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
    setCode(exampleCode);
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

  return (
    <div className="min-h-screen bg-[#111418] text-white">
      <div className="px-40 flex flex-1 justify-center py-5">
        <div className="layout-content-container flex flex-col max-w-[960px] flex-1">
          <div className="flex flex-wrap justify-between gap-3 p-4">
            <p className="text-white tracking-light text-[32px] font-bold leading-tight min-w-72">Code Analysis</p>
          </div>

          {/* Language Selection */}
          <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
            <label className="flex flex-col min-w-40 flex-1">
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
              <input
                type="text"
                value={filePath}
                onChange={(e) => setFilePath(e.target.value)}
                placeholder="Optional file path"
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-white focus:outline-0 focus:ring-0 border border-[#3b4754] bg-[#1b2127] focus:border-[#3b4754] h-14 placeholder:text-[#9cabba] p-[15px] text-base font-normal leading-normal"
              />
            </label>
          </div>

          {/* Code Input */}
          <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
            <label className="flex flex-col min-w-40 flex-1">
              <textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="Enter your code here"
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-white focus:outline-0 focus:ring-0 border border-[#3b4754] bg-[#1b2127] focus:border-[#3b4754] min-h-36 placeholder:text-[#9cabba] p-[15px] text-base font-normal leading-normal"
              />
            </label>
          </div>

          {/* Load Example Button */}
          <div className="flex px-4 py-3 justify-start">
            <button
              onClick={loadExampleCode}
              className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-[#283039] text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-[#3b4754] transition-colors"
            >
              <span className="truncate">Load Example</span>
            </button>
          </div>

          {/* Detect Button */}
          <div className="flex px-4 py-3 justify-start">
            <button
              onClick={handleDetectSmells}
              disabled={loading || !code.trim()}
              className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-12 px-5 bg-[#0c7ff2] text-white text-base font-bold leading-normal tracking-[0.015em] hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? (
                <LoadingSpinner size="sm" text="" />
              ) : (
                <span className="truncate">Detect Code Smells</span>
              )}
            </button>
          </div>

          {/* Error Display */}
          {error && (
            <div className="px-4 py-3">
              <ErrorMessage error={error} />
            </div>
          )}

          {/* Summary Section */}
          {smellResults && (
            <>
              <h2 className="text-white text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">Summary</h2>
              <div className="flex flex-wrap gap-4 p-4">
                <div className="flex min-w-[158px] flex-1 flex-col gap-2 rounded-lg p-6 bg-[#283039]">
                  <p className="text-white text-base font-medium leading-normal">Total Issues</p>
                  <p className="text-white tracking-light text-2xl font-bold leading-tight">{totalSmells}</p>
                  <p className="text-[#0bda5b] text-base font-medium leading-normal">+10%</p>
                </div>
                <div className="flex min-w-[158px] flex-1 flex-col gap-2 rounded-lg p-6 bg-[#283039]">
                  <p className="text-white text-base font-medium leading-normal">Quality Score</p>
                  <p className="text-white tracking-light text-2xl font-bold leading-tight">{smellSummary.quality_score || 85}/100</p>
                  <p className="text-[#fa6238] text-base font-medium leading-normal">-5%</p>
                </div>
                <div className="flex min-w-[158px] flex-1 flex-col gap-2 rounded-lg p-6 bg-[#283039]">
                  <p className="text-white text-base font-medium leading-normal">Top Recommendations</p>
                  <p className="text-white tracking-light text-2xl font-bold leading-tight">
                    {smellSummary.recommendations?.slice(0, 3).join(', ') || '1. Refactor long methods 2. Reduce code duplication 3. Improve variable naming'}
                  </p>
                  <p className="text-[#0bda5b] text-base font-medium leading-normal">+20%</p>
                </div>
              </div>

              {/* Results Visualization */}
              <h2 className="text-white text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">Results</h2>
              <SmellVisualization smells={smellResults.smells} />

              {/* Filters */}
              <h3 className="text-white text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">Filter</h3>
              <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
                <label className="flex flex-col min-w-40 flex-1">
                  <select
                    value={filterSeverity}
                    onChange={(e) => setFilterSeverity(e.target.value)}
                    className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-white focus:outline-0 focus:ring-0 border border-[#3b4754] bg-[#1b2127] focus:border-[#3b4754] h-14 placeholder:text-[#9cabba] p-[15px] text-base font-normal leading-normal"
                    style={{backgroundImage: "url('data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 width=%2724px%27 height=%2724px%27 fill=%27rgb(156,171,186)%27 viewBox=%270 0 256 256%27%3e%3cpath d=%27M181.66,170.34a8,8,0,0,1,0,11.32l-48,48a8,8,0,0,1-11.32,0l-48-48a8,8,0,0,1,11.32-11.32L128,212.69l42.34-42.35A8,8,0,0,1,181.66,170.34Zm-96-84.68L128,43.31l42.34,42.35a8,8,0,0,0,11.32-11.32l-48-48a8,8,0,0,0-11.32,0l-48,48A8,8,0,0,0,85.66,85.66Z%27%3e%3c/path%3e%3c/svg%3e')", backgroundRepeat: 'no-repeat', backgroundPosition: 'right 15px center'}}
                  >
                    <option value="all">All Severities</option>
                    {severities.map(severity => (
                      <option key={severity} value={severity}>{severity}</option>
                    ))}
                  </select>
                </label>
              </div>

              <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
                <label className="flex flex-col min-w-40 flex-1">
                  <select
                    value={filterCategory}
                    onChange={(e) => setFilterCategory(e.target.value)}
                    className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-white focus:outline-0 focus:ring-0 border border-[#3b4754] bg-[#1b2127] focus:border-[#3b4754] h-14 placeholder:text-[#9cabba] p-[15px] text-base font-normal leading-normal"
                    style={{backgroundImage: "url('data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 width=%2724px%27 height=%2724px%27 fill=%27rgb(156,171,186)%27 viewBox=%270 0 256 256%27%3e%3cpath d=%27M181.66,170.34a8,8,0,0,1,0,11.32l-48,48a8,8,0,0,1-11.32,0l-48-48a8,8,0,0,1,11.32-11.32L128,212.69l42.34-42.35A8,8,0,0,1,181.66,170.34Zm-96-84.68L128,43.31l42.34,42.35a8,8,0,0,0,11.32-11.32l-48-48a8,8,0,0,0-11.32,0l-48,48A8,8,0,0,0,85.66,85.66Z%27%3e%3c/path%3e%3c/svg%3e')", backgroundRepeat: 'no-repeat', backgroundPosition: 'right 15px center'}}
                  >
                    <option value="all">All Categories</option>
                    {categories.map(category => (
                      <option key={category} value={category}>{category}</option>
                    ))}
                  </select>
                </label>
              </div>

              {/* Search */}
              <div className="px-4 py-3">
                <label className="flex flex-col min-w-40 h-12 w-full">
                  <div className="flex w-full flex-1 items-stretch rounded-lg h-full">
                    <div className="text-[#9cabba] flex border-none bg-[#283039] items-center justify-center pl-4 rounded-l-lg border-r-0">
                      <Search className="w-6 h-6" />
                    </div>
                    <input
                      type="text"
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      placeholder="Search code smells"
                      className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-white focus:outline-0 focus:ring-0 border-none bg-[#283039] focus:border-none h-full placeholder:text-[#9cabba] px-4 rounded-l-none border-l-0 pl-2 text-base font-normal leading-normal"
                    />
                  </div>
                </label>
              </div>

              {/* Code Smells List */}
              <h3 className="text-white text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">Code Smells</h3>
              <div className="space-y-4 px-4">
                {filteredSmells.length > 0 ? (
                  filteredSmells.map((smell, index) => (
                    <SmellCard key={index} smell={smell} />
                  ))
                ) : (
                  <div className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-8 text-center">
                    <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-4" />
                    <h3 className="text-lg font-semibold text-white mb-2">
                      No Issues Found
                    </h3>
                    <p className="text-[#9cabba]">
                      {totalSmells === 0 
                        ? "Great! Your code looks clean." 
                        : "No issues match your current filters."}
                    </p>
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default CodeSmellDashboard;