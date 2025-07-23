import React, { useState } from 'react';
import { useApiCall } from '../../hooks/useApi';
import LoadingSpinner from '../Common/LoadingSpinner';
import ErrorMessage from '../Common/ErrorMessage';
import { Github, Download, CheckCircle, FileText, Code2, GitBranch } from 'lucide-react';

const GitHubImport = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [selectedRepo, setSelectedRepo] = useState('');
  const [selectedBranch, setSelectedBranch] = useState('');
  const [importProgress, setImportProgress] = useState(0);
  const [importResults, setImportResults] = useState(null);
  const [isImporting, setIsImporting] = useState(false);
  
  const { execute: connectGitHub, loading: connectLoading, error: connectError } = useApiCall();
  const { execute: importRepo, loading: importLoading, error: importError } = useApiCall();

  // Mock repository data
  const repositories = [
    {
      id: 1,
      name: 'my-awesome-project',
      stars: 123,
      language: 'Python',
      description: 'This is a sample repository for DevMind.'
    },
    {
      id: 2,
      name: 'web-app',
      stars: 45,
      language: 'JavaScript',
      description: 'A modern web application built with React.'
    }
  ];

  const branches = ['main', 'develop', 'feature/new-ui', 'hotfix/bug-fix'];

  const handleConnectGitHub = async () => {
    try {
      // Simulate GitHub connection
      setIsConnected(true);
    } catch (error) {
      console.error('GitHub connection failed:', error);
    }
  };

  const handleImport = async () => {
    if (!selectedRepo || !selectedBranch) return;
    
    setIsImporting(true);
    setImportProgress(0);
    
    // Simulate import progress
    const progressInterval = setInterval(() => {
      setImportProgress(prev => {
        if (prev >= 100) {
          clearInterval(progressInterval);
          setIsImporting(false);
          setImportResults({
            totalFiles: 123,
            totalLines: 12345,
            codeSmells: 15
          });
          return 100;
        }
        return prev + 10;
      });
    }, 300);
  };

  const selectedRepoData = repositories.find(repo => repo.name === selectedRepo);

  return (
    <div className="min-h-screen bg-[#111418] text-white">
      <div className="px-40 flex flex-1 justify-center py-5">
        <div className="layout-content-container flex flex-col w-[512px] max-w-[512px] py-5 max-w-[960px] flex-1">
          
          {/* Header */}
          <h2 className="text-white tracking-light text-[28px] font-bold leading-tight px-4 text-center pb-3 pt-5">
            Connect your repository
          </h2>
          <p className="text-white text-base font-normal leading-normal pb-3 pt-1 px-4 text-center">
            Connect your repository to EV MIND to analyze your code and get insights.
          </p>

          {/* Connect GitHub Button */}
          <div className="flex px-4 py-3 justify-center">
            <button
              onClick={handleConnectGitHub}
              disabled={connectLoading || isConnected}
              className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-[#0c7ff2] text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors gap-2"
            >
              {connectLoading ? (
                <LoadingSpinner size="sm" text="" />
              ) : (
                <>
                  <Github className="w-5 h-5" />
                  <span className="truncate">
                    {isConnected ? 'Connected to GitHub' : 'Connect with GitHub'}
                  </span>
                  {isConnected && <CheckCircle className="w-4 h-4" />}
                </>
              )}
            </button>
          </div>

          {connectError && (
            <div className="px-4 py-3">
              <ErrorMessage error={connectError} />
            </div>
          )}

          {/* Repository Selection */}
          {isConnected && (
            <>
              <h2 className="text-white text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">
                Select a repository
              </h2>
              <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
                <label className="flex flex-col min-w-40 flex-1">
                  <select
                    value={selectedRepo}
                    onChange={(e) => setSelectedRepo(e.target.value)}
                    className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-white focus:outline-0 focus:ring-0 border border-[#3b4754] bg-[#1b2127] focus:border-[#3b4754] h-14 placeholder:text-[#9cabba] p-[15px] text-base font-normal leading-normal"
                    style={{backgroundImage: "url('data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 width=%2724px%27 height=%2724px%27 fill=%27rgb(156,171,186)%27 viewBox=%270 0 256 256%27%3e%3cpath d=%27M181.66,170.34a8,8,0,0,1,0,11.32l-48,48a8,8,0,0,1-11.32,0l-48-48a8,8,0,0,1,11.32-11.32L128,212.69l42.34-42.35A8,8,0,0,1,181.66,170.34Zm-96-84.68L128,43.31l42.34,42.35a8,8,0,0,0,11.32-11.32l-48-48a8,8,0,0,0-11.32,0l-48,48A8,8,0,0,0,85.66,85.66Z%27%3e%3c/path%3e%3c/svg%3e')", backgroundRepeat: 'no-repeat', backgroundPosition: 'right 15px center'}}
                  >
                    <option value="">Select a repository</option>
                    {repositories.map(repo => (
                      <option key={repo.id} value={repo.name}>{repo.name}</option>
                    ))}
                  </select>
                </label>
              </div>

              {/* Repository Details */}
              {selectedRepoData && (
                <div className="p-4 grid grid-cols-[20%_1fr] gap-x-6">
                  <div className="col-span-2 grid grid-cols-subgrid border-t border-t-[#3b4754] py-5">
                    <p className="text-[#9cabba] text-sm font-normal leading-normal">Stars</p>
                    <p className="text-white text-sm font-normal leading-normal">{selectedRepoData.stars}</p>
                  </div>
                  <div className="col-span-2 grid grid-cols-subgrid border-t border-t-[#3b4754] py-5">
                    <p className="text-[#9cabba] text-sm font-normal leading-normal">Language</p>
                    <p className="text-white text-sm font-normal leading-normal">{selectedRepoData.language}</p>
                  </div>
                  <div className="col-span-2 grid grid-cols-subgrid border-t border-t-[#3b4754] py-5">
                    <p className="text-[#9cabba] text-sm font-normal leading-normal">Description</p>
                    <p className="text-white text-sm font-normal leading-normal">{selectedRepoData.description}</p>
                  </div>
                </div>
              )}

              {/* Branch Selection */}
              <h2 className="text-white text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">
                Select a branch
              </h2>
              <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
                <label className="flex flex-col min-w-40 flex-1">
                  <select
                    value={selectedBranch}
                    onChange={(e) => setSelectedBranch(e.target.value)}
                    className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-white focus:outline-0 focus:ring-0 border border-[#3b4754] bg-[#1b2127] focus:border-[#3b4754] h-14 placeholder:text-[#9cabba] p-[15px] text-base font-normal leading-normal"
                    style={{backgroundImage: "url('data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 width=%2724px%27 height=%2724px%27 fill=%27rgb(156,171,186)%27 viewBox=%270 0 256 256%27%3e%3cpath d=%27M181.66,170.34a8,8,0,0,1,0,11.32l-48,48a8,8,0,0,1-11.32,0l-48-48a8,8,0,0,1,11.32-11.32L128,212.69l42.34-42.35A8,8,0,0,1,181.66,170.34Zm-96-84.68L128,43.31l42.34,42.35a8,8,0,0,0,11.32-11.32l-48-48a8,8,0,0,0-11.32,0l-48,48A8,8,0,0,0,85.66,85.66Z%27%3e%3c/path%3e%3c/svg%3e')", backgroundRepeat: 'no-repeat', backgroundPosition: 'right 15px center'}}
                  >
                    <option value="">Select a branch</option>
                    {branches.map(branch => (
                      <option key={branch} value={branch}>{branch}</option>
                    ))}
                  </select>
                </label>
              </div>

              {/* Import Button */}
              <div className="flex px-4 py-3 justify-center">
                <button
                  onClick={handleImport}
                  disabled={!selectedRepo || !selectedBranch || isImporting}
                  className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-[#0c7ff2] text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors gap-2"
                >
                  {isImporting ? (
                    <>
                      <LoadingSpinner size="sm" text="" />
                      <span>Importing...</span>
                    </>
                  ) : (
                    <>
                      <Download className="w-4 h-4" />
                      <span className="truncate">Import</span>
                    </>
                  )}
                </button>
              </div>

              {/* Import Progress */}
              {(isImporting || importProgress > 0) && (
                <>
                  <h2 className="text-white text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">
                    Import progress
                  </h2>
                  <div className="flex flex-col gap-3 p-4">
                    <div className="flex gap-6 justify-between">
                      <p className="text-white text-base font-medium leading-normal">
                        {isImporting ? 'Importing...' : 'Import Complete'}
                      </p>
                    </div>
                    <div className="rounded bg-[#3b4754]">
                      <div 
                        className="h-2 rounded bg-white transition-all duration-300" 
                        style={{width: `${importProgress}%`}} 
                      />
                    </div>
                    <p className="text-[#9cabba] text-sm font-normal leading-normal">{importProgress}%</p>
                  </div>
                </>
              )}

              {/* Import Results */}
              {importResults && (
                <>
                  <h2 className="text-white text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">
                    Import results
                  </h2>
                  <div className="flex flex-wrap gap-4 p-4">
                    <div className="flex min-w-[158px] flex-1 flex-col gap-2 rounded-lg p-6 border border-[#3b4754]">
                      <p className="text-white text-base font-medium leading-normal">Total files</p>
                      <p className="text-white tracking-light text-2xl font-bold leading-tight">{importResults.totalFiles}</p>
                    </div>
                    <div className="flex min-w-[158px] flex-1 flex-col gap-2 rounded-lg p-6 border border-[#3b4754]">
                      <p className="text-white text-base font-medium leading-normal">Total lines of code</p>
                      <p className="text-white tracking-light text-2xl font-bold leading-tight">{importResults.totalLines}</p>
                    </div>
                    <div className="flex min-w-[158px] flex-1 flex-col gap-2 rounded-lg p-6 border border-[#3b4754]">
                      <p className="text-white text-base font-medium leading-normal">Code smells detected</p>
                      <p className="text-white tracking-light text-2xl font-bold leading-tight">{importResults.codeSmells}</p>
                    </div>
                  </div>
                  <div className="flex px-4 py-3 justify-center">
                    <button className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-[#0c7ff2] text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-blue-600 transition-colors gap-2">
                      <FileText className="w-4 h-4" />
                      <span className="truncate">View results</span>
                    </button>
                  </div>
                </>
              )}

              {importError && (
                <div className="px-4 py-3">
                  <ErrorMessage error={importError} />
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default GitHubImport;