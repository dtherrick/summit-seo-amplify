import React, { useState } from 'react';
import { useNavigate } from '@tanstack/react-router';
import {
  Button,
  Flex,
  Heading,
  Card,
  StepperField,
  TextField,
  SelectField,
  RadioGroupField,
  Text,
  View,
  Alert,
} from '@aws-amplify/ui-react';

// Define types for survey data if they become complex
// interface SurveyData { ... }

const totalSteps = 3; // Example total steps

export const OnboardingSurveyPage: React.FC = () => {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState<any>({}); // Replace 'any' with a proper type
  const [formError, setFormError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleNext = () => {
    // Add validation for the current step's fields if needed
    // if (!validateStep(currentStep, formData)) {
    //   setFormError('Please fill all required fields for this step.');
    //   return;
    // }
    setFormError(null);
    if (currentStep < totalSteps) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePrevious = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = event.target;
    // const checked = (event.target as HTMLInputElement).checked; // For checkboxes
    setFormData((prev: any) => ({
      ...prev,
      [name]: type === 'checkbox' ? (event.target as HTMLInputElement).checked : value,
    }));
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setFormError(null);
    // Final validation if any
    // if (!validateStep(currentStep, formData)) {
    //   setFormError('Please fill all required fields.');
    //   return;
    // }
    setIsSubmitting(true);
    try {
      // TODO: Replace with actual API call to save survey data
      console.log('Submitting survey data:', formData);
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call
      // Navigate to dashboard or next appropriate page on successful submission
      navigate({ to: '/dashboard' });
    } catch (err) {
      if (err instanceof Error) {
        setFormError(err.message || 'Failed to submit survey. Please try again.');
      } else {
        setFormError('An unexpected error occurred.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <Flex direction="column" gap="medium">
            <Heading level={4}>Step 1: Business Information</Heading>
            <TextField
              label="Business Name"
              name="businessName"
              value={formData.businessName || ''}
              onChange={handleChange}
              isRequired
            />
            <TextField
              label="Business Website URL"
              name="websiteUrl"
              type="url"
              value={formData.websiteUrl || ''}
              onChange={handleChange}
              isRequired
            />
            <SelectField
              label="Industry"
              name="industry"
              value={formData.industry || ''}
              onChange={handleChange}
              placeholder="Select your industry"
              isRequired
            >
              <option value="tech">Technology</option>
              <option value="ecommerce">E-commerce</option>
              <option value="health">Healthcare</option>
              <option value="finance">Finance</option>
              <option value="other">Other</option>
            </SelectField>
          </Flex>
        );
      case 2:
        return (
          <Flex direction="column" gap="medium">
            <Heading level={4}>Step 2: Target Audience</Heading>
            <TextField
              label="Describe your primary target audience"
              name="targetAudience"
              value={formData.targetAudience || ''}
              onChange={handleChange}
              isMultiline
              rows={3}
            />
            <RadioGroupField
              label="Primary Goal for SEO"
              name="seoGoal"
              value={formData.seoGoal || ''}
              onChange={handleChange} // Note: RadioGroupField might need a different onChange prop or direct value handling
            >
              <Text>Increase organic traffic</Text>
              <Text>Improve search rankings for specific keywords</Text>
              <Text>Generate more leads/sales</Text>
            </RadioGroupField>
          </Flex>
        );
      case 3:
        return (
          <Flex direction="column" gap="medium">
            <Heading level={4}>Step 3: Competitors (Optional)</Heading>
            <TextField
              label="List up to 3 main competitors (URLs, one per line)"
              name="competitors"
              value={formData.competitors || ''}
              onChange={handleChange}
              isMultiline
              rows={3}
            />
            <Text fontSize="small">We'll analyze these to help tailor your SEO strategy.</Text>
          </Flex>
        );
      default:
        return <Text>Unknown step</Text>;
    }
  };

  return (
    <Flex direction="column" alignItems="center" paddingTop="xl" paddingX="medium">
      <Card variation="elevated" width={{ base: '100%', medium: '80%', large: '700px' }} padding="large">
        <Heading level={2} textAlign="center" marginBottom="large">
          Tell Us About Your Business
        </Heading>

        <StepperField
          steps={Array.from({ length: totalSteps }, (_, i) => ({ title: `Step ${i + 1}` }))}
          activeStepIndex={currentStep - 1}
          onStepClick={(index) => setCurrentStep(index + 1) } // Basic step navigation
          variation="small"
          marginBottom="large"
        />

        <form onSubmit={handleSubmit}>
          <View marginBottom="large">
            {renderStepContent()}
          </View>

          {formError && (
            <Alert variation="error" isDismissible={true} onDismiss={() => setFormError(null)} marginBottom="medium">
              {formError}
            </Alert>
          )}

          <Flex justifyContent="space-between" marginTop="large">
            <Button
              onClick={handlePrevious}
              disabled={currentStep === 1 || isSubmitting}
            >
              Previous
            </Button>
            {currentStep < totalSteps ? (
              <Button onClick={handleNext} variation="primary" disabled={isSubmitting}>
                Next
              </Button>
            ) : (
              <Button type="submit" variation="primary" isLoading={isSubmitting} disabled={isSubmitting}>
                Submit Survey
              </Button>
            )}
          </Flex>
        </form>
      </Card>
    </Flex>
  );
};