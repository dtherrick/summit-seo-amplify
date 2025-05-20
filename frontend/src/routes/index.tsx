import { createFileRoute, Navigate } from '@tanstack/react-router';
import LandingPageContent from '../components/marketing/LandingPageContent';
import { Layout } from '../components/common/Layout'; // Adjust if path is different
import { useAuth } from '../contexts/AuthContext'; // Adjust path as needed

export const Route = createFileRoute('/')({
  component: IndexPage,
});

function IndexPage() {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    // You might want a more sophisticated loading indicator here or handle it in __root.tsx
    return (
      <Layout showNav={false}>
        <div>Loading...</div>
      </Layout>
    );
  }

  if (user) {
    // If user is logged in, redirect to dashboard or onboarding based on survey status
    // This logic might be more complex depending on your requirements, e.g. checking user.has_completed_survey
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <Layout showNav={false}>
      <LandingPageContent />
    </Layout>
  );
}