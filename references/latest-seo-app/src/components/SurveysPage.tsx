import React, { useEffect, useState } from 'react';
import { Table, Typography, Card, Space, message, Tag, Tooltip, Button } from 'antd';
import type { Key } from 'react';
import { surveyApi, type SurveyResponseDB } from '../lib/api';
import SurveyDetailsModal from './SurveyDetailsModal';

const { Title } = Typography;

const SurveysPage: React.FC = () => {
  const [surveys, setSurveys] = useState<SurveyResponseDB[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedSurvey, setSelectedSurvey] = useState<SurveyResponseDB | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Helper function to split comma-separated strings into arrays
  const splitKeywords = (keywords: string): string[] => {
    return keywords.split(',').map(k => k.trim()).filter(Boolean);
  };

  useEffect(() => {
    const fetchSurveys = async () => {
      try {
        const response = await surveyApi.getAllSurveys();
        setSurveys(response);
      } catch (error) {
        console.error('Error fetching surveys:', error);
        message.error('Failed to fetch surveys. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchSurveys();
  }, []);

  const handleViewDetails = (survey: SurveyResponseDB) => {
    setSelectedSurvey(survey);
    setIsModalOpen(true);
  };

  const columns = [
    {
      title: 'Customer ID',
      dataIndex: 'customer_id',
      key: 'customer_id',
      sorter: (a: SurveyResponseDB, b: SurveyResponseDB) => a.customer_id.localeCompare(b.customer_id),
    },
    {
      title: 'Brand Name',
      dataIndex: ['response_data', 'general_information', 'brand_name'],
      key: 'brand_name',
      sorter: (a: SurveyResponseDB, b: SurveyResponseDB) => 
        a.response_data.general_information.brand_name.localeCompare(b.response_data.general_information.brand_name),
    },
    {
      title: 'Categories',
      dataIndex: ['response_data', 'general_information', 'categories'],
      key: 'categories',
      render: (categories: string[]) => (
        <Space wrap>
          {categories.map(category => (
            <Tag key={category} color="blue">{category}</Tag>
          ))}
        </Space>
      ),
      filters: [
        { text: 'Technology', value: 'Technology' },
        { text: 'Fashion', value: 'Fashion' },
        { text: 'Health & Wellness', value: 'Health & Wellness' },
        { text: 'Food & Beverage', value: 'Food & Beverage' },
        { text: 'Travel', value: 'Travel' },
        { text: 'Home & Garden', value: 'Home & Garden' },
        { text: 'Education', value: 'Education' },
        { text: 'Finance', value: 'Finance' },
        { text: 'Entertainment', value: 'Entertainment' },
        { text: 'Automotive', value: 'Automotive' },
      ],
      onFilter: (value: Key | boolean, record: SurveyResponseDB) => 
        record.response_data.general_information.categories.includes(value as string),
    },
    {
      title: 'Target Audience',
      dataIndex: ['response_data', 'audience', 'who_is_your_audience'],
      key: 'target_audience',
      ellipsis: true,
      render: (text: string) => (
        <Tooltip title={text}>
          <span>{text}</span>
        </Tooltip>
      ),
    },
    {
      title: 'Seed Keywords',
      dataIndex: ['response_data', 'seo', 'seed_keywords'],
      key: 'seed_keywords',
      render: (keywords: string) => (
        <Space wrap>
          {splitKeywords(keywords).map(keyword => (
            <Tag key={keyword} color="green">{keyword}</Tag>
          ))}
        </Space>
      ),
    },
    {
      title: 'Key Competitors',
      dataIndex: ['response_data', 'competitors', 'key_competitors'],
      key: 'key_competitors',
      ellipsis: true,
      render: (text: string) => (
        <Tooltip title={text}>
          <span>{text}</span>
        </Tooltip>
      ),
    },
    {
      title: 'Content Pillars',
      dataIndex: ['response_data', 'content_pillars'],
      key: 'content_pillars',
      ellipsis: true,
      render: (text: string) => (
        <Tooltip title={text}>
          <span>{text}</span>
        </Tooltip>
      ),
    },
    {
      title: 'Created',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date: string) => new Date(date).toLocaleDateString(),
      sorter: (a: SurveyResponseDB, b: SurveyResponseDB) => 
        new Date(a.created_at).getTime() - new Date(b.created_at).getTime(),
    },
    {
      title: 'Last Updated',
      dataIndex: 'updated_at',
      key: 'updated_at',
      render: (date: string) => new Date(date).toLocaleDateString(),
      sorter: (a: SurveyResponseDB, b: SurveyResponseDB) => 
        new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime(),
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_: any, record: SurveyResponseDB) => (
        <Button type="link" onClick={() => handleViewDetails(record)}>
          View Details
        </Button>
      ),
    },
  ];

  return (
    <div className="p-6">
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        <Title level={2}>Surveys</Title>
        <Card>
          <Table
            dataSource={surveys}
            columns={columns}
            rowKey="id"
            loading={loading}
            pagination={{ 
              pageSize: 10,
              showSizeChanger: true,
              showQuickJumper: true,
              showTotal: (total) => `Total ${total} items`,
            }}
            scroll={{ x: true }}
          />
        </Card>
      </Space>

      {selectedSurvey && (
        <SurveyDetailsModal
          survey={selectedSurvey}
          open={isModalOpen}
          onClose={() => {
            setIsModalOpen(false);
            setSelectedSurvey(null);
          }}
        />
      )}
    </div>
  );
};

export default SurveysPage; 