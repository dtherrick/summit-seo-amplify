import { Outlet, createRootRoute } from '@tanstack/react-router';
import { TanStackRouterDevtools } from '@tanstack/router-devtools';
import { Layout } from '../components/common/Layout'; // Adjust path as needed
import { Flex, Loader } from '@aws-amplify/ui-react';
import { useAuth } from '../contexts/AuthContext'; // Adjust path as needed

export const Route = createRootRoute({
  component: RootComponent,
  // Optional: Add a global pending/error/notfound component here
  // pendingComponent: () => <GlobalSpinner />,
});

function RootComponent() {
  const { isLoading: authIsLoading } = useAuth();

  // This is a basic loading state; a more sophisticated one might be needed
  // if there are route-level loading states from TanStack Router itself.
  if (authIsLoading) {
    return (
      <Flex justifyContent="center" alignItems="center" minHeight="100vh">
        <Loader size="large" />
      </Flex>
    );
  }

  return (
    <Layout>
      <Outlet />
      {/* Conditionally render Devtools, e.g., only in development */}
      {process.env.NODE_ENV === 'development' && <TanStackRouterDevtools />}
    </Layout>
  );
}