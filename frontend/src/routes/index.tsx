import { createFileRoute, Navigate } from '@tanstack/react-router';
import { LandingPage } from '../pages/LandingPage'; // Corrected import
import { useAuth } from '../contexts/AuthContext'; // Adjust path as needed

export const Route = createFileRoute('/')({
  component: IndexPage,
});

function IndexPage() {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    // You might want a more sophisticated loading indicator here or handle it in __root.tsx
    // Consider if LandingPage itself has a loading state or can be shown.
    // For now, keeping a simple loading div, but this could be improved.
    return <div>Loading...</div>; // Simplified loading, as LandingPage has its own Layout
  }

  if (user) {
    // If user is logged in, redirect to dashboard or onboarding based on survey status
    // This logic might be more complex depending on your requirements, e.g. checking user.has_completed_survey
    return <Navigate to="/dashboard" replace />;
  }

  // Render the LandingPage directly as it contains its own Layout
  return <LandingPage />;
}