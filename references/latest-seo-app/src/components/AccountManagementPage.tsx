import React from 'react';
import { Card, Tabs, Form, Input, Button, Switch, Select, Space } from 'antd';
import {
  UserOutlined,
  LockOutlined,
  CreditCardOutlined,
  TeamOutlined,
  ApiOutlined,
} from '@ant-design/icons';

const { TabPane } = Tabs;

const AccountManagementPage: React.FC = () => {
  const [form] = Form.useForm();

  return (
    <div className="account-management-page">
      <Card>
        <Tabs defaultActiveKey="1">
          <TabPane
            tab={
              <span>
                <UserOutlined />
                Profile
              </span>
            }
            key="1"
          >
            <Form layout="vertical" form={form}>
              <Form.Item
                name="name"
                label="Full Name"
                rules={[{ required: true, message: 'Please input your name!' }]}
              >
                <Input placeholder="Your name" />
              </Form.Item>
              <Form.Item
                name="email"
                label="Email"
                rules={[
                  { required: true, message: 'Please input your email!' },
                  { type: 'email', message: 'Please enter a valid email!' }
                ]}
              >
                <Input placeholder="Your email" />
              </Form.Item>
              <Form.Item>
                <Button type="primary">Save Changes</Button>
              </Form.Item>
            </Form>
          </TabPane>

          <TabPane
            tab={
              <span>
                <LockOutlined />
                Security
              </span>
            }
            key="2"
          >
            <Form layout="vertical">
              <Form.Item
                name="currentPassword"
                label="Current Password"
                rules={[{ required: true, message: 'Please input your current password!' }]}
              >
                <Input.Password />
              </Form.Item>
              <Form.Item
                name="newPassword"
                label="New Password"
                rules={[{ required: true, message: 'Please input your new password!' }]}
              >
                <Input.Password />
              </Form.Item>
              <Form.Item>
                <Button type="primary">Update Password</Button>
              </Form.Item>
            </Form>
          </TabPane>

          <TabPane
            tab={
              <span>
                <CreditCardOutlined />
                Billing
              </span>
            }
            key="3"
          >
            <Space direction="vertical" style={{ width: '100%' }}>
              <Card size="small" title="Current Plan">
                <p>Pro Plan - $49/month</p>
                <Button type="primary">Upgrade Plan</Button>
              </Card>
              <Card size="small" title="Payment Method">
                <p>Visa ending in 4242</p>
                <Button>Update Payment Method</Button>
              </Card>
            </Space>
          </TabPane>

          <TabPane
            tab={
              <span>
                <TeamOutlined />
                Team
              </span>
            }
            key="4"
          >
            <Form layout="vertical">
              <Form.Item
                name="inviteEmail"
                label="Invite Team Member"
                rules={[
                  { required: true, message: 'Please input an email!' },
                  { type: 'email', message: 'Please enter a valid email!' }
                ]}
              >
                <Input placeholder="colleague@example.com" />
              </Form.Item>
              <Form.Item
                name="role"
                label="Role"
                rules={[{ required: true, message: 'Please select a role!' }]}
              >
                <Select>
                  <Select.Option value="admin">Admin</Select.Option>
                  <Select.Option value="editor">Editor</Select.Option>
                  <Select.Option value="viewer">Viewer</Select.Option>
                </Select>
              </Form.Item>
              <Form.Item>
                <Button type="primary">Send Invitation</Button>
              </Form.Item>
            </Form>
          </TabPane>

          <TabPane
            tab={
              <span>
                <ApiOutlined />
                API
              </span>
            }
            key="5"
          >
            <Space direction="vertical" style={{ width: '100%' }}>
              <Card size="small" title="API Key">
                <Input.Password value="your-api-key-here" readOnly />
                <Button style={{ marginTop: 16 }}>Generate New Key</Button>
              </Card>
              <Card size="small" title="API Access">
                <Form layout="vertical">
                  <Form.Item label="Enable API Access">
                    <Switch defaultChecked />
                  </Form.Item>
                </Form>
              </Card>
            </Space>
          </TabPane>
        </Tabs>
      </Card>
    </div>
  );
};

export default AccountManagementPage; 