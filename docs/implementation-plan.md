Okay, here is a detailed Implementation Plan for the AI Marketing Assistant SaaS MVP, based on the provided `product-requirements.md` and `tech-stack.md`. This plan assumes an iterative approach, building foundational elements first.

**Legend:**

*   `(FE)`: Frontend (React/Vite, Amplify UI/MUI/Chakra)
*   `(BE)`: Backend (Python/FastAPI, Lambda, API Gateway)
*   `(DB)`: Database (DynamoDB, OpenSearch)
*   `(Infra)`: Infrastructure (AWS CDK, Cognito, SQS, Step Functions, Fargate, Bedrock, CloudWatch, etc.)
*   `(AI)`: AI-specific components (Crawling workers, RAG, Prompting Logic)
*   `(Admin)`: Control Plane / Admin Features

---

## **Implementation Plan: AI Marketing Assistant SaaS (MVP)**

**Goal:** Implement the MVP features defined in `product-requirements.md` using the specified `tech-stack.md`.

**Process Notes:**

*   Follow Test-Driven Development (TDD) principles where applicable, especially for backend logic. Write tests *before* or *alongside* implementation.
*   Each step includes validation criteria. Ensure these are met before proceeding.
*   Commit changes frequently with descriptive messages.
*   Update `docs/progress.md` after completing significant steps or encountering blockers.
*   Continuously validate against `docs/architecture.mermaid` and `docs/tech-stack.md`.

---

### **Phase 0: Project Setup & Foundation**

1.  **Initialize Project Repositories:**
    *   Instruction: Create separate Git repositories (or a monorepo structure) for Frontend and Backend code.
    *   Validation: Repositories exist and are accessible. Basic README files are present.
2.  **Setup AWS Environment & CDK:**
    *   Instruction: Set up AWS account(s). Configure AWS CLI/SDK access. Initialize AWS CDK project (TypeScript/Python). Define basic environment configurations (dev, staging, prod - though MVP focuses on deploying to one initially).
    *   Validation: CDK project bootstraps successfully. Can deploy a simple placeholder resource (e.g., an S3 bucket) via CDK.
3.  **Configure Cognito User Pool:**
    *   Instruction: Define and deploy Cognito User Pool using CDK (`REQ-FE-AUTH-04`). Configure required attributes (`REQ-FE-AUTH-01`: Email, Business Name, Website URL; add standard `name`, `sub`), password policies (`REQ-FE-AUTH-03`), and MFA settings (optional for MVP, but consider structure). Define user groups (`Admin`, `BasicTier`, `PremiumTier`, `Trial`).
    *   Validation: Cognito User Pool exists in AWS. Can manually create/confirm a test user via the AWS console. Groups are defined.
4.  **Initialize Frontend Project:**
    *   Instruction: Initialize React project using Vite (`NFR-MAINT-01`). Install core dependencies (React Router, state management library - e.g., Zustand, UI library - e.g., MUI, AWS Amplify JS libraries). Set up basic project structure (components, pages, services).
    *   Validation: `npm run dev` starts the dev server. A basic placeholder page renders in the browser. Amplify libraries are installed.
5.  **Initialize Backend Project:**
    *   Instruction: Initialize Python/FastAPI project. Set up basic project structure (routers, models, services, tests). Install core dependencies (FastAPI, Pydantic, Boto3, AWS Lambda Powertools - recommended for logging/tracing/metrics). Configure basic testing setup (e.g., `pytest`).
    *   Validation: Basic FastAPI app runs locally. A simple health check endpoint (`/health`) returns `{"status": "ok"}`. `pytest` runs successfully (even with no tests initially).
6.  **Setup API Gateway & Basic Lambda Integration:**
    *   Instruction: Define an API Gateway (HTTP API recommended for simplicity) using CDK (`BE`). Create a basic Lambda function (e.g., the health check endpoint) using CDK and deploy the FastAPI app to it. Configure API Gateway to route requests to the Lambda function.
    *   Validation: Calling the deployed API Gateway health check endpoint URL returns `{"status": "ok"}`.
7.  **Setup DynamoDB Core Tables:**
    *   Instruction: Define DynamoDB table schemas using CDK (`DB`, `NFR-SEC-04`) for:
        *   `Users`: PK=`TenantID`, SK=`UserID` (Store profile info, tier, etc.)
        *   `Tenants`: PK=`TenantID` (Store business info, survey data, competitor URLs, config)
    *   Validation: Tables are created in AWS via CDK deployment. Table definitions enforce TenantID as part of the key schema for isolation.
8.  **Setup CI/CD Pipelines (Basic):**
    *   Instruction: Configure basic CI/CD pipelines using AWS CodePipeline/CodeBuild (or GitHub Actions) (`Infra`, `NFR-MAINT-01`).
        *   Frontend: Trigger on push to `main`, build, and deploy to Amplify Hosting.
        *   Backend: Trigger on push to `main`, run linters/tests, package, and deploy Lambda/API Gateway via CDK.
    *   Validation: Pushing changes to the main branch automatically triggers builds and deployments for both frontend and backend.

---

### **Phase 1: Core Authentication & Onboarding**

9.  **Implement Frontend Sign-Up:**
    *   Instruction: Create the Sign-Up page/component (`FE`). Use Amplify UI components or chosen UI library (`REQ-FE-AUTH-01`). Integrate with Amplify Auth library to call Cognito `signUp`. Handle confirmation codes if enabled.
    *   Validation: User can enter required details (Business Name, Website, Email, Password) and click "Sign Up". A confirmation email is sent (if configured). A new user appears in Cognito (potentially in an unconfirmed state).
10. **Implement Frontend Sign-In/Sign-Out:**
    *   Instruction: Create the Sign-In page/component (`FE`). Use Amplify Auth library to call `signIn`. Implement session management (tokens stored securely). Implement a Sign-Out button calling `signOut` (`REQ-FE-AUTH-02`). Implement basic routing protection (redirect to sign-in if not authenticated).
    *   Validation: User can log in with confirmed credentials. App state reflects authenticated status. Sign-out clears session and redirects. Protected routes are inaccessible without login.
11. **Implement Password Reset:**
    *   Instruction: Create frontend components for initiating password reset (request code) and confirming reset (enter code and new password) (`FE`, `REQ-FE-AUTH-03`). Integrate with Amplify Auth library methods.
    *   Validation: User can successfully request and complete a password reset flow via email.
12. **Implement Backend User Profile Creation:**
    *   Instruction: Create a mechanism (e.g., Cognito Post-Confirmation Lambda Trigger) (`BE`, `DB`) to:
        *   Create a `Tenant` record in DynamoDB upon first user confirmation for that business (derive `TenantID`, maybe from a unique aspect of the first user or generate UUID). Associate Business Name/Website from signup. Assign default 'Trial' or 'Basic' tier.
        *   Create a `User` record in DynamoDB linked to the `TenantID` and Cognito `sub` (UserID). Store email.
    *   Validation: After a new user signs up and confirms, corresponding `Tenant` and `User` records are created in DynamoDB with correct initial data and linkage.
13. **Implement Frontend Initial Survey Wizard (UI):**
    *   Instruction: Create the multi-step wizard UI (`FE`, `REQ-FE-ONB-01`, `REQ-FE-ONB-02`). Include form fields for all details specified in `REQ-FE-ONB-04` (Industry, Audience, Products, Location, Goals, Competitors, Marketing Activities, Brand Tone, Guardrails). Implement client-side validation.
    *   Validation: The wizard UI renders correctly, allows navigation between steps, and captures input. Basic form validation works.
14. **Implement Backend API for Saving Survey Data:**
    *   Instruction: Create a secure FastAPI endpoint (`BE`) that accepts the survey data (`REQ-FE-ONB-04`). Validate input. Update the corresponding `Tenant` record in DynamoDB (`DB`). Ensure endpoint is protected and only allows the tenant owner to update their data. Apply tier limits for competitors (`REQ-FE-ONB-05`).
    *   Validation: Submitting the survey from the frontend successfully calls the API. The `Tenant` record in DynamoDB is updated with the survey responses. API correctly rejects requests exceeding competitor limits based on the tenant's tier (initially test with default tier).
15. **Implement Frontend Survey Submission:**
    *   Instruction: Connect the survey wizard UI (`FE`) to the backend API. Handle API call states (loading, success, error). Provide feedback to the user upon completion. Allow skipping (`REQ-FE-ONB-01`).
    *   Validation: User can complete or skip the survey. Data is saved correctly via the API call upon completion.

---

### **Phase 2: AI Analysis & Plan Generation**

16. **Setup SQS Queues:**
    *   Instruction: Define SQS queues using CDK (`Infra`) for triggering asynchronous tasks: e.g., `WebsiteAnalysisQueue`, `CompetitorAnalysisQueue`, `PlanGenerationQueue`. Configure Dead Letter Queues (DLQs).
    *   Validation: Queues and DLQs are created in AWS via CDK deployment.
17. **Setup Fargate Cluster & Task Definition (for Crawling):**
    *   Instruction: Define an ECS Cluster and Fargate Task Definition using CDK (`Infra`, `REQ-AI-CAP-02`). Include necessary permissions (e.g., network access). Package the Python web scraping script (using Playwright/Puppeteer) into a Docker container. Store the image in ECR.
    *   Validation: Fargate cluster exists. Task Definition is registered. Docker image builds successfully and is pushed to ECR. Can manually run a Fargate task using the definition.
18. **Implement Web Crawler Worker:**
    *   Instruction: Develop the Python script (`AI`, `REQ-AI-CAP-02`) to:
        *   Accept a URL and TenantID as input.
        *   Use Playwright/Puppeteer to crawl the website (respect `robots.txt`, limit depth, handle JS).
        *   Extract specified elements (`REQ-FE-AIR-02`: titles, descriptions, H1s, content, links, basic tech checks).
        *   Implement rate limiting and error handling.
        *   Store results temporarily (e.g., S3 or directly pass to next step if small enough).
    *   Validation: Unit tests for parsing logic. Integration test: Running the script against a test website successfully extracts the required data and handles basic errors (404s, timeouts). The script runs successfully as a Fargate task.
19. **Implement Analysis Trigger Endpoint:**
    *   Instruction: Create a secure FastAPI endpoint (`BE`, `REQ-FE-AIR-01`) that users can trigger (e.g., after onboarding or from dashboard). The endpoint should place messages onto `WebsiteAnalysisQueue` and `CompetitorAnalysisQueue` (for each competitor up to tier limit) containing necessary context (URL, TenantID). Provide immediate feedback to the user that analysis has started.
    *   Validation: Calling the endpoint results in messages being correctly placed onto the SQS queues. The frontend receives confirmation that the process started.
20. **Implement Analysis Orchestration (Step Functions - Optional but Recommended):**
    *   Instruction: Define an AWS Step Functions state machine (`Infra`, `REQ-AI-API-03`) triggered by SQS messages. Orchestrate the flow:
        *   Trigger Fargate crawler task for user site.
        *   Trigger Fargate crawler task(s) for competitor site(s).
        *   Wait for completion.
        *   Gather results.
        *   Trigger Plan Generation Lambda.
    *   *Alternative (Simpler MVP):* Use Lambda functions triggered directly by SQS queues, managing state within DynamoDB if needed.
    *   Validation: A message on `WebsiteAnalysisQueue` successfully triggers the Step Function (or Lambda chain). Fargate tasks are invoked. Logs show the intended flow.
21. **Setup Vector Store (OpenSearch Serverless):**
    *   Instruction: Provision an OpenSearch Serverless collection with vector engine enabled using CDK (`DB`, `REQ-AI-CAP-07`). Configure access policies.
    *   Validation: OpenSearch collection is accessible. Can manually index and query a sample vector document.
22. **Implement SEO Knowledge Base Loading:**
    *   Instruction: Develop a script/process (`Admin`, `AI`) to load and vectorize the initial SEO knowledge base content (provided by SaaS owner) into the OpenSearch vector store (`REQ-AI-CAP-07`).
    *   Validation: SEO documents are processed, vectorized, and indexed in OpenSearch. Can perform a similarity search via OpenSearch API and retrieve relevant document chunks.
23. **Implement Bedrock Integration Layer:**
    *   Instruction: Create Python service/functions (`BE`, `AI`) to interact with Amazon Bedrock (`REQ-AI-CAP-08`, `REQ-AI-API-01`). Abstract model calling logic. Include functions for sending prompts and receiving structured responses.
    *   Validation: Unit tests mock Bedrock calls. Integration test: Can successfully call a Bedrock model (e.g., Claude) with a simple prompt and receive a response via the integration layer.
24. **Implement Plan Generation Logic:**
    *   Instruction: Create a Lambda function (`BE`, `AI`) triggered by the orchestration step (or SQS queue). This function will:
        *   Retrieve user/tenant data (goals, survey info) and analysis results (user site, competitors).
        *   Query the OpenSearch vector store for relevant SEO best practices (RAG) (`REQ-AI-CAP-07`).
        *   Construct a detailed prompt for the Bedrock LLM (`REQ-AI-DAT-02`), including context, analysis results, RAG context, and goals.
        *   Call Bedrock to generate the marketing plan outline and suggested tasks (`REQ-FE-PLN-01`, `REQ-FE-PLN-02`).
        *   Parse the structured response from the LLM.
        *   Save the generated plan and tasks to DynamoDB (`DB`), linked to the `TenantID`.
    *   Validation: Invoking the Lambda (manually or via Step Functions/SQS) with sample analysis data results in a structured plan and tasks being stored in DynamoDB. Prompt engineering yields relevant, actionable SEO suggestions based on sample inputs.
25. **Implement Frontend Plan/Task Display:**
    *   Instruction: Create a new page/section in the frontend (`FE`) to display the generated marketing plan outline and the list of suggested tasks (`REQ-FE-PLN-03`, `REQ-FE-TSK-01`, `REQ-FE-TSK-02`). Fetch this data from a new backend API endpoint.
    *   Validation: Plan and tasks fetched from the backend are displayed clearly to the user.

---

### **Phase 3: Task Management & Dashboard**

26. **Implement Backend API for Task Data:**
    *   Instruction: Create secure FastAPI endpoints (`BE`) to:
        *   Fetch tasks for the logged-in tenant.
        *   Update task status (`REQ-FE-TSK-03`, `REQ-FE-TSK-04`).
        *   Edit task details (`REQ-FE-TSK-06`).
        *   Add custom tasks (`REQ-FE-TSK-07`).
    *   Validation: API endpoints function correctly with test client (e.g., Postman) and enforce tenant isolation. Correct data is retrieved/updated in DynamoDB.
27. **Implement Frontend Task Management UI:**
    *   Instruction: Enhance the task list UI (`FE`) to allow:
        *   Changing status via dropdown/buttons (`REQ-FE-TSK-03`).
        *   Filtering/Sorting tasks (`REQ-FE-TSK-05`).
        *   Opening a modal/view to edit task details (`REQ-FE-TSK-06`).
        *   Adding new custom tasks via a form (`REQ-FE-TSK-07`).
    *   Validation: User can interact with tasks as specified. Changes are reflected in the UI and persisted via backend API calls.
28. **Implement AI Feedback on Task Edits/Additions:**
    *   Instruction: Modify the backend update/add task endpoints (`BE`, `AI`) to trigger a background AI re-evaluation (e.g., lightweight Bedrock call or rule-based check) when tasks are edited or added (`REQ-FE-TSK-06`, `REQ-FE-TSK-07`). This might involve placing a message on a new `TaskFeedbackQueue` processed by a Lambda. Update the task or suggest related modifications asynchronously.
    *   Validation: Editing/adding a task triggers the background process. (Simulate AI feedback initially, e.g., adding a comment or slightly modifying the task description after a delay).
29. **Implement Frontend Feedback for Task AI Processing:**
    *   Instruction: Update the frontend (`FE`) to show an indicator when AI is processing changes to a task (`REQ-FE-TSK-06`, `REQ-FE-TSK-07`). Use polling or WebSockets (if implemented) to update the UI once processing is complete.
    *   Validation: User sees a visual cue ("AI is reviewing...") after editing/adding a task. UI updates appropriately once the (simulated) background process completes.
30. **Implement Backend Dashboard Data API:**
    *   Instruction: Create a secure FastAPI endpoint (`BE`) to calculate and return dashboard metrics based on task data in DynamoDB (`REQ-FE-DSH-02`): Task Completion Rate, Task Counts by Status. Add logic for the qualitative goal assessment (can be simple rules based on task completion initially).
    *   Validation: API endpoint returns correctly calculated metrics based on sample task data in DynamoDB for the tenant.
31. **Implement Frontend Dashboard UI:**
    *   Instruction: Create the Dashboard page (`FE`). Display the metrics fetched from the backend API using charts or summary statistics (`REQ-FE-DSH-01`, `REQ-FE-DSH-02`).
    *   Validation: Dashboard page renders and displays the correct data fetched from the API.
32. **Implement Re-assessment Trigger:**
    *   Instruction: Add a button on the Dashboard (`FE`) to trigger the re-assessment (`REQ-FE-DSH-03`). Connect this to the existing analysis trigger endpoint (`BE`) or a dedicated one. Implement the once-per-day limit logic in the backend.
    *   Validation: Clicking the button triggers the analysis/plan generation flow. The backend correctly enforces the rate limit.
33. **Implement Re-assessment Suggestion:**
    *   Instruction: Add logic (can be frontend or backend) to check task progress (`BE`/`FE`) and display a suggestion message/notification to the user to trigger re-assessment (`REQ-FE-DSH-03`).
    *   Validation: When a certain number/percentage of tasks are marked 'Done', the suggestion appears in the UI.

---

### **Phase 4: Settings, Notifications & Control Plane Basics**

34. **Implement Backend Profile/Settings API:**
    *   Instruction: Create secure FastAPI endpoints (`BE`) to:
        *   Fetch user profile and tenant business/survey data (`REQ-FE-SET-01`, `REQ-FE-SET-02`).
        *   Update editable user profile (Name) and tenant business details (Name, Website, Survey data).
        *   Fetch current subscription tier (`REQ-FE-SET-03`).
        *   (Placeholder for notification preferences `REQ-FE-SET-04`).
        *   Initiate account deletion request (`REQ-FE-SET-05`) - flags tenant/user for deletion.
    *   Validation: API endpoints allow fetching and updating the specified data in DynamoDB, respecting tenant isolation. Deletion request flags the records correctly.
35. **Implement Frontend Settings Page:**
    *   Instruction: Create the Settings page (`FE`) with forms to view/edit profile, business details, and survey data (`REQ-FE-SET-01`, `REQ-FE-SET-02`). Display current tier and link to placeholder billing portal (`REQ-FE-SET-03`). Add account deletion request button.
    *   Validation: User can view and successfully update their information via the Settings page. Tier is displayed. Deletion request works.
36. **Implement Basic Notification System (DB & API):**
    *   Instruction: Add DynamoDB table (`Notifications`: PK=`TenantID` or `Global`, SK=`NotificationID`) (`DB`). Create backend endpoints (`BE`) to:
        *   Fetch notifications for the current user/tenant.
        *   Mark notifications as read.
        *   (Internal endpoint/method) Create tenant-specific notifications (e.g., "Analysis complete").
    *   Validation: Notifications can be created and fetched via API. Read status can be updated.
37. **Implement Frontend Notification Center:**
    *   Instruction: Add a notification icon/panel to the main UI (`FE`, `REQ-FE-NOT-01`). Fetch and display unread/recent notifications. Show unread count indicator (`REQ-FE-NOT-02`). Allow marking as read.
    *   Validation: Notifications generated by backend processes (e.g., analysis completion - need to add this trigger) appear in the UI. Read status updates correctly.
38. **Implement Basic Audit Logging:**
    *   Instruction: Create DynamoDB table (`AuditLogs`: PK=`TenantID`, SK=`Timestamp#LogID`) (`DB`, `NFR-SEC-05`). Implement a utility/decorator in the backend (`BE`) to automatically log key actions (login, plan generation, settings changes, task updates, deletion requests) to this table, including TenantID, UserID (if applicable), ActionType, Timestamp, basic details (`REQ-CP-MON-04`).
    *   Validation: Performing key actions in the application results in corresponding log entries being created in the `AuditLogs` table with correct details.
39. **Implement Control Plane Foundation (Admin Role & Basic View):**
    *   Instruction: In the frontend (`FE`, `Admin`), implement logic to check if the logged-in user belongs to the 'Admin' Cognito group. If so, display an 'Admin' section in the navigation. Create a basic Admin dashboard page.
    *   Validation: Users in the 'Admin' group see the Admin section; other users do not.
40. **Implement Tenant List View (Admin):**
    *   Instruction: Create a secure Admin-only API endpoint (`BE`, `Admin`) to list all `Tenant` records from DynamoDB. Display this list in the Admin dashboard (`FE`, `Admin`, `REQ-CP-TEN-01`). Include basic info like Business Name, Email (of first user), Tier, Status (Active/Inactive/Trial).
    *   Validation: Admin user can view the list of tenants fetched from the backend.
41. **Implement Tenant Detail View & Status/Tier Change (Admin):**
    *   Instruction: Create Admin API endpoints (`BE`, `Admin`) to fetch detailed tenant info (`REQ-CP-TEN-02`) and update tenant status (Activate/Deactivate - `REQ-CP-TEN-03`) and tier (`REQ-CP-TEN-04`, `REQ-CP-TEN-05`). Implement corresponding UI elements in the Admin section (`FE`, `Admin`). Ensure Audit Logging for these admin actions.
    *   Validation: Admin can view tenant details. Admin can change a tenant's status and tier, and the changes are reflected in the Tenant record and audit logs. Tier changes correctly gate features (re-test competitor limits).

---

### **Phase 5: Control Plane Advanced & Monitoring**

42. **Implement Usage Metering Data Collection:**
    *   Instruction: Instrument backend code (`BE`, `AI`) to record relevant usage metrics (`REQ-CP-BIL-01`):
        *   LLM Token Counts: Capture from Bedrock responses. Store aggregated counts (e.g., daily per tenant) in DynamoDB or CloudWatch Metrics.
        *   Analysis Frequency: Log analysis triggers.
        *   Competitor Count: Already stored (verify accessible for reporting).
        *   Store this data linked to `TenantID`.
    *   Validation: Performing actions like analysis/plan generation results in measurable metrics being recorded/updated (check logs, DynamoDB, or CloudWatch Metrics).
43. **Implement Billing Integration Hooks (Placeholder):**
    *   Instruction: Add placeholders in the backend (`BE`, `REQ-CP-BIL-02`) where billing events would be triggered (e.g., after tier change, on usage thresholds). This could be logging an event, putting a message on a dedicated SQS queue, or setting a flag in DynamoDB.
    *   Validation: Performing actions like an admin changing a tier triggers the defined placeholder hook (e.g., logs a specific message).
44. **Implement Admin Dashboard Metrics Display:**
    *   Instruction: Enhance the Admin dashboard (`FE`, `Admin`) to display basic business metrics (`REQ-CP-BIL-03`) by querying aggregated data (e.g., active tenants per tier - count from Tenant table). (Note: MRR/Billing data comes from external system).
    *   Validation: Admin dashboard shows correct counts of tenants by tier/status.
45. **Implement Platform Health Monitoring Dashboard (Basic):**
    *   Instruction: Set up a basic CloudWatch Dashboard (`Infra`, `REQ-CP-MON-01`) showing key metrics: API Gateway latency/errors, Lambda invocation counts/errors, SQS queue depth, Fargate CPU/Memory utilization (if available).
    *   Validation: CloudWatch dashboard displays relevant metrics from deployed services.
46. **Implement Feature Flag Mechanism:**
    *   Instruction: Design a simple feature flag system (`BE`, `Admin`). Could use a DynamoDB table (`FeatureFlags`) or AWS AppConfig. Implement backend logic to check flags. Create Admin UI (`FE`, `Admin`) to toggle flags (`REQ-CP-MON-02`). Integrate flag checks around 1-2 minor features initially.
    *   Validation: Admin can toggle a feature flag. The corresponding feature behaves differently in the user application based on the flag's state.
47. **Implement SEO KB Management Interface (Placeholder/Basic):**
    *   Instruction: Create a basic Admin UI (`FE`, `Admin`, `REQ-CP-MON-03`) allowing upload of new KB documents (e.g., text files to an S3 bucket). Set up a Lambda trigger on S3 upload to process and update the OpenSearch vector index (`AI`).
    *   Validation: Admin can upload a document. The document content is processed and becomes searchable in the vector store (verify via test query).
48. **Implement Admin Audit Log Viewer:**
    *   Instruction: Create Admin API endpoint (`BE`, `Admin`) to query the `AuditLogs` table (`REQ-CP-MON-04`), allowing filtering by TenantID, UserID, ActionType, Timestamp range. Implement UI (`FE`, `Admin`) to display logs and provide filtering options.
    *   Validation: Admin can view and filter audit logs generated by user and admin actions.
49. **Implement Global Announcement System:**
    *   Instruction: Add DynamoDB table (`Announcements`) (`DB`). Create Admin API endpoints (`BE`, `Admin`) to create/edit/publish announcements with target tiers (`REQ-CP-MON-05`). Create Admin UI (`FE`, `Admin`) for management. Modify the frontend notification fetching logic (`FE`) to include active global/tier-specific announcements (`REQ-FE-NOT-01`).
    *   Validation: Admin can create an announcement targeted at specific tiers. Users in those tiers see the announcement in their notification center.

---

### **Phase 6: Finalization & Deployment Prep**

50. **Security Hardening & Review:**
    *   Instruction: Review all code and infrastructure configurations (`Infra`, `BE`, `FE`) against OWASP Top 10 (`NFR-SEC-03`). Ensure proper input validation, output encoding, secure headers, IAM least privilege, DynamoDB access patterns strictly enforce tenant isolation (`NFR-SEC-04`). Review Cognito settings. Configure AWS WAF if deemed necessary.
    *   Validation: Conduct manual code review focused on security. Run automated security scanning tools if available. Verify tenant data isolation through testing (try to access another tenant's data via API manipulation).
51. **Performance Testing & Optimization:**
    *   Instruction: Test frontend load times (`NFR-PERF-01`). Analyze backend API response times under simulated load (`NFR-PERF-02`). Optimize slow database queries, Lambda cold starts (provisioned concurrency if needed), frontend bundle size (code splitting). Check AI task completion times.
    *   Validation: Load times and response times meet targets defined in NFRs. Key workflows complete within acceptable timeframes.
52. **Usability Review:**
    *   Instruction: Perform internal usability testing (`NFR-USE-01`). Click through all user flows, checking for clarity, consistency, and ease of use for the target persona. Refine UI/UX based on feedback.
    *   Validation: Key user flows are intuitive and meet the requirements of the target persona.
53. **Final Documentation Review:**
    *   Instruction: Ensure READMEs are up-to-date. Add necessary user documentation placeholders. Review all code comments and JSDoc (`NFR-MAINT-01`). Ensure Privacy Policy/Terms of Service are drafted (content is external, but ensure link points are ready) (`NFR-COMP-01`).
    *   Validation: Documentation is clear, accurate, and complete for MVP.
54. **Prepare Production Deployment:**
    *   Instruction: Finalize production environment configuration in CDK (`Infra`). Set up necessary monitoring/alarms in CloudWatch (`NFR-REL-01`). Perform a full deployment to a staging environment mirroring production. Conduct final end-to-end testing.
    *   Validation: Staging deployment succeeds. All critical user flows work correctly in the staging environment. Key alarms are configured.

---

This plan provides a detailed roadmap. Steps may need adjustment based on discoveries during development. Remember to prioritize the core value proposition for the MVP.