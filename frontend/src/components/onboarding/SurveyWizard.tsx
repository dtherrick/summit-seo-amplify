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
            validator: async (_, values) => {
              if (!values || values.length === 0) return Promise.resolve(); // Allow empty
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
            validator: async (_, values) => {
              if (!values || values.length === 0) return Promise.resolve(); // Allow empty
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
  const navigate = useNavigate();
  const [form] = Form.useForm<SurveyData>(); // Main form instance
  const [current, setCurrent] = useState(0);
  const [isConfirmationModalVisible, setIsConfirmationModalVisible] = useState(false);
  const [confirmedSurveyData, setConfirmedSurveyData] = useState<SurveyData | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false); // Added for loading state

  // Initial values for the form, can be set here if needed
  // useEffect(() => {
  //   form.setFieldsValue({
  //     competitors_content: { key_competitors: [''] }, // Example if you need to init dynamic fields
  //   });
  // }, [form]);

  const validateAndProceed = async () => {
    try {
      // Validate only fields visible in the current step.
      // This is tricky with a single form. AntD's Form.List might be better for dynamic fields.
      // For now, we'll rely on field-level rules.
      // A more robust way might be to get all field names for the current step and validate those.
      // const currentSectionKey = stepsMeta[current].sectionKey;
      // const fieldsToValidate = Object.keys(form.getFieldsValue()).filter(key => key.startsWith(currentSectionKey));
      // await form.validateFields(fieldsToValidate); // This needs more precise field names.

      // For simplicity, validate all touched fields or rely on button submit for full validation
      // For a step-by-step wizard, usually you validate the current step's fields
      // We'll just proceed and let final submit handle full validation or add specific validation logic here later.
      setCurrent(current + 1);
    } catch (errorInfo) {
      console.log('Validation Failed:', errorInfo);
    }
  };

  const next = () => {
    // If we want to validate per step before proceeding:
    // validateAndProceed();
    // For now, just increment step. Validation will happen on individual field rules
    // or on final submit.
    if (current < stepsMeta.length - 1) {
        setCurrent(current + 1);
    }
  };

  const prev = () => {
    if (current > 0) {
        setCurrent(current - 1);
    }
  };

  const handleSkip = () => {
    // alert('Survey Skipped (Placeholder)'); // Old placeholder
    navigate({ to: '/dashboard' }); // Navigate to dashboard
  };

  const handleFinalSubmit = async () => {
    try {
      const values = await form.validateFields();
      // Instead of direct submission, show confirmation modal first
      setConfirmedSurveyData(values);
      setIsConfirmationModalVisible(true);
    } catch (errorInfo) {
      console.log('Validation Failed before confirmation:', errorInfo);
      message.error('Please correct the errors before proceeding to confirmation.');
    }
  };

  const executeActualSubmission = async () => {
    if (!confirmedSurveyData) return;
    setIsConfirmationModalVisible(false);
    setIsSubmitting(true);
    console.log('Survey Data to be submitted:', confirmedSurveyData);
    try {
      // Call the new service function
      // Ensure confirmedSurveyData matches SurveyDataPayload structure
      const result = await submitSurvey(confirmedSurveyData as SurveyDataPayload);

      console.log('API Submission Result:', result);
      message.success(result.message || 'Survey Submitted Successfully!');
      navigate({ to: '/dashboard' });
    } catch (error: any) {
      console.error("Survey submission error in component:", error);
      message.error(error.message || 'Survey submission failed. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const renderConfirmationContent = (values: SurveyData | null) => {
    if (!values) return null;

    // Helper to render array values or a default message
    const renderArray = (arr: string[] | undefined) => arr && arr.length > 0 ? arr.join(', ') : 'Not provided';
    const renderString = (str: string | undefined) => str && str.length > 0 ? str : 'Not provided';

    return (
      <Descriptions bordered column={1} size="small">
        {values.general_information && (
          <>
            <Descriptions.Item label="Brand Name" labelStyle={{ fontWeight: 'bold' }}>
              {renderString(values.general_information.brand_name)}
            </Descriptions.Item>
            <Descriptions.Item label="Brand Description" labelStyle={{ fontWeight: 'bold' }}>
              {renderString(values.general_information.brand_description)}
            </Descriptions.Item>
            <Descriptions.Item label="Primary Products/Services" labelStyle={{ fontWeight: 'bold' }}>
              {renderString(values.general_information.products_services)}
            </Descriptions.Item>
            <Descriptions.Item label="Location Information" labelStyle={{ fontWeight: 'bold' }}>
              {renderString(values.general_information.location_info)}
            </Descriptions.Item>
            <Descriptions.Item label="Website URL" labelStyle={{ fontWeight: 'bold' }}>
              {values.general_information.url ? `https://${values.general_information.url}` : 'Not provided'}
            </Descriptions.Item>
            <Descriptions.Item label="Categories" labelStyle={{ fontWeight: 'bold' }}>
              {renderArray(values.general_information.categories)}
            </Descriptions.Item>
            <Descriptions.Item label="Specific Niche" labelStyle={{ fontWeight: 'bold' }}>
              {renderString(values.general_information.niche)}
            </Descriptions.Item>
          </>
        )}

        {values.audience && (
          <>
            <Descriptions.Item label="Target Audience" labelStyle={{ fontWeight: 'bold' }}>
              {renderString(values.audience.who_is_your_audience)}
            </Descriptions.Item>
            <Descriptions.Item label="Audience Needs/Preferences" labelStyle={{ fontWeight: 'bold' }}>
              {renderString(values.audience.needs_and_preferences)}
            </Descriptions.Item>
          </>
        )}

        {values.seo && (
          <>
            <Descriptions.Item label="Seed Keywords" labelStyle={{ fontWeight: 'bold' }}>
              {renderArray(values.seo.seed_keywords)}
            </Descriptions.Item>
            {values.seo.pillar_keywords && (
              <>
                <Descriptions.Item label="Informational Intent Keywords" labelStyle={{ fontWeight: 'bold' }}>
                  {renderArray(values.seo.pillar_keywords.informational_intent)}
                </Descriptions.Item>
                <Descriptions.Item label="Commercial Intent Keywords" labelStyle={{ fontWeight: 'bold' }}>
                  {renderArray(values.seo.pillar_keywords.commercial_intent)}
                </Descriptions.Item>
                <Descriptions.Item label="Transactional Intent Keywords" labelStyle={{ fontWeight: 'bold' }}>
                  {renderArray(values.seo.pillar_keywords.transactional_intent)}
                </Descriptions.Item>
                <Descriptions.Item label="Brand Intent Keywords" labelStyle={{ fontWeight: 'bold' }}>
                  {renderArray(values.seo.pillar_keywords.brand_intent)}
                </Descriptions.Item>
              </>
            )}
          </>
        )}

        {values.competitors_content && (
          <>
            <Descriptions.Item label="Key Competitors (URLs)" labelStyle={{ fontWeight: 'bold' }}>
              {renderArray(values.competitors_content.key_competitors)}
            </Descriptions.Item>
            <Descriptions.Item label="Secondary Competitors (URLs)" labelStyle={{ fontWeight: 'bold' }}>
              {renderArray(values.competitors_content.secondary_competitors)}
            </Descriptions.Item>
          </>
        )}

        <Descriptions.Item label="Content Guardrails" labelStyle={{ fontWeight: 'bold' }}>
          {renderString(values.guardrails)}
        </Descriptions.Item>
        <Descriptions.Item label="Content Pillars" labelStyle={{ fontWeight: 'bold' }}>
          {renderString(values.content_pillars)}
        </Descriptions.Item>
        <Descriptions.Item label="Brand Image/Tone Guidelines" labelStyle={{ fontWeight: 'bold' }}>
          {renderString(values.brand_image_tone)}
        </Descriptions.Item>

        {values.goals && (
          <Descriptions.Item label="Primary Goals" labelStyle={{ fontWeight: 'bold' }}>
            {renderArray(values.goals.primary_goals?.map(goalValue =>
              primaryGoalsList.find(g => g.value === goalValue)?.label || goalValue
            ))}
          </Descriptions.Item>
        )}
        {values.goals?.current_marketing_activities && (
          <Descriptions.Item label="Current Marketing Activities" labelStyle={{ fontWeight: 'bold' }}>
            {renderArray(values.goals.current_marketing_activities.map(activityValue =>
              commonMarketingActivities.find(a => a.value === activityValue)?.label || activityValue
            ))}
          </Descriptions.Item>
        )}
      </Descriptions>
    );
  };

  const CurrentStepComponent = stepsMeta[current].content;

  return (
    <Row justify="center" align="middle" style={{ minHeight: '100vh', padding: '20px' }}>
      <Col xs={24} sm={23} md={22} lg={20} xl={20} xxl={18}>
        <Card
          title={<Title level={3} style={{ textAlign: 'center', marginBottom: 0 }}>Tell Us About Your Business</Title>}
          bordered={false}
        >
          <Steps
            current={current}
            items={stepsMeta.map(item => ({
              key: item.title,
              title: <div style={{ whiteSpace: 'normal', overflowWrap: 'break-word' }}>{item.title}</div>,
              style: { flex: 1, textAlign: 'center' }
            }))}
            style={{ marginBottom: '32px', display: 'flex', width: '100%' }}
          />

          <Form
            form={form}
            layout="vertical"
            name="surveyForm"
            // onFinish={handleFinalSubmit} // We'll call this manually from the last step's button
            initialValues={{ // Set initial values for the form here if necessary
                // e.g. general_information: { brand_name: "My Test Brand"}
            }}
          >
            <div className="steps-content" style={{ marginTop: '24px', padding: '24px', background: '#f9f9f9', borderRadius: '8px' }}>
              <CurrentStepComponent />
            </div>

            <div className="steps-action" style={{ marginTop: '24px', textAlign: 'right' }}>
              <Space>
                <Button onClick={handleSkip} style={{ marginRight: 8 }}>
                  Skip Survey
                </Button>
                {current > 0 && (
                  <Button style={{ margin: '0 8px' }} onClick={() => prev()}>
                    Previous
                  </Button>
                )}
                {current < stepsMeta.length - 1 && (
                  <Button type="primary" onClick={() => next()}>
                    Next
                  </Button>
                )}
                {current === stepsMeta.length - 1 && (
                  <Button type="primary" onClick={handleFinalSubmit}>
                    Submit Survey
                  </Button>
                )}
              </Space>
            </div>
          </Form>
          <Modal
            title="Confirm Your Survey Submission"
            open={isConfirmationModalVisible}
            onOk={executeActualSubmission}
            onCancel={() => setIsConfirmationModalVisible(false)}
            width={800} // Adjust width as needed
            okText={isSubmitting ? "Submitting..." : "Submit"} // Change button text on loading
            okButtonProps={{ loading: isSubmitting }} // Show loading spinner on button
            cancelText="Edit"
          >
            {renderConfirmationContent(confirmedSurveyData)}
          </Modal>
        </Card>
      </Col>
    </Row>
  );
};