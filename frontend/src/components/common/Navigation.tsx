import React from 'react';
import { Link } from '@tanstack/react-router';
import { View, Flex, Button, Heading, useTheme } from '@aws-amplify/ui-react';
import { useAuth } from '../../contexts/AuthContext'; // Adjust path as needed

export const Navigation: React.FC = () => {
  const { tokens } = useTheme();
  const { user, handleSignOut, isLoading } = useAuth();

  return (
    <View
      as="nav"
      backgroundColor={tokens.colors.background.secondary}
      padding={`${tokens.space.medium} ${tokens.space.large}`}
      className="shadow-md"
    >
      <Flex justifyContent="space-between" alignItems="center">
        <Link to="/">
          <Heading level={3} className="text-blue-600 hover:text-blue-800 transition-colors">
            Summit SEO
          </Heading>
        </Link>
        <Flex alignItems="center" gap={tokens.space.small}>
          {user ? (
            <>
              <Link to="/dashboard">
                <Button variation="link" size="small">Dashboard</Button>
              </Link>
              {/* Add other authenticated links here, e.g., /settings */}
              <Button variation="primary" size="small" onClick={handleSignOut} isLoading={isLoading}>
                Sign Out
              </Button>
            </>
          ) : (
            <>
              <Link to="/login">
                <Button variation="link" size="small">Login</Button>
              </Link>
              <Link to="/signup">
                <Button variation="primary" size="small">Sign Up</Button>
              </Link>
            </>
          )}
        </Flex>
      </Flex>
    </View>
  );
};