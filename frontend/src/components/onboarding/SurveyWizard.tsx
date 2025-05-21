import React, { useState } from 'react';
import { Steps, Button, Card, Form, Input, Row, Col, Typography, Space, Select, Checkbox } from 'antd';
import { useNavigate } from '@tanstack/react-router';

const { Title } = Typography;
const { Option } = Select;

// Define interfaces for Survey Data
interface SurveyData {
  industry?: string;
  niche?: string;
  targetAudience?: string;
  productsServices?: string;
  locationInfo?: string;
  marketingGoals?: string[];
  competitors?: { url: string }[];
  currentMarketingActivities?: string[];
  brandImageTone?: string;
  aiGuardrails?: string;
}

// Define props for each step component
interface StepProps {
  formData: SurveyData;
  setFormData: React.Dispatch<React.SetStateAction<SurveyData>>;
  next: () => void;
  prev: () => void;
}

// Placeholder for Step 1: Industry & Audience
const Step1IndustryAudience: React.FC<StepProps> = ({ formData, setFormData, next }) => {
  const [form] = Form.useForm();
  return (
    <Form
      form={form}
      layout="vertical"
      onFinish={next}
      initialValues={formData}
    >
      <Title level={4} style={{ marginBottom: '24px' }}>Step 1: About Your Business</Title>
      <Form.Item
        name="industry"
        label="What industry is your business in?"
        rules={[{ required: true, message: 'Please input your industry!' }]}
      >
        <Input
          placeholder="e.g., E-commerce, Local Bakery, SaaS"
          value={formData.industry}
          onChange={(e) => setFormData(prev => ({...prev, industry: e.target.value}))}
        />
      </Form.Item>
      <Form.Item
        name="niche"
        label="What is your specific niche? (Optional)"
      >
        <Input
          placeholder="e.g., Organic Dog Treats, Handmade Wedding Invitations"
          value={formData.niche}
          onChange={(e) => setFormData(prev => ({...prev, niche: e.target.value}))}
        />
      </Form.Item>
      <Form.Item
        name="targetAudience"
        label="Describe your target audience."
        rules={[{ required: true, message: 'Please describe your target audience!' }]}
      >
        <Input.TextArea
          rows={3}
          placeholder="e.g., Young professionals aged 25-35 interested in sustainable products."
          value={formData.targetAudience}
          onChange={(e) => setFormData(prev => ({...prev, targetAudience: e.target.value}))}
        />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit">
          Next
        </Button>
      </Form.Item>
    </Form>
  );
};

// Placeholder for Step 2: Products/Services & Location
const Step2ProductsLocation: React.FC<StepProps> = ({ formData, setFormData, next, prev }) => {
  const [form] = Form.useForm();
  return (
    <Form
      form={form}
      layout="vertical"
      onFinish={next}
      initialValues={formData}
    >
      <Title level={4} style={{ marginBottom: '24px' }}>Step 2: Offerings & Location</Title>
      <Form.Item
        name="productsServices"
        label="What are your primary products or services?"
        rules={[{ required: true, message: 'Please list your primary products/services!' }]}
      >
        <Input.TextArea
          rows={3}
          placeholder="e.g., Custom Web Design, Artisanal Coffee Beans, Online Yoga Classes"
          value={formData.productsServices}
          onChange={(e) => setFormData(prev => ({...prev, productsServices: e.target.value}))}
        />
      </Form.Item>
      <Form.Item
        name="locationInfo"
        label="Do you serve a specific local area? If so, where? (Optional)"
      >
        <Input
          placeholder="e.g., San Francisco, CA or 'Online Only'"
          value={formData.locationInfo}
          onChange={(e) => setFormData(prev => ({...prev, locationInfo: e.target.value}))}
        />
      </Form.Item>
      <Form.Item>
        <Space>
          <Button onClick={prev}>
            Previous
          </Button>
          <Button type="primary" htmlType="submit">
            Next
          </Button>
        </Space>
      </Form.Item>
    </Form>
  );
};

// TODO: Implement Step 5: Current Marketing, Brand Tone, AI Guardrails

const Step3MarketingGoals: React.FC<StepProps> = (props) => (
  <div>Step 3: Marketing Goals Content (To be implemented) <Button onClick={props.prev}>Prev</Button> <Button type="primary" onClick={props.next}>Next</Button></div>
);

const Step4Competitors: React.FC<StepProps> = (props) => (
  <div>Step 4: Competitors Content (To be implemented) <Button onClick={props.prev}>Prev</Button> <Button type="primary" onClick={props.next}>Next</Button></div>
);

const Step5FinalDetails: React.FC<StepProps> = (props) => (
  <div>Step 5: Final Details Content (To be implemented) <Button onClick={props.prev}>Prev</Button> <Button type="primary" onClick={() => alert('Survey Submitted (Placeholder)')}>Submit</Button></div>
);

const steps: { title: string; content: React.FC<StepProps> }[] = [
  {
    title: 'Business Basics',
    content: Step1IndustryAudience,
  },
  {
    title: 'Offerings & Location',
    content: Step2ProductsLocation,
  },
  {
    title: 'Marketing Goals',
    content: Step3MarketingGoals,
  },
  {
    title: 'Competitors',
    content: Step4Competitors,
  },
  {
    title: 'Final Details',
    content: Step5FinalDetails,
  },
];

export const SurveyWizard: React.FC = () => {
  const navigate = useNavigate();
  const [current, setCurrent] = useState(0);
  const [formData, setFormData] = useState<SurveyData>({
    competitors: [{ url: '' }], // Initialize with one competitor field
    marketingGoals: [],
    currentMarketingActivities: [],
  });

  const next = () => {
    setCurrent(current + 1);
  };

  const prev = () => {
    setCurrent(current - 1);
  };

  const handleSkip = () => {
    // TODO: Decide where to navigate on skip. Dashboard?
    alert('Survey Skipped (Placeholder)');
    // navigate({ to: '/dashboard' }); // Example navigation
  };

  const handleSubmit = () => {
    // TODO: Implement actual submission logic
    // This will involve an API call to the backend
    console.log('Survey Data:', formData);
    alert('Survey Submitted (Placeholder) - Check console for data.');
    // navigate({ to: '/dashboard' }); // Example: Navigate to dashboard after submission
  };

  const CurrentStepComponent = steps[current].content;

  return (
    <Row justify="center" align="middle" style={{ minHeight: 'calc(100vh - 64px)', padding: '20px' }}> {/* Adjust 64px if header height is different */}
      <Col xs={24} sm={20} md={16} lg={12} xl={10}>
        <Card title={<Title level={2} style={{ textAlign: 'center' }}>Tell Us About Your Business</Title>} bordered={false}>
          <Steps current={current} items={steps.map(item => ({ key: item.title, title: item.title }))} style={{ marginBottom: '32px' }}/>

          <div className="steps-content" style={{ marginTop: '24px', padding: '24px', background: '#f9f9f9', borderRadius: '8px' }}>
            <CurrentStepComponent formData={formData} setFormData={setFormData} next={next} prev={prev} />
          </div>

          <div className="steps-action" style={{ marginTop: '24px', textAlign: 'right' }}>
            <Space>
              <Button onClick={handleSkip}>
                Skip Survey
              </Button>
              {/* Navigation buttons are now within each step component for form handling */}
              {/* Submit button will be in the last step component */}
            </Space>
          </div>
        </Card>
      </Col>
    </Row>
  );
};