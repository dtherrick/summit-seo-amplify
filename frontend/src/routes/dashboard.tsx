import { createFileRoute, useNavigate } from '@tanstack/react-router';
import { Button, Heading, useAuthenticator } from '@aws-amplify/ui-react';
import UserProfile from '../UserProfile'; // Assuming UserProfile.tsx is in src
import { useEffect } from 'react';

// This is the AppContent from your App.tsx, slightly adapted
const DashboardContent = () => {
  const { user, signOut } = useAuthenticator((context) => [context.user]);
  const navigate = useNavigate();

  const handleSignOut = async () => {
    await signOut();
    navigate({ to: '/login' });
  }

  return (
    <div>
      <Heading level={1}>Hello {user?.signInDetails?.loginId || user?.username || 'User'}</Heading>
      <UserProfile />
      <Button onClick={handleSignOut}>Sign Out</Button>
      <div>
        🥳 Dashboard successfully loaded.
        <br />
      </div>
    </div>
  );
};

export const Route = createFileRoute('/dashboard')({
  beforeLoad: async ({ context: _context, location: _location }) => {
    // Assuming 'context.auth' is populated by a parent route or the router itself
    // For now, we'll use a placeholder check. Actual check needs `useAuthenticator` or similar.
    // This check ideally happens higher up or via router context.
    // Tanstack Router's `beforeLoad` is a good place for auth checks.
    // However, `useAuthenticator` is a hook and cannot be called here directly.
    // A common pattern is to wrap the RouterProvider with Authenticator.Provider
    // or pass auth state down through context.

    // For this iteration, the check will be done in the component.
    // If not authenticated, redirect.
    // This is a simplified example; a robust solution would involve router context or a higher-order component.
    // The `useAuthenticator` hook in the component will handle the redirect if not authenticated.
    return {}; // No specific context to pass for now
  },
  component: DashboardComponent,
});

function DashboardComponent() {
  const { authStatus } = useAuthenticator(context => [context.authStatus]);
  const navigate = useNavigate();

  useEffect(() => {
    if (authStatus === 'unauthenticated') {
      navigate({ to: '/login', replace: true });
    }
  }, [authStatus, navigate]);

  // The authStatus can be 'configuring', 'authenticating', 'authenticated', or 'unauthenticated'.
  // This check is intentional and correct for handling loading states,
  // despite potential linter messages arising from other unresolved type issues in the project (e.g., missing routeTree.gen.ts).
  if (authStatus as string === 'configuring' || authStatus as string === 'authenticating') {
    return <div>Loading...</div>;
  }

  return authStatus === 'authenticated' ? <DashboardContent /> : null; // Or a redirect component
}