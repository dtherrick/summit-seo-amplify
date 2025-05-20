import React, { ReactNode } from 'react';
import { View, Flex } from '@aws-amplify/ui-react';
import { Navigation } from './Navigation'; // Assuming Navigation will be in the same directory

interface LayoutProps {
  children: ReactNode;
  showNav?: boolean;
}

export const Layout: React.FC<LayoutProps> = ({ children, showNav = true }) => {
  return (
    <Flex direction="column" minHeight="100vh" className="bg-gray-100 dark:bg-gray-900">
      {showNav && <Navigation />}
      <View as="main" flex="1" className="p-4 md:p-6">
        {children}
      </View>
      {/* Optional: Footer can be added here */}
      {/* <View as="footer" padding="medium" backgroundColor="neutral.20">
        <Text textAlign="center">© 2024 Summit SEO Amplify</Text>
      </View> */}
    </Flex>
  );
};