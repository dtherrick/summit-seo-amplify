import { Authenticator, useAuthenticator, Button, Heading } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';
import UserProfile from './UserProfile';

const AppContent = () => {
  const { user, signOut } = useAuthenticator((context) => [context.user]);

  return (
    <div>
      <Heading level={1}>Hello {user?.signInDetails?.loginId || user?.username || 'User'}</Heading>
      <UserProfile />
      <Button onClick={signOut}>Sign Out</Button>
    </div>
  );
};

function App() {
  return (
    <Authenticator loginMechanisms={['email']}>
      {({ signOut: _signOut, user: _user }) => (
        <main>
          <AppContent />
          <div>
            🥳 App successfully hosted.
            <br />
          </div>
        </main>
      )}
    </Authenticator>
  );
}

export default App;
