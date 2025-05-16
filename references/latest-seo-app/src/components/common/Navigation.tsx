import { Link } from '@tanstack/react-router';
import { useAuth } from '../../contexts/AuthContext';
import { Layout, Button, Space, Switch } from 'antd';
import type { Dispatch, SetStateAction } from 'react';

const { Header } = Layout;

interface NavigationProps {
  isDarkMode: boolean;
  setIsDarkMode: Dispatch<SetStateAction<boolean>>;
}

export function Navigation({ isDarkMode, setIsDarkMode }: NavigationProps) {
  const { user, logout } = useAuth();

  const isAdmin = user?.roles.includes('business_admin');
  const isSuperuser = user?.roles.includes('superuser');

  return (
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
      <div style={{ 
        fontSize: '24px', 
        fontWeight: 'bold',
        color: isDarkMode ? '#ffffff' : '#000000'
      }}>
        <Link to="/">Summit Agents</Link>
      </div>
      <Space>
        <Switch
          checked={isDarkMode}
          onChange={setIsDarkMode}
          checkedChildren="🌙"
          unCheckedChildren="☀️"
        />
        {user ? (
          <>
            <Link to="/dashboard">
              <Button>Dashboard</Button>
            </Link>
            {(isAdmin || isSuperuser) && (
              <Link to="/users">
                <Button>User Management</Button>
              </Link>
            )}
            <Button onClick={logout}>Logout</Button>
          </>
        ) : (
          <>
            <Link to="/login">
              <Button>Sign In</Button>
            </Link>
            <Link to="/signup">
              <Button type="primary">Get Started</Button>
            </Link>
          </>
        )}
      </Space>
    </Header>
  );
} 