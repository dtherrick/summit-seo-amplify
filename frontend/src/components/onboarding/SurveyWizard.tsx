import React, { useState } from 'react';
import { Steps, Button, Card, Form, Input, Row, Col, Typography, Space, Select, Checkbox, Modal, Descriptions, message } from 'antd';
import { useNavigate } from '@tanstack/react-router';
import { submitSurvey, type SurveyDataPayload } from '../../services/onboardingService'; // Import the service

const { Title, Text } = Typography;
const { Option } = Select;

// Define interfaces for Survey Data
interface SurveyData {
  general_information?: {
    brand_name?: string;
    brand_description?: string;
    url?: string;
    categories?: string[];
    products_services?: string;
    location_info?: string;
    niche?: string;
  };
  audience?: {
    who_is_your_audience?: string;
    needs_and_preferences?: string;
  };
  seo?: {
    seed_keywords?: string[];
    pillar_keywords?: {
      informational_intent?: string[];
      commercial_intent?: string[];
      transactional_intent?: string[];
      brand_intent?: string[];
    };
  };
  competitors_content?: { // Renamed from 'competitors' to avoid conflict with top-level 'competitors' if any
    key_competitors?: string[];
    secondary_competitors?: string[];
  };
  guardrails?: string; // Top-level as in old survey
  content_pillars?: string; // Top-level as in old survey
  brand_image_tone?: string; // Added this top-level field
  goals?: {
    primary_goals?: string[];
    current_marketing_activities?: string[];
  };
  // Fields from the original SurveyData that might still be needed or can be mapped/removed later
  // industry?: string; // Covered by general_information.categories or could be a new field if distinct
  // niche?: string; // Could be part of brand_description or a new specific field
  // productsServices?: string; // Could be part of brand_description or a new specific field
  // locationInfo?: string; // Can be a new field in general_information if needed
  // marketingGoals?: string[]; // Covered by goals.primary_goals
  // currentMarketingActivities?: string[]; // New field, can be added to a relevant section or a new 'marketing' section
  // brandImageTone?: string; // New field, can be added to 'audience' or 'general_information'
  // aiGuardrails?: string; // Covered by 'guardrails'
}

// Define props for each step component
interface StepProps {
  // formData: SurveyData; // Will be managed by the main Form instance
  // setFormData: React.Dispatch<React.SetStateAction<SurveyData>>; // Will be managed by the main Form instance
  // next: () => void; // Handled by main form's submit or wizard's next
  // prev: () => void; // Handled by wizard's prev
}

const categoriesList = [
  'Fashion',
  'Technology',
  'Health & Wellness',
  'Food & Beverage',
  'Travel',
  'Home & Garden',
  'Education',
  'Finance',
  'Entertainment',
  'Automotive',
];

const primaryGoalsList = [
  { label: 'Increase organic traffic', value: 'increase_traffic' },
  { label: 'Improve search rankings', value: 'improve_rankings' },
  { label: 'Generate more leads', value: 'generate_leads' },
  { label: 'Boost online sales', value: 'boost_sales' },
  { label: 'Build brand awareness', value: 'brand_awareness' },
  { label: 'Establish thought leadership', value: 'thought_leadership' },
  { label: 'Enter new markets', value: 'market_expansion' },
  // Add other goals from the old survey if any
];

const commonMarketingActivities = [
  { label: 'SEO (Search Engine Optimization)', value: 'seo' },
  { label: 'Content Marketing (Blogging, Articles)', value: 'content_marketing' },
  { label: 'Social Media Marketing', value: 'social_media' },
  { label: 'Email Marketing', value: 'email_marketing' },
  { label: 'PPC Advertising (Google Ads, Social Ads)', value: 'ppc_advertising' },
  { label: 'Affiliate Marketing', value: 'affiliate_marketing' },
  { label: 'Influencer Marketing', value: 'influencer_marketing' },
  { label: 'Video Marketing', value: 'video_marketing' },
];

// Step 1: General Information
const Step1GeneralInformation: React.FC<StepProps> = () => {
  return (
    <>
      <Title level={4} style={{ marginBottom: '24px' }}>General Information</Title>
      <Form.Item
        name={['general_information', 'brand_name']}
        label="Brand Name"
        rules={[{ required: true, message: 'Please input your brand name!' }]}
      >
        <Input placeholder="Enter your brand name" />
      </Form.Item>
      <Form.Item
        name={['general_information', 'brand_description']}
        label="Description"
        rules={[{ max: 500, message: 'Description cannot exceed 500 characters.' }]}
      >
        <Input.TextArea
          rows={4}
          placeholder="Describe your brand"
          maxLength={500}
          showCount
        />
      </Form.Item>
      <Form.Item
        name={['general_information', 'products_services']}
        label="Primary Products/Services"
        rules={[{ max: 500, message: 'Products/Services description cannot exceed 500 characters.' }]}
      >
        <Input.TextArea
          rows={3}
          placeholder="e.g., Custom Web Design, Artisanal Coffee Beans, Online Yoga Classes"
          maxLength={500}
          showCount
        />
      </Form.Item>
      <Form.Item
        name={['general_information', 'location_info']}
        label="Location Information (if applicable)"
      >
        <Input placeholder="e.g., San Francisco, CA or 'Online Only'" />
      </Form.Item>
      <Form.Item
        name={['general_information', 'url']}
        label="Website URL"
        rules={[
          { required: true, message: 'Please input your website URL!' },
          {
            pattern: /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([\/\w .-]*)*\/?$/,
            message: 'Please enter a valid URL (e.g., example.com or https://example.com)',
          }
        ]}
      >
        <Input
          placeholder="example.com"
          addonBefore="https://"
        />
      </Form.Item>
      <Form.Item
        name={['general_information', 'categories']}
        label="Categories"
      >
        <Select
          mode="multiple"
          style={{ width: '100%' }}
          placeholder="Select categories"
          options={categoriesList.map(cat => ({ label: cat, value: cat }))}
        />
      </Form.Item>
      <Form.Item
        name={['general_information', 'niche']}
        label="Specific Niche (Optional)"
      >
        <Input placeholder="e.g., Organic Dog Treats, Handmade Wedding Invitations" />
      </Form.Item>
    </>
  );
};

// Step 2: Audience
const Step2Audience: React.FC<StepProps> = () => {
  return (
    <>
      <Title level={4} style={{ marginBottom: '24px' }}>Audience</Title>
      <Form.Item
        name={['audience', 'who_is_your_audience']}
        label="Who is your target audience?"
        rules={[{ max: 250, message: 'Audience description cannot exceed 250 characters.' }]}
      >
        <Input.TextArea
          rows={4}
          placeholder="Describe your target audience"
          maxLength={250}
          showCount
        />
      </Form.Item>
      <Form.Item
        name={['audience', 'needs_and_preferences']}
        label="What are their needs and preferences?"
        rules={[{ max: 500, message: 'Needs/Preferences description cannot exceed 500 characters.' }]}
      >
        <Input.TextArea
          rows={4}
          placeholder="Describe audience needs and preferences"
          maxLength={500}
          showCount
        />
      </Form.Item>
    </>
  );
};

// Step 3: SEO & Keywords
const Step3SeoKeywords: React.FC<StepProps> = () => {
  return (
    <>
      <Title level={4} style={{ marginBottom: '24px' }}>SEO & Keywords</Title>
      <Form.Item
        name={['seo', 'seed_keywords']}
        label="Seed Keywords"
      >
        <Select
          mode="tags"
          style={{ width: '100%' }}
          placeholder="Enter keywords or phrases (e.g., local bakery, best coffee)"
          tokenSeparators={[',']}
        />
      </Form.Item>
      <Form.Item
        name={['seo', 'pillar_keywords', 'informational_intent']}
        label="Informational Intent Keywords"
      >
        <Select
          mode="tags"
          style={{ width: '100%' }}
          placeholder="Keywords for information-seeking customers (e.g., how to bake bread)"
          tokenSeparators={[',']}
        />
      </Form.Item>
      <Form.Item
        name={['seo', 'pillar_keywords', 'commercial_intent']}
        label="Commercial Intent Keywords"
      >
        <Select
          mode="tags"
          style={{ width: '100%' }}
          placeholder="Keywords for customers ready to buy (e.g., buy sourdough starter)"
          tokenSeparators={[',']}
        />
      </Form.Item>
      <Form.Item
        name={['seo', 'pillar_keywords', 'transactional_intent']}
        label="Transactional Intent Keywords"
      >
        <Select
          mode="tags"
          style={{ width: '100%' }}
          placeholder="Keywords for customers ready to buy from you (e.g., order [Your Brand] bread)"
          tokenSeparators={[',']}
        />
      </Form.Item>
      <Form.Item
        name={['seo', 'pillar_keywords', 'brand_intent']}
        label="Brand Intent Keywords"
      >
        <Select
          mode="tags"
          style={{ width: '100%' }}
          placeholder="Keywords related to your brand (e.g., [Your Brand] reviews)"
          tokenSeparators={[',']}
        />
      </Form.Item>
    </>
  );
};

// Step 4: Competitors & Content
const Step4CompetitorsContent: React.FC<StepProps> = () => {
  return (
    <>
      <Title level={4} style={{ marginBottom: '24px' }}>Competitors & Content</Title>
      <Form.Item
        name={['competitors_content', 'key_competitors']}
        label="Key Competitors (URLs)"
        rules={[
          {
            validator: async (_, values: string[] | undefined) => {
              if (!values || values.length === 0) return Promise.resolve(); // Allow empty
              if (values.length > 10) return Promise.reject(new Error('You can add a maximum of 10 key competitors.'));
              const urlPattern = /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([\/\w .-]*)*\/?$/;
              for (const value of values) {
                if (!urlPattern.test(value)) {
                  return Promise.reject(new Error(`'${value}' is not a valid URL format.`));
                }
              }
              return Promise.resolve();
            },
          },
        ]}
      >
        <Select
          mode="tags"
          style={{ width: '100%' }}
          placeholder="Enter your main competitors' website URLs"
          tokenSeparators={[' ', ',']}
        />
      </Form.Item>
      <Form.Item
        name={['competitors_content', 'secondary_competitors']}
        label="Secondary Competitors (URLs)"
        rules={[
          {
            validator: async (_, values: string[] | undefined) => {
              if (!values || values.length === 0) return Promise.resolve(); // Allow empty
              if (values.length > 10) return Promise.reject(new Error('You can add a maximum of 10 secondary competitors.'));
              const urlPattern = /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([\/\w .-]*)*\/?$/;
              for (const value of values) {
                if (!urlPattern.test(value)) {
                  return Promise.reject(new Error(`'${value}' is not a valid URL format.`));
                }
              }
              return Promise.resolve();
            },
          },
        ]}
      >
        <Select
          mode="tags"
          style={{ width: '100%' }}
          placeholder="Enter your secondary competitors' website URLs"
          tokenSeparators={[' ', ',']}
        />
      </Form.Item>
      <Form.Item
        name="guardrails" // Top-level
        label="Content Guardrails"
        rules={[{ max: 500, message: 'Guardrails cannot exceed 500 characters.' }]}
      >
        <Input.TextArea
          rows={4}
          placeholder="Specify topics or areas you don't want content generated about"
          maxLength={500}
          showCount
        />
      </Form.Item>
      <Form.Item
        name="content_pillars" // Top-level
        label="Content Pillars"
        rules={[{ max: 500, message: 'Content pillars description cannot exceed 500 characters.' }]}
      >
        <Input.TextArea
          rows={4}
          placeholder="Specify key themes for content generation"
          maxLength={500}
          showCount
        />
      </Form.Item>
      <Form.Item
        name="brand_image_tone" // Top-level
        label="Brand Image/Tone Guidelines"
        rules={[{ max: 500, message: 'Brand image/tone guidelines cannot exceed 500 characters.' }]}
      >
        <Input.TextArea
          rows={4}
          placeholder="Describe your desired brand voice (e.g., professional, friendly, witty, informative)"
          maxLength={500}
          showCount
        />
      </Form.Item>
    </>
  );
};

// Step 5: Goals
const Step5Goals: React.FC<StepProps> = () => {
  return (
    <>
      <Title level={4} style={{ marginBottom: '24px' }}>Goals & Current Activities</Title>
      <Form.Item
        name={['goals', 'current_marketing_activities']}
        label="What are your current marketing activities?"
      >
        <Select
          mode="tags"
          style={{ width: '100%' }}
          placeholder="Select or type your current marketing activities (e.g., SEO, Blogging)"
          options={commonMarketingActivities}
          tokenSeparators={[',']}
        />
      </Form.Item>
      <Form.Item
        name={['goals', 'primary_goals']}
        label="Primary Business Goals"
        rules={[
          { required: true, message: 'Please specify at least one primary goal!' },
          {
            validator: async (_, value) => {
              if (value && value.length > 3) {
                return Promise.reject(new Error('Please select a maximum of 3 goals.'));
              }
              return Promise.resolve();
            },
          }
        ]}
      >
        <Select
          mode="multiple"
          style={{ width: '100%' }}
          placeholder="Select your primary business goals"
          options={primaryGoalsList}
        />
      </Form.Item>
    </>
  );
};


// Placeholder for Step 1: Industry & Audience
// const Step1IndustryAudience: React.FC<StepProps> = ({ formData, setFormData, next }) => {
//   const [form] = Form.useForm();
//   return (
//     <Form
//       form={form}
//       layout="vertical"
//       onFinish={next}
//       initialValues={formData}
//     >
//       <Title level={4} style={{ marginBottom: '24px' }}>Step 1: About Your Business</Title>
//       <Form.Item
//         name="industry"
//         label="What industry is your business in?"
//         rules={[{ required: true, message: 'Please input your industry!' }]}
//       >
//         <Input
//           placeholder="e.g., E-commerce, Local Bakery, SaaS"
//           value={formData.industry}
//           onChange={(e) => setFormData(prev => ({...prev, industry: e.target.value}))}
//         />
//       </Form.Item>
//       <Form.Item
//         name="niche"
//         label="What is your specific niche? (Optional)"
//       >
//         <Input
//           placeholder="e.g., Organic Dog Treats, Handmade Wedding Invitations"
//           value={formData.niche}
//           onChange={(e) => setFormData(prev => ({...prev, niche: e.target.value}))}
//         />
//       </Form.Item>
//       <Form.Item
//         name="targetAudience"
//         label="Describe your target audience."
//         rules={[{ required: true, message: 'Please describe your target audience!' }]}
//       >
//         <Input.TextArea
//           rows={3}
//           placeholder="e.g., Young professionals aged 25-35 interested in sustainable products."
//           value={formData.targetAudience}
//           onChange={(e) => setFormData(prev => ({...prev, targetAudience: e.target.value}))}
//         />
//       </Form.Item>
//       <Form.Item>
//         <Button type="primary" htmlType="submit">
//           Next
//         </Button>
//       </Form.Item>
//     </Form>
//   );
// };

// Placeholder for Step 2: Products/Services & Location
// const Step2ProductsLocation: React.FC<StepProps> = ({ formData, setFormData, next, prev }) => {
//   const [form] = Form.useForm();
//   return (
//     <Form
//       form={form}
//       layout="vertical"
//       onFinish={next}
//       initialValues={formData}
//     >
//       <Title level={4} style={{ marginBottom: '24px' }}>Step 2: Offerings & Location</Title>
//       <Form.Item
//         name="productsServices"
//         label="What are your primary products or services?"
//         rules={[{ required: true, message: 'Please list your primary products/services!' }]}
//       >
//         <Input.TextArea
//           rows={3}
//           placeholder="e.g., Custom Web Design, Artisanal Coffee Beans, Online Yoga Classes"
//           value={formData.productsServices}
//           onChange={(e) => setFormData(prev => ({...prev, productsServices: e.target.value}))}
//         />
//       </Form.Item>
//       <Form.Item
//         name="locationInfo"
//         label="Do you serve a specific local area? If so, where? (Optional)"
//       >
//         <Input
//           placeholder="e.g., San Francisco, CA or 'Online Only'"
//           value={formData.locationInfo}
//           onChange={(e) => setFormData(prev => ({...prev, locationInfo: e.target.value}))}
//         />
//       </Form.Item>
//       <Form.Item>
//         <Space>
//           <Button onClick={prev}>
//             Previous
//           </Button>
//           <Button type="primary" htmlType="submit">
//             Next
//           </Button>
//         </Space>
//       </Form.Item>
//     </Form>
//   );
// };

// TODO: Implement Step 5: Current Marketing, Brand Tone, AI Guardrails
// Commenting out old placeholder steps that are being replaced
// const Step3MarketingGoals: React.FC<StepProps> = (props) => (
//   <div>Step 3: Marketing Goals Content (To be implemented) <Button onClick={props.prev}>Prev</Button> <Button type="primary" onClick={props.next}>Next</Button></div>
// );

// const Step4Competitors: React.FC<StepProps> = (props) => (
//   <div>Step 4: Competitors Content (To be implemented) <Button onClick={props.prev}>Prev</Button> <Button type="primary" onClick={props.next}>Next</Button></div>
// );

// const Step5FinalDetails: React.FC<StepProps> = (props) => (
//   <div>Step 5: Final Details Content (To be implemented) <Button onClick={props.prev}>Prev</Button> <Button type="primary" onClick={() => alert('Survey Submitted (Placeholder)')}>Submit</Button></div>
// );

const stepsMeta: { title: string; content: React.FC<StepProps>; sectionKey: string; }[] = [
  {
    title: 'General Information',
    content: Step1GeneralInformation,
    sectionKey: 'general_information',
  },
  {
    title: 'Audience',
    content: Step2Audience,
    sectionKey: 'audience',
  },
  {
    title: 'SEO & Keywords',
    content: Step3SeoKeywords,
    sectionKey: 'seo',
  },
  {
    title: 'Competitors & Content',
    content: Step4CompetitorsContent,
    sectionKey: 'competitors_content', // or a more general key if guardrails/pillars are validated here
  },
  {
    title: 'Goals',
    content: Step5Goals,
    sectionKey: 'goals',
  },
];

export const SurveyWizard: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [form] = Form.useForm<SurveyData>();
  const navigate = useNavigate();
  const [isSubmissionModalVisible, setIsSubmissionModalVisible] = useState(false);
  const [submittedData, setSubmittedData] = useState<SurveyData | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSkipping, setIsSkipping] = useState(false);

  // Define steps with their content and associated field names for validation
  // NOTE: Replace placeholders with actual field names for each step
  const surveySteps = [
    {
      title: 'General Information',
      content: <Step1GeneralInformation />,
      fields: [
        ['general_information', 'brand_name'],
        ['general_information', 'brand_description'],
        ['general_information', 'products_services'],
        ['general_information', 'location_info'],
        ['general_information', 'url'],
        ['general_information', 'categories'],
        ['general_information', 'niche'],
      ],
    },
    {
      title: 'Audience',
      content: <Step2Audience />,
      fields: [
        ['audience', 'who_is_your_audience'],
        ['audience', 'needs_and_preferences'],
      ],
    },
    {
      title: 'SEO & Keywords',
      content: <Step3SeoKeywords />,
      fields: [
        ['seo', 'seed_keywords'],
        ['seo', 'pillar_keywords', 'informational_intent'],
        ['seo', 'pillar_keywords', 'commercial_intent'],
        ['seo', 'pillar_keywords', 'transactional_intent'],
        // Ensure all fields from Step3SeoKeywords are listed
      ],
    },
    {
      title: 'Competitors & Content',
      content: <Step4CompetitorsContent />,
      fields: [
        ['competitors_content', 'key_competitors'],
        ['competitors_content', 'secondary_competitors'],
        ['content_pillars'], // Assuming this is a top-level field potentially related to this step
        ['brand_image_tone'], // Assuming this is a top-level field potentially related
      ],
    },
    {
      title: 'Goals & Guardrails',
      content: <Step5Goals />,
      fields: [
        ['goals', 'primary_goals'],
        ['goals', 'current_marketing_activities'],
        ['guardrails'], // Assuming this is a top-level field
      ],
    },
  ];

  const validateAndProceed = async () => {
    try {
      // Validate only fields for the current step
      const currentFields = surveySteps[currentStep].fields;
      await form.validateFields(currentFields);
      setCurrentStep(currentStep + 1);
    } catch (errorInfo) {
      console.log('Validation Failed:', errorInfo);
      message.error('Please complete all required fields in the current step.');
    }
  };

  const next = async () => {
    if (currentStep < surveySteps.length - 1) {
      await validateAndProceed();
    } else {
      // This is the last step, prepare for submission
      try {
        // Validate all fields one last time before showing confirmation
        await form.validateFields();
        const values = form.getFieldsValue(true); // Get all values
        setSubmittedData(values);
        setIsSubmissionModalVisible(true);
      } catch (errorInfo) {
        console.log('Final Validation Failed:', errorInfo);
        message.error('Please ensure all survey information is correctly filled out.');
      }
    }
  };

  const prev = () => {
    setCurrentStep(currentStep - 1);
  };

  const handleSkip = () => {
    setIsSkipping(true);
    // Potentially save any partial data if desired, or just navigate
    message.info('Survey skipped. You can complete it later from your profile settings.');
    setTimeout(() => {
      navigate({ to: '/dashboard' }); // Or to another appropriate page
      setIsSkipping(false);
    }, 1500);
  };

  const handleFinalSubmit = async () => {
    await executeActualSubmission();
  };

  const executeActualSubmission = async () => {
    if (!submittedData) {
      message.error('No data to submit.');
      return;
    }
    setIsSubmitting(true);
    try {
      const ensureHttps = (url: string | undefined): string | undefined => {
        if (!url || url.trim() === '') return undefined;
        if (!url.startsWith('http://') && !url.startsWith('https://')) {
          return `https://${url.trim()}`;
        }
        return url.trim();
      };

      const mapToPayload = (data: SurveyData): SurveyDataPayload => {
        const payload: SurveyDataPayload = {
          general_information: data.general_information ? {
            ...data.general_information,
            url: ensureHttps(data.general_information.url),
          } : {},
          audience: data.audience || {},
          seo: data.seo ? {
            ...data.seo,
            // Assuming seed_keywords and pillar_keywords don't contain URLs needing scheme
          } : {},
          competitors_content: data.competitors_content ? {
            ...data.competitors_content,
            key_competitors: data.competitors_content.key_competitors?.map(ensureHttps).filter(Boolean) as string[] | undefined,
            secondary_competitors: data.competitors_content.secondary_competitors?.map(ensureHttps).filter(Boolean) as string[] | undefined,
          } : {},
          guardrails: data.guardrails || '',
          content_pillars: data.content_pillars || '',
          brand_image_tone: data.brand_image_tone || '',
          goals: data.goals || {},
        };
        // Remove undefined fields from payload to keep it clean, Pydantic will use defaults if set
        // Or, ensure default {} or '' are acceptable by backend if fields are truly optional
        // For this iteration, we are sending empty objects/strings as per original mapping logic
        return payload as SurveyDataPayload;
      };

      const apiPayload = mapToPayload(submittedData);

      await submitSurvey(apiPayload); // Call the service
      message.success('Survey submitted successfully!');
      setIsSubmissionModalVisible(false);
      navigate({ to: '/dashboard' }); // Navigate to dashboard or a success page
    } catch (error) {
      console.error('Survey submission error:', error);
      message.error('Failed to submit survey. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const renderConfirmationContent = (values: SurveyData | null) => {
    if (!values) return <Text>No data to display.</Text>;

    const renderArray = (arr: string[] | undefined) => arr && arr.length > 0 ? arr.join(', ') : 'Not provided';
    const renderString = (str: string | undefined) => str && str.length > 0 ? str : 'Not provided';

    return (
      <Descriptions bordered column={1} size="small">
        <Descriptions.Item label="Brand Name">{renderString(values.general_information?.brand_name)}</Descriptions.Item>
        <Descriptions.Item label="Description">{renderString(values.general_information?.brand_description)}</Descriptions.Item>
        <Descriptions.Item label="URL">{renderString(values.general_information?.url)}</Descriptions.Item>
        <Descriptions.Item label="Categories">{renderArray(values.general_information?.categories)}</Descriptions.Item>
        <Descriptions.Item label="Products/Services">{renderString(values.general_information?.products_services)}</Descriptions.Item>
        <Descriptions.Item label="Location">{renderString(values.general_information?.location_info)}</Descriptions.Item>
        <Descriptions.Item label="Niche">{renderString(values.general_information?.niche)}</Descriptions.Item>

        <Descriptions.Item label="Target Audience">{renderString(values.audience?.who_is_your_audience)}</Descriptions.Item>
        <Descriptions.Item label="Audience Needs/Preferences">{renderString(values.audience?.needs_and_preferences)}</Descriptions.Item>

        <Descriptions.Item label="Seed Keywords">{renderArray(values.seo?.seed_keywords)}</Descriptions.Item>
        {/* Add more SEO fields as needed */}

        <Descriptions.Item label="Key Competitors">{renderArray(values.competitors_content?.key_competitors)}</Descriptions.Item>
        <Descriptions.Item label="Secondary Competitors">{renderArray(values.competitors_content?.secondary_competitors)}</Descriptions.Item>

        <Descriptions.Item label="Content Pillars">{renderString(values.content_pillars)}</Descriptions.Item>
        <Descriptions.Item label="Brand Image/Tone">{renderString(values.brand_image_tone)}</Descriptions.Item>
        <Descriptions.Item label="Guardrails">{renderString(values.guardrails)}</Descriptions.Item>

        <Descriptions.Item label="Primary Goals">{renderArray(values.goals?.primary_goals)}</Descriptions.Item>
        <Descriptions.Item label="Current Marketing Activities">{renderArray(values.goals?.current_marketing_activities)}</Descriptions.Item>
      </Descriptions>
    );
  };


  return (
    <Card title="Business Onboarding Survey" style={{ margin: 'auto', maxWidth: '1000px' }}>
       <Row justify="center" style={{ marginBottom: 24 }}>
        <Col xs={24} sm={20} md={18} lg={24} xl={24} xxl={24}> {/* Adjusted Col spans */}
          <Steps
            current={currentStep}
            labelPlacement="vertical"
            items={surveySteps.map(item => ({ key: item.title, title: item.title }))}
            className="survey-steps-flex" // Ensure this class is defined for flex behavior
          />
        </Col>
      </Row>
      <Form form={form} layout="vertical" name="survey_wizard_form">
        <div style={{ marginTop: 24, marginBottom: 24, padding: '20px', border: '1px solid #f0f0f0', borderRadius: '8px' }}>
          {surveySteps[currentStep].content}
        </div>
        <Row justify="space-between" gutter={16} style={{ marginTop: 24 }}>
          <Col>
            {currentStep > 0 && (
              <Button style={{ margin: '0 8px' }} onClick={prev} disabled={isSubmitting || isSkipping}>
                Previous
              </Button>
            )}
          </Col>
          <Col>
            <Space>
              <Button onClick={handleSkip} danger disabled={isSubmitting || isSkipping}>
                {isSkipping ? 'Skipping...' : 'Skip for Now'}
              </Button>
              {currentStep < surveySteps.length - 1 ? (
                <Button type="primary" onClick={next} loading={isSubmitting} disabled={isSkipping}>
                  Next
                </Button>
              ) : (
                <Button type="primary" onClick={next} loading={isSubmitting} disabled={isSkipping}>
                  Review & Submit
                </Button>
              )}
            </Space>
          </Col>
        </Row>
      </Form>
      <Modal
        title="Confirm Submission"
        open={isSubmissionModalVisible}
        onOk={handleFinalSubmit}
        onCancel={() => setIsSubmissionModalVisible(false)}
        confirmLoading={isSubmitting}
        width={800}
        okText="Submit Survey"
        cancelText="Back to Edit"
      >
        <Title level={5} style={{marginBottom: '16px'}}>Please review your survey responses before submitting:</Title>
        {renderConfirmationContent(submittedData)}
      </Modal>
    </Card>
  );
};

// Add this CSS to your global stylesheet (e.g., index.css or App.css)
// .survey-steps-flex .ant-steps-item {
//   flex: 1;
// }
// .survey-steps-flex .ant-steps-item-title {
//   white-space: normal; /* Allow text wrapping */
//   overflow: visible; /* Ensure wrapped text is visible */
//   text-overflow: clip; /* Optional: if you still want to clip if it somehow overflows a very small container */
// }