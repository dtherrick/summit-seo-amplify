import { createFileRoute, Navigate } from '@tanstack/react-router';
import { ConfirmSignupForm } from '../components/auth/ConfirmSignupForm';
import { useAuth } from '../contexts/AuthContext'; // Adjust path as needed
import { Flex, Loader } from '@aws-amplify/ui-react';

export const Route = createFileRoute('/confirm-signup')({
  component: ConfirmSignupPage,
  validateSearch: (search: Record<string, unknown>): { username?: string } => {
    return {
      username: typeof search.username === 'string' ? search.username : undefined,
    };
  },
});

function ConfirmSignupPage() {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return (
      <Flex justifyContent="center" alignItems="center" minHeight="100vh">
        <Loader size="large" />
      </Flex>
    );
  }

  if (user) {
    // If user is somehow already logged in, redirect them
    return <Navigate to="/dashboard" replace />;
  }

  return <ConfirmSignupForm />;
}