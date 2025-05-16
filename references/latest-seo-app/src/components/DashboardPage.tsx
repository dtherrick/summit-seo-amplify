import React from 'react';
import { Table, Card, Tag, Button, Space } from 'antd';
import { Line } from '@ant-design/charts';

const DashboardPage: React.FC = () => {
  // Sample data for the table
  const tableData = [
    {
      key: '1',
      name: 'John Brown',
      age: 32,
      address: 'New York No. 1 Lake Park',
      tags: ['NICE', 'DEVELOPER'],
    },
    {
      key: '2',
      name: 'Jim Green',
      age: 42,
      address: 'London No. 1 Lake Park',
      tags: ['LOSER'],
    },
    {
      key: '3',
      name: 'Joe Black',
      age: 32,
      address: 'Sydney No. 1 Lake Park',
      tags: ['COOL', 'TEACHER'],
    },
  ];

  // Sample data for the line chart
  const chartData = [
    { year: '2019', value: 3 },
    { year: '2020', value: 4 },
    { year: '2021', value: 3.5 },
    { year: '2022', value: 5 },
    { year: '2023', value: 4.9 },
  ];

  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      render: (text: string) => <a>{text}</a>,
    },
    {
      title: 'Age',
      dataIndex: 'age',
      key: 'age',
    },
    {
      title: 'Address',
      dataIndex: 'address',
      key: 'address',
    },
    {
      title: 'Tags',
      key: 'tags',
      dataIndex: 'tags',
      render: (tags: string[]) => (
        <>
          {tags.map(tag => {
            let color = tag.length > 5 ? 'geekblue' : 'green';
            if (tag === 'LOSER') {
              color = 'volcano';
            }
            return (
              <Tag color={color} key={tag}>
                {tag}
              </Tag>
            );
          })}
        </>
      ),
    },
    {
      title: 'Action',
      key: 'action',
      render: (_: any, record: any) => (
        <Space size="middle">
          <Button type="link">Invite {record.name}</Button>
          <Button type="link" danger>Delete</Button>
        </Space>
      ),
    },
  ];

  return (
    <div className="dashboard-page">
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        <Card title="Line Chart Demo">
          <Line
            data={chartData}
            xField="year"
            yField="value"
            point={{
              size: 5,
              shape: 'diamond',
            }}
            label={{
              style: {
                fill: '#aaa',
              },
            }}
          />
        </Card>
        
        <Card title="User Data">
          <Table columns={columns} dataSource={tableData} />
        </Card>
      </Space>
    </div>
  );
};

export default DashboardPage; 