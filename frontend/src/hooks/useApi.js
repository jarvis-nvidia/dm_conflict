import { useState, useEffect } from 'react';
import { apiEndpoints } from '../utils/api';

export const useApi = (apiCall, dependencies = []) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!apiCall) return;

    const fetchData = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const response = await apiCall();
        setData(response.data);
      } catch (err) {
        setError(err.response?.data || err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, dependencies);

  return { data, loading, error };
};

export const useApiCall = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const execute = async (apiCall, onSuccess, onError) => {
    setLoading(true);
    setError(null);

    try {
      const response = await apiCall();
      if (onSuccess) onSuccess(response.data);
      return response.data;
    } catch (err) {
      const errorData = err.response?.data || err.message;
      setError(errorData);
      if (onError) onError(errorData);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { execute, loading, error };
};

// Custom hooks for specific API calls
export const useHealthCheck = () => {
  return useApi(apiEndpoints.health);
};

export const useSupportedLanguages = () => {
  return useApi(apiEndpoints.getSupportedLanguages);
};

export const useAgentStatus = () => {
  return useApi(apiEndpoints.getAgentStatus);
};

export const useUserProgress = (userId) => {
  return useApi(
    userId ? () => apiEndpoints.getUserLearningProgress(userId) : null,
    [userId]
  );
};