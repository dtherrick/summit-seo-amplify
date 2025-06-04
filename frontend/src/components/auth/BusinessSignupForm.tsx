import React, { useState } from 'react';
import { useNavigate } from '@tanstack/react-router';
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
import type { SignUpInput } from 'aws-amplify/auth';

export const BusinessSignupForm: React.FC = () => {
  const navigate = useNavigate();
  const { handleSignUp, isLoading, error: authError } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [businessName, setBusinessName] = useState('');
  const [businessWebsite, setBusinessWebsite] = useState('');
  const [formError, setFormError] = useState<string | null>(null);

  const onSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setFormError(null);
    if (password !== confirmPassword) {
      setFormError('Passwords do not match.');
      return;
    }
    if (!email || !password || !businessName || !businessWebsite) {
      setFormError('Email, password, business name, and business website are required.');
      return;
    }

    const newTenantId = crypto.randomUUID();

    const signUpInput: SignUpInput = {
      username: email,
      password: password,
      options: {
        userAttributes: {
          email: email,
          'custom:tenant_id': newTenantId,
          'custom:business_name': businessName,
          'custom:business_website': businessWebsite,
        },
      },
    };

    try {
      const result = await handleSignUp(signUpInput);
      if (result.nextStep.signUpStep === 'CONFIRM_SIGN_UP') {
        navigate({ to: '/confirm-signup', search: { username: email } });
      } else {
        navigate({ to: '/dashboard' });
      }
    } catch (err) {
      if (err instanceof Error) {
        setFormError(err.message || 'Sign up failed. Please try again.');
      } else {
        setFormError('An unexpected error occurred during sign up.');
      }
    }
  };

  return (
    <Flex justifyContent="center" alignItems="center" paddingTop="xl" className="min-h-[calc(100vh-150px)]">
      <Card variation="outlined" width={{ base: '90%', medium: '450px' }} padding="large">
        <Heading level={3} textAlign="center" marginBottom="medium">
          Create Your Account
        </Heading>
        <form onSubmit={onSubmit}>
          <Flex direction="column" gap="medium">
            <TextField
              label="Business Name"
              name="businessName"
              value={businessName}
              onChange={(e) => setBusinessName(e.target.value)}
              isRequired
              disabled={isLoading}
            />
            <TextField
              label="Business Website URL"
              name="businessWebsite"
              type="url"
              value={businessWebsite}
              onChange={(e) => setBusinessWebsite(e.target.value)}
              placeholder="https://example.com"
              isRequired
              disabled={isLoading}
            />
            <TextField
              label="Email"
              name="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
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
            <PasswordField
              label="Confirm Password"
              name="confirmPassword"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              isRequired
              disabled={isLoading}
            />
            {(formError || authError) && (
              <Alert variation="error" isDismissible={true} onDismiss={() => setFormError(null)}>
                {formError || authError?.message}
              </Alert>
            )}
            <Button type="submit" variation="primary" isLoading={isLoading} isFullWidth>
              Sign Up
            </Button>
            <View textAlign="center">
              <Text fontSize="small">
                Already have an account?{' '}
                <Button variation="link" size="small" onClick={() => navigate({ to: '/login' })}>
                  Login
                </Button>
              </Text>
            </View>
          </Flex>
        </form>
      </Card>
    </Flex>
  );
};