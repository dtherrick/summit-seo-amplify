import React, { useState, useEffect } from 'react';
import { fetchAuthSession } from 'aws-amplify/auth';
import { TextField, Button, Heading, View, Card, Flex, Text, Alert } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';
import { get, put } from 'aws-amplify/api';

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
      // console.log('Fetching profile...'); // Example of a potentially useful log to keep if desired

      let authToken = '';
      try {
        const session = await fetchAuthSession();
        // console.log('Current user session:', session);

        const idToken = session.tokens?.idToken;
        // const accessToken = session.tokens?.accessToken; // Removed unused accessToken

        // console.log('ID Token available:', !!idToken);
        // console.log('Access Token available:', !!accessToken);

        if (idToken) {
          authToken = idToken.toString();
          // console.log('ID Token prefix:', authToken.substring(0, 20) + '...');
        } else {
          console.error('ID token is undefined. Cannot make authenticated API call.');
          setError('Authentication token is missing. Please try logging out and back in.');
          setIsLoading(false);
          return;
        }
        // Optional: log current authenticated user from Amplify
        // const user = await getCurrentUser();
        // console.log('Current authenticated user:', user);

      } catch (err) {
        console.error('Error fetching auth session:', err);
        setError('Failed to fetch authentication session. Please try logging out and back in.');
        setIsLoading(false);
        return;
      }

      try {
        // Path should be relative to the configured endpoint (e.g., "users/me")
        const path = 'users/me'; // No leading slash
        // console.log('Making API GET request to path:', path);

        // Call the API using get method from Amplify v6 with manual authorization
        const { body } = await get({
          apiName: 'SummitSEOAmplifyAPI',
          path: path,
          options: {
            headers: {
              Authorization: authToken ? `Bearer ${authToken}` : ''
            }
          }
        }).response;

        const json = await body.json();
        // console.log('API response:', json);

        // Proper type conversion using unknown as intermediate type
        const responseData = json as unknown as UserProfileData;

        if (responseData) {
          setProfile(responseData);
          setEditFullName(responseData.full_name || '');
        } else {
          console.error('Received null or undefined profile data from API');
          setError('Profile data is missing or invalid.');
          setProfile(null);
        }
      } catch (err: any) {
        console.error('Error fetching user profile:', err);
        setError(`Failed to fetch user profile: ${err.message || 'Unknown error'}`);
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
    // console.log('Saving profile with full_name:', editFullName); // Example

    let authToken = '';

    try {
      // Get auth token for API call
      const session = await fetchAuthSession();
      if (session.tokens?.idToken) {
        authToken = session.tokens.idToken.toString();
      }
    } catch (err) {
      console.error('Error getting auth token:', err);
    }

    try {
      // Path should be relative to the configured endpoint (e.g., "users/me")
      const path = 'users/me'; // No leading slash
      // console.log('Making API PUT request to path:', path);

      // Call the API using put method from Amplify v6 with manual authorization
      const { body } = await put({
        apiName: 'SummitSEOAmplifyAPI',
        path: path,
        options: {
          headers: {
            Authorization: authToken ? `Bearer ${authToken}` : ''
          },
          body: {
            full_name: editFullName,
          },
        },
      }).response;

      // If needed, parse response
      await body.json(); // Removed assignment to unused 'result'
      // console.log('Update response:', result);

      setProfile({ ...profile, full_name: editFullName });
      setSaveSuccess(true);
    } catch (err: any) {
      console.error('Error saving user profile:', err);
      const errorMessage = err.message || 'Failed to save profile. Please try again.';
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