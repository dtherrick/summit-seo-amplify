import { createFileRoute, redirect, Outlet } from '@tanstack/react-router';
// import { OnboardingSurveyPage } from '../components/onboarding/OnboardingSurveyPage'; // No longer needed
import { ProtectedRoute } from '../components/auth/ProtectedRoute'; // Adjust path as needed

export const Route = createFileRoute('/onboarding')({
  beforeLoad: ({ location }) => {
    // Assuming context.auth.isAuthenticated or similar exists for checking auth
    // If not authenticated, ProtectedRoute might handle it, or redirect here
    // For now, focusing on redirecting to the survey if on /onboarding
    if (location.pathname === '/onboarding') {
      throw redirect({
        to: '/onboarding/survey',
        // search: {
        //   // You can pass search params if needed
        // },
        // replace: true, // Optional: if you want to replace the history entry
      });
    }
  },
  component: OnboardingLayout, // Or a simple wrapper component
});

// This component will likely not be rendered if beforeLoad always redirects /onboarding.
// However, it serves as the layout for child routes like /onboarding/survey.
function OnboardingLayout() {
  return (
    <ProtectedRoute>
      {/* Outlet will render child routes like /onboarding/survey */}
      <Outlet />
    </ProtectedRoute>
  );
}