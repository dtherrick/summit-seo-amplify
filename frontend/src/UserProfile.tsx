import React, { useState, useEffect } from 'react';
import { get, put } from 'aws-amplify/api';
import { TextField, Button, Heading, View, Card, Flex, Text, Alert } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';

interface UserProfileData {
  user_id: string;
  cognito_id: string;
  email: string;
  full_name?: string;
  // Add other profile fields here as needed
}

const UserProfile: React.FC = () => {
  const [profile, setProfile] = useState<UserProfileData | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [editFullName, setEditFullName] = useState<string>('');
  const [isSaving, setIsSaving] = useState<boolean>(false);
  const [saveSuccess, setSaveSuccess] = useState<boolean>(false);
  const [saveError, setSaveError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProfile = async () => {
      setIsLoading(true);
      setError(null);
      setSaveSuccess(false);
      setSaveError(null);
      try {
        const restOperation = get({
          apiName: 'SummitSEOAmplifyAPI', // Replace with your actual API name configured in Amplify
          path: '/users/me',
        });
        const { body } = await restOperation.response;
        const data = await body.json();
        setProfile(data);
        setEditFullName(data.full_name || '');
      } catch (err: any) {
        console.error('Error fetching user profile:', err);
        setError('Failed to fetch user profile. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchProfile();
  }, []);

  const handleSaveProfile = async () => {
    if (!profile) return;
    setIsSaving(true);
    setSaveSuccess(false);
    setSaveError(null);
    try {
      const restOperation = put({
        apiName: 'SummitSEOAmplifyAPI', // Replace with your actual API name
        path: '/users/me',
        options: {
          body: {
            full_name: editFullName,
          },
        },
      });
      await restOperation.response;
      setProfile({ ...profile, full_name: editFullName });
      setSaveSuccess(true);
    } catch (err: any) {
      console.error('Error saving user profile:', err);
      const errorMessage = err.response?.data?.detail || 'Failed to save profile. Please try again.';
      setSaveError(errorMessage);
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return <Text>Loading profile...</Text>;
  }

  if (error) {
    return <Alert variation="error" heading="Error">{error}</Alert>;
  }

  if (!profile) {
    return <Text>No profile data found.</Text>;
  }

  return (
    <Card variation="outlined" width="100%" maxWidth="500px" margin="20px auto">
      <Flex direction="column" gap="medium">
        <Heading level={3}>User Profile</Heading>

        <View>
          <Text fontWeight="bold">Email:</Text>
          <Text>{profile.email}</Text>
        </View>
        <View>
          <Text fontWeight="bold">User ID:</Text>
          <Text>{profile.user_id}</Text>
        </View>

        <TextField
          label="Full Name"
          value={editFullName}
          onChange={(e) => {
            setEditFullName(e.target.value);
            setSaveSuccess(false); // Reset success message on change
            setSaveError(null); // Reset error message on change
          }}
          placeholder="Enter your full name"
        />

        {saveSuccess && (
          <Alert variation="success" isDismissible={true} onDismiss={() => setSaveSuccess(false)}>
            Profile saved successfully!
          </Alert>
        )}
        {saveError && (
          <Alert variation="error" isDismissible={true} onDismiss={() => setSaveError(null)} heading="Save Error">
            {saveError}
          </Alert>
        )}

        <Button onClick={handleSaveProfile} variation="primary" isLoading={isSaving} disabled={isSaving}>
          {isSaving ? 'Saving...' : 'Save Profile'}
        </Button>
      </Flex>
    </Card>
  );
};

export default UserProfile;