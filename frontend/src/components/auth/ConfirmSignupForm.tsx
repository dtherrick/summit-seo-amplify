import React, { useState, useEffect } from 'react';
import { useNavigate, useSearch } from '@tanstack/react-router';
import { useAuth } from '../../contexts/AuthContext'; // Adjust path as needed
import {
  Button,
  Flex,
  Heading,
  TextField,
  View,
  Alert,
  Card,
  Text,
} from '@aws-amplify/ui-react';

interface ConfirmSignupSearch {
  username?: string;
}

export const ConfirmSignupForm: React.FC = () => {
  const navigate = useNavigate();
  const { handleConfirmSignUp, handleResendSignUpCode, isLoading, error: authError } = useAuth();
  const search: ConfirmSignupSearch = useSearch({ from: '/confirm-signup' });

  const [username, setUsername] = useState(search.username || '');
  const [confirmationCode, setConfirmationCode] = useState('');
  const [formError, setFormError] = useState<string | null>(null);
  const [resendMessage, setResendMessage] = useState<string | null>(null);

  useEffect(() => {
    if (search.username) {
      setUsername(search.username);
    }
  }, [search.username]);

  const onSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setFormError(null);
    if (!username || !confirmationCode) {
      setFormError('Username and confirmation code are required.');
      return;
    }
    try {
      await handleConfirmSignUp({ username, confirmationCode });
      // On successful confirmation, redirect to login or auto-sign-in if configured
      navigate({ to: '/login', search: { confirmed: true } });
    } catch (err) {
      if (err instanceof Error) {
        setFormError(err.message || 'Confirmation failed. Please check the code and try again.');
      } else {
        setFormError('An unexpected error occurred during confirmation.');
      }
    }
  };

  const onResendCode = async () => {
    setFormError(null);
    setResendMessage(null);
    if (!username) {
      setFormError('Username (email) is required to resend code.');
      return;
    }
    try {
      await handleResendSignUpCode({ username });
      setResendMessage('Confirmation code resent successfully.');
    } catch (err) {
      if (err instanceof Error) {
        setFormError(err.message || 'Failed to resend code.');
      } else {
        setFormError('An unexpected error occurred while resending code.');
      }
    }
  };

  return (
    <Flex justifyContent="center" alignItems="center" paddingTop="xl" className="min-h-[calc(100vh-150px)]">
      <Card variation="outlined" width={{ base: '90%', medium: '400px' }} padding="large">
        <Heading level={3} textAlign="center" marginBottom="medium">
          Confirm Your Account
        </Heading>
        <form onSubmit={onSubmit}>
          <Flex direction="column" gap="medium">
            <Text>A confirmation code has been sent to your email. Please enter it below.</Text>
            <TextField
              label="Email (Username)"
              name="username"
              type="email"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              isRequired
              disabled={isLoading || !!search.username} // Disable if username came from search param
            />
            <TextField
              label="Confirmation Code"
              name="confirmationCode"
              value={confirmationCode}
              onChange={(e) => setConfirmationCode(e.target.value)}
              isRequired
              disabled={isLoading}
            />
            {(formError || authError) && (
              <Alert variation="error" isDismissible={true} onDismiss={() => setFormError(null)}>
                {formError || authError?.message}
              </Alert>
            )}
            {resendMessage && (
              <Alert variation="success" isDismissible={true} onDismiss={() => setResendMessage(null)}>
                {resendMessage}
              </Alert>
            )}
            <Button type="submit" variation="primary" isLoading={isLoading} isFullWidth>
              Confirm Account
            </Button>
            <Button variation="link" size="small" onClick={onResendCode} disabled={isLoading || !username} isFullWidth>
              Resend Code
            </Button>
          </Flex>
        </form>
        <View textAlign="center" marginTop="medium">
          <Button variation="link" size="small" onClick={() => navigate({ to: '/login' })}>
            Back to Login
          </Button>
        </View>
      </Card>
    </Flex>
  );
};