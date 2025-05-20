import React, { useState } from 'react';
import { useNavigate, useSearch } from '@tanstack/react-router';
import { useAuth } from '../../contexts/AuthContext'; // Adjust path as needed
import {
  Button,
  Flex,
  Heading,
  PasswordField,
  Text,
  TextField,
  View,
  Alert,
  Card,
} from '@aws-amplify/ui-react';

// Define the type for the search params we expect for redirection
interface LoginSearch {
  redirect?: string;
}

export const LoginForm: React.FC = () => {
  const navigate = useNavigate();
  const { handleSignIn, isLoading, error: authError } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [formError, setFormError] = useState<string | null>(null);

  // Get the redirect path from search params, if any
  const search: LoginSearch = useSearch({ from: '/login' });
  const redirectPath = search.redirect || '/dashboard';

  const onSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setFormError(null);
    if (!username || !password) {
      setFormError('Username and password are required.');
      return;
    }
    try {
      await handleSignIn({ username, password });
      navigate({ to: redirectPath, replace: true });
    } catch (err) {
      // err is already set in AuthContext, but we might want specific form error messages
      if (err instanceof Error) {
        setFormError(err.message || 'Login failed. Please check your credentials.');
      } else {
        setFormError('An unexpected error occurred during login.');
      }
    }
  };

  return (
    <Flex justifyContent="center" alignItems="center" paddingTop="xl" className="min-h-[calc(100vh-150px)]">
      <Card variation="outlined" width={{ base: '90%', medium: '400px' }} padding="large">
        <Heading level={3} textAlign="center" marginBottom="medium">
          Login to Summit SEO
        </Heading>
        <form onSubmit={onSubmit}>
          <Flex direction="column" gap="medium">
            <TextField
              label="Email"
              name="username" // Cognito uses 'username', which can be email
              type="email"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              isRequired
              disabled={isLoading}
            />
            <PasswordField
              label="Password"
              name="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              isRequired
              disabled={isLoading}
            />
            {(formError || authError) && (
              <Alert variation="error" isDismissible={true} onDismiss={() => setFormError(null)}>
                {formError || authError?.message}
              </Alert>
            )}
            <Button type="submit" variation="primary" isLoading={isLoading} isFullWidth>
              Login
            </Button>
            <View textAlign="center">
              <Text fontSize="small">
                Don't have an account?{' '}
                <Button variation="link" size="small" onClick={() => navigate({ to: '/signup' })}>
                  Sign Up
                </Button>
              </Text>
              <Text fontSize="small" marginTop="xs">
                <Button variation="link" size="small" onClick={() => navigate({ to: '/forgot-password' })}> {/* Placeholder for forgot password */}
                  Forgot Password?
                </Button>
              </Text>
            </View>
          </Flex>
        </form>
      </Card>
    </Flex>
  );
};