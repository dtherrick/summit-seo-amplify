import { createFileRoute } from '@tanstack/react-router';
import { OnboardingSurveyPage } from '../components/onboarding/OnboardingSurveyPage';
import { ProtectedRoute } from '../components/auth/ProtectedRoute'; // Adjust path as needed

export const Route = createFileRoute('/onboarding')({
  component: OnboardingPage,
});

function OnboardingPage() {
  return (
    <ProtectedRoute>
      <OnboardingSurveyPage />
    </ProtectedRoute>
  );
}