import { post } from 'aws-amplify/api';
import { fetchAuthSession } from 'aws-amplify/auth';

// Define an interface for the survey data payload, mirroring backend SurveySubmissionPayload
// This helps with type safety on the frontend when preparing the data.
interface GeneralInformationPayload {
  brand_name?: string;
  brand_description?: string;
  url?: string;
  categories?: string[];
  products_services?: string;
  location_info?: string;
  niche?: string;
}

interface AudiencePayload {
  who_is_your_audience?: string;
  needs_and_preferences?: string;
}

interface PillarKeywordsPayload {
  informational_intent?: string[];
  commercial_intent?: string[];
  transactional_intent?: string[];
  brand_intent?: string[];
}

interface SeoPayload {
  seed_keywords?: string[];
  pillar_keywords?: PillarKeywordsPayload;
}

interface CompetitorsContentPayload {
  key_competitors?: string[];
  secondary_competitors?: string[];
}

interface GoalsPayload {
  primary_goals?: string[];
  current_marketing_activities?: string[];
}

export interface SurveyDataPayload {
  general_information?: GeneralInformationPayload;
  audience?: AudiencePayload;
  seo?: SeoPayload;
  competitors_content?: CompetitorsContentPayload;
  guardrails?: string;
  content_pillars?: string;
  brand_image_tone?: string;
  goals?: GoalsPayload;
}

/**
 * Submits the onboarding survey data to the backend.
 * @param surveyData The survey data collected from the user.
 * @returns The response from the API.
 * @throws Will throw an error if the API call fails or if authentication fails.
 */
export const submitSurvey = async (surveyData: SurveyDataPayload) => {
  console.log('Attempting to submit survey data:', surveyData);
  try {
    const session = await fetchAuthSession();
    const idToken = session.tokens?.idToken?.toString();

    if (!idToken) {
      console.error('No ID token found. User might not be authenticated.');
      throw new Error('User is not authenticated. Cannot submit survey.');
    }

    const response = await post({
      apiName: 'SummitSEOAmplifyAPI', // This must match the API name in amplify_outputs.json and main.tsx
      path: '/onboarding/survey',
      options: {
        headers: {
          Authorization: `Bearer ${idToken}`,
        },
        body: surveyData,
      },
    }).response;

    console.log('Survey submission response status:', response.statusCode);
    const responseBody = await response.body.json();
    console.log('Survey submission response body:', responseBody);

    if (response.statusCode < 200 || response.statusCode >= 300) {
        throw new Error(`Survey submission failed with status ${response.statusCode}: ${JSON.stringify(responseBody)}`);
    }

    return responseBody;
  } catch (error) {
    console.error('Error submitting survey:', error);
    // Re-throw the error so the calling component can handle it (e.g., show a message to the user)
    throw error;
  }
};