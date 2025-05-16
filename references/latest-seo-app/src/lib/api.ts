import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export interface SurveyData {
  general_information: {
    brand_name: string;
    brand_description: string;
    url: string;
    categories: string[];
  };
  audience: {
    who_is_your_audience: string;
    needs_and_preferences: string;
  };
  seo: {
    seed_keywords: string;
    pillar_keywords: {
      informational_intent: string;
      commercial_intent: string;
      transactional_intent: string;
      brand_intent: string;
    };
  };
  competitors: {
    key_competitors: string;
    secondary_competitors: string;
  };
  guardrails: string;
  content_pillars: string;
}

export interface SurveyResponse {
  customer_id: string;
  response_data: {
    general_information: {
      brand_name: string;
      brand_description: string;
      url: string;
      categories: string[];
    };
    audience: {
      who_is_your_audience: string;
      needs_and_preferences: string;
    };
    seo: {
      seed_keywords: string;
      pillar_keywords: {
        informational_intent: string;
        commercial_intent: string;
        transactional_intent: string;
        brand_intent: string;
      };
    };
    competitors: {
      key_competitors: string;
      secondary_competitors: string;
    };
    guardrails: string;
    content_pillars: string;
  };
}

export interface SurveyResponseDB extends SurveyResponse {
  id: number;
  created_at: string;
  updated_at: string;
}

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const surveyApi = {
  createSurvey: async (data: SurveyResponse): Promise<SurveyResponseDB> => {
    const response = await api.post<SurveyResponseDB>('/surveys', data);
    return response.data;
  },
  
  getAllSurveys: async (): Promise<SurveyResponseDB[]> => {
    const response = await api.get<SurveyResponseDB[]>('/surveys');
    return response.data;
  },
  
  getSurvey: async (customerId: string): Promise<SurveyResponseDB> => {
    const response = await api.get<SurveyResponseDB>(`/surveys/${customerId}`);
    return response.data;
  },
  
  getSurveyExample: async (): Promise<SurveyResponse> => {
    const response = await api.get<SurveyResponse>('/surveys/schema/example');
    return response.data;
  },

  async submitSurvey(values: any): Promise<void> {
    // Format the URL properly
    const url = values.general_information?.url;
    const formattedUrl = url
      ? (url.startsWith('http://') || url.startsWith('https://') ? url : `https://${url}`)
      : '';
    
    // Create the survey data with the correct nested structure
    const surveyData = {
      customer_id: 'temp-customer-id', // TODO: Get from auth context
      response_data: {
        general_information: {
          brand_name: values.general_information?.brand_name || '',
          brand_description: values.general_information?.brand_description || '',
          url: formattedUrl,
          categories: values.general_information?.categories || [],
        },
        audience: {
          who_is_your_audience: values.audience?.who_is_your_audience || '',
          needs_and_preferences: values.audience?.needs_and_preferences || '',
        },
        seo: {
          seed_keywords: values.seo?.seed_keywords?.join(', ') || '',
          pillar_keywords: {
            informational_intent: values.seo?.pillar_keywords?.informational_intent?.join(', ') || '',
            commercial_intent: values.seo?.pillar_keywords?.commercial_intent?.join(', ') || '',
            transactional_intent: values.seo?.pillar_keywords?.transactional_intent?.join(', ') || '',
            brand_intent: values.seo?.pillar_keywords?.brand_intent?.join(', ') || '',
          }
        },
        competitors: {
          key_competitors: values.competitors?.key_competitors?.join(', ') || '',
          secondary_competitors: values.competitors?.secondary_competitors?.join(', ') || '',
        },
        guardrails: values.guardrails || '',
        content_pillars: values.content_pillars || '',
      }
    };

    const response = await axios.post('/api/v1/surveys', surveyData);
    if (!response.data) {
      throw new Error('Failed to submit survey');
    }
  }
}; 