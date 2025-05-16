import { Navigate } from '@tanstack/react-router';
import { useAuth } from '../../contexts/AuthContext';

type RoleType = 'superuser' | 'business_admin' | 'business_user';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredRole?: RoleType;
}

export function ProtectedRoute({ children, requiredRole }: ProtectedRouteProps) {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" />;
  }

  // If no specific role is required, just being authenticated is enough
  if (!requiredRole) {
    return <>{children}</>;
  }

  // Check if user has the required role
  const hasRequiredRole = user.roles.some((role: string) => role === requiredRole);
  if (!hasRequiredRole) {
    return <Navigate to="/unauthorized" />;
  }

  return <>{children}</>;
} 