import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api',
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const login = (username, password) => {
  return apiClient.post('/auth/login', { username, password });
};

export const signup = (username, password) => {
  return apiClient.post('/auth/register', { username, password });
};

export const getExpenses = () => {
  return apiClient.get('/expenses');
};

export const createExpense = (expense) => {
  return apiClient.post('/expenses', expense);
};

export const deleteExpense = (id) => {
  return apiClient.delete(`/expenses/${id}`);
};

export const getSummary = (period) => {
  return apiClient.get(`/expenses/summary?period=${period}`);
};
