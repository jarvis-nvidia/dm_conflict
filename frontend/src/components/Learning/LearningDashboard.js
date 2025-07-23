import React, { useState, useEffect } from 'react';
import { useApiCall, useUserProgress } from '../../hooks/useApi';
import { apiEndpoints } from '../../utils/api';
import LoadingSpinner from '../Common/LoadingSpinner';
import ErrorMessage from '../Common/ErrorMessage';
import UserProgress from './UserProgress';
import PersonalizedSuggestions from './PersonalizedSuggestions';
import { 
  Brain, 
  TrendingUp, 
  Target, 
  Award,
  BookOpen,
  Clock,
  Code,
  GitCommit,
  User,
  Settings
} from 'lucide-react';

const LearningDashboard = () => {
  const [userId, setUserId] = useState('demo_user');
  const [activeTab, setActiveTab] = useState('progress');
  const [learningData, setLearningData] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [codeToLearn, setCodeToLearn] = useState('');
  const [learnLanguage, setLearnLanguage] = useState('python');
  
  const { data: userProgress, loading: progressLoading, error: progressError } = useUserProgress(userId);
  const { execute: getRecommendations, loading: recLoading } = useApiCall();
  const { execute: learnPattern, loading: learnLoading } = useApiCall();

  useEffect(() => {
    if (userId) {
      fetchRecommendations();
    }
  }, [userId]);

  const fetchRecommendations = async () => {
    try {
      const recData = await getRecommendations(() => 
        apiEndpoints.getPersonalizedRecommendations({
          user_id: userId,
          context: {
            language: 'python',
            recent_activity: 'code_analysis'
          }
        })
      );
      setRecommendations(recData);
    } catch (error) {
      console.error('Failed to fetch recommendations:', error);
    }
  };

  const handleLearnFromCode = async () => {
    if (!codeToLearn.trim()) return;
    
    try {
      await learnPattern(() => 
        apiEndpoints.learnUserPattern({
          user_id: userId,
          learning_type: 'code_style',
          data: {
            code: codeToLearn,
            language: learnLanguage,
            timestamp: new Date().toISOString()
          }
        })
      );
      // Refresh data after learning
      fetchRecommendations();
      setCodeToLearn(''); // Clear the input
    } catch (error) {
      console.error('Failed to learn from code:', error);
    }
  };

  const tabs = [
    { id: 'progress', label: 'Progress' },
    { id: 'suggestions', label: 'Suggestions' },
    { id: 'learning', label: 'Learning' },
    { id: 'settings', label: 'Settings' }
  ];

  const stats = [
    {
      title: 'Total Sessions',
      value: userProgress?.progress?.total_sessions || 25,
      change: '+10%',
      positive: true
    },
    {
      title: 'Learning Streak',
      value: `${userProgress?.progress?.learning_streak || 7} days`,
      change: '+5%',
      positive: true
    },
    {
      title: 'Code Analyzed',
      value: userProgress?.progress?.code_analyzed || 150,
      change: '+15%',
      positive: true
    },
    {
      title: 'Patterns Learned',
      value: userProgress?.progress?.patterns_learned || 30,
      change: '+8%',
      positive: true
    }
  ];

  return (
    <div className="min-h-screen bg-[#111418] text-white">
      <div className="px-40 flex flex-1 justify-center py-5">
        <div className="layout-content-container flex flex-col max-w-[960px] flex-1">
          <div className="flex flex-wrap justify-between gap-3 p-4">
            <p className="text-white tracking-light text-[32px] font-bold leading-tight min-w-72">Dashboard</p>
          </div>

          {/* Stats Cards */}
          <div className="flex flex-wrap gap-4 p-4">
            {stats.map((stat, index) => (
              <div key={stat.title} className="flex min-w-[158px] flex-1 flex-col gap-2 rounded-lg p-6 bg-[#283039]">
                <p className="text-white text-base font-medium leading-normal">{stat.title}</p>
                <p className="text-white tracking-light text-2xl font-bold leading-tight">{stat.value}</p>
                <p className={`text-base font-medium leading-normal ${stat.positive ? 'text-[#0bda5b]' : 'text-[#fa6238]'}`}>
                  {stat.change}
                </p>
              </div>
            ))}
          </div>

          {/* Tab Navigation */}
          <div className="pb-3">
            <div className="flex border-b border-[#3b4754] px-4 gap-8">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex flex-col items-center justify-center border-b-[3px] pb-[13px] pt-4 transition-colors ${
                    activeTab === tab.id
                      ? 'border-b-white text-white'
                      : 'border-b-transparent text-[#9cabba] hover:text-white'
                  }`}
                >
                  <p className="text-sm font-bold leading-normal tracking-[0.015em]">{tab.label}</p>
                </button>
              ))}
            </div>
          </div>

          {/* Tab Content */}
          {activeTab === 'progress' && (
            <>
              <h2 className="text-white text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">Progress Overview</h2>
              <div className="flex flex-wrap gap-4 px-4 py-6">
                {/* Learning Progress Chart */}
                <div className="flex min-w-72 flex-1 flex-col gap-2 rounded-lg border border-[#3b4754] p-6">
                  <p className="text-white text-base font-medium leading-normal">Learning Progress Over Time</p>
                  <p className="text-white tracking-light text-[32px] font-bold leading-tight truncate">+15%</p>
                  <div className="flex gap-1">
                    <p className="text-[#9cabba] text-base font-normal leading-normal">Last 30 Days</p>
                    <p className="text-[#0bda5b] text-base font-medium leading-normal">+15%</p>
                  </div>
                  <div className="flex min-h-[180px] flex-1 flex-col gap-8 py-4">
                    <svg width="100%" height="148" viewBox="-3 0 478 150" fill="none" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none">
                      <path
                        d="M0 109C18.1538 109 18.1538 21 36.3077 21C54.4615 21 54.4615 41 72.6154 41C90.7692 41 90.7692 93 108.923 93C127.077 93 127.077 33 145.231 33C163.385 33 163.385 101 181.538 101C199.692 101 199.692 61 217.846 61C236 61 236 45 254.154 45C272.308 45 272.308 121 290.462 121C308.615 121 308.615 149 326.769 149C344.923 149 344.923 1 363.077 1C381.231 1 381.231 81 399.385 81C417.538 81 417.538 129 435.692 129C453.846 129 453.846 25 472 25V149H326.769H0V109Z"
                        fill="url(#paint0_linear_1131_5935)"
                      />
                      <path
                        d="M0 109C18.1538 109 18.1538 21 36.3077 21C54.4615 21 54.4615 41 72.6154 41C90.7692 41 90.7692 93 108.923 93C127.077 93 127.077 33 145.231 33C163.385 33 163.385 101 181.538 101C199.692 101 199.692 61 217.846 61C236 61 236 45 254.154 45C272.308 45 272.308 121 290.462 121C308.615 121 308.615 149 326.769 149C344.923 149 344.923 1 363.077 1C381.231 1 381.231 81 399.385 81C417.538 81 417.538 129 435.692 129C453.846 129 453.846 25 472 25"
                        stroke="#9cabba"
                        strokeWidth="3"
                        strokeLinecap="round"
                      />
                      <defs>
                        <linearGradient id="paint0_linear_1131_5935" x1="236" y1="1" x2="236" y2="149" gradientUnits="userSpaceOnUse">
                          <stop stopColor="#283039" />
                          <stop offset="1" stopColor="#283039" stopOpacity="0" />
                        </linearGradient>
                      </defs>
                    </svg>
                    <div className="flex justify-around">
                      <p className="text-[#9cabba] text-[13px] font-bold leading-normal tracking-[0.015em]">Week 1</p>
                      <p className="text-[#9cabba] text-[13px] font-bold leading-normal tracking-[0.015em]">Week 2</p>
                      <p className="text-[#9cabba] text-[13px] font-bold leading-normal tracking-[0.015em]">Week 3</p>
                      <p className="text-[#9cabba] text-[13px] font-bold leading-normal tracking-[0.015em]">Week 4</p>
                    </div>
                  </div>
                </div>

                {/* Category Chart */}
                <div className="flex min-w-72 flex-1 flex-col gap-2 rounded-lg border border-[#3b4754] p-6">
                  <p className="text-white text-base font-medium leading-normal">Patterns Learned by Category</p>
                  <p className="text-white tracking-light text-[32px] font-bold leading-tight truncate">+20%</p>
                  <div className="flex gap-1">
                    <p className="text-[#9cabba] text-base font-normal leading-normal">Last 30 Days</p>
                    <p className="text-[#0bda5b] text-base font-medium leading-normal">+20%</p>
                  </div>
                  <div className="grid min-h-[180px] grid-flow-col gap-6 grid-rows-[1fr_auto] items-end justify-items-center px-3">
                    <div className="border-[#9cabba] bg-[#283039] border-t-2 w-full" style={{height: '60%'}} />
                    <p className="text-[#9cabba] text-[13px] font-bold leading-normal tracking-[0.015em]">Category A</p>
                    <div className="border-[#9cabba] bg-[#283039] border-t-2 w-full" style={{height: '90%'}} />
                    <p className="text-[#9cabba] text-[13px] font-bold leading-normal tracking-[0.015em]">Category B</p>
                    <div className="border-[#9cabba] bg-[#283039] border-t-2 w-full" style={{height: '50%'}} />
                    <p className="text-[#9cabba] text-[13px] font-bold leading-normal tracking-[0.015em]">Category C</p>
                    <div className="border-[#9cabba] bg-[#283039] border-t-2 w-full" style={{height: '30%'}} />
                    <p className="text-[#9cabba] text-[13px] font-bold leading-normal tracking-[0.015em]">Category D</p>
                  </div>
                </div>
              </div>

              {/* Learning Metrics */}
              <h2 className="text-white text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">Learning Metrics</h2>
              <div className="flex flex-col gap-3 p-4">
                <div className="flex gap-6 justify-between">
                  <p className="text-white text-base font-medium leading-normal">Overall Learning Progress</p>
                  <p className="text-white text-sm font-normal leading-normal">75%</p>
                </div>
                <div className="rounded bg-[#3b4754]">
                  <div className="h-2 rounded bg-white" style={{width: '75%'}} />
                </div>
              </div>
              <div className="flex flex-col gap-3 p-4">
                <div className="flex gap-6 justify-between">
                  <p className="text-white text-base font-medium leading-normal">Code Analysis Completion</p>
                  <p className="text-white text-sm font-normal leading-normal">50%</p>
                </div>
                <div className="rounded bg-[#3b4754]">
                  <div className="h-2 rounded bg-white" style={{width: '50%'}} />
                </div>
              </div>
              <div className="flex flex-col gap-3 p-4">
                <div className="flex gap-6 justify-between">
                  <p className="text-white text-base font-medium leading-normal">Pattern Recognition Accuracy</p>
                  <p className="text-white text-sm font-normal leading-normal">90%</p>
                </div>
                <div className="rounded bg-[#3b4754]">
                  <div className="h-2 rounded bg-white" style={{width: '90%'}} />
                </div>
              </div>
            </>
          )}

          {activeTab === 'suggestions' && (
            <PersonalizedSuggestions 
              recommendations={recommendations} 
              loading={recLoading}
              onRefresh={fetchRecommendations}
            />
          )}

          {activeTab === 'learning' && (
            <div className="space-y-6">
              <div className="bg-[#283039] rounded-lg p-6 m-4">
                <h3 className="text-lg font-semibold text-white mb-4">
                  Learn from Code
                </h3>
                <p className="text-[#9cabba] mb-4">
                  Help the AI learn your coding patterns by analyzing your code.
                </p>
                
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-white mb-2">
                      Code to Learn From
                    </label>
                    <textarea
                      value={codeToLearn}
                      onChange={(e) => setCodeToLearn(e.target.value)}
                      placeholder="Paste your code here..."
                      className="w-full h-40 px-3 py-2 border border-[#3b4754] rounded-lg bg-[#1b2127] text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-mono text-sm resize-none"
                    />
                  </div>
                  
                  <div className="flex items-center space-x-4">
                    <select 
                      value={learnLanguage}
                      onChange={(e) => setLearnLanguage(e.target.value)}
                      className="px-3 py-2 border border-[#3b4754] rounded-lg bg-[#1b2127] text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="python">Python</option>
                      <option value="javascript">JavaScript</option>
                      <option value="java">Java</option>
                      <option value="typescript">TypeScript</option>
                    </select>
                    
                    <button
                      onClick={handleLearnFromCode}
                      disabled={learnLoading || !codeToLearn.trim()}
                      className="flex items-center space-x-2 px-4 py-2 bg-[#0c7ff2] hover:bg-blue-600 disabled:bg-gray-400 text-white rounded-lg transition-colors"
                    >
                      {learnLoading ? (
                        <LoadingSpinner size="sm" text="" />
                      ) : (
                        <>
                          <Brain className="w-4 h-4" />
                          <span>Learn from Code</span>
                        </>
                      )}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'settings' && (
            <div className="bg-[#283039] rounded-lg p-6 m-4">
              <h3 className="text-lg font-semibold text-white mb-4">
                Learning Settings
              </h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-white">
                      Auto-learn from code analysis
                    </label>
                    <p className="text-xs text-[#9cabba]">
                      Automatically learn from your coding patterns
                    </p>
                  </div>
                  <input type="checkbox" className="rounded" defaultChecked />
                </div>
                
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-white">
                      Personalized suggestions
                    </label>
                    <p className="text-xs text-[#9cabba]">
                      Get suggestions based on your coding style
                    </p>
                  </div>
                  <input type="checkbox" className="rounded" defaultChecked />
                </div>
                
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-white">
                      Learning notifications
                    </label>
                    <p className="text-xs text-[#9cabba]">
                      Get notified about new learning insights
                    </p>
                  </div>
                  <input type="checkbox" className="rounded" />
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LearningDashboard;