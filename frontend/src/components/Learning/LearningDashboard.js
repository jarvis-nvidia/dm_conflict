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

  const handleLearnFromCode = async (code, language) => {
    try {
      await learnPattern(() => 
        apiEndpoints.learnUserPattern({
          user_id: userId,
          learning_type: 'code_style',
          data: {
            code,
            language,
            timestamp: new Date().toISOString()
          }
        })
      );
      // Refresh data after learning
      fetchRecommendations();
    } catch (error) {
      console.error('Failed to learn from code:', error);
    }
  };

  const tabs = [
    { id: 'progress', label: 'Progress', icon: TrendingUp },
    { id: 'suggestions', label: 'Suggestions', icon: Brain },
    { id: 'learning', label: 'Learning', icon: BookOpen },
    { id: 'settings', label: 'Settings', icon: Settings }
  ];

  const stats = [
    {
      title: 'Total Sessions',
      value: userProgress?.progress?.total_sessions || 0,
      icon: Clock,
      color: 'blue'
    },
    {
      title: 'Learning Streak',
      value: `${userProgress?.progress?.learning_streak || 0} days`,
      icon: Award,
      color: 'green'
    },
    {
      title: 'Code Analyzed',
      value: userProgress?.progress?.code_analyzed || 0,
      icon: Code,
      color: 'purple'
    },
    {
      title: 'Patterns Learned',
      value: userProgress?.progress?.patterns_learned || 0,
      icon: Brain,
      color: 'orange'
    }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Learning Dashboard
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Track your coding patterns, get personalized suggestions, and improve your development skills.
        </p>
      </div>

      {/* User Selection */}
      <div className="mb-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4">
          <div className="flex items-center space-x-4">
            <User className="w-5 h-5 text-gray-500" />
            <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
              User ID:
            </label>
            <input
              type="text"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              className="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-sm"
              placeholder="Enter user ID"
            />
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div key={stat.title} className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                    {stat.title}
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {stat.value}
                  </p>
                </div>
                <div className={`p-3 rounded-full bg-${stat.color}-100 dark:bg-${stat.color}-900/20`}>
                  <Icon className={`w-6 h-6 text-${stat.color}-600 dark:text-${stat.color}-400`} />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Tab Navigation */}
      <div className="mb-6">
        <nav className="flex space-x-8">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  activeTab === tab.id
                    ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300'
                    : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="space-y-6">
        {activeTab === 'progress' && (
          <UserProgress 
            userProgress={userProgress} 
            loading={progressLoading} 
            error={progressError}
          />
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
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Learn from Code
              </h3>
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                Help the AI learn your coding patterns by analyzing your code.
              </p>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Code to Learn From
                  </label>
                  <textarea
                    placeholder="Paste your code here..."
                    className="w-full h-40 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-mono text-sm"
                  />
                </div>
                
                <div className="flex items-center space-x-4">
                  <select className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white">
                    <option value="python">Python</option>
                    <option value="javascript">JavaScript</option>
                    <option value="java">Java</option>
                  </select>
                  
                  <button
                    disabled={learnLoading}
                    className="flex items-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white rounded-lg transition-colors"
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
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Learning Settings
            </h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    Auto-learn from code analysis
                  </label>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    Automatically learn from your coding patterns
                  </p>
                </div>
                <input type="checkbox" className="rounded" defaultChecked />
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    Personalized suggestions
                  </label>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    Get suggestions based on your coding style
                  </p>
                </div>
                <input type="checkbox" className="rounded" defaultChecked />
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    Learning notifications
                  </label>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
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
  );
};

export default LearningDashboard;