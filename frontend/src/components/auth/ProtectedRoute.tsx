import React, { ReactNode } from 'react';
import { Navigate, useLocation } from '@tanstack/react-router';
import { useAuth } from '../../contexts/AuthContext'; // Adjust path as needed
import { Flex, Loader } from '@aws-amplify/ui-react';

interface ProtectedRouteProps {
  children: ReactNode;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { user, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return (
      <Flex justifyContent="center" alignItems="center" minHeight="80vh">
        <Loader size="large" />
      </Flex>
    );
  }

  if (!user) {
    // Redirect them to the /login page, but save the current location they were
    // trying to go to when they were redirected. This allows us to send them
    // along to that page after they login, which is a nicer user experience
    // than dropping them off on the home page.
    return <Navigate to="/login" search={{ redirect: location.href }} />;
  }

  return <>{children}</>;
};