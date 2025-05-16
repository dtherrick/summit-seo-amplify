import React from 'react';
import { Modal, Typography, Descriptions, Tag, Space, Divider } from 'antd';
import type { SurveyResponseDB } from '../lib/api';

const { Title, Text } = Typography;

interface SurveyDetailsModalProps {
  survey: SurveyResponseDB;
  open: boolean;
  onClose: () => void;
}

const SurveyDetailsModal: React.FC<SurveyDetailsModalProps> = ({ survey, open, onClose }) => {
  const { response_data } = survey;

  // Helper function to split comma-separated strings into arrays
  const splitKeywords = (keywords: string): string[] => {
    return keywords.split(',').map(k => k.trim()).filter(Boolean);
  };

  return (
    <Modal
      title="Survey Details"
      open={open}
      onCancel={onClose}
      width={800}
      footer={null}
    >
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        {/* General Information Section */}
        <div>
          <Title level={4}>General Information</Title>
          <Descriptions column={1}>
            <Descriptions.Item label="Brand Name">
              {response_data.general_information.brand_name}
            </Descriptions.Item>
            <Descriptions.Item label="Description">
              {response_data.general_information.brand_description}
            </Descriptions.Item>
            <Descriptions.Item label="Website">
              <a href={response_data.general_information.url} target="_blank" rel="noopener noreferrer">
                {response_data.general_information.url}
              </a>
            </Descriptions.Item>
            <Descriptions.Item label="Categories">
              <Space wrap>
                {response_data.general_information.categories.map(category => (
                  <Tag key={category} color="blue">{category}</Tag>
                ))}
              </Space>
            </Descriptions.Item>
          </Descriptions>
        </div>

        <Divider />

        {/* Audience Section */}
        <div>
          <Title level={4}>Target Audience</Title>
          <Descriptions column={1}>
            <Descriptions.Item label="Who is your audience?">
              {response_data.audience.who_is_your_audience}
            </Descriptions.Item>
            <Descriptions.Item label="Needs and Preferences">
              {response_data.audience.needs_and_preferences}
            </Descriptions.Item>
          </Descriptions>
        </div>

        <Divider />

        {/* SEO Section */}
        <div>
          <Title level={4}>SEO Information</Title>
          <Descriptions column={1}>
            <Descriptions.Item label="Seed Keywords">
              <Space wrap>
                {splitKeywords(response_data.seo.seed_keywords).map(keyword => (
                  <Tag key={keyword} color="green">{keyword}</Tag>
                ))}
              </Space>
            </Descriptions.Item>
            <Descriptions.Item label="Informational Intent Keywords">
              <Space wrap>
                {splitKeywords(response_data.seo.pillar_keywords.informational_intent).map(keyword => (
                  <Tag key={keyword} color="orange">{keyword}</Tag>
                ))}
              </Space>
            </Descriptions.Item>
            <Descriptions.Item label="Commercial Intent Keywords">
              <Space wrap>
                {splitKeywords(response_data.seo.pillar_keywords.commercial_intent).map(keyword => (
                  <Tag key={keyword} color="purple">{keyword}</Tag>
                ))}
              </Space>
            </Descriptions.Item>
            <Descriptions.Item label="Transactional Intent Keywords">
              <Space wrap>
                {splitKeywords(response_data.seo.pillar_keywords.transactional_intent).map(keyword => (
                  <Tag key={keyword} color="red">{keyword}</Tag>
                ))}
              </Space>
            </Descriptions.Item>
            <Descriptions.Item label="Brand Intent Keywords">
              <Space wrap>
                {splitKeywords(response_data.seo.pillar_keywords.brand_intent).map(keyword => (
                  <Tag key={keyword} color="cyan">{keyword}</Tag>
                ))}
              </Space>
            </Descriptions.Item>
          </Descriptions>
        </div>

        <Divider />

        {/* Competitors Section */}
        <div>
          <Title level={4}>Competitors</Title>
          <Descriptions column={1}>
            <Descriptions.Item label="Key Competitors">
              {response_data.competitors.key_competitors}
            </Descriptions.Item>
            <Descriptions.Item label="Secondary Competitors">
              {response_data.competitors.secondary_competitors}
            </Descriptions.Item>
          </Descriptions>
        </div>

        <Divider />

        {/* Content Section */}
        <div>
          <Title level={4}>Content Strategy</Title>
          <Descriptions column={1}>
            <Descriptions.Item label="Content Pillars">
              {response_data.content_pillars}
            </Descriptions.Item>
            <Descriptions.Item label="Content Guardrails">
              {response_data.guardrails}
            </Descriptions.Item>
          </Descriptions>
        </div>

        <Divider />

        {/* Metadata */}
        <div>
          <Title level={4}>Survey Information</Title>
          <Descriptions column={2}>
            <Descriptions.Item label="Customer ID">
              {survey.customer_id}
            </Descriptions.Item>
            <Descriptions.Item label="Created">
              {new Date(survey.created_at).toLocaleString()}
            </Descriptions.Item>
            <Descriptions.Item label="Last Updated">
              {new Date(survey.updated_at).toLocaleString()}
            </Descriptions.Item>
          </Descriptions>
        </div>
      </Space>
    </Modal>
  );
};

export default SurveyDetailsModal; 