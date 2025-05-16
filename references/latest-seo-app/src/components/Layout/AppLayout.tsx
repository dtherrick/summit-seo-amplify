import React from 'react';
import { Layout, Menu, Switch, theme, ConfigProvider, App } from 'antd';
import { Link, useLocation } from 'react-router-dom';
import {
  HomeOutlined,
  UserOutlined,
  FormOutlined,
  DashboardOutlined,
  SettingOutlined,
} from '@ant-design/icons';

const { Header, Sider, Content } = Layout;

interface AppLayoutProps {
  children: React.ReactNode;
}

const AppLayout: React.FC<AppLayoutProps> = ({ children }) => {
  const location = useLocation();
  const [isDarkMode, setIsDarkMode] = React.useState(false);

  const menuItems = [
    {
      key: '/',
      icon: <HomeOutlined />,
      label: <Link to="/">Home</Link>,
    },
    {
      key: '/signup',
      icon: <UserOutlined />,
      label: <Link to="/signup">Sign Up</Link>,
    },
    {
      key: '/onboarding',
      icon: <FormOutlined />,
      label: <Link to="/onboarding">Onboarding</Link>,
    },
    {
      key: '/dashboard',
      icon: <DashboardOutlined />,
      label: <Link to="/dashboard">Dashboard</Link>,
    },
    {
      key: '/account',
      icon: <SettingOutlined />,
      label: <Link to="/account">Account</Link>,
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
      <App>
        <Layout style={{ minHeight: '100vh' }}>
          <Sider
            width={200}
            style={{
              background: isDarkMode ? '#141414' : '#ffffff',
              borderRight: `1px solid ${isDarkMode ? '#303030' : '#f0f0f0'}`,
            }}
          >
            <div style={{ 
              padding: '16px',
              textAlign: 'center',
              borderBottom: `1px solid ${isDarkMode ? '#303030' : '#f0f0f0'}`,
              marginBottom: '16px'
            }}>
              <div className="logo" style={{ 
                fontSize: '24px', 
                fontWeight: 'bold',
                color: isDarkMode ? '#ffffff' : '#000000'
              }}>
                Summit Agents
              </div>
            </div>
            <Menu
              mode="inline"
              selectedKeys={[location.pathname]}
              items={menuItems}
              style={{
                background: 'transparent',
                border: 'none'
              }}
            />
          </Sider>
          <Layout>
            <Header style={{
              padding: '0 16px',
              background: isDarkMode ? '#141414' : '#ffffff',
              borderBottom: `1px solid ${isDarkMode ? '#303030' : '#f0f0f0'}`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'flex-end'
            }}>
              <Switch
                checked={isDarkMode}
                onChange={setIsDarkMode}
                checkedChildren="🌙"
                unCheckedChildren="☀️"
              />
            </Header>
            <Content style={{
              margin: '24px',
              padding: '24px',
              background: isDarkMode ? '#141414' : '#ffffff',
              borderRadius: '8px',
              minHeight: 280
            }}>
              {children}
            </Content>
          </Layout>
        </Layout>
      </App>
    </ConfigProvider>
  );
};

export default AppLayout; 