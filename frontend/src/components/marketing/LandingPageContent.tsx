import React from 'react';
import { Heading, Text, View } from '@aws-amplify/ui-react';

const LandingPageContent: React.FC = () => {
  return (
    <View padding="large" textAlign="center">
      <Heading level={1}>Welcome to Summit SEO Amplify!</Heading>
      <Text>
        Supercharge your SEO with our AI-powered tools.
      </Text>
      {/* Add more marketing content, call to action buttons, etc. here */}
    </View>
  );
};

export default LandingPageContent;