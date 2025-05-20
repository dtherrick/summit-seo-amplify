import React, { useState } from 'react';
import { useNavigate } from '@tanstack/react-router';
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
  PasswordField,
} from '@aws-amplify/ui-react';

export const ForgotPasswordForm: React.FC = () => {
  const navigate = useNavigate();
  const { handleForgotPassword, handleConfirmForgotPassword, isLoading, error: authError } = useAuth();
  const [username, setUsername] = useState('');
  const [confirmationCode, setConfirmationCode] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [formError, setFormError] = useState<string | null>(null);
  const [step, setStep] = useState<'request' | 'confirm'>('request');

  const onRequestCode = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setFormError(null);
    if (!username) {
      setFormError('Email is required.');
      return;
    }
    try {
      await handleForgotPassword({ username });
      setStep('confirm');
    } catch (err) {
      if (err instanceof Error) {
        setFormError(err.message || 'Failed to request password reset. Please try again.');
      } else {
        setFormError('An unexpected error occurred.');
      }
    }
  };

  const onConfirmReset = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setFormError(null);
    if (!confirmationCode || !newPassword) {
      setFormError('Confirmation code and new password are required.');
      return;
    }
    try {
      await handleConfirmForgotPassword({ username, confirmationCode, newPassword });
      navigate({ to: '/login' }); // Redirect to login on success
    } catch (err) {
      if (err instanceof Error) {
        setFormError(err.message || 'Failed to reset password. Please check the code and try again.');
      } else {
        setFormError('An unexpected error occurred.');
      }
    }
  };

  return (
    <Flex justifyContent="center" alignItems="center" paddingTop="xl" className="min-h-[calc(100vh-150px)]">
      <Card variation="outlined" width={{ base: '90%', medium: '400px' }} padding="large">
        <Heading level={3} textAlign="center" marginBottom="medium">
          Reset Password
        </Heading>
        {step === 'request' ? (
          <form onSubmit={onRequestCode}>
            <Flex direction="column" gap="medium">
              <Text>Enter your email address and we'll send you a code to reset your password.</Text>
              <TextField
                label="Email"
                name="username"
                type="email"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                isRequired
                disabled={isLoading}
              />
              {(formError || authError) && (
                <Alert variation="error" isDismissible={true} onDismiss={() => setFormError(null)}>
                  {formError || authError?.message}
                </Alert>
              )}
              <Button type="submit" variation="primary" isLoading={isLoading} isFullWidth>
                Send Code
              </Button>
            </Flex>
          </form>
        ) : (
          <form onSubmit={onConfirmReset}>
            <Flex direction="column" gap="medium">
              <Text>A confirmation code has been sent to {username}. Enter the code and your new password.</Text>
              <TextField
                label="Confirmation Code"
                name="confirmationCode"
                value={confirmationCode}
                onChange={(e) => setConfirmationCode(e.target.value)}
                isRequired
                disabled={isLoading}
              />
              <PasswordField
                label="New Password"
                name="newPassword"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                isRequired
                disabled={isLoading}
                // Add password policies/rules display here if desired
              />
              {(formError || authError) && (
                <Alert variation="error" isDismissible={true} onDismiss={() => setFormError(null)}>
                  {formError || authError?.message}
                </Alert>
              )}
              <Button type="submit" variation="primary" isLoading={isLoading} isFullWidth>
                Reset Password
              </Button>
            </Flex>
          </form>
        )}
        <View textAlign="center" marginTop="medium">
          <Button variation="link" size="small" onClick={() => navigate({ to: '/login' })}>
            Back to Login
          </Button>
        </View>
      </Card>
    </Flex>
  );
};