import { createFileRoute, Navigate } from '@tanstack/react-router';
import { ForgotPasswordForm } from '../components/auth/ForgotPasswordForm';
import { useAuth } from '../contexts/AuthContext'; // Adjust path as needed
import { Flex, Loader } from '@aws-amplify/ui-react';

export const Route = createFileRoute('/forgot-password')({
  component: ForgotPasswordPage,
});

function ForgotPasswordPage() {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return (
      <Flex justifyContent="center" alignItems="center" minHeight="100vh">
        <Loader size="large" />
      </Flex>
    );
  }

  if (user) {
    // If user is already logged in, they probably don't need to reset their password
    return <Navigate to="/dashboard" replace />;
  }

  return <ForgotPasswordForm />;
}