import { useEffect, useState } from "react";
import type { Schema } from "../amplify/data/resource";
import { generateClient } from "aws-amplify/data";
import { Authenticator, useAuthenticator, Button, Heading } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';

const client = generateClient<Schema>();

const AppContent = () => {
  const { user, signOut } = useAuthenticator((context) => [context.user]);

  return (
    <div>
      <Heading level={1}>Hello {user?.signInDetails?.loginId || user?.username || 'User'}</Heading>
      {/* Your protected app content here */}
      <Button onClick={signOut}>Sign Out</Button>
    </div>
  );
};

function App() {
  const [todos, setTodos] = useState<Array<Schema["Todo"]["type"]>>([]);

  useEffect(() => {
    client.models.Todo.observeQuery().subscribe({
      next: (data) => setTodos([...data.items]),
    });
  }, []);

  function createTodo() {
    client.models.Todo.create({ content: window.prompt("Todo content") });
  }

  return (
    <Authenticator loginMechanisms={['email']}>
      {({ signOut: _signOut, user: _user }) => (
        <main>
          <AppContent />
          <h1>My todos</h1>
          <button onClick={createTodo}>+ new</button>
          <ul>
            {todos.map((todo) => (
              <li key={todo.id}>{todo.content}</li>
            ))}
          </ul>
          <div>
            🥳 App successfully hosted. Try creating a new todo.
            <br />
            <a href="https://docs.amplify.aws/react/start/quickstart/#make-frontend-updates">
              Review next step of this tutorial.
            </a>
          </div>
        </main>
      )}
    </Authenticator>
  );
}

export default App;
