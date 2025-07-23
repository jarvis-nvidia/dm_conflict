import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API endpoints
export const apiEndpoints = {
  // Health check
  health: () => api.get('/health'),

  // Code Analysis
  analyzeCode: (data) => api.post('/api/v2/analyze-code-advanced', data),
  detectCodeSmells: (data) => api.post('/api/v2/detect-code-smells', data),
  
  // Learning System
  learnUserPattern: (data) => api.post('/api/v2/learn-user-pattern', data),
  getPersonalizedRecommendations: (data) => api.post('/api/v2/get-personalized-recommendations', data),
  getUserLearningProgress: (userId) => api.get(`/api/v2/user-learning-progress/${userId}`),
  
  // Repository Analysis
  processRepository: (data) => api.post('/api/process-repository', data),
  
  // General
  getSupportedLanguages: () => api.get('/api/v2/supported-languages'),
  getAgentStatus: () => api.get('/api/agent-status'),
  
  // RAG System
  queryCodebase: (data) => api.post('/api/query-codebase', data),
  
  // Code generation
  generateCommitMessage: (data) => api.post('/api/generate-commit', data),
  
  // Debug
  debugCode: (data) => api.post('/api/debug-code', data),
  reviewCode: (data) => api.post('/api/review-code', data),
};

export default api;