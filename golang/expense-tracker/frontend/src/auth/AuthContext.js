// Cache-busting comment
import React, { createContext, useState, useEffect } from 'react';
import { login as loginApi, signup as signupApi } from '../services/api';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));

  useEffect(() => {
    if (token) {
      // A real app would validate the token with the backend
      // For this example, we'll just decode it
      try {
        const decoded = JSON.parse(atob(token.split('.')[1]));
        setUser({ username: decoded.username, id: decoded.user_id });
      } catch (e) {
        console.error('Invalid token', e);
        setToken(null);
        localStorage.removeItem('token');
      }
    } 
  }, [token]);

  const login = async (username, password) => {
    const response = await loginApi(username, password);
    const { token } = response.data;
    setToken(token);
    localStorage.setItem('token', token);
  };

  const signup = async (username, password) => {
    await signupApi(username, password);
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
  };

  return (
    <AuthContext.Provider value={{ user, token, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
