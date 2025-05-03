# **Product Requirements Document: AI Marketing Assistant SaaS (MVP)**

**Version:** 1.1 (Final MVP)
**Date:** {{date}}
**Author:** Damian Herrick

## 1. Introduction

This document outlines the product requirements for the Minimum Viable Product (MVP) of an AI-powered Software-as-a-Service (SaaS) application designed to assist businesses with their marketing activities, primarily focusing on Search Engine Optimization (SEO). The application aims to augment or replace tasks typically handled by junior to early-mid-career marketers. It will gather business information via user input and an optional survey, conduct automated research (website analysis, competitor analysis), generate marketing plans with actionable *suggested* tasks, allow users to manage task execution *manually*, and track progress via a dashboard. The system architecture is envisioned in three distinct planes: Application, Control, and Generative AI. This PRD serves as a guide for the development team.

## 2. Goals

*   **Business Goal:** Launch a viable SaaS product (MVP) with tiered subscription levels (Basic, Premium, Enterprise) to validate the core value proposition, attract early adopters, and gather feedback for future iterations.
*   **Product Goal:** Deliver an intuitive platform that simplifies marketing planning for businesses by leveraging AI, providing actionable insights, clear suggested tasks based on SEO best practices, and basic progress tracking.
*   **User Goal:** Enable businesses to improve their understanding of SEO opportunities, receive AI-generated task recommendations to guide their marketing efforts, track manual task completion, and gain insights at a lower cost than traditional expert services.

## 3. User Personas

*   **Target End-User (Customer):**
    *   *Description:* Small-to-medium business owners, marketing managers in small teams, or solopreneurs. Assumed to be familiar with using SaaS tools (beyond basic office software) but are not looking to write code. They seek powerful marketing assistance abstracted into an easy-to-use interface.
    *   *Primary Pain Points:* Difficulty and time required for effective SEO, high cost of hiring SEO experts/agencies, challenge of keeping up with algorithm changes and competitor actions.
*   **SaaS Administrator (You):**
    *   *Description:* The business owner operating the SaaS platform. Needs oversight of tenants, billing integration points, platform health, tier management, and maintenance of the AI's SEO knowledge base.

## 4. Functional Requirements

### 4.1 Application Plane (End-User Facing)

#### 4.1.1 User Authentication & Authorization
*   **REQ-FE-AUTH-01:** Users must be able to create an account. Required information: Business Name, Business Website URL, User Email Address, Password. Other standard fields (e.g., User Name) may be included.
*   **REQ-FE-AUTH-02:** Registered users must be able to log in and log out securely.
*   **REQ-FE-AUTH-03:** Implement a password reset mechanism.
*   **REQ-FE-AUTH-04:** User session management and authentication will leverage AWS Amplify services (or equivalent secure standard).
*   **REQ-FE-AUTH-05:** Access to features and usage limits (e.g., number of competitors) must be gated based on the user's subscription tier (Basic, Premium, Enterprise).

#### 4.1.2 Onboarding & Data Collection
*   **REQ-FE-ONB-01:** After initial account creation, users should be prompted (but not forced) to complete an initial survey to provide deeper business context to the AI.
*   **REQ-FE-ONB-02:** The initial survey will be presented as a **multi-step wizard** interface for the MVP. (Future iterations may explore conversational AI interfaces).
*   **REQ-FE-ONB-03:** Collect Core Business Details (Minimum required at signup: Name, Website URL):
    *   Business Name
    *   Website URL (Primary)
    *   User Email Addresses (for access)
*   **REQ-FE-ONB-04:** Collect Additional Details (via optional multi-step survey wizard):
    *   Industry/Niche
    *   Target Audience Description
    *   Primary Products/Services Offered
    *   Location Information (if business serves a local area)
    *   Marketing Goals (Allow selection/input of up to 3 key goals for MVP). Prioritization not required for MVP.
    *   Competitor Information (Website URLs).
    *   Current Marketing Activities (e.g., using checkboxes, text fields).
    *   Brand Image/Tone Guidelines
    *   AI Guardrails (e.g., topics to avoid).
*   **REQ-FE-ONB-05:** The number of competitors a user can input is limited by subscription tier:
    *   Basic: Up to 3 competitors.
    *   Premium: Up to 10 competitors.
    *   Enterprise: Unlimited competitors (within technical feasibility).
*   **REQ-FE-ONB-06:** Allow users to review and edit their submitted business information (core details and survey responses) later through a settings/profile area.

#### 4.1.3 AI Research & Analysis (Triggered after Onboarding/User Request)
*   **REQ-FE-AIR-01:** The system must initiate AI analysis based on the collected data (minimum: website URL). This process must provide clear feedback to the user that it's running (e.g., loading indicator, status message: "Analyzing your website...").
*   **REQ-FE-AIR-02:** AI performs analysis of the user's provided website URL.
    *   MVP Scope: Analyze landing page. If a blog exists, analyze the main blog page and individual posts. If product pages exist, analyze the main catalog/shop page and individual product pages. Crawling depth limited to max 2 levels from the initial URL.
    *   Analysis Elements: Basic technical SEO check (titles, descriptions, H1s found), content analysis (keyword identification, topic extraction), site structure overview (identified pages), **basic mobile-friendliness check (best-effort based on viewport/meta tags), detection of broken internal links found during crawl.**
*   **REQ-FE-AIR-03:** AI performs analysis of the provided competitor website URLs (up to tier limit).
    *   MVP Scope: Similar crawling depth (max 2 levels) and content/structure analysis as the user's own site.
    *   Analysis Elements: Identify primary keywords/topics competitors seem to target based on content analysis. *Estimate* competitor search ranking effectiveness for relevant terms *based solely on content analysis*. Identify basic site technology via best-effort page source analysis (e.g., common patterns for WordPress, Shopify). Compare content themes/structures to the user's site. (Integration with external tech analysis services like BuiltWith is out of scope for MVP).
*   **REQ-FE-AIR-04:** AI synthesizes information from user inputs (survey, core details), website analysis, competitor analysis, the provided SEO knowledge base (see REQ-AI-CAP-07), and its general knowledge to understand the business context and goals.

#### 4.1.4 Marketing Plan & Task Generation
*   **REQ-FE-PLN-01:** Based on the analysis, the AI must generate a basic marketing plan focused on achieving the user's stated goals (up to 3). The plan should outline key SEO-driven strategies/focus areas.
*   **REQ-FE-PLN-02:** The plan must be broken down into clear, defined, actionable **suggested** tasks for the user to implement manually. Direct AI task execution is out of scope for MVP.
    *   Examples: "Suggest writing a blog post about [topic]", "Suggest optimizing the title tag for page [URL]", "Suggest researching keywords for [product/service]".
    *   Task details like difficulty, priority, impact, or categorization are *not* required for MVP task generation.
*   **REQ-FE-PLN-03:** The generated plan and tasks must be presented to the user in a clear, understandable format (e.g., a list or board view within the dashboard).

#### 4.1.5 Task Management & Execution Control
*   **REQ-FE-TSK-01:** Display the list of AI-suggested tasks in a dedicated section or dashboard.
*   **REQ-FE-TSK-02:** Each task should be viewable with its full description.
*   **REQ-FE-TSK-03:** For each task, the user must be able to manually manage its status. MVP Statuses:
    *   `To Do` (Default for new suggestions)
    *   `In Progress`
    *   `Done`
    *   `Ignored` (User chooses not to pursue this task)
*   **REQ-FE-TSK-04:** The system must persist the user-defined status of tasks.
*   **REQ-FE-TSK-05:** Users must be able to filter and sort the task list (e.g., by status).
*   **REQ-FE-TSK-06:** Users must be able to edit the details (e.g., description) of AI-suggested tasks. This action should trigger an AI re-evaluation in the background. The UI should notify the user that the AI is considering their edit (e.g., "AI is reviewing your changes...") and update the task/suggestions accordingly once complete.
*   **REQ-FE-TSK-07:** Users must be able to add their own custom tasks to the list. Adding a custom task should also trigger an AI re-evaluation in the background, with similar UI feedback to the user as editing tasks.

#### 4.1.6 Dashboard & Progress Tracking
*   **REQ-FE-DSH-01:** Provide a dashboard summarizing marketing progress based primarily on **manual task completion**. Direct integration with external analytics is out of scope for MVP.
*   **REQ-FE-DSH-02:** The MVP dashboard should visualize key information sourced from internal application data:
    *   Task Completion Rate (percentage of non-ignored tasks marked 'Done').
    *   Number of tasks by status (`To Do`, `In Progress`, `Done`, `Ignored`).
    *   High-level goal status indicator (e.g., AI's qualitative assessment: 'On Track', 'Needs Attention' based on task progress towards goals).
*   **REQ-FE-DSH-03:** Users must be able to trigger an AI re-assessment of their marketing plan/progress via a dedicated button.
    *   Limit: Max once per day per **tenant** account.
    *   Auto-Monitoring: The AI should monitor task progress relative to goals and *suggest* to the user when a re-assessment might be beneficial (e.g., via a notification or dashboard message: "You've completed several tasks, consider requesting an AI plan update.").

#### 4.1.7 User Profile & Settings
*   **REQ-FE-SET-01:** Allow users to view and edit their profile information (Name, Email) and core business details (Business Name, Website).
*   **REQ-FE-SET-02:** Allow users to view and edit the extended business information provided in the survey.
*   **REQ-FE-SET-03:** Allow users to view their current subscription tier. Provide a link to an external billing portal for subscription changes.
*   **REQ-FE-SET-04:** Allow users to manage notification preferences (if applicable, e.g., email summaries, disable specific in-app notifications).
*   **REQ-FE-SET-05:** Provide a mechanism for users to request account deletion. This should trigger an admin workflow or automated process (respecting data retention policies) to deactivate and eventually delete the user's account and associated tenant data.

#### 4.1.8 Notification Center
*   **REQ-FE-NOT-01:** Implement an in-app notification center where users can view system-generated messages (e.g., "AI analysis complete", "AI suggests re-assessment") and global announcements pushed by the admin.
*   **REQ-FE-NOT-02:** Provide an indicator for unread notifications.

### 4.2 Control Plane (SaaS Admin Facing)

#### 4.2.1 Tenant Management
*   **REQ-CP-TEN-01:** Admin must be able to view a list of all tenant (customer) accounts.
*   **REQ-CP-TEN-02:** Admin must be able to view details for each tenant (account info, subscription tier, key usage data, basic audit log trail).
*   **REQ-CP-TEN-03:** Admin must be able to manually activate/deactivate tenant accounts.
*   **REQ-CP-TEN-04:** Admin must be able to manually assign/change the subscription tier for a tenant.
*   **REQ-CP-TEN-05:** The system must support assigning a 'Trial' status to a tenant, potentially with an expiry date or specific trial limitations, manageable by the Admin. (Actual trial logic/limitations defined separately).

#### 4.2.2 Billing & Metering Integration
*   **REQ-CP-BIL-01:** The system must track usage metrics per tenant relevant for billing and operational monitoring. MVP metrics:
    *   AI LLM Tokens Consumed (Input/Output, per tenant)
    *   Cloud Resource Usage estimation (if feasible to attribute, e.g., DB usage, compute time per tenant)
    *   Number of Competitors Tracked (for tier enforcement)
    *   Frequency of AI Analysis/Re-assessments (for monitoring/potential future rate limiting)
*   **REQ-CP-BIL-02:** Provide mechanisms (e.g., API hooks triggered on events, database flags, database streams) to allow integration with a third-party billing system (e.g., Stripe, Chargebee - implementation of the billing system itself is external).
*   **REQ-CP-BIL-03:** Admin dashboard should display key business metrics (e.g., Active tenants per tier, total tenants. MRR/Billing data will likely come from the external billing system).

#### 4.2.3 Platform Monitoring & Management
*   **REQ-CP-MON-01:** Basic dashboard showing overall platform health (API latency, error rates, background job queues).
*   **REQ-CP-MON-02:** Interface for managing system-wide settings and **feature flags** (enabling/disabling specific features globally or per tier).
*   **REQ-CP-MON-03:** Interface or process for the Administrator to manage and update the SEO Knowledge Base used by the AI.
*   **REQ-CP-MON-04:** Interface for viewing key **audit logs** per tenant (e.g., login history, plan generation triggers, major setting changes, account deletion requests). Log data should be searchable/filterable by tenant/user/action type.
*   **REQ-CP-MON-05:** Interface for creating and publishing **global announcements** visible to all users or users on specific tiers via the in-app notification center (`REQ-FE-NOT-01`).

### 4.3 Generative AI Plane

#### 4.3.1 AI Core Capabilities
*   **REQ-AI-CAP-01:** Ability to process structured text inputs describing a business, its goals, competitors, brand guidelines, etc.
*   **REQ-AI-CAP-02:** Ability to perform web crawling/scraping of specified URLs (user's site, competitor sites).
    *   Must respect `robots.txt` directives.
    *   Must have capability to render JavaScript to analyze content on dynamic sites (e.g., using headless browser libraries like Playwright/Puppeteer).
    *   Implement reasonable rate limiting (per domain and globally) and robust error handling for inaccessible sites or timeouts.
*   **REQ-AI-CAP-03:** Ability to analyze text content to identify keywords, topics, and potentially sentiment.
*   **REQ-AI-CAP-04:** Ability to synthesize gathered information to generate a structured marketing plan outline.
*   **REQ-AI-CAP-05:** Ability to break down plan components into specific, actionable **suggested** task descriptions.
*   **REQ-AI-CAP-06:** Ability to provide feedback/suggestions when users edit or add tasks, triggered by the backend.
*   **REQ-AI-CAP-07:** Ability to access and utilize a dedicated knowledge base of SEO best practices provided and maintained by the SaaS owner. This will likely involve Retrieval-Augmented Generation (RAG) techniques using vector embeddings or similar.
*   **REQ-AI-CAP-08:** Underlying LLM technology choice is flexible (e.g., AWS Bedrock models, external APIs like OpenAI/Anthropic via custom integration). Architecture should abstract this interaction.

#### 4.3.2 API & Integration
*   **REQ-AI-API-01:** Expose AI functionalities via secure internal APIs consumable by the Application Plane backend.
*   **REQ-AI-API-02:** APIs should accept structured input (e.g., JSON containing business data, URLs, task context) and return structured output (e.g., JSON with plan details, task suggestions, feedback).
*   **REQ-AI-API-03:** Handle potentially long-running AI tasks (like analysis, plan generation) asynchronously. The Application Plane backend must be able to poll for status or receive callbacks upon completion.

#### 4.3.3 Data Handling & Prompt Engineering
*   **REQ-AI-DAT-01:** Ensure user data passed to the AI is handled securely and privately. User data must *not* be used for training the global AI models, only for generating results for that specific user's tenant. This must be clearly stated in the Privacy Policy and Terms of Service.
*   **REQ-AI-DAT-02:** Develop, test, and refine prompts used to instruct the AI for analysis, plan generation, task suggestion, and feedback to ensure relevant, accurate, safe, and helpful outputs, grounded in the provided SEO knowledge base.

## 5. Non-Functional Requirements

*   **NFR-PERF-01:** The web application interface (Application Plane) must be responsive and load quickly. Target < 3 seconds load time for major page views under expected load.
*   **NFR-PERF-02:** AI analysis and generation tasks should provide feedback on progress. Standard LLM latency (seconds) is expected for interactive elements (e.g., task feedback). Longer processes (initial site/competitor analysis, full plan generation) should complete within a reasonable timeframe (target < 2 minutes, user must be informed if expected to be longer). Asynchronous processing is key.
*   **NFR-SCAL-01:** The architecture must be designed for scalability using appropriate AWS services (e.g., Lambda, Fargate, DynamoDB auto-scaling, Bedrock).
*   **NFR-SCAL-02:** AI processing (LLM calls, crawling workers) must scale independently from the core application logic.
*   **NFR-REL-01:** The platform should aim for high availability (target 99.9% uptime) leveraging AWS infrastructure capabilities.
*   **NFR-SEC-01:** All communication must be encrypted end-to-end (HTTPS/TLS). Data at rest should be encrypted.
*   **NFR-SEC-02:** Implement robust authentication (AWS Amplify) and authorization controls (tier-based access, user roles if applicable later).
*   **NFR-SEC-03:** Protect against common web vulnerabilities (OWASP Top 10) through secure coding practices, input validation, and potentially WAF configuration.
*   **NFR-SEC-04:** Ensure strict tenant data isolation at the database level (DynamoDB partition keys MUST include tenant ID) and throughout the application logic.
*   **NFR-SEC-05:** Implement **audit logging** for security-sensitive events and key user/admin actions (logins, data changes, administrative actions). Logs must be stored securely and retained according to policy.
*   **NFR-USE-01:** The user interface should be intuitive and minimize friction for the target persona (SaaS-familiar, non-technical marketer).
*   **NFR-MAINT-01:** Codebase (React/Vite frontend, chosen backend language - e.g., Python/Node.js) must follow established best practices, be well-commented, include automated tests (unit, integration), and be deployed via CI/CD pipelines.
*   **NFR-COMP-01:** Adhere to relevant data privacy regulations (e.g., GDPR, CCPA). Provide clear Privacy Policy and Terms of Service, including data retention and deletion procedures, and the commitment *not* to use tenant data for global model training.

## 6. Architecture Overview

*   **Application Plane:**
    *   **Frontend:** React (using Vite). Single Page Application (SPA). AWS Amplify for Auth and potentially API integration. State management library (e.g., Zustand, Redux Toolkit). UI component library (e.g., MUI, Chakra UI). Includes Notification component/service.
    *   **Backend:** API layer (e.g., Python/FastAPI or Node.js/Express deployed on AWS Lambda via API Gateway, or containers on Fargate). Handles business logic, DynamoDB interaction, orchestrates asynchronous AI tasks (e.g., via SQS + Lambda/Fargate workers), handles audit logging.
    *   **Data Store:** AWS DynamoDB (NoSQL). Partitioning strategy designed for tenant isolation and common access patterns. Includes tables/structures for Audit Logs and Notifications.
*   **Control Plane:**
    *   **Frontend:** Separate simple admin interface (React/Vite acceptable). Secure authentication for admin users. Includes UI for Announcements, Audit Log viewing, Trial Status management, Feature Flags, KB Management.
    *   **Backend:** Dedicated set of secure API endpoints (e.g., Lambda functions via API Gateway with IAM authorization) for admin operations, interacting with DynamoDB, triggering billing events, managing announcements/flags.
*   **Generative AI Plane:**
    *   **Orchestration:** Backend services manage calls to AI models.
    *   **LLM Interaction:** Interface with AWS Bedrock or direct integration layer for external LLM APIs (e.g., OpenAI).
    *   **Knowledge Base:** RAG implementation (e.g., vector database like Pinecone/OpenSearch/ChromaDB populated and queried as part of the AI workflow).
    *   **Web Crawling:** Asynchronous workers (e.g., Python scripts using Playwright/Puppeteer on Fargate or Lambda with increased memory/timeout). Managed via queues (e.g., SQS).
*   **Data Store:** *(Includes tables/structures for Audit Logs, Notifications, potentially Admin Announcements, Tenant trial status flags)*
## 7. Data Requirements

*   User account data (credentials, profile info, tenant ID)
*   Tenant/Business data (core details, survey responses, tier level, configuration, trial status flags if applicable)
*   Competitor data (URLs provided by user, linked to tenant)
*   Website analysis data (results from crawling user/competitor sites, raw content snippets, extracted metadata, linked to tenant, basic tech checks results)
*   Generated Marketing Plans (structure, associated goals, linked to tenant)
*   Generated & Custom Tasks (description, status, creation date, completion date, linked to plan/goal and tenant)
*   Usage/Metering data (API calls, token counts, analysis jobs run, timestamps, linked to tenant)
*   System logs (application events, errors, admin activity)
*   SEO Knowledge Base content (vector embeddings, source documents/data for RAG).
*   **Audit Log data** (Timestamp, TenantID, UserID (if applicable), Action Type, Details, IP Address (optional))
*   **Notification data** (TenantID/Global, Message Content, Read Status, Timestamp)
*   **Admin Announcement data** (Content, Target Tier(s), Start/End Date, Active Status)

## 8. Out of Scope (for Version 1.0 / MVP)

*   **Direct AI execution of tasks** (AI only *suggests* tasks).
*   Automated link building (suggestion or execution).
*   Social media marketing features.
*   Paid advertising (PPC) features.
*   Deep technical SEO audits requiring specialized tools.
*   **Direct integrations with external analytics** (GA, GSC) for fetching live metrics.
*   A/B testing features.
*   Multi-user collaboration features within a single tenant account.
*   Live search engine rank tracking.
*   Advanced competitor analysis (backlinks, ad spend).
*   Integration with external tech analysis tools (e.g., BuiltWith).
*   Conversational AI interface for onboarding or task management.

## 9. Future Considerations

*   Enabling AI execution of specific tasks (content drafting, meta description generation) with user review/approval workflows.
*   Integrating with Google Analytics/Search Console for richer dashboard metrics and ROI tracking.
*   Expanding AI capabilities (content gap analysis, backlink opportunity suggestions, keyword clustering).
*   Support for multi-channel marketing strategies (Social, Email).
*   Collaboration features for teams (multiple user seats per tenant).
*   Customizable reporting and **data exports** (e.g., tasks to CSV).
*   Allowing more granular goal setting and tracking.
*   Conversational AI interactions.
*   Integration with third-party tools (BuiltWith, SEMrush API, etc.).
*   **Admin Tenant Impersonation** (for support, with strict controls and auditing).