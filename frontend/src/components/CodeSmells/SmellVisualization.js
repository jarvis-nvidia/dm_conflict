import React from 'react';

const SmellVisualization = ({ smells = [] }) => {
  // Process smell data for visualization
  const smellCategories = smells.reduce((acc, smell) => {
    const category = smell.category || smell.smell_type || 'Unknown';
    acc[category] = (acc[category] || 0) + 1;
    return acc;
  }, {});

  const categories = Object.keys(smellCategories);
  const maxCount = Math.max(...Object.values(smellCategories), 1);

  // If no smells, show empty state
  if (smells.length === 0) {
    return (
      <div className="flex flex-wrap gap-4 px-4 py-6">
        <div className="flex min-w-72 flex-1 flex-col gap-2 rounded-lg border border-[#3b4754] p-6">
          <p className="text-white text-base font-medium leading-normal">Code Smell Distribution</p>
          <div className="flex items-center justify-center min-h-[180px]">
            <p className="text-[#9cabba] text-sm">No code smells detected yet</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-wrap gap-4 px-4 py-6">
      <div className="flex min-w-72 flex-1 flex-col gap-2 rounded-lg border border-[#3b4754] p-6">
        <p className="text-white text-base font-medium leading-normal">Code Smell Distribution</p>
        <div className="grid min-h-[180px] grid-flow-col gap-6 grid-rows-[1fr_auto] items-end justify-items-center px-3">
          {categories.slice(0, 4).map((category) => {
            const count = smellCategories[category];
            const height = (count / maxCount) * 100;
            
            return (
              <React.Fragment key={category}>
                <div 
                  className="border-[#9cabba] bg-[#283039] border-t-2 w-full transition-all duration-300 hover:bg-[#3b4754]" 
                  style={{ height: `${height}%` }}
                  title={`${category}: ${count} issues`}
                />
                <p className="text-[#9cabba] text-[13px] font-bold leading-normal tracking-[0.015em] text-center">
                  {category.length > 12 ? category.substring(0, 10) + '...' : category}
                </p>
              </React.Fragment>
            );
          })}
          
          {/* Fill empty slots if less than 4 categories */}
          {categories.length < 4 && Array.from({ length: 4 - categories.length }).map((_, index) => (
            <React.Fragment key={`empty-${index}`}>
              <div className="border-[#9cabba] bg-[#283039] border-t-2 w-full opacity-30" style={{ height: '10%' }} />
              <p className="text-[#9cabba] text-[13px] font-bold leading-normal tracking-[0.015em] opacity-30">-</p>
            </React.Fragment>
          ))}
        </div>
        
        <div className="mt-4 text-xs text-[#9cabba] text-center">
          Total issues: {smells.length}
        </div>
      </div>
    </div>
  );
};

export default SmellVisualization;