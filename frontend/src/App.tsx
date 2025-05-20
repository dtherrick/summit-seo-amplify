import { Outlet } from '@tanstack/react-router';

// App.tsx is now a simple layout component, though root.tsx serves a similar purpose.
// It could be removed or used for ultra-top-level context providers if needed,
// but with TanStack Router, router-level context is often preferred.
function App() {
  return (
    <>
      {/* If you had global elements outside of router views, they could go here. */}
      {/* For instance, a global notification system UI that isn't tied to a route. */}
      {/* However, most content will be rendered via the <Outlet /> in root.tsx */}
      {/* This App component is likely not strictly necessary anymore. */}
      <Outlet />
    </>
  );
}

export default App;
