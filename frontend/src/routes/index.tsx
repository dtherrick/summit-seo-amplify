import { createFileRoute } from '@tanstack/react-router';
import { LandingPage } from '../pages/LandingPage'; // Adjusted path

export const Route = createFileRoute('/')({
  component: LandingPageComponent,
});

function LandingPageComponent() {
  return <LandingPage />;
}