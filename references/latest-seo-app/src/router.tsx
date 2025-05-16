import { createRouter, RouterProvider, Route, RootRoute, Navigate } from '@tanstack/react-router';
import { LoginForm } from './components/auth/LoginForm';
import { BusinessSignupForm } from './components/auth/BusinessSignupForm';
import { UserManagement } from './components/user/UserManagement';
import { ProtectedRoute } from './components/auth/ProtectedRoute';
import { Navigation } from './components/common/Navigation';
import { LandingPage } from './components/LandingPage';
import { OnboardingSurveyPage } from './components/OnboardingSurveyPage';
import { Dashboard } from './components/Dashboard';
import { useAuth } from './contexts/AuthContext';
import { Layout as AntLayout, ConfigProvider, theme } from 'antd';
import { useState } from 'react';

const { Content } = AntLayout;

// Layout component
function Layout({ children, showNav = true }: { children: React.ReactNode; showNav?: boolean }) {
  const [isDarkMode, setIsDarkMode] = useState(false);

  return (
    <ConfigProvider
      theme={{
        algorithm: isDarkMode ? theme.darkAlgorithm : theme.defaultAlgorithm,
        token: {
          colorPrimary: '#32a9be',
          borderRadius: 6,
          colorBgContainer: isDarkMode ? '#141414' : '#ffffff',
          colorBgLayout: isDarkMode ? '#000000' : '#f0f2f5',
        },
      }}
    >
      <AntLayout className="min-h-screen">
        {showNav && <Navigation isDarkMode={isDarkMode} setIsDarkMode={setIsDarkMode} />}
        <Content 
          style={{ 
            background: isDarkMode ? '#000000' : '#f0f2f5',
            minHeight: 'calc(100vh - 64px)',
            marginTop: showNav ? 64 : 0
          }}
        >
          {children}
        </Content>
      </AntLayout>
    </ConfigProvider>
  );
}

// Create the root route
const rootRoute = new RootRoute();

// Create routes
const indexRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/',
  component: () => {
    const { user } = useAuth();
    if (user) {
      return <Navigate to="/dashboard" />;
    }
    return (
      <Layout showNav={false}>
        <LandingPage />
      </Layout>
    );
  },
});

const loginRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/login',
  component: () => {
    const { user } = useAuth();
    if (user) {
      return <Navigate to="/dashboard" />;
    }
    return (
      <Layout>
        <LoginForm />
      </Layout>
    );
  },
});

const signupRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/signup',
  component: () => {
    const { user } = useAuth();
    if (user) {
      return <Navigate to="/onboarding" />;
    }
    return (
      <Layout>
        <BusinessSignupForm />
      </Layout>
    );
  },
});

const onboardingRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/onboarding',
  component: () => (
    <Layout>
      <ProtectedRoute>
        <OnboardingSurveyPage />
      </ProtectedRoute>
    </Layout>
  ),
});

const dashboardRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/dashboard',
  component: () => {
    const { user } = useAuth();
    // If user hasn't completed the survey, redirect to onboarding
    if (user && !user.has_completed_survey) {
      return <Navigate to="/onboarding" />;
    }
    return (
      <Layout>
        <ProtectedRoute>
          <Dashboard />
        </ProtectedRoute>
      </Layout>
    );
  },
});

const usersRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/users',
  component: () => (
    <Layout>
      <ProtectedRoute requiredRole="business_admin">
        <UserManagement />
      </ProtectedRoute>
    </Layout>
  ),
});

const unauthorizedRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/unauthorized',
  component: () => (
    <Layout>
      <div className="flex items-center justify-center min-h-[calc(100vh-4rem)]">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Unauthorized</h1>
          <p className="text-gray-600">You don't have permission to access this page.</p>
        </div>
      </div>
    </Layout>
  ),
});

// Create and configure router
const router = createRouter({
  routeTree: rootRoute.addChildren([
    indexRoute,
    loginRoute,
    signupRoute,
    onboardingRoute,
    dashboardRoute,
    usersRoute,
    unauthorizedRoute,
  ]),
  defaultPendingComponent: () => (
    <div className="flex items-center justify-center min-h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
    </div>
  ),
});

// Register router for type safety
declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router;
  }
}

// Router component
export function Router() {
  const { isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return <RouterProvider router={router} />;
} 