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
  // Add other business-related fields if needed, e.g., businessName
  // const [businessName, setBusinessName] = useState('');
  const [formError, setFormError] = useState<string | null>(null);

  const onSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setFormError(null);
    if (password !== confirmPassword) {
      setFormError('Passwords do not match.');
      return;
    }
    if (!email || !password) {
      setFormError('Email and password are required.');
      return;
    }

    const signUpInput: SignUpInput = {
      username: email, // Cognito uses username, which will be the email
      password: password,
      options: {
        userAttributes: {
          email: email, // Standard attribute
          // Add custom attributes here, prefixed with 'custom:'
          // e.g., 'custom:business_name': businessName,
        },
        // autoSignIn: true // Optional: attempt to sign in user after successful sign up
      },
    };

    try {
      const result = await handleSignUp(signUpInput);
      // If sign up requires confirmation, navigate to a confirmation page
      if (result.nextStep.signUpStep === 'CONFIRM_SIGN_UP') {
        navigate({ to: '/confirm-signup', search: { username: email } });
      } else {
        // If autoSignIn is enabled and successful, or if no confirmation needed
        navigate({ to: '/dashboard' }); // Or to onboarding if that's the next step
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
              hasShowPasswordToggle
              disabled={isLoading}
              // Consider adding password strength indicator or policy display
            />
            <PasswordField
              label="Confirm Password"
              name="confirmPassword"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              isRequired
              hasShowPasswordToggle
              disabled={isLoading}
            />
            {/* Example for a custom attribute (uncomment and adjust if needed)
            <TextField
              label="Business Name"
              name="businessName"
              value={businessName}
              onChange={(e) => setBusinessName(e.target.value)}
              // isRequired if applicable
              disabled={isLoading}
            />
            */}
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