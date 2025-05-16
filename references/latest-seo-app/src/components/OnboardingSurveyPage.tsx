import React, { useState, useEffect } from 'react';
import { Steps, Button, Form, Input, Card, Select, Space, Modal, App } from 'antd';
import type { FormInstance } from 'antd/es/form';
import { useNavigate } from '@tanstack/react-router';
import { surveyApi, type SurveyResponse } from '../lib/api';
import { useAuth } from '../contexts/AuthContext';

const { TextArea } = Input;
const { Option } = Select;

const categories = [
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

interface StepType {
  title: string;
  content: React.ReactElement;
  sectionKey: string;
}

const steps: StepType[] = [
  {
    title: 'General Information',
    sectionKey: 'general_information',
    content: (
      <>
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
          <TextArea 
            rows={4} 
            placeholder="Describe your brand"
            maxLength={500}
            showCount
          />
        </Form.Item>
        <Form.Item
          name={['general_information', 'url']}
          label="Website URL"
          rules={[
            { required: true, message: 'Please input your website URL!' },
            {
              pattern: /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*\/?$/,
              message: 'Please enter a valid URL (e.g., example.com or https://example.com)',
            }
          ]}
        >
          <Input 
            placeholder="example.com or https://example.com"
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
            options={categories.map(cat => ({ label: cat, value: cat }))}
          />
        </Form.Item>
      </>
    ),
  },
  {
    title: 'Audience',
    sectionKey: 'audience',
    content: (
      <>
        <Form.Item
          name={['audience', 'who_is_your_audience']}
          label="Who is your target audience?"
        >
          <TextArea 
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
          <TextArea 
            rows={4} 
            placeholder="Describe audience needs and preferences"
            maxLength={500}
            showCount
          />
        </Form.Item>
      </>
    ),
  },
  {
    title: 'SEO & Keywords',
    sectionKey: 'seo',
    content: (
      <>
        <Form.Item
          name={['seo', 'seed_keywords']}
          label="Seed Keywords"
        >
          <Select
            mode="tags"
            style={{ width: '100%' }}
            placeholder="Enter keywords"
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
            placeholder="Keywords for information-seeking customers"
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
            placeholder="Keywords for customers ready to buy"
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
            placeholder="Keywords for customers ready to buy from you"
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
            placeholder="Keywords related to your brand"
            tokenSeparators={[',']}
          />
        </Form.Item>
      </>
    ),
  },
  {
    title: 'Competitors & Content',
    sectionKey: 'competitors',
    content: (
      <>
        <Form.Item
          name={['competitors', 'key_competitors']}
          label="Key Competitors"
        >
          <Select
            mode="tags"
            style={{ width: '100%' }}
            placeholder="Enter your main competitors"
            tokenSeparators={[',']}
          />
        </Form.Item>
        <Form.Item
          name={['competitors', 'secondary_competitors']}
          label="Secondary Competitors"
        >
          <Select
            mode="tags"
            style={{ width: '100%' }}
            placeholder="Enter your secondary competitors"
            tokenSeparators={[',']}
          />
        </Form.Item>
        <Form.Item
          name="guardrails"
          label="Content Guardrails"
        >
          <TextArea 
            rows={4} 
            placeholder="Specify topics or areas you don't want content generated about"
            maxLength={500}
            showCount
          />
        </Form.Item>
        <Form.Item
          name="content_pillars"
          label="Content Pillars"
        >
          <TextArea 
            rows={4} 
            placeholder="Specify key themes for content generation"
            maxLength={500}
            showCount
          />
        </Form.Item>
      </>
    ),
  },
  {
    title: 'Goals',
    sectionKey: 'goals',
    content: (
      <>
        <Form.Item
          name={['goals', 'primary_goals']}
          label="Primary Business Goals"
          rules={[{ required: true, message: 'Please specify at least one primary goal!' }]}
        >
          <Select
            mode="multiple"
            style={{ width: '100%' }}
            placeholder="Select your primary business goals"
            options={[
              { label: 'Increase organic traffic', value: 'increase_traffic' },
              { label: 'Improve search rankings', value: 'improve_rankings' },
              { label: 'Generate more leads', value: 'generate_leads' },
              { label: 'Boost online sales', value: 'boost_sales' },
              { label: 'Build brand awareness', value: 'brand_awareness' },
              { label: 'Establish thought leadership', value: 'thought_leadership' },
              { label: 'Enter new markets', value: 'market_expansion' },
            ]}
          />
        </Form.Item>
        <Form.Item
          name={['goals', 'target_metrics']}
          label="Target Metrics"
        >
          <TextArea 
            rows={4} 
            placeholder="What specific metrics would you like to improve? (e.g., 'Increase organic traffic by 50% in 6 months', 'Achieve top 3 rankings for key product terms')"
            maxLength={500}
            showCount
          />
        </Form.Item>
        <Form.Item
          name={['goals', 'timeline']}
          label="Timeline"
          rules={[{ required: true, message: 'Please select a timeline!' }]}
        >
          <Select
            style={{ width: '100%' }}
            placeholder="Select your target timeline"
            options={[
              { label: '3 months', value: '3_months' },
              { label: '6 months', value: '6_months' },
              { label: '1 year', value: '1_year' },
              { label: 'Long term (1+ years)', value: 'long_term' },
            ]}
          />
        </Form.Item>
        <Form.Item
          name={['goals', 'budget_range']}
          label="Monthly Budget Range"
        >
          <Select
            style={{ width: '100%' }}
            placeholder="Select your monthly budget range"
            options={[
              { label: '$500 - $1,000', value: '500_1000' },
              { label: '$1,000 - $2,500', value: '1000_2500' },
              { label: '$2,500 - $5,000', value: '2500_5000' },
              { label: '$5,000 - $10,000', value: '5000_10000' },
              { label: '$10,000+', value: '10000_plus' },
            ]}
          />
        </Form.Item>
        <Form.Item
          name={['goals', 'additional_notes']}
          label="Additional Notes"
        >
          <TextArea 
            rows={4} 
            placeholder="Any other goals or specific requirements you'd like to share?"
            maxLength={500}
            showCount
          />
        </Form.Item>
      </>
    ),
  },
];

export function OnboardingSurveyPage() {
  const [current, setCurrent] = useState(0);
  const [form] = Form.useForm();
  const navigate = useNavigate();
  const { message } = App.useApp();
  const [loading, setLoading] = useState(false);
  const [isInstructionsModalVisible, setIsInstructionsModalVisible] = useState(true);
  const [isConfirmModalVisible, setIsConfirmModalVisible] = useState(false);
  const { markSurveyCompleted, user } = useAuth();

  useEffect(() => {
    // Check if user is logged in and has completed the survey
    if (user?.has_completed_survey) {
      navigate({ to: '/dashboard' });
    }
  }, [user, navigate]);

  const next = async () => {
    try {
      const currentFields = form.getFieldsValue(true);
      const currentStepFields = Object.keys(currentFields).filter(field => {
        const fieldPath = field.split('.');
        return fieldPath[0] === steps[current].sectionKey;
      });
      
      await form.validateFields(currentFields);
      setCurrent(current + 1);
    } catch (errorInfo) {
      console.log('Validation failed:', errorInfo);
    }
  };

  const prev = () => {
    setCurrent(current - 1);
  };

  const handleSubmit = async () => {
    setIsConfirmModalVisible(true);
  };

  const renderConfirmationContent = (values: any) => {
    return (
      <div className="space-y-4">
        {steps.map((step, index) => (
          <div key={index} className="border-b pb-4 last:border-b-0">
            <h3 className="font-medium text-lg mb-2">{step.title}</h3>
            {Object.entries(values[step.sectionKey] || {}).map(([key, value]) => (
              <div key={key} className="mb-2">
                <span className="font-medium">{key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}: </span>
                <span>{Array.isArray(value) ? value.join(', ') : value?.toString()}</span>
              </div>
            ))}
          </div>
        ))}
      </div>
    );
  };

  const handleFinalSubmit = async () => {
    setLoading(true);
    try {
      const values = form.getFieldsValue(true);
      await surveyApi.submitSurvey(values);
      markSurveyCompleted();
      message.success('Survey submitted successfully!');
      navigate({ to: '/dashboard' });
    } catch (error) {
      console.error('Error submitting survey:', error);
      message.error('Failed to submit survey. Please try again.');
    } finally {
      setLoading(false);
      setIsConfirmModalVisible(false);
    }
  };

  return (
    <div className="onboarding-survey-page">
      <Card>
        <Steps current={current} items={steps.map(item => ({ title: item.title }))} />
        <div style={{ marginTop: 24 }}>
          <Form form={form} layout="vertical" onFinish={handleSubmit}>
            {steps[current].content}
          </Form>
        </div>
        <div style={{ marginTop: 24 }}>
          <Space>
            {current > 0 && (
              <Button onClick={prev}>
                Previous
              </Button>
            )}
            {current < steps.length - 1 && (
              <Button type="primary" onClick={next}>
                Next
              </Button>
            )}
            {current === steps.length - 1 && (
              <Button 
                type="primary" 
                onClick={handleSubmit}
                loading={loading}
              >
                Review & Submit
              </Button>
            )}
          </Space>
        </div>
      </Card>

      <Modal
        title="Welcome to the Brand Survey"
        open={isInstructionsModalVisible}
        onOk={() => setIsInstructionsModalVisible(false)}
        footer={[
          <Button key="start" type="primary" onClick={() => setIsInstructionsModalVisible(false)}>
            Start Survey
          </Button>
        ]}
        className="brand-survey-modal"
      >
        <div className="space-y-6">
          <p className="text-base leading-relaxed text-gray-600">
            Welcome to our brand survey! This survey will help us understand your brand better and provide more accurate content generation.
          </p>
          
          <div className="bg-blue-50 p-4 rounded-lg">
            <h4 className="text-base font-medium text-gray-900 mb-3">Required Information:</h4>
            <ul className="list-disc pl-5 text-base text-gray-600 space-y-1">
              <li>Brand Name</li>
              <li>Website URL</li>
            </ul>
          </div>
          
          <div className="bg-green-50 p-4 rounded-lg">
            <h4 className="text-base font-medium text-gray-900 mb-3">Optional Information:</h4>
            <p className="text-base text-gray-600">
              While only the brand name and website URL are required, we encourage you to provide as much information as possible. The more details you share, the better our AI agents can understand your brand and generate more accurate, targeted content.
            </p>
          </div>
          
          <div className="bg-yellow-50 p-4 rounded-lg">
            <h4 className="text-base font-medium text-gray-900 mb-3">What happens if I skip optional fields?</h4>
            <p className="text-base text-gray-600 mb-2">
              If you choose to skip optional fields, our AI agents will attempt to determine the missing information based on:
            </p>
            <ul className="list-disc pl-5 text-base text-gray-600 space-y-1">
              <li>Analysis of your brand's website content</li>
              <li>Industry knowledge and best practices</li>
              <li>Market research and competitor analysis</li>
            </ul>
          </div>
        </div>
      </Modal>

      <Modal
        title="Review Your Survey Responses"
        open={isConfirmModalVisible}
        onOk={handleFinalSubmit}
        onCancel={() => setIsConfirmModalVisible(false)}
        width={800}
        footer={[
          <Button key="back" onClick={() => setIsConfirmModalVisible(false)}>
            Revise Responses
          </Button>,
          <Button key="submit" type="primary" loading={loading} onClick={handleFinalSubmit}>
            Submit Survey
          </Button>,
        ]}
      >
        {renderConfirmationContent(form.getFieldsValue(true))}
      </Modal>
    </div>
  );
} 