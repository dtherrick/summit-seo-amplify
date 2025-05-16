import os
import sys
# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import random
from typing import List
import json
from sqlalchemy import inspect
from app.core.database import engine

# API base URL
BASE_URL = "http://localhost:8000/api/v1/surveys"

def generate_brand_name() -> str:
    prefixes = ["Tech", "Eco", "Smart", "Global", "Next", "Future", "Digital", "Innovative", "Modern", "Peak"]
    suffixes = ["Solutions", "Systems", "Technologies", "Innovations", "Platform", "Hub", "Network", "Labs", "Group", "Pro"]
    return f"{random.choice(prefixes)}{random.choice(suffixes)}"

def generate_url(brand_name: str) -> str:
    domain_extensions = [".com", ".io", ".tech", ".ai", ".co"]
    sanitized_name = brand_name.lower().replace(" ", "")
    return f"https://www.{sanitized_name}{random.choice(domain_extensions)}"

def generate_categories() -> List[str]:
    all_categories = [
        "Fashion", "Technology", "Health & Wellness", "Food & Beverage",
        "Travel", "Home & Garden", "Education", "Finance", "Entertainment", "Automotive"
    ]
    return random.sample(all_categories, random.randint(1, 3))

def generate_keywords(brand_name: str, categories: List[str]) -> dict:
    base_keywords = [
        "best", "top", "innovative", "leading", "professional",
        "expert", "trusted", "premium", "quality", "advanced"
    ]
    
    return {
        "informational_intent": f"how to choose {' '.join(categories)}, understanding {random.choice(categories).lower()}",
        "commercial_intent": f"{random.choice(base_keywords)} {random.choice(categories).lower()} solutions",
        "transactional_intent": f"buy {brand_name} products, {brand_name} pricing",
        "brand_intent": f"{brand_name}, {brand_name} reviews, {brand_name} products"
    }

def generate_survey_data():
    brand_name = generate_brand_name()
    categories = generate_categories()
    
    return {
        "customer_id": f"CUST_{random.randint(1000, 9999)}",
        "response_data": {
            "general_information": {
                "brand_name": brand_name,
                "brand_description": f"Leading provider of {' and '.join(categories).lower()} solutions",
                "url": generate_url(brand_name),
                "categories": categories
            },
            "audience": {
                "who_is_your_audience": f"Professionals and businesses in the {' and '.join(categories).lower()} sectors",
                "needs_and_preferences": "Looking for innovative, reliable, and cost-effective solutions"
            },
            "seo": {
                "seed_keywords": f"{brand_name.lower()}, {', '.join(categories).lower()}",
                "pillar_keywords": generate_keywords(brand_name, categories)
            },
            "competitors": {
                "key_competitors": f"Major{random.choice(categories)}, Premium{random.choice(categories)}",
                "secondary_competitors": f"Alternative{random.choice(categories)}, Budget{random.choice(categories)}"
            },
            "guardrails": "No specific pricing details, no competitor comparisons, no unverified claims",
            "content_pillars": f"Innovation, Quality, Customer Success, {', '.join(categories)}"
        }
    }

def create_survey_response(data):
    response = requests.post(BASE_URL, json=data)
    if response.status_code == 200:
        print(f"Successfully created survey for customer {data['customer_id']}")
        return response.json()
    else:
        print(f"Error creating survey: {response.status_code}")
        print(response.text)
        return None

def get_survey_response(customer_id):
    response = requests.get(f"{BASE_URL}/{customer_id}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error retrieving survey: {response.status_code}")
        return None

def check_survey_table_exists():
    """
    Check if the survey_responses table exists in the database
    """
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    if "survey_responses" in tables:
        print("✓ survey_responses table exists")
        # Optionally print table structure
        columns = inspector.get_columns("survey_responses")
        print("\nTable structure:")
        for column in columns:
            print(f"- {column['name']}: {column['type']}")
        return True
    else:
        print("✗ survey_responses table does not exist!")
        print("\nMake sure you have run your database migrations or created the table.")
        print("The table should be created automatically when you run the FastAPI application.")
        return False

def main():
    # Check if table exists before proceeding
    if not check_survey_table_exists():
        print("Exiting: Please create the database table first.")
        return
        
    # Generate and send 5 sample surveys
    created_surveys = []
    for _ in range(5):
        survey_data = generate_survey_data()
        result = create_survey_response(survey_data)
        if result:
            created_surveys.append(result)
    
    print("\nCreated Surveys:")
    print("---------------")
    for survey in created_surveys:
        print(f"Customer ID: {survey['customer_id']}")
        print(f"Brand: {survey['response_data']['general_information']['brand_name']}")
        print(f"Categories: {', '.join(survey['response_data']['general_information']['categories'])}")
        print("---------------")
    
    # Verify we can retrieve the data
    if created_surveys:
        first_survey = created_surveys[0]
        retrieved_survey = get_survey_response(first_survey['customer_id'])
        if retrieved_survey:
            print("\nVerifying data retrieval:")
            print(f"Retrieved survey for {retrieved_survey['customer_id']}")
            print(json.dumps(retrieved_survey, indent=2))

if __name__ == "__main__":
    main() 