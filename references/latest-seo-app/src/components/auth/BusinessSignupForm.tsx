import { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate } from '@tanstack/react-router';
import { Form, Input, Button, Card, Typography, Alert, Space } from 'antd';
import { UserOutlined, LockOutlined, BankOutlined } from '@ant-design/icons';

const { Title } = Typography;

interface SignupFormValues {
  businessName: string;
  email: string;
  password: string;
  confirmPassword: string;
}

export function BusinessSignupForm() {
  const [error, setError] = useState('');
  const { signupBusiness, login } = useAuth();
  const navigate = useNavigate();

  const onFinish = async (values: SignupFormValues) => {
    setError('');

    if (values.password !== values.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (values.password.length < 8) {
      setError('Password must be at least 8 characters long');
      return;
    }

    try {
      await signupBusiness(values.businessName, values.email, values.password);
      // After successful signup, log in automatically
      await login(values.email, values.password);
      // Redirect to onboarding
      navigate({ to: '/onboarding' });
    } catch (err) {
      setError('Failed to create business account. Please try again.');
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '0 auto', padding: '20px' }}>
      <Card>
        <Title level={2} style={{ textAlign: 'center', marginBottom: '24px' }}>
          Create Business Account
        </Title>
        
        {error && (
          <Alert
            message={error}
            type="error"
            showIcon
            style={{ marginBottom: '24px' }}
          />
        )}
        
        <Form
          name="signup"
          onFinish={onFinish}
          layout="vertical"
          requiredMark={false}
        >
          <Form.Item
            name="businessName"
            rules={[{ required: true, message: 'Please input your business name!' }]}
          >
            <Input
              prefix={<BankOutlined />}
              placeholder="Business Name"
              size="large"
            />
          </Form.Item>

          <Form.Item
            name="email"
            rules={[
              { required: true, message: 'Please input your email!' },
              { type: 'email', message: 'Please enter a valid email!' }
            ]}
          >
            <Input
              prefix={<UserOutlined />}
              placeholder="Email"
              size="large"
            />
          </Form.Item>
          
          <Form.Item
            name="password"
            rules={[
              { required: true, message: 'Please input your password!' },
              { min: 8, message: 'Password must be at least 8 characters long!' }
            ]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="Password"
              size="large"
            />
          </Form.Item>

          <Form.Item
            name="confirmPassword"
            dependencies={['password']}
            rules={[
              { required: true, message: 'Please confirm your password!' },
              ({ getFieldValue }) => ({
                validator(_, value) {
                  if (!value || getFieldValue('password') === value) {
                    return Promise.resolve();
                  }
                  return Promise.reject(new Error('The two passwords do not match!'));
                },
              }),
            ]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="Confirm Password"
              size="large"
            />
          </Form.Item>
          
          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              size="large"
              block
            >
              Create Account
            </Button>
          </Form.Item>

          <div style={{ textAlign: 'center' }}>
            <Space direction="vertical" size="small">
              <span className="text-gray-600">
                Already have an account?{' '}
                <Button 
                  type="link" 
                  onClick={() => navigate({ to: '/login' })}
                  style={{ padding: 0 }}
                >
                  Sign in
                </Button>
              </span>
            </Space>
          </div>
        </Form>
      </Card>
    </div>
  );
} 