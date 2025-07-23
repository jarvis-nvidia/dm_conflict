import React from 'react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line
} from 'recharts';

const SmellVisualization = ({ smells = [] }) => {
  if (!smells || smells.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Code Smell Analysis
        </h3>
        <div className="text-center py-8">
          <p className="text-gray-600 dark:text-gray-400">
            No data available for visualization
          </p>
        </div>
      </div>
    );
  }

  // Process data for visualizations
  const severityData = smells.reduce((acc, smell) => {
    const severity = smell.severity || 'unknown';
    acc[severity] = (acc[severity] || 0) + 1;
    return acc;
  }, {});

  const categoryData = smells.reduce((acc, smell) => {
    const category = smell.category || 'other';
    acc[category] = (acc[category] || 0) + 1;
    return acc;
  }, {});

  const severityChartData = Object.entries(severityData).map(([severity, count]) => ({
    name: severity,
    count,
    fill: getSeverityColor(severity)
  }));

  const categoryChartData = Object.entries(categoryData).map(([category, count]) => ({
    name: category,
    value: count,
    fill: getCategoryColor(category)
  }));

  // Confidence distribution
  const confidenceData = smells.reduce((acc, smell) => {
    const confidence = Math.round((smell.confidence || 0) * 100);
    const range = Math.floor(confidence / 10) * 10;
    const rangeKey = `${range}-${range + 9}%`;
    acc[rangeKey] = (acc[rangeKey] || 0) + 1;
    return acc;
  }, {});

  const confidenceChartData = Object.entries(confidenceData).map(([range, count]) => ({
    name: range,
    count
  }));

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Severity Distribution */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Issues by Severity
        </h3>
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={severityChartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis 
              dataKey="name" 
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
            <Bar dataKey="count" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Category Distribution */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Issues by Category
        </h3>
        <ResponsiveContainer width="100%" height={200}>
          <PieChart>
            <Pie
              data={categoryChartData}
              cx="50%"
              cy="50%"
              innerRadius={40}
              outerRadius={80}
              paddingAngle={5}
              dataKey="value"
            >
              {categoryChartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.fill} />
              ))}
            </Pie>
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#1F2937', 
                border: '1px solid #374151',
                borderRadius: '6px',
                color: '#F3F4F6'
              }}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Confidence Distribution */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Confidence Distribution
        </h3>
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={confidenceChartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis 
              dataKey="name" 
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
              dataKey="count" 
              stroke="#3B82F6" 
              strokeWidth={2}
              dot={{ fill: '#3B82F6' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

// Helper functions
const getSeverityColor = (severity) => {
  const colors = {
    critical: '#DC2626',
    high: '#EA580C',
    medium: '#D97706',
    low: '#059669',
    unknown: '#6B7280'
  };
  return colors[severity] || colors.unknown;
};

const getCategoryColor = (category) => {
  const colors = {
    security: '#DC2626',
    performance: '#059669',
    maintainability: '#3B82F6',
    complexity: '#D97706',
    style: '#8B5CF6',
    other: '#6B7280'
  };
  return colors[category] || colors.other;
};

export default SmellVisualization;