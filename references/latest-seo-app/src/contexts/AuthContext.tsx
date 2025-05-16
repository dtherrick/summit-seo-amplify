import { createContext, useContext, useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import axios from 'axios';

// Configure axios base URL
axios.defaults.baseURL = 'http://localhost:8000';

interface User {
  id: string;
  email: string;
  business_id: string;
  roles: string[];
  has_completed_survey?: boolean;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  error: Error | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  signupBusiness: (name: string, email: string, password: string) => Promise<void>;
  markSurveyCompleted: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const queryClient = useQueryClient();

  // Query to fetch current user
  const { isLoading, error } = useQuery({
    queryKey: ['user'],
    queryFn: async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) return null;

        const { data } = await axios.get<User>('/api/v1/auth/users/me', {
          headers: { Authorization: `Bearer ${token}` }
        });
        setUser(data);
        return data;
      } catch (error) {
        localStorage.removeItem('token');
        setUser(null);
        throw error;
      }
    },
    retry: false
  });

  // Login mutation
  const loginMutation = useMutation({
    mutationFn: async ({ email, password }: { email: string; password: string }) => {
      const { data } = await axios.post('/api/v1/auth/login', { email, password });
      return data;
    },
    onSuccess: (data) => {
      localStorage.setItem('token', data.access_token);
      queryClient.invalidateQueries({ queryKey: ['user'] });
    }
  });

  // Business signup mutation
  const signupMutation = useMutation({
    mutationFn: async ({
      name,
      email,
      password
    }: {
      name: string;
      email: string;
      password: string;
    }) => {
      const { data } = await axios.post('/api/v1/auth/business/signup', {
        name,
        admin_email: email,
        admin_password: password
      });
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['user'] });
    }
  });

  // Logout function
  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
    queryClient.clear();
  };

  // Mark survey as completed
  const markSurveyCompleted = () => {
    if (user) {
      setUser({ ...user, has_completed_survey: true });
    }
  };

  // Set up axios interceptor for authentication
  useEffect(() => {
    const interceptor = axios.interceptors.request.use((config) => {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    return () => {
      axios.interceptors.request.eject(interceptor);
    };
  }, []);

  const value = {
    user,
    isLoading,
    error,
    login: (email: string, password: string) =>
      loginMutation.mutateAsync({ email, password }),
    logout,
    signupBusiness: (name: string, email: string, password: string) =>
      signupMutation.mutateAsync({ name, email, password }),
    markSurveyCompleted
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
} 