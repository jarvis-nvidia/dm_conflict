import React, { useState } from 'react';
import { Search, Github, Star, GitBranch, Calendar, ExternalLink } from 'lucide-react';

const RepositorySelector = ({ onSelect }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedRepo, setSelectedRepo] = useState(null);

  // Mock repositories for demonstration
  const repositories = [
    {
      id: 1,
      name: 'awesome-python',
      full_name: 'vinta/awesome-python',
      description: 'A curated list of awesome Python frameworks, libraries, software and resources',
      language: 'Python',
      stars: 156000,
      forks: 23000,
      updated_at: '2024-01-15T10:30:00Z',
      url: 'https://github.com/vinta/awesome-python',
      owner: {
        login: 'vinta',
        avatar_url: 'https://github.com/vinta.png'
      }
    },
    {
      id: 2,
      name: 'react',
      full_name: 'facebook/react',
      description: 'A declarative, efficient, and flexible JavaScript library for building user interfaces.',
      language: 'JavaScript',
      stars: 204000,
      forks: 42000,
      updated_at: '2024-01-14T15:45:00Z',
      url: 'https://github.com/facebook/react',
      owner: {
        login: 'facebook',
        avatar_url: 'https://github.com/facebook.png'
      }
    },
    {
      id: 3,
      name: 'tensorflow',
      full_name: 'tensorflow/tensorflow',
      description: 'An Open Source Machine Learning Framework for Everyone',
      language: 'C++',
      stars: 175000,
      forks: 88000,
      updated_at: '2024-01-13T08:20:00Z',
      url: 'https://github.com/tensorflow/tensorflow',
      owner: {
        login: 'tensorflow',
        avatar_url: 'https://github.com/tensorflow.png'
      }
    },
    {
      id: 4,
      name: 'django',
      full_name: 'django/django',
      description: 'The Web framework for perfectionists with deadlines.',
      language: 'Python',
      stars: 69000,
      forks: 29000,
      updated_at: '2024-01-12T12:30:00Z',
      url: 'https://github.com/django/django',
      owner: {
        login: 'django',
        avatar_url: 'https://github.com/django.png'
      }
    },
    {
      id: 5,
      name: 'vue',
      full_name: 'vuejs/vue',
      description: 'Vue.js is a progressive, incrementally-adoptable JavaScript framework for building UI on the web.',
      language: 'JavaScript',
      stars: 207000,
      forks: 33000,
      updated_at: '2024-01-11T16:15:00Z',
      url: 'https://github.com/vuejs/vue',
      owner: {
        login: 'vuejs',
        avatar_url: 'https://github.com/vuejs.png'
      }
    }
  ];

  const filteredRepos = repositories.filter(repo =>
    repo.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    repo.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
    repo.owner.login.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleRepoSelect = (repo) => {
    setSelectedRepo(repo);
    if (onSelect) {
      onSelect(repo);
    }
  };

  const formatNumber = (num) => {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getLanguageColor = (language) => {
    const colors = {
      Python: '#3776ab',
      JavaScript: '#f1e05a',
      'C++': '#f34b7d',
      Java: '#b07219',
      TypeScript: '#2b7489',
      Go: '#00ADD8',
      Rust: '#dea584',
      Ruby: '#701516'
    };
    return colors[language] || '#6b7280';
  };

  return (
    <div className="space-y-6">
      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search repositories..."
          className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        />
      </div>

      {/* Repository List */}
      <div className="space-y-4">
        {filteredRepos.map((repo) => (
          <div
            key={repo.id}
            className={`p-4 border rounded-lg cursor-pointer transition-all ${
              selectedRepo?.id === repo.id
                ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
            }`}
            onClick={() => handleRepoSelect(repo)}
          >
            <div className="flex items-start space-x-3">
              <img
                src={repo.owner.avatar_url}
                alt={repo.owner.login}
                className="w-10 h-10 rounded-full"
              />
              
              <div className="flex-1 min-w-0">
                <div className="flex items-center space-x-2 mb-1">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white truncate">
                    {repo.full_name}
                  </h3>
                  <a
                    href={repo.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-gray-500 hover:text-blue-500"
                    onClick={(e) => e.stopPropagation()}
                  >
                    <ExternalLink className="w-4 h-4" />
                  </a>
                </div>
                
                <p className="text-gray-600 dark:text-gray-400 text-sm mb-3 line-clamp-2">
                  {repo.description}
                </p>
                
                <div className="flex items-center space-x-4 text-sm text-gray-500 dark:text-gray-400">
                  <div className="flex items-center space-x-1">
                    <div
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: getLanguageColor(repo.language) }}
                    />
                    <span>{repo.language}</span>
                  </div>
                  
                  <div className="flex items-center space-x-1">
                    <Star className="w-4 h-4" />
                    <span>{formatNumber(repo.stars)}</span>
                  </div>
                  
                  <div className="flex items-center space-x-1">
                    <GitBranch className="w-4 h-4" />
                    <span>{formatNumber(repo.forks)}</span>
                  </div>
                  
                  <div className="flex items-center space-x-1">
                    <Calendar className="w-4 h-4" />
                    <span>{formatDate(repo.updated_at)}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredRepos.length === 0 && (
        <div className="text-center py-12">
          <Github className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
            No repositories found
          </h3>
          <p className="text-gray-600 dark:text-gray-400">
            Try adjusting your search term or browse popular repositories above.
          </p>
        </div>
      )}
    </div>
  );
};

export default RepositorySelector;