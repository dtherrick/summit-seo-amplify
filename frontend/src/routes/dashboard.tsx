import { createFileRoute } from '@tanstack/react-router';
import { ProtectedRoute } from '../components/auth/ProtectedRoute'; // Adjust path as needed
import { Heading, View, Text } from '@aws-amplify/ui-react';
import { useAuth } from '../contexts/AuthContext'; // Adjust path as needed

export const Route = createFileRoute('/dashboard')({
  component: DashboardPage,
});

function DashboardPlaceholder() {
  const { user } = useAuth();
  return (
    <View padding="large">
      <Heading level={2} marginBottom="medium">Dashboard</Heading>
      <Text>Welcome back, {user?.signInDetails?.loginId || user?.username || 'User'}!</Text>
      <Text marginTop="medium">Your personalized SEO dashboard is coming soon.</Text>
      {/* Placeholder for future content like survey summary, analysis section, etc. */}
    </View>
  );
}

function DashboardPage() {
  return (
    <ProtectedRoute>
      <DashboardPlaceholder />
    </ProtectedRoute>
  );
}