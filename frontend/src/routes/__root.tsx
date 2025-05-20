import { Outlet, createRootRoute } from '@tanstack/react-router';
//import React from 'react';

export const Route = createRootRoute({
  component: RootComponent,
});

function RootComponent() {
  return (
    <>
      {/* Add any global layout components here, like a navbar if not part of LandingPage header */}
      <Outlet />
    </>
  );
}