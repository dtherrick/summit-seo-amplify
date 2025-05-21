// frontend/src/routes/onboarding/survey.tsx
import { createFileRoute } from '@tanstack/react-router';
import { SurveyWizard } from '../../components/onboarding/SurveyWizard'; // Adjust path as necessary

export const Route = createFileRoute('/onboarding/survey' as const)({
  component: SurveyWizardComponent,
});

function SurveyWizardComponent() {
  return <SurveyWizard />;
}