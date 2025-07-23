import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { TrendingUp, Calendar, Target, Award, Clock, Code } from 'lucide-react';
import LoadingSpinner from '../Common/LoadingSpinner';
import ErrorMessage from '../Common/ErrorMessage';

const UserProgress = ({ userProgress, loading, error }) => {
  if (loading) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <LoadingSpinner size="lg" text="Loading progress data..." />
      </div>
    );
  }

  if (error) {
    return <ErrorMessage error={error} />;
  }

  const progress = userProgress?.progress || {};
  const analytics = userProgress?.analytics || {};
  const achievements = userProgress?.achievements || [];

  // Mock data for demonstration
  const mockProgressData = [
    { date: '2024-01-01', score: 65, sessions: 2 },
    { date: '2024-01-02', score: 68, sessions: 3 },
    { date: '2024-01-03', score: 72, sessions: 1 },
    { date: '2024-01-04', score: 75, sessions: 4 },
    { date: '2024-01-05', score: 78, sessions: 2 },
    { date: '2024-01-06', score: 82, sessions: 3 },
    { date: '2024-01-07', score: 85, sessions: 5 },
  ];

  const mockActivityData = [
    { activity: 'Code Analysis', count: 45 },
    { activity: 'Smell Detection', count: 32 },
    { activity: 'Pattern Learning', count: 28 },
    { activity: 'Suggestions', count: 15 },
  ];

  const progressMetrics = [
    {
      title: 'Total Sessions',
      value: progress.total_sessions || 0,
      icon: Clock,
      color: 'blue',
      change: '+5.2%'
    },
    {
      title: 'Learning Streak',
      value: `${progress.learning_streak || 0} days`,
      icon: Award,
      color: 'green',
      change: '+1 day'
    },
    {
      title: 'Code Quality Score',
      value: progress.quality_score || 75,
      icon: Target,
      color: 'purple',
      change: '+8 points'
    },
    {
      title: 'Patterns Learned',
      value: progress.patterns_learned || 12,
      icon: Code,
      color: 'orange',
      change: '+3 patterns'
    }
  ];

  return (
    <div className="space-y-6">
      {/* Progress Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {progressMetrics.map((metric) => {
          const Icon = metric.icon;
          return (
            <div key={metric.title} className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                    {metric.title}
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {metric.value}
                  </p>
                  <p className="text-sm text-green-600 dark:text-green-400 mt-1">
                    {metric.change}
                  </p>
                </div>
                <div className={`p-3 rounded-full bg-${metric.color}-100 dark:bg-${metric.color}-900/20`}>
                  <Icon className={`w-6 h-6 text-${metric.color}-600 dark:text-${metric.color}-400`} />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Progress Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center space-x-2">
            <TrendingUp className="w-5 h-5" />
            <span>Progress Over Time</span>
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={mockProgressData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis 
                dataKey="date" 
                tick={{ fill: '#6B7280', fontSize: 12 }}
                axisLine={{ stroke: '#6B7280' }}
              />
              <YAxis 
                tick={{ fill: '#6B7280', fontSize: 12 }}
                axisLine={{ stroke: '#6B7280' }}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1F2937', 
                  border: '1px solid #374151',
                  borderRadius: '6px',
                  color: '#F3F4F6'
                }}
              />
              <Line 
                type="monotone" 
                dataKey="score" 
                stroke="#3B82F6" 
                strokeWidth={2}
                dot={{ fill: '#3B82F6' }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Activity Breakdown
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={mockActivityData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis 
                dataKey="activity" 
                tick={{ fill: '#6B7280', fontSize: 12 }}
                axisLine={{ stroke: '#6B7280' }}
              />
              <YAxis 
                tick={{ fill: '#6B7280', fontSize: 12 }}
                axisLine={{ stroke: '#6B7280' }}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1F2937', 
                  border: '1px solid #374151',
                  borderRadius: '6px',
                  color: '#F3F4F6'
                }}
              />
              <Bar dataKey="count" fill="#10B981" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Achievements */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center space-x-2">
          <Award className="w-5 h-5" />
          <span>Achievements</span>
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {/* Mock achievements */}
          <div className="flex items-center space-x-3 p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-800">
            <div className="p-2 bg-yellow-100 dark:bg-yellow-900/30 rounded-full">
              <Award className="w-5 h-5 text-yellow-600 dark:text-yellow-400" />
            </div>
            <div>
              <h4 className="font-medium text-yellow-900 dark:text-yellow-200">
                First Analysis
              </h4>
              <p className="text-sm text-yellow-700 dark:text-yellow-300">
                Completed your first code analysis
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-3 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
            <div className="p-2 bg-blue-100 dark:bg-blue-900/30 rounded-full">
              <Target className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <h4 className="font-medium text-blue-900 dark:text-blue-200">
                Code Explorer
              </h4>
              <p className="text-sm text-blue-700 dark:text-blue-300">
                Analyzed 10 different files
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-3 p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
            <div className="p-2 bg-green-100 dark:bg-green-900/30 rounded-full">
              <TrendingUp className="w-5 h-5 text-green-600 dark:text-green-400" />
            </div>
            <div>
              <h4 className="font-medium text-green-900 dark:text-green-200">
                Quality Improver
              </h4>
              <p className="text-sm text-green-700 dark:text-green-300">
                Improved code quality by 25%
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center space-x-2">
          <Calendar className="w-5 h-5" />
          <span>Recent Activity</span>
        </h3>
        
        <div className="space-y-4">
          {/* Mock activity items */}
          <div className="flex items-center space-x-3 p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
            <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900 dark:text-white">
                Analyzed Python code for complexity issues
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                2 hours ago
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-3 p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900 dark:text-white">
                Learned new coding patterns from JavaScript file
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                5 hours ago
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-3 p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
            <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900 dark:text-white">
                Detected 5 code smells in repository analysis
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                1 day ago
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserProgress;