``` typerscript
import React from 'react';
import { Button, Typography, Space, Card, Row, Col, Layout, Switch, ConfigProvider, theme, Divider } from 'antd';
import { Link, useNavigate } from '@tanstack/react-router';
import {
  RocketOutlined,
  CheckCircleOutlined,
  StarOutlined,
  LineChartOutlined,
  TeamOutlined,
  FormOutlined,
  UserOutlined,
  BarChartOutlined,
  ArrowRightOutlined,
  GithubOutlined,
  TwitterOutlined,
  LinkedinOutlined,
  AimOutlined,
} from '@ant-design/icons';

const { Title, Text, Paragraph, Link: AntLink } = Typography;
const { Header, Footer } = Layout;

export function LandingPage() {
  const navigate = useNavigate();
  const [isDarkMode, setIsDarkMode] = React.useState(false);

  const features = [
    {
      icon: <CheckCircleOutlined className="text-2xl text-primary" />,
      title: 'AI-Powered SEO Analysis',
      description: 'Get instant insights and recommendations for your website',
    },
    {
      icon: <StarOutlined className="text-2xl text-primary" />,
      title: 'Keyword Optimization',
      description: 'Discover and track the most effective keywords for your content',
    },
    {
      icon: <LineChartOutlined className="text-2xl text-primary" />,
      title: 'Performance Tracking',
      description: 'Monitor your SEO progress with detailed analytics',
    },
    {
      icon: <TeamOutlined className="text-2xl text-primary" />,
      title: 'Team Collaboration',
      description: 'Work together with your team on SEO strategies',
    },
  ];

  const howItWorks = [
    {
      icon: <FormOutlined className="text-4xl text-primary" />,
      title: 'Share Your Brand Info',
      description: 'Tell us about your brand and website',
    },
    {
      icon: <UserOutlined className="text-4xl text-primary" />,
      title: 'Define Your Audience',
      description: 'Help us understand your target audience and their needs',
    },
    {
      icon: <AimOutlined className="text-4xl text-primary" />,
      title: 'Define Your Goals',
      description: 'Set clear objectives and success metrics for your SEO strategy',
    },
    {
      icon: <BarChartOutlined className="text-4xl text-primary" />,
      title: 'Get Personalized SEO Strategy',
      description: 'Receive AI-powered recommendations tailored to your brand',
    },
  ];

  const sectionStyle = {
    width: '100%',
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '0 24px',
    textAlign: 'center' as const,
  };

  const cardStyle = {
    textAlign: 'center' as const,
    height: '100%',
    background: isDarkMode ? '#141414' : '#ffffff',
    display: 'flex',
    flexDirection: 'column' as const,
    justifyContent: 'flex-start' as const,
  };

  const cardContentStyle = {
    flex: 1,
    display: 'flex',
    flexDirection: 'column' as const,
    justifyContent: 'flex-start' as const,
    gap: '16px',
  };

  const footerLinkStyle = {
    color: isDarkMode ? 'rgba(255, 255, 255, 0.65)' : 'rgba(0, 0, 0, 0.65)',
  };

  const footerSections = [
    {
      title: 'Product',
      links: [
        { text: 'Features', href: '#features' },
        { text: 'Pricing', href: '/pricing' },
        { text: 'Documentation', href: '/docs' },
      ],
    },
    {
      title: 'Company',
      links: [
        { text: 'About Us', href: '/about' },
        { text: 'Blog', href: '/blog' },
        { text: 'Careers', href: '/careers' },
      ],
    },
    {
      title: 'Resources',
      links: [
        { text: 'Support', href: '/support' },
        { text: 'Terms of Service', href: '/terms' },
        { text: 'Privacy Policy', href: '/privacy' },
      ],
    },
  ];

  return (
    <ConfigProvider
      theme={{
        algorithm: isDarkMode ? theme.darkAlgorithm : theme.defaultAlgorithm,
        token: {
          colorPrimary: '#32a9be',
          borderRadius: 6,
          colorBgContainer: isDarkMode ? '#141414' : '#ffffff',
          colorBgLayout: isDarkMode ? '#000000' : '#f0f2f5',
        },
      }}
    >
      <Layout className="min-h-screen">
        {/* Custom Header */}
        <Header style={{ 
          background: isDarkMode ? '#141414' : '#fff', 
          borderBottom: `1px solid ${isDarkMode ? '#303030' : '#f0f0f0'}`,
          position: 'fixed',
          width: '100%',
          zIndex: 1,
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          padding: '0 50px'
        }}>
          <div className="logo" style={{ 
            fontSize: '24px', 
            fontWeight: 'bold',
            color: isDarkMode ? '#ffffff' : '#000000'
          }}>
            Summit Agents
          </div>
          <Space>
            <Switch
              checked={isDarkMode}
              onChange={setIsDarkMode}
              checkedChildren="🌙"
              unCheckedChildren="☀️"
            />
            <Button onClick={() => navigate({ to: '/login' })}>Sign In</Button>
            <Button 
              type="primary" 
              icon={<RocketOutlined />}
              onClick={() => navigate({ to: '/signup' })}
            >
              Get Started
            </Button>
          </Space>
        </Header>

        <div className="landing-page" style={{ 
          marginTop: 64,
          background: isDarkMode ? '#000000' : '#ffffff',
          minHeight: 'calc(100vh - 64px)',
        }}>
          {/* Hero Section */}
          <div style={{...sectionStyle, paddingTop: '64px', paddingBottom: '64px'}}>
            <Title level={1} style={{textAlign: 'center', marginBottom: 32}}>
              Welcome to Summit Agents
            </Title>
            <Paragraph style={{textAlign: 'center', fontSize: '1.25rem', marginBottom: 32}}>
              Leverage AI-powered insights to optimize your content and boost your search rankings.
              Get started today and watch your organic traffic soar.
            </Paragraph>
            <Space size="large" style={{justifyContent: 'center', width: '100%'}}>
              <Button 
                type="primary" 
                size="large"
                icon={<RocketOutlined />}
                onClick={() => navigate({ to: '/signup' })}
              >
                Get Started
              </Button>
              <Button 
                size="large"
                onClick={() => navigate({ to: '/login' })}
              >
                Sign In
              </Button>
            </Space>
          </div>

          {/* How It Works Section */}
          <div style={{
            background: isDarkMode ? '#141414' : '#f0f2f5',
            padding: '64px 0',
          }}>
            <div style={sectionStyle}>
              <Title level={2} style={{textAlign: 'center', marginBottom: 48}}>
                How It Works
              </Title>
              <Row gutter={[48, 24]} justify="center" align="middle">
                {howItWorks.map((step, index) => (
                  <React.Fragment key={index}>
                    <Col xs={24} sm={24} md={5}>
                      <Card style={cardStyle} bordered={false} bodyStyle={cardContentStyle}>
                        <div style={{fontSize: '2.5rem', marginBottom: 24, color: '#32a9be'}}>{step.icon}</div>
                        <Title level={4} style={{textAlign: 'center', marginBottom: 16}}>{step.title}</Title>
                        <Text style={{textAlign: 'center', display: 'block'}}>{step.description}</Text>
                      </Card>
                    </Col>
                    {index < howItWorks.length - 1 && (
                      <Col xs={24} sm={24} md={1} style={{
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        height: '100%'
                      }}>
                        <div style={{
                          width: '100%',
                          height: '2px',
                          background: isDarkMode ? '#ffffff' : '#000000',
                          position: 'relative',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center'
                        }}>
                          <ArrowRightOutlined style={{
                            position: 'absolute',
                            fontSize: '24px',
                            color: isDarkMode ? '#ffffff' : '#000000',
                          }} />
                        </div>
                      </Col>
                    )}
                  </React.Fragment>
                ))}
              </Row>
              <div style={{ marginTop: 48 }}>
                <Button 
                  type="primary" 
                  size="large"
                  icon={<RocketOutlined />}
                  onClick={() => navigate({ to: '/signup' })}
                >
                  Get Started
                </Button>
              </div>
            </div>
          </div>

          {/* Features Section */}
          <div style={{...sectionStyle, padding: '64px 24px'}}>
            <Title level={2} style={{textAlign: 'center', marginBottom: 48}}>
              Features
            </Title>
            <Row gutter={[32, 32]} justify="center">
              {features.map((feature, index) => (
                <Col xs={24} sm={12} md={6} key={index}>
                  <Card style={cardStyle} bordered={false} bodyStyle={cardContentStyle}>
                    <div style={{fontSize: '2.5rem', marginBottom: 24, color: '#32a9be'}}>{feature.icon}</div>
                    <Title level={4} style={{textAlign: 'center', marginBottom: 16}}>{feature.title}</Title>
                    <Text style={{textAlign: 'center', display: 'block'}}>{feature.description}</Text>
                  </Card>
                </Col>
              ))}
            </Row>
          </div>

          {/* Call to Action Section */}
          <div style={{
            background: isDarkMode ? '#141414' : '#f0f2f5',
            padding: '64px 0',
          }}>
            <div style={sectionStyle}>
              <Title level={2} style={{textAlign: 'center', marginBottom: 32}}>
                Ready to Boost Your SEO Rankings?
              </Title>
              <Button 
                type="primary" 
                size="large"
                icon={<RocketOutlined />}
                onClick={() => navigate({ to: '/signup' })}
              >
                Get Started
              </Button>
            </div>
          </div>

          {/* Footer Section */}
          <Footer style={{
            background: isDarkMode ? '#141414' : '#ffffff',
            padding: '64px 24px 24px',
          }}>
            <div style={sectionStyle}>
              <Row gutter={[48, 32]} justify="space-between">
                {footerSections.map((section, index) => (
                  <Col xs={24} sm={8} key={index}>
                    <Title level={5} style={{marginBottom: 24}}>{section.title}</Title>
                    <Space direction="vertical" size={12}>
                      {section.links.map((link, linkIndex) => (
                        <AntLink key={linkIndex} href={link.href} style={footerLinkStyle}>
                          {link.text}
                        </AntLink>
                      ))}
                    </Space>
                  </Col>
                ))}
              </Row>
              
              <Divider style={{ margin: '48px 0 24px' }} />
              
              <Row justify="space-between" align="middle">
                <Col>
                  <Text style={footerLinkStyle}>
                    © {new Date().getFullYear()} Summit Agents. All rights reserved.
                  </Text>
                </Col>
                <Col>
                  <Space size={24}>
                    <AntLink href="https://github.com" target="_blank" style={footerLinkStyle}>
                      <GithubOutlined style={{ fontSize: '20px' }} />
                    </AntLink>
                    <AntLink href="https://twitter.com" target="_blank" style={footerLinkStyle}>
                      <TwitterOutlined style={{ fontSize: '20px' }} />
                    </AntLink>
                    <AntLink href="https://linkedin.com" target="_blank" style={footerLinkStyle}>
                      <LinkedinOutlined style={{ fontSize: '20px' }} />
                    </AntLink>
                  </Space>
                </Col>
              </Row>
            </div>
          </Footer>
        </div>
      </Layout>
    </ConfigProvider>
  );
} 
```
