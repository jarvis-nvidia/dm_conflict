import React from 'react';
import { 
  AlertTriangle, 
  XCircle, 
  Info, 
  CheckCircle, 
  ExternalLink,
  Code,
  MapPin,
  Target
} from 'lucide-react';

const SmellCard = ({ smell }) => {
  const {
    smell_type = 'Unknown Issue',
    description = 'No description available',
    severity = 'low',
    category = 'other',
    line_number = 0,
    column = 0,
    file_path = '',
    suggestion = '',
    confidence = 1,
    metadata = {}
  } = smell;

  const getSeverityIcon = () => {
    switch (severity) {
      case 'critical':
        return <XCircle className="w-5 h-5 text-red-500" />;
      case 'high':
        return <AlertTriangle className="w-5 h-5 text-orange-500" />;
      case 'medium':
        return <AlertTriangle className="w-5 h-5 text-yellow-500" />;
      case 'low':
        return <Info className="w-5 h-5 text-blue-500" />;
      default:
        return <Info className="w-5 h-5 text-gray-500" />;
    }
  };

  const getSeverityColor = () => {
    switch (severity) {
      case 'critical':
        return 'border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/20';
      case 'high':
        return 'border-orange-200 dark:border-orange-800 bg-orange-50 dark:bg-orange-900/20';
      case 'medium':
        return 'border-yellow-200 dark:border-yellow-800 bg-yellow-50 dark:bg-yellow-900/20';
      case 'low':
        return 'border-blue-200 dark:border-blue-800 bg-blue-50 dark:bg-blue-900/20';
      default:
        return 'border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50';
    }
  };

  const getSeverityBadge = () => {
    const baseClasses = 'px-2 py-1 text-xs font-medium rounded-full';
    switch (severity) {
      case 'critical':
        return `${baseClasses} bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300`;
      case 'high':
        return `${baseClasses} bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300`;
      case 'medium':
        return `${baseClasses} bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300`;
      case 'low':
        return `${baseClasses} bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300`;
      default:
        return `${baseClasses} bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-300`;
    }
  };

  const getCategoryIcon = () => {
    switch (category) {
      case 'security':
        return <XCircle className="w-4 h-4 text-red-500" />;
      case 'performance':
        return <Target className="w-4 h-4 text-green-500" />;
      case 'maintainability':
        return <Code className="w-4 h-4 text-blue-500" />;
      case 'complexity':
        return <AlertTriangle className="w-4 h-4 text-orange-500" />;
      default:
        return <Info className="w-4 h-4 text-gray-500" />;
    }
  };

  return (
    <div className={`rounded-lg border-2 p-6 transition-all hover:shadow-md ${getSeverityColor()}`}>
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          {getSeverityIcon()}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              {smell_type}
            </h3>
            <div className="flex items-center space-x-2 mt-1">
              <span className={getSeverityBadge()}>
                {severity.toUpperCase()}
              </span>
              <div className="flex items-center space-x-1 text-sm text-gray-600 dark:text-gray-400">
                {getCategoryIcon()}
                <span>{category}</span>
              </div>
            </div>
          </div>
        </div>
        
        <div className="text-right">
          <div className="text-sm text-gray-600 dark:text-gray-400">
            Confidence: {Math.round(confidence * 100)}%
          </div>
        </div>
      </div>

      <div className="mb-4">
        <p className="text-gray-800 dark:text-gray-200 leading-relaxed">
          {description}
        </p>
      </div>

      <div className="flex items-center space-x-4 mb-4 text-sm text-gray-600 dark:text-gray-400">
        <div className="flex items-center space-x-1">
          <MapPin className="w-4 h-4" />
          <span>Line {line_number}</span>
          {column > 0 && <span>, Col {column}</span>}
        </div>
        
        {file_path && (
          <div className="flex items-center space-x-1">
            <Code className="w-4 h-4" />
            <span className="truncate max-w-xs">{file_path}</span>
          </div>
        )}
      </div>

      {suggestion && (
        <div className="mt-4 p-4 bg-blue-50 dark:bg-blue-900/30 rounded-lg border border-blue-200 dark:border-blue-800">
          <div className="flex items-start space-x-2">
            <CheckCircle className="w-5 h-5 text-blue-500 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-medium text-blue-900 dark:text-blue-100 mb-1">
                Suggested Fix
              </h4>
              <p className="text-blue-800 dark:text-blue-200 text-sm">
                {suggestion}
              </p>
            </div>
          </div>
        </div>
      )}

      {metadata && Object.keys(metadata).length > 0 && (
        <div className="mt-4 p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
          <h4 className="font-medium text-gray-900 dark:text-white mb-2 text-sm">
            Additional Details
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {Object.entries(metadata).map(([key, value]) => (
              <div key={key} className="text-sm">
                <span className="font-medium text-gray-700 dark:text-gray-300">
                  {key.replace(/_/g, ' ')}:
                </span>
                <span className="text-gray-600 dark:text-gray-400 ml-2">
                  {String(value)}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default SmellCard;