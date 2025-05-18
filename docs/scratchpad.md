❯ curl -X GET \
  'https://qi9k0zm7z8.execute-api.us-east-1.amazonaws.com/api/v1/users/me' \
  -H 'Authorization: Bearer eyJraWQiOiJqN0Y0bURHcmRPd3l5aUFhenZ1NkM5Q1BEcGl5S2dvQzZjUVI0ZEZKODhzPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJmNDY4ZTQ5OC1mMDUxLTcwNWYtZTY4NC1kMTU0NDRkNzJhZTUiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfYW1Xb0tNa2NGIiwiY29nbml0bzp1c2VybmFtZSI6ImY0NjhlNDk4LWYwNTEtNzA1Zi1lNjg0LWQxNTQ0NGQ3MmFlNSIsIm9yaWdpbl9qdGkiOiIyNzE2ZjZkNi03OGJjLTQ5Y2MtYTVmZi1kZDZiYzc4YjNjODciLCJhdWQiOiI0czBwZXEyY3Y3dnV1dnEwMGZya3J0MTNoYiIsImV2ZW50X2lkIjoiNzFiYTcyYmItMjk4Mi00YWQ5LWE4ZmUtNTZmNmNmNTA3YmNiIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3NDc1OTk1NTgsImV4cCI6MTc0NzYwMzE1OCwiaWF0IjoxNzQ3NTk5NTU4LCJqdGkiOiIwYTRhNDM5ZC0xNTkxLTQxZDAtYmVlMy00MWM1OWUzZWQ0OWQiLCJlbWFpbCI6ImRhbWlhbi5oZXJyaWNrQGdtYWlsLmNvbSJ9.kX8CBwsv8RmAnKibzjZtkbIEPzhnBfZ9Z6mIXVQOps8lA5Rv0RnCRZIBtPrcpmPvm1yg9uIXlUaCyruz0fjxrirmgjJ0sEBjVUJPNmCUcclzbUzn5nqpkJl74P8EfqPOqvTC2vi8OpXIE-_EVUvlorcFFMMcbaJVv2XnTCnFhU1p3LFthMbCGzQZrxxuOm2z9HcaxyudODr3n62VbxK-mO263e0aRu6Aml2voSFWgn3Zw9GUiLksfujzmvqYUqAFqSXkrDyi4WJEhOWUktL6pwGCN3PgfDp3C4Fl6RFnpNgYFYsziJH5wHO0uQXFBfBc2PWUKAaIE5JvQcFZ5_EbCQ' \
  -H 'Accept: */*' \
  -H 'Origin: http://127.0.0.1:5173' \
  -v
Note: Unnecessary use of -X or --request, GET is already inferred.
* Host qi9k0zm7z8.execute-api.us-east-1.amazonaws.com:443 was resolved.
* IPv6: (none)
* IPv4: 34.196.116.239, 35.153.45.167
*   Trying 34.196.116.239:443...
* Connected to qi9k0zm7z8.execute-api.us-east-1.amazonaws.com (34.196.116.239) port 443
* ALPN: curl offers h2,http/1.1
* TLSv1.3 (OUT), TLS handshake, Client hello (1):
*  CAfile: /etc/ssl/certs/ca-certificates.crt
*  CApath: /etc/ssl/certs
* TLSv1.3 (IN), TLS handshake, Server hello (2):
* TLSv1.3 (IN), TLS handshake, Encrypted Extensions (8):
* TLSv1.3 (IN), TLS handshake, Certificate (11):
* TLSv1.3 (IN), TLS handshake, CERT verify (15):
* TLSv1.3 (IN), TLS handshake, Finished (20):
* TLSv1.3 (OUT), TLS change cipher, Change cipher spec (1):
* TLSv1.3 (OUT), TLS handshake, Finished (20):
* SSL connection using TLSv1.3 / TLS_AES_128_GCM_SHA256 / X25519 / RSASSA-PSS
* ALPN: server accepted h2
* Server certificate:
*  subject: CN=*.execute-api.us-east-1.amazonaws.com
*  start date: Jun 23 00:00:00 2024 GMT
*  expire date: Jul 21 23:59:59 2025 GMT
*  subjectAltName: host "qi9k0zm7z8.execute-api.us-east-1.amazonaws.com" matched cert's "*.execute-api.us-east-1.amazonaws.com"
*  issuer: C=US; O=Amazon; CN=Amazon RSA 2048 M02
*  SSL certificate verify ok.
*   Certificate level 0: Public key type RSA (2048/112 Bits/secBits), signed using sha256WithRSAEncryption
*   Certificate level 1: Public key type RSA (2048/112 Bits/secBits), signed using sha256WithRSAEncryption
*   Certificate level 2: Public key type RSA (2048/112 Bits/secBits), signed using sha256WithRSAEncryption
* using HTTP/2
* [HTTP/2] [1] OPENED stream for https://qi9k0zm7z8.execute-api.us-east-1.amazonaws.com/api/v1/users/me
* [HTTP/2] [1] [:method: GET]
* [HTTP/2] [1] [:scheme: https]
* [HTTP/2] [1] [:authority: qi9k0zm7z8.execute-api.us-east-1.amazonaws.com]
* [HTTP/2] [1] [:path: /api/v1/users/me]
* [HTTP/2] [1] [user-agent: curl/8.5.0]
* [HTTP/2] [1] [authorization: Bearer eyJraWQiOiJqN0Y0bURHcmRPd3l5aUFhenZ1NkM5Q1BEcGl5S2dvQzZjUVI0ZEZKODhzPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJmNDY4ZTQ5OC1mMDUxLTcwNWYtZTY4NC1kMTU0NDRkNzJhZTUiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfYW1Xb0tNa2NGIiwiY29nbml0bzp1c2VybmFtZSI6ImY0NjhlNDk4LWYwNTEtNzA1Zi1lNjg0LWQxNTQ0NGQ3MmFlNSIsIm9yaWdpbl9qdGkiOiIyNzE2ZjZkNi03OGJjLTQ5Y2MtYTVmZi1kZDZiYzc4YjNjODciLCJhdWQiOiI0czBwZXEyY3Y3dnV1dnEwMGZya3J0MTNoYiIsImV2ZW50X2lkIjoiNzFiYTcyYmItMjk4Mi00YWQ5LWE4ZmUtNTZmNmNmNTA3YmNiIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3NDc1OTk1NTgsImV4cCI6MTc0NzYwMzE1OCwiaWF0IjoxNzQ3NTk5NTU4LCJqdGkiOiIwYTRhNDM5ZC0xNTkxLTQxZDAtYmVlMy00MWM1OWUzZWQ0OWQiLCJlbWFpbCI6ImRhbWlhbi5oZXJyaWNrQGdtYWlsLmNvbSJ9.kX8CBwsv8RmAnKibzjZtkbIEPzhnBfZ9Z6mIXVQOps8lA5Rv0RnCRZIBtPrcpmPvm1yg9uIXlUaCyruz0fjxrirmgjJ0sEBjVUJPNmCUcclzbUzn5nqpkJl74P8EfqPOqvTC2vi8OpXIE-_EVUvlorcFFMMcbaJVv2XnTCnFhU1p3LFthMbCGzQZrxxuOm2z9HcaxyudODr3n62VbxK-mO263e0aRu6Aml2voSFWgn3Zw9GUiLksfujzmvqYUqAFqSXkrDyi4WJEhOWUktL6pwGCN3PgfDp3C4Fl6RFnpNgYFYsziJH5wHO0uQXFBfBc2PWUKAaIE5JvQcFZ5_EbCQ]
* [HTTP/2] [1] [accept: */*]
* [HTTP/2] [1] [origin: http://127.0.0.1:5173]
> GET /api/v1/users/me HTTP/2
> Host: qi9k0zm7z8.execute-api.us-east-1.amazonaws.com
> User-Agent: curl/8.5.0
> Authorization: Bearer eyJraWQiOiJqN0Y0bURHcmRPd3l5aUFhenZ1NkM5Q1BEcGl5S2dvQzZjUVI0ZEZKODhzPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJmNDY4ZTQ5OC1mMDUxLTcwNWYtZTY4NC1kMTU0NDRkNzJhZTUiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfYW1Xb0tNa2NGIiwiY29nbml0bzp1c2VybmFtZSI6ImY0NjhlNDk4LWYwNTEtNzA1Zi1lNjg0LWQxNTQ0NGQ3MmFlNSIsIm9yaWdpbl9qdGkiOiIyNzE2ZjZkNi03OGJjLTQ5Y2MtYTVmZi1kZDZiYzc4YjNjODciLCJhdWQiOiI0czBwZXEyY3Y3dnV1dnEwMGZya3J0MTNoYiIsImV2ZW50X2lkIjoiNzFiYTcyYmItMjk4Mi00YWQ5LWE4ZmUtNTZmNmNmNTA3YmNiIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3NDc1OTk1NTgsImV4cCI6MTc0NzYwMzE1OCwiaWF0IjoxNzQ3NTk5NTU4LCJqdGkiOiIwYTRhNDM5ZC0xNTkxLTQxZDAtYmVlMy00MWM1OWUzZWQ0OWQiLCJlbWFpbCI6ImRhbWlhbi5oZXJyaWNrQGdtYWlsLmNvbSJ9.kX8CBwsv8RmAnKibzjZtkbIEPzhnBfZ9Z6mIXVQOps8lA5Rv0RnCRZIBtPrcpmPvm1yg9uIXlUaCyruz0fjxrirmgjJ0sEBjVUJPNmCUcclzbUzn5nqpkJl74P8EfqPOqvTC2vi8OpXIE-_EVUvlorcFFMMcbaJVv2XnTCnFhU1p3LFthMbCGzQZrxxuOm2z9HcaxyudODr3n62VbxK-mO263e0aRu6Aml2voSFWgn3Zw9GUiLksfujzmvqYUqAFqSXkrDyi4WJEhOWUktL6pwGCN3PgfDp3C4Fl6RFnpNgYFYsziJH5wHO0uQXFBfBc2PWUKAaIE5JvQcFZ5_EbCQ
> Accept: */*
> Origin: http://127.0.0.1:5173
>
* TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
< HTTP/2 401
< date: Sun, 18 May 2025 21:08:50 GMT
< content-type: application/json
< content-length: 47
< www-authenticate: Bearer
< access-control-allow-origin: http://127.0.0.1:5173
< vary: origin
< access-control-allow-credentials: true
< apigw-requestid: KyDfdgZ9oAMEYpA=
<
* Connection #0 to host qi9k0zm7z8.execute-api.us-east-1.amazonaws.com left intact
{"detail":"Invalid authentication credentials"}

Decoded JWT:

```json
Token header
------------
{
  "alg": "RS256",
  "kid": "j7F4mDGrdOwyyiAazvu6C9CPDpiyKgoC6cQR4dFJ88s="
}

Token claims
------------
{
  "aud": "4s0peq2cv7vuuvq00frkrt13hb",
  "auth_time": 1747599558,
  "cognito:username": "f468e498-f051-705f-e684-d15444d72ae5",
  "email": "damian.herrick@gmail.com",
  "email_verified": true,
  "event_id": "71ba72bb-2982-4ad9-a8fe-56f6cf507bcb",
  "exp": 1747603158,
  "iat": 1747599558,
  "iss": "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_amWoKMkcF",
  "jti": "0a4a439d-1591-41d0-bee3-41c59e3ed49d",
  "origin_jti": "2716f6d6-78bc-49cc-a5ff-dd6bc78b3c87",
  "sub": "f468e498-f051-705f-e684-d15444d72ae5",
  "token_use": "id"
}
```

JSON log from the API Gateway: 
```json
{
    "accountId": "825765427811",
    "apiId": "qi9k0zm7z8",
    "authorizer_claims_property": "-",
    "authorizer_error": "-",
    "authorizer_property": "-",
    "awsEndpointRequestId": "88d54618-b7bc-445e-9bd2-d2eb1e8a2045",
    "awsEndpointRequestId2": "-",
    "customDomain_basePathMatched": "-",
    "domainName": "qi9k0zm7z8.execute-api.us-east-1.amazonaws.com",
    "domainPrefix": "qi9k0zm7z8",
    "error_message": "-",
    "error_messageString": "-",
    "error_responseType": "-",
    "extendedRequestId": "KyDfdgZ9oAMEYpA=",
    "httpMethod": "GET",
    "identity_accountId": "-",
    "identity_caller": "-",
    "identity_cognitoAuthenticationProvider": "-",
    "identity_cognitoAuthenticationType": "-",
    "identity_cognitoIdentityId": "-",
    "identity_cognitoIdentityPoolId": "-",
    "identity_principalOrgId": "-",
    "identity_clientCert_clientCertPem": "-",
    "identity_clientCert_subjectDN": "-",
    "identity_clientCert_issuerDN": "-",
    "identity_clientCert_serialNumber": "-",
    "identity_clientCert_validity_notBefore": "-",
    "identity_clientCert_validity_notAfter": "-",
    "identity_sourceIp": "71.142.4.44",
    "identity_user": "-",
    "identity_userAgent": "curl/8.5.0",
    "identity_userArn": "-",
    "integration_error": "-",
    "integration_integrationStatus": "200",
    "integration_latency": "39",
    "integration_requestId": "88d54618-b7bc-445e-9bd2-d2eb1e8a2045",
    "integration_status": "401",
    "integrationErrorMessage": "-",
    "integrationLatency": "39",
    "integrationStatus_alternate": "200",
    "path": "/api/v1/users/me",
    "protocol": "HTTP/1.1",
    "requestId": "KyDfdgZ9oAMEYpA=",
    "requestTime": "18/May/2025:21:08:50 +0000",
    "requestTimeEpoch": "1747602530",
    "responseLatency": "71",
    "responseLength": "47",
    "routeKey": "GET /api/v1/users/me",
    "stage": "$default",
    "status": "401"
}