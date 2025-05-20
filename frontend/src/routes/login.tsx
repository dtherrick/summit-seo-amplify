import { createFileRoute, Navigate } from '@tanstack/react-router';
import { LoginForm } from '../components/auth/LoginForm';
import { useAuth } from '../contexts/AuthContext'; // Adjust path as needed
import { Flex, Loader } from '@aws-amplify/ui-react';

export const Route = createFileRoute('/login')({
  component: LoginPage,
  // TanStack Router v1 allows defining search param validation in the route
  validateSearch: (search: Record<string, unknown>): { redirect?: string } => {
    return {
      redirect: typeof search.redirect === 'string' ? search.redirect : undefined,
    };
  },
});

function LoginPage() {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return (
      <Flex justifyContent="center" alignItems="center" minHeight="100vh">
        <Loader size="large" />
      </Flex>
    );
  }

  if (user) {
    // If user is already logged in, redirect them (e.g., to dashboard)
    // This could also use the 'redirect' search param if it makes sense
    return <Navigate to="/dashboard" replace />;
  }

  return <LoginForm />;
}