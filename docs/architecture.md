# Summit SEO Amplify - Architecture Documentation

## Package Management

The project uses modern package management tools to ensure reproducible builds and efficient dependency resolution:

- **Backend (Python)**: Using `uv` as the package manager
  - Faster installation of dependencies compared to pip
  - Deterministic builds with lockfiles
  - Compatible with standard Python packaging
  - Better caching and parallel installations

- **Frontend (Node.js)**: Using npm as the package manager
  - Standard Node.js package management
  - Compatible with Amplify ecosystem

## Technology Stack

### Backend
- **Framework**: FastAPI
- **Runtime**: Python 3.10+
- **Deployment**: AWS Lambda via API Gateway
- **Database**: DynamoDB
- **Authentication**: AWS Cognito
- **AI Services**: AWS Bedrock

### Frontend
- **Framework**: React with Vite
- **Hosting**: AWS Amplify
- **State Management**: React Context + Zustand/Redux

## Architecture Overview

The application follows a serverless architecture pattern with the frontend hosted on AWS Amplify and the backend running on AWS Lambda. Please refer to `architecture.mermaid` for a detailed diagram of the system components and their interactions.

## Development Setup

Please refer to the README.md files in the frontend and backend directories for detailed setup instructions:

- Backend: Python environment setup with uv
- Frontend: Node.js environment setup with npm

## Infrastructure Management

Infrastructure is defined and deployed using a combination of:
- AWS Amplify Console for frontend hosting and CI/CD
- AWS CDK for backend infrastructure as code
- GitHub Actions for automated testing and deployment
