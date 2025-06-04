import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import {
  getCurrentUser,
  signOut as amplifySignOut,
  type SignUpInput,
  signIn,
  confirmSignUp,
  resendSignUpCode,
  resetPassword,
  confirmResetPassword,
  signUp as amplifySignUp
} from 'aws-amplify/auth';
import type { AuthUser, SignUpOutput, SignInOutput } from 'aws-amplify/auth';

interface AuthContextType {
  user: AuthUser | null;
  isLoading: boolean;
  error: Error | null;
  fetchCurrentUser: () => Promise<void>;
  handleSignIn: (input: { username: string; password?: string }) => Promise<SignInOutput>;
  handleSignOut: () => Promise<void>;
  handleSignUp: (input: SignUpInput) => Promise<SignUpOutput>;
  handleConfirmSignUp: (input: { username: string; confirmationCode: string }) => Promise<void>;
  handleResendSignUpCode: (input: { username: string }) => Promise<void>;
  handleForgotPassword: (input: { username: string }) => Promise<void>;
  handleConfirmForgotPassword: (input: { username: string; newPassword: string; confirmationCode: string }) => Promise<void>;
  // TODO: Add types for other auth functions if needed (e.g., federated sign-in)
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchCurrentUser = async () => {
    setIsLoading(true);
    try {
      const currentUser = await getCurrentUser();
      setUser(currentUser);
      // Optionally, fetch session to get tokens if needed elsewhere
      // await fetchAuthSession();
    } catch (err) {
      setUser(null);
      // Don't setError here, as it's normal not to have a user initially
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchCurrentUser();
  }, []);

  const handleSignIn = async (input: { username: string; password?: string }) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await signIn(input);
      await fetchCurrentUser(); // Re-fetch user after sign-in
      return result;
    } catch (err: any) {
      setError(err);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const handleSignOut = async () => {
    setIsLoading(true);
    setError(null);
    try {
      await amplifySignOut();
      setUser(null);
    } catch (err: any) {
      setError(err);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const handleSignUp = async (input: SignUpInput) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await amplifySignUp(input);
      return result;
    } catch (err: any) {
      setError(err);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const handleConfirmSignUp = async (input: { username: string; confirmationCode: string }) => {
    setIsLoading(true);
    setError(null);
    try {
      await confirmSignUp(input);
    } catch (err: any) {
      setError(err);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const handleResendSignUpCode = async (input: { username: string }) => {
    setIsLoading(true);
    setError(null);
    try {
      await resendSignUpCode(input);
    } catch (err: any) {
      setError(err);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const handleForgotPassword = async (input: { username: string }) => {
    setIsLoading(true);
    setError(null);
    try {
      await resetPassword(input);
    } catch (err: any) {
      setError(err);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

 const handleConfirmForgotPassword = async (input: { username: string; newPassword: string; confirmationCode: string }) => {
    setIsLoading(true);
    setError(null);
    try {
      await confirmResetPassword({
        username: input.username,
        newPassword: input.newPassword,
        confirmationCode: input.confirmationCode
      });
    } catch (err: any) {
      setError(err);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthContext.Provider value={{
      user,
      isLoading,
      error,
      fetchCurrentUser,
      handleSignIn,
      handleSignOut,
      handleSignUp,
      handleConfirmSignUp,
      handleResendSignUpCode,
      handleForgotPassword,
      handleConfirmForgotPassword
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};