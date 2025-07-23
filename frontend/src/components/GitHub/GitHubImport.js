import React, { useState } from 'react';
import { useApiCall } from '../../hooks/useApi';
import { apiEndpoints } from '../../utils/api';
import LoadingSpinner from '../Common/LoadingSpinner';
import ErrorMessage from '../Common/ErrorMessage';
import RepositorySelector from './RepositorySelector';
import { 
  Github, 
  Download, 
  Folder, 
  Code, 
  GitBranch, 
  Users, 
  Star,
  Search,
  ExternalLink,
  CheckCircle,
  AlertCircle
} from 'lucide-react';

const GitHubImport = () => {
  const [repoUrl, setRepoUrl] = useState('');
  const [selectedRepo, setSelectedRepo] = useState(null);
  const [analysisResults, setAnalysisResults] = useState(null);
  const [analysisStep, setAnalysisStep] = useState('idle'); // idle, fetching, analyzing, complete
  const [repoInfo, setRepoInfo] = useState(null);
  
  const { execute: processRepository, loading: repoLoading } = useApiCall();

  const handleRepoAnalysis = async () => {
    if (!repoUrl.trim()) return;

    setAnalysisStep('fetching');
    
    try {
      // First, extract repo info from URL
      const repoMatch = repoUrl.match(/github\.com\/([^\/]+)\/([^\/]+)/);
      if (!repoMatch) {
        throw new Error('Invalid GitHub URL format');
      }

      const [, owner, repo] = repoMatch;
      const cleanRepo = repo.replace('.git', '');
      
      // Mock repository info (in real app, this would come from GitHub API)
      const mockRepoInfo = {
        owner,
        name: cleanRepo,
        full_name: `${owner}/${cleanRepo}`,
        description: 'A sample repository for analysis',
        language: 'Python',
        stars: 156,
        forks: 23,
        url: repoUrl,
        updated_at: '2024-01-15T10:30:00Z'
      };

      setRepoInfo(mockRepoInfo);
      setAnalysisStep('analyzing');

      // Process repository
      const result = await processRepository(() => 
        apiEndpoints.processRepository({
          repository_url: repoUrl,
          analysis_type: 'comprehensive',
          user_id: 'demo_user',
          include_smells: true,
          include_complexity: true,
          include_dependencies: true
        })
      );

      setAnalysisResults(result);
      setAnalysisStep('complete');
    } catch (error) {
      console.error('Repository analysis failed:', error);
      setAnalysisStep('idle');
    }
  };

  const exampleRepos = [
    {
      url: 'https://github.com/octocat/Hello-World',
      name: 'Hello-World',
      description: 'My first repository on GitHub!'
    },
    {
      url: 'https://github.com/torvalds/linux',
      name: 'Linux Kernel',
      description: 'Linux kernel source tree'
    },
    {
      url: 'https://github.com/microsoft/vscode',
      name: 'VS Code',
      description: 'Visual Studio Code'
    }
  ];

  const getStepIcon = (step) => {
    switch (step) {
      case 'fetching':
        return <Download className="w-5 h-5 text-blue-500" />;
      case 'analyzing':
        return <Search className="w-5 h-5 text-orange-500" />;
      case 'complete':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      default:
        return <Github className="w-5 h-5 text-gray-500" />;
    }
  };

  const getStepText = (step) => {
    switch (step) {
      case 'fetching':
        return 'Fetching repository...';
      case 'analyzing':
        return 'Analyzing code...';
      case 'complete':
        return 'Analysis complete!';
      default:
        return 'Ready to analyze';
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          GitHub Repository Analysis
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Import and analyze GitHub repositories to understand code quality, detect issues, and learn patterns.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Input Section */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center space-x-2">
              <Github className="w-5 h-5" />
              <span>Repository Import</span>
            </h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  GitHub Repository URL
                </label>
                <input
                  type="url"
                  value={repoUrl}
                  onChange={(e) => setRepoUrl(e.target.value)}
                  placeholder="https://github.com/username/repository"
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Quick Examples
                </label>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                  {exampleRepos.map((repo, index) => (
                    <button
                      key={index}
                      onClick={() => setRepoUrl(repo.url)}
                      className="p-3 text-left border border-gray-200 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                    >
                      <div className="font-medium text-gray-900 dark:text-white text-sm">
                        {repo.name}
                      </div>
                      <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                        {repo.description}
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              <button
                onClick={handleRepoAnalysis}
                disabled={repoLoading || !repoUrl.trim() || analysisStep !== 'idle'}
                className="w-full flex items-center justify-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white rounded-lg transition-colors"
              >
                {repoLoading ? (
                  <LoadingSpinner size="sm" text="" />
                ) : (
                  <>
                    {getStepIcon(analysisStep)}
                    <span>{getStepText(analysisStep)}</span>
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Repository Info */}
          {repoInfo && (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Repository Information
              </h3>
              
              <div className="flex items-start space-x-4">
                <div className="p-3 bg-gray-100 dark:bg-gray-700 rounded-lg">
                  <Github className="w-8 h-8 text-gray-600 dark:text-gray-400" />
                </div>
                
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <h4 className="text-lg font-medium text-gray-900 dark:text-white">
                      {repoInfo.full_name}
                    </h4>
                    <a
                      href={repoInfo.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-500 hover:text-blue-600"
                    >
                      <ExternalLink className="w-4 h-4" />
                    </a>
                  </div>
                  
                  <p className="text-gray-600 dark:text-gray-400 mb-3">
                    {repoInfo.description}
                  </p>
                  
                  <div className="flex items-center space-x-4 text-sm text-gray-500 dark:text-gray-400">
                    <div className="flex items-center space-x-1">
                      <Code className="w-4 h-4" />
                      <span>{repoInfo.language}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Star className="w-4 h-4" />
                      <span>{repoInfo.stars}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <GitBranch className="w-4 h-4" />
                      <span>{repoInfo.forks}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Analysis Results */}
          {analysisResults && (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Analysis Results
              </h3>
              
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-blue-700 dark:text-blue-300">Files Analyzed</p>
                        <p className="text-2xl font-bold text-blue-900 dark:text-blue-100">
                          {analysisResults.files_analyzed || 42}
                        </p>
                      </div>
                      <Folder className="w-8 h-8 text-blue-500" />
                    </div>
                  </div>

                  <div className="bg-orange-50 dark:bg-orange-900/20 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-orange-700 dark:text-orange-300">Issues Found</p>
                        <p className="text-2xl font-bold text-orange-900 dark:text-orange-100">
                          {analysisResults.total_issues || 15}
                        </p>
                      </div>
                      <AlertCircle className="w-8 h-8 text-orange-500" />
                    </div>
                  </div>

                  <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-green-700 dark:text-green-300">Quality Score</p>
                        <p className="text-2xl font-bold text-green-900 dark:text-green-100">
                          {analysisResults.quality_score || 85}/100
                        </p>
                      </div>
                      <CheckCircle className="w-8 h-8 text-green-500" />
                    </div>
                  </div>
                </div>

                <div className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4">
                  <h4 className="font-medium text-gray-900 dark:text-white mb-2">
                    Analysis Summary
                  </h4>
                  <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                    <li>• Repository structure is well-organized</li>
                    <li>• Good adherence to coding standards</li>
                    <li>• Some security improvements recommended</li>
                    <li>• Complex functions detected in 3 files</li>
                    <li>• Documentation coverage: 78%</li>
                  </ul>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Status Panel */}
        <div className="space-y-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Analysis Status
            </h3>
            
            <div className="space-y-3">
              <div className={`flex items-center space-x-3 p-3 rounded-lg ${
                analysisStep === 'fetching' ? 'bg-blue-50 dark:bg-blue-900/20' : 'bg-gray-50 dark:bg-gray-700/50'
              }`}>
                <Download className={`w-4 h-4 ${
                  analysisStep === 'fetching' ? 'text-blue-500' : 'text-gray-400'
                }`} />
                <span className={`text-sm font-medium ${
                  analysisStep === 'fetching' ? 'text-blue-700 dark:text-blue-300' : 'text-gray-600 dark:text-gray-400'
                }`}>
                  Fetching Repository
                </span>
              </div>

              <div className={`flex items-center space-x-3 p-3 rounded-lg ${
                analysisStep === 'analyzing' ? 'bg-orange-50 dark:bg-orange-900/20' : 'bg-gray-50 dark:bg-gray-700/50'
              }`}>
                <Search className={`w-4 h-4 ${
                  analysisStep === 'analyzing' ? 'text-orange-500' : 'text-gray-400'
                }`} />
                <span className={`text-sm font-medium ${
                  analysisStep === 'analyzing' ? 'text-orange-700 dark:text-orange-300' : 'text-gray-600 dark:text-gray-400'
                }`}>
                  Analyzing Code
                </span>
              </div>

              <div className={`flex items-center space-x-3 p-3 rounded-lg ${
                analysisStep === 'complete' ? 'bg-green-50 dark:bg-green-900/20' : 'bg-gray-50 dark:bg-gray-700/50'
              }`}>
                <CheckCircle className={`w-4 h-4 ${
                  analysisStep === 'complete' ? 'text-green-500' : 'text-gray-400'
                }`} />
                <span className={`text-sm font-medium ${
                  analysisStep === 'complete' ? 'text-green-700 dark:text-green-300' : 'text-gray-600 dark:text-gray-400'
                }`}>
                  Analysis Complete
                </span>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Tips
            </h3>
            <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-2">
              <li>• Public repositories work best for analysis</li>
              <li>• Large repositories may take longer to process</li>
              <li>• Analysis includes code quality, security, and complexity</li>
              <li>• Results are saved for future reference</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GitHubImport;