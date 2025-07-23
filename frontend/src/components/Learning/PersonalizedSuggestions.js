import React from 'react';
import { RefreshCw, Lightbulb, Code, Target, TrendingUp, CheckCircle } from 'lucide-react';
import LoadingSpinner from '../Common/LoadingSpinner';

const PersonalizedSuggestions = ({ recommendations, loading, onRefresh }) => {
  if (loading) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <LoadingSpinner size="lg" text="Loading personalized suggestions..." />
      </div>
    );
  }

  const suggestions = recommendations?.recommendations || {};
  const stylesSuggestions = suggestions.style_suggestions || [];
  const qualitySuggestions = suggestions.quality_suggestions || [];
  const learningTips = suggestions.learning_tips || [];

  const mockSuggestions = {
    style_suggestions: [
      "Consider using snake_case for function names",
      "Your preferred indentation is 4 spaces",
      "Add type hints to improve code clarity",
      "Use more descriptive variable names",
    ],
    quality_suggestions: [
      "Break down complex functions into smaller ones",
      "Add error handling for edge cases",
      "Consider using list comprehensions for better readability",
      "Add docstrings to your functions",
    ],
    learning_tips: [
      "You're improving in code complexity management",
      "Focus on security best practices",
      "Learn more about Python design patterns",
      "Practice writing unit tests",
    ]
  };

  // Use mock data if no real data
  const finalStyleSuggestions = stylesSuggestions.length > 0 ? stylesSuggestions : mockSuggestions.style_suggestions;
  const finalQualitySuggestions = qualitySuggestions.length > 0 ? qualitySuggestions : mockSuggestions.quality_suggestions;
  const finalLearningTips = learningTips.length > 0 ? learningTips : mockSuggestions.learning_tips;

  const suggestionCategories = [
    {
      title: 'Style Suggestions',
      items: finalStyleSuggestions,
      icon: Code,
      color: 'blue',
      description: 'Improve your coding style consistency'
    },
    {
      title: 'Quality Improvements',
      items: finalQualitySuggestions,
      icon: Target,
      color: 'green',
      description: 'Enhance your code quality'
    },
    {
      title: 'Learning Tips',
      items: finalLearningTips,
      icon: TrendingUp,
      color: 'purple',
      description: 'Areas for skill development'
    }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center space-x-2">
              <Lightbulb className="w-5 h-5" />
              <span>Personalized Suggestions</span>
            </h3>
            <p className="text-gray-600 dark:text-gray-400 mt-1">
              AI-powered recommendations based on your coding patterns
            </p>
          </div>
          <button
            onClick={onRefresh}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {/* Suggestion Categories */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {suggestionCategories.map((category) => {
          const Icon = category.icon;
          return (
            <div key={category.title} className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <div className="flex items-center space-x-3 mb-4">
                <div className={`p-2 rounded-full bg-${category.color}-100 dark:bg-${category.color}-900/20`}>
                  <Icon className={`w-5 h-5 text-${category.color}-600 dark:text-${category.color}-400`} />
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900 dark:text-white">
                    {category.title}
                  </h4>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {category.description}
                  </p>
                </div>
              </div>

              <div className="space-y-3">
                {category.items.map((item, index) => (
                  <div key={index} className="flex items-start space-x-3 p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                    <CheckCircle className="w-4 h-4 text-green-500 flex-shrink-0 mt-0.5" />
                    <p className="text-sm text-gray-800 dark:text-gray-200">
                      {item}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>

      {/* Personalized Insights */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-lg shadow-sm border border-blue-200 dark:border-blue-800 p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Your Coding Insights
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-gray-900 dark:text-white mb-2">
              Strengths
            </h4>
            <ul className="space-y-1 text-sm text-gray-700 dark:text-gray-300">
              <li>• Consistent code formatting</li>
              <li>• Good function naming conventions</li>
              <li>• Proper error handling in most cases</li>
              <li>• Clean code structure</li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-900 dark:text-white mb-2">
              Areas for Growth
            </h4>
            <ul className="space-y-1 text-sm text-gray-700 dark:text-gray-300">
              <li>• Complex function decomposition</li>
              <li>• More comprehensive documentation</li>
              <li>• Security best practices</li>
              <li>• Performance optimization</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Progress Tracking */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Suggestion Progress
        </h3>
        
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span className="text-sm font-medium text-gray-900 dark:text-white">
                Code Style Improvements
              </span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-32 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div className="bg-green-500 h-2 rounded-full" style={{ width: '78%' }}></div>
              </div>
              <span className="text-sm text-gray-600 dark:text-gray-400">78%</span>
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
              <span className="text-sm font-medium text-gray-900 dark:text-white">
                Quality Enhancements
              </span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-32 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div className="bg-blue-500 h-2 rounded-full" style={{ width: '65%' }}></div>
              </div>
              <span className="text-sm text-gray-600 dark:text-gray-400">65%</span>
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-3 h-3 bg-purple-500 rounded-full"></div>
              <span className="text-sm font-medium text-gray-900 dark:text-white">
                Learning Goals
              </span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-32 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div className="bg-purple-500 h-2 rounded-full" style={{ width: '45%' }}></div>
              </div>
              <span className="text-sm text-gray-600 dark:text-gray-400">45%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PersonalizedSuggestions;