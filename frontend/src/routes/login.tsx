import { createFileRoute } from '@tanstack/react-router';
import { Authenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';
import { useNavigate } from '@tanstack/react-router';
import { useEffect } from 'react';
import { useAuthenticator } from '@aws-amplify/ui-react';


export const Route = createFileRoute('/login')({
  component: LoginComponent,
});

function LoginComponent() {
  const navigate = useNavigate();
  const { authStatus } = useAuthenticator(context => [context.authStatus]);

  useEffect(() => {
    if (authStatus === 'authenticated') {
      navigate({ to: '/dashboard', replace: true });
    }
  }, [authStatus, navigate]);

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <Authenticator />
    </div>
  );
}