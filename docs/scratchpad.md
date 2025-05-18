UserProfile.tsx:36 Current user session: {tokens: {…}, credentials: {…}, identityId: 'us-east-1:c043747a-63e3-ce89-c390-bccc6d51cbde', userSub: 'f468e498-f051-705f-e684-d15444d72ae5'}
UserProfile.tsx:42 ID Token available: true
UserProfile.tsx:43 Access Token available: true
UserProfile.tsx:48 ID Token prefix: eyJraWQiOiJqN0Y0bURH...
UserProfile.tsx:36 Current user session: {tokens: {…}, credentials: {…}, identityId: 'us-east-1:c043747a-63e3-ce89-c390-bccc6d51cbde', userSub: 'f468e498-f051-705f-e684-d15444d72ae5'}
UserProfile.tsx:42 ID Token available: true
UserProfile.tsx:43 Access Token available: true
UserProfile.tsx:48 ID Token prefix: eyJraWQiOiJqN0Y0bURH...
UserProfile.tsx:53 Current authenticated user: {username: 'f468e498-f051-705f-e684-d15444d72ae5', userId: 'f468e498-f051-705f-e684-d15444d72ae5', signInDetails: {…}}
UserProfile.tsx:62 Making API GET request to path: users/me
UserProfile.tsx:53 Current authenticated user: {username: 'f468e498-f051-705f-e684-d15444d72ae5', userId: 'f468e498-f051-705f-e684-d15444d72ae5', signInDetails: {…}}
UserProfile.tsx:62 Making API GET request to path: users/me
UserProfile.tsx:65 
            
            
           GET https://qi9k0zm7z8.execute-api.us-east-1.amazonaws.com/api/v1/users/me 401 (Unauthorized)
fetchTransferHandler @ chunk-U65UG6PV.js?v=0915441c:6318
composedHandler @ chunk-U65UG6PV.js?v=0915441c:6292
retryMiddleware @ chunk-U65UG6PV.js?v=0915441c:6018
userAgentMiddleware @ chunk-U65UG6PV.js?v=0915441c:6278
(anonymous) @ chunk-U65UG6PV.js?v=0915441c:6298
transferHandler @ aws-amplify_api.js?v=0915441c:7430
await in transferHandler
(anonymous) @ aws-amplify_api.js?v=0915441c:7478
await in (anonymous)
job @ aws-amplify_api.js?v=0915441c:7271
createCancellableOperation @ aws-amplify_api.js?v=0915441c:7304
publicHandler @ aws-amplify_api.js?v=0915441c:7460
get3 @ aws-amplify_api.js?v=0915441c:7486
get4 @ aws-amplify_api.js?v=0915441c:7494
fetchProfile @ UserProfile.tsx:65
await in fetchProfile
(anonymous) @ UserProfile.tsx:97
commitHookEffectListMount @ chunk-NXESFFTV.js?v=0915441c:16963
invokePassiveEffectMountInDEV @ chunk-NXESFFTV.js?v=0915441c:18374
invokeEffectsInDev @ chunk-NXESFFTV.js?v=0915441c:19754
commitDoubleInvokeEffectsInDEV @ chunk-NXESFFTV.js?v=0915441c:19739
flushPassiveEffectsImpl @ chunk-NXESFFTV.js?v=0915441c:19556
flushPassiveEffects @ chunk-NXESFFTV.js?v=0915441c:19500
commitRootImpl @ chunk-NXESFFTV.js?v=0915441c:19469
commitRoot @ chunk-NXESFFTV.js?v=0915441c:19330
performSyncWorkOnRoot @ chunk-NXESFFTV.js?v=0915441c:18948
flushSyncCallbacks @ chunk-NXESFFTV.js?v=0915441c:9166
(anonymous) @ chunk-NXESFFTV.js?v=0915441c:18677
UserProfile.tsx:90 Error fetching user profile: UnknownError: Unknown error
    at buildRestApiError (aws-amplify_api.js?v=0915441c:7250:24)
    at parseRestApiServiceError (aws-amplify_api.js?v=0915441c:7204:12)
    at async job (aws-amplify_api.js?v=0915441c:7273:15)
    at async fetchProfile (UserProfile.tsx:65:26)
fetchProfile @ UserProfile.tsx:90
await in fetchProfile
(anonymous) @ UserProfile.tsx:97
commitHookEffectListMount @ chunk-NXESFFTV.js?v=0915441c:16963
invokePassiveEffectMountInDEV @ chunk-NXESFFTV.js?v=0915441c:18374
invokeEffectsInDev @ chunk-NXESFFTV.js?v=0915441c:19754
commitDoubleInvokeEffectsInDEV @ chunk-NXESFFTV.js?v=0915441c:19739
flushPassiveEffectsImpl @ chunk-NXESFFTV.js?v=0915441c:19556
flushPassiveEffects @ chunk-NXESFFTV.js?v=0915441c:19500
commitRootImpl @ chunk-NXESFFTV.js?v=0915441c:19469
commitRoot @ chunk-NXESFFTV.js?v=0915441c:19330
performSyncWorkOnRoot @ chunk-NXESFFTV.js?v=0915441c:18948
flushSyncCallbacks @ chunk-NXESFFTV.js?v=0915441c:9166
(anonymous) @ chunk-NXESFFTV.js?v=0915441c:18677
UserProfile.tsx:65 
            
            
           GET https://qi9k0zm7z8.execute-api.us-east-1.amazonaws.com/api/v1/users/me 401 (Unauthorized)
fetchTransferHandler @ chunk-U65UG6PV.js?v=0915441c:6318
composedHandler @ chunk-U65UG6PV.js?v=0915441c:6292
retryMiddleware @ chunk-U65UG6PV.js?v=0915441c:6018
userAgentMiddleware @ chunk-U65UG6PV.js?v=0915441c:6278
(anonymous) @ chunk-U65UG6PV.js?v=0915441c:6298
transferHandler @ aws-amplify_api.js?v=0915441c:7430
await in transferHandler
(anonymous) @ aws-amplify_api.js?v=0915441c:7478
await in (anonymous)
job @ aws-amplify_api.js?v=0915441c:7271
createCancellableOperation @ aws-amplify_api.js?v=0915441c:7304
publicHandler @ aws-amplify_api.js?v=0915441c:7460
get3 @ aws-amplify_api.js?v=0915441c:7486
get4 @ aws-amplify_api.js?v=0915441c:7494
fetchProfile @ UserProfile.tsx:65
await in fetchProfile
(anonymous) @ UserProfile.tsx:97
commitHookEffectListMount @ chunk-NXESFFTV.js?v=0915441c:16963
commitPassiveMountOnFiber @ chunk-NXESFFTV.js?v=0915441c:18206
commitPassiveMountEffects_complete @ chunk-NXESFFTV.js?v=0915441c:18179
commitPassiveMountEffects_begin @ chunk-NXESFFTV.js?v=0915441c:18169
commitPassiveMountEffects @ chunk-NXESFFTV.js?v=0915441c:18159
flushPassiveEffectsImpl @ chunk-NXESFFTV.js?v=0915441c:19543
flushPassiveEffects @ chunk-NXESFFTV.js?v=0915441c:19500
commitRootImpl @ chunk-NXESFFTV.js?v=0915441c:19469
commitRoot @ chunk-NXESFFTV.js?v=0915441c:19330
performSyncWorkOnRoot @ chunk-NXESFFTV.js?v=0915441c:18948
flushSyncCallbacks @ chunk-NXESFFTV.js?v=0915441c:9166
(anonymous) @ chunk-NXESFFTV.js?v=0915441c:18677
UserProfile.tsx:90 Error fetching user profile: UnknownError: Unknown error
    at buildRestApiError (aws-amplify_api.js?v=0915441c:7250:24)
    at parseRestApiServiceError (aws-amplify_api.js?v=0915441c:7204:12)
    at async job (aws-amplify_api.js?v=0915441c:7273:15)
    at async fetchProfile (UserProfile.tsx:65:26)
fetchProfile @ UserProfile.tsx:90
await in fetchProfile
(anonymous) @ UserProfile.tsx:97
commitHookEffectListMount @ chunk-NXESFFTV.js?v=0915441c:16963
commitPassiveMountOnFiber @ chunk-NXESFFTV.js?v=0915441c:18206
commitPassiveMountEffects_complete @ chunk-NXESFFTV.js?v=0915441c:18179
commitPassiveMountEffects_begin @ chunk-NXESFFTV.js?v=0915441c:18169
commitPassiveMountEffects @ chunk-NXESFFTV.js?v=0915441c:18159
flushPassiveEffectsImpl @ chunk-NXESFFTV.js?v=0915441c:19543
flushPassiveEffects @ chunk-NXESFFTV.js?v=0915441c:19500
commitRootImpl @ chunk-NXESFFTV.js?v=0915441c:19469
commitRoot @ chunk-NXESFFTV.js?v=0915441c:19330
performSyncWorkOnRoot @ chunk-NXESFFTV.js?v=0915441c:18948
flushSyncCallbacks @ chunk-NXESFFTV.js?v=0915441c:9166
(anonymous) @ chunk-NXESFFTV.js?v=0915441c:18677
injected.js:5 Caught error handling <hide-notification> message
(anonymous) @ injected.js:5
Promise.catch
r @ injected.js:5


/users/me headers:
:authority
qi9k0zm7z8.execute-api.us-east-1.amazonaws.com
:method
GET
:path
/api/v1/users/me
:scheme
https
accept
*/*
accept-encoding
gzip, deflate, br, zstd
accept-language
en-US,en;q=0.9
authorization
Bearer eyJraWQiOiJqN0Y0bURHcmRPd3l5aUFhenZ1NkM5Q1BEcGl5S2dvQzZjUVI0ZEZKODhzPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJmNDY4ZTQ5OC1mMDUxLTcwNWYtZTY4NC1kMTU0NDRkNzJhZTUiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfYW1Xb0tNa2NGIiwiY29nbml0bzp1c2VybmFtZSI6ImY0NjhlNDk4LWYwNTEtNzA1Zi1lNjg0LWQxNTQ0NGQ3MmFlNSIsIm9yaWdpbl9qdGkiOiIwZmI3YjlhMy1lMjZhLTQxOTctYTRhYy00YTUzYmVhZjlhOWYiLCJhdWQiOiI0czBwZXEyY3Y3dnV1dnEwMGZya3J0MTNoYiIsImV2ZW50X2lkIjoiNWQ3ZmE0NjEtZTQ0Mi00YjY3LWEzZDMtODJmOTE3MjAxNDUyIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3NDc1OTYxOTksImV4cCI6MTc0NzU5OTc5OSwiaWF0IjoxNzQ3NTk2MTk5LCJqdGkiOiI0OGNhYmQyOC1iZTE4LTRmZWMtYmNiNy1mMjIxZjRmMGYwMjMiLCJlbWFpbCI6ImRhbWlhbi5oZXJyaWNrQGdtYWlsLmNvbSJ9.ItqMuZh1mJk2nCO_zq-geSQTQtoYs-IfPAkOBbYB_ak-PKOV5JHm5WcRuy7ebdIbH0G_fJCoF-YRSM6NOVPxGaUKPetwKqbOzwKRZF3sLA_rV3SXRE43i4gpsY2u6RhtU_i8qhFANH_S_uo4RscNyb74-SY_sdz0W_39WEHILnIMiOCY-h-Co6irenGp3Y0NKgB7Mo-4zvFJfVBrNgL1UhfBgpi7zFqpOv53dX4Sr4Pt0JAfoWnLpnld01UuDsmkOtOzqpsh2Cb0y8xp6cC_0uPGX5oasF0PYIM1zTRo0Llc83qK4I59jQObohD1t0YU0Q-0sRQVYBAOHf5aJ4GENw
dnt
1
origin
http://127.0.0.1:5173
priority
u=1, i
referer
http://127.0.0.1:5173/
sec-ch-ua
"Not.A/Brand";v="99", "Chromium";v="136"
sec-ch-ua-mobile
?0
sec-ch-ua-platform
"Windows"
sec-fetch-dest
empty
sec-fetch-mode
cors
sec-fetch-site
cross-site
user-agent
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36