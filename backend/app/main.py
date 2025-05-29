from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from botocore.exceptions import ClientError, BotoCoreError

from .core.config import settings
from .api.router import api_router

app = FastAPI(
    title="Summit SEO Amplify API",
    description="API for Summit SEO Amplify SaaS platform",
    version="0.1.0"
)

# CORS Middleware Configuration
# Adjust origins as needed for your deployed frontend
origins = [
    "http://localhost:5173", # Local Vite dev server
    # Add your deployed frontend URL here if known, e.g., "https://your-amplify-app.amplifyapp.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Exception Handlers ---
@app.exception_handler(ClientError)
async def botocore_clienterror_exception_handler(request: Request, exc: ClientError):
    # Log the error for debugging if needed
    # logger.error(f"Boto3 ClientError: {exc}")
    return JSONResponse(
        status_code=500, # Or be more specific based on exc.response['Error']['Code']
        content={"detail": f"An AWS Client error occurred: {exc.response.get('Error', {}).get('Message', 'Unknown error')}"},
    )

@app.exception_handler(BotoCoreError)
async def botocore_coreerror_exception_handler(request: Request, exc: BotoCoreError):
    # logger.error(f"Boto3 BotoCoreError: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": f"An AWS Core error occurred: {str(exc)}"},
    )
# --- End Exception Handlers ---

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to Summit SEO Amplify API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Handler for AWS Lambda
handler = Mangum(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)