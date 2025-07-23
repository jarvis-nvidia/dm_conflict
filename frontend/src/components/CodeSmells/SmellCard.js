import React from 'react';
import { ArrowRight, AlertTriangle, AlertCircle, Info } from 'lucide-react';

const SmellCard = ({ smell }) => {
  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'high':
        return 'text-red-400';
      case 'medium':
        return 'text-yellow-400';
      case 'low':
        return 'text-blue-400';
      default:
        return 'text-gray-400';
    }
  };

  const getSeverityIcon = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'high':
        return <AlertTriangle className="w-4 h-4" />;
      case 'medium':
        return <AlertCircle className="w-4 h-4" />;
      case 'low':
        return <Info className="w-4 h-4" />;
      default:
        return <Info className="w-4 h-4" />;
    }
  };

  return (
    <div className="p-4">
      <div className="flex items-stretch justify-between gap-4 rounded-lg">
        <div className="flex flex-[2_2_0px] flex-col gap-4">
          <div className="flex flex-col gap-1">
            <div className="flex items-center gap-2">
              <span className={getSeverityColor(smell.severity)}>
                {getSeverityIcon(smell.severity)}
              </span>
              <p className="text-white text-base font-bold leading-tight">
                {smell.smell_type || smell.type || 'Code Smell'}
              </p>
              <span className={`px-2 py-1 text-xs rounded-full ${getSeverityColor(smell.severity)} bg-opacity-20`}>
                {smell.severity || 'Unknown'}
              </span>
            </div>
            <p className="text-[#9cabba] text-sm font-normal leading-normal">
              {smell.description}
            </p>
            {smell.suggestion && (
              <p className="text-blue-300 text-sm font-normal leading-normal mt-2">
                <strong>Suggestion:</strong> {smell.suggestion}
              </p>
            )}
          </div>
          {smell.line_number && (
            <button className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-8 px-4 flex-row-reverse bg-[#283039] text-white pr-2 gap-1 text-sm font-medium leading-normal w-fit hover:bg-[#3b4754] transition-colors">
              <ArrowRight className="w-4 h-4" />
              <span className="truncate">Line {smell.line_number || smell.line}</span>
            </button>
          )}
        </div>
        <div
          className="w-full bg-center bg-no-repeat aspect-video bg-cover rounded-lg flex-1"
          style={{backgroundImage: "url('https://images.unsplash.com/photo-1744324472890-d4cac1650e2e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzl8MHwxfHNlYXJjaHwyfHxnZW9tZXRyaWMlMjBicmFpbnxlbnwwfHx8fDE3NTMyOTA4NjF8MA&ixlib=rb-4.1.0&q=85')"}}
        />
      </div>
    </div>
  );
};

export default SmellCard;