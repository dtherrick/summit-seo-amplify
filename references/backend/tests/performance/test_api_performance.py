"""Performance tests for API endpoints.

This module contains performance tests for API endpoints,
measuring response times, concurrent request handling,
and resource utilization.
"""

import pytest
import asyncio
import time
from typing import List
from httpx import AsyncClient
import psutil
import statistics

from tests.factories import BusinessFactory, UserFactory, SurveyResponseFactory

pytestmark = [pytest.mark.asyncio, pytest.mark.performance]

async def measure_response_time(
    client: AsyncClient,
    method: str,
    url: str,
    **kwargs
) -> float:
    """Measure response time for a single request."""
    start_time = time.perf_counter()
    response = await client.request(method, url, **kwargs)
    end_time = time.perf_counter()
    
    assert response.status_code < 500  # Ensure no server errors
    return end_time - start_time

async def measure_concurrent_requests(
    client: AsyncClient,
    method: str,
    url: str,
    num_requests: int,
    **kwargs
) -> List[float]:
    """Measure response times for concurrent requests."""
    tasks = [
        measure_response_time(client, method, url, **kwargs)
        for _ in range(num_requests)
    ]
    return await asyncio.gather(*tasks)

def get_process_metrics():
    """Get current process CPU and memory usage."""
    process = psutil.Process()
    return {
        'cpu_percent': process.cpu_percent(),
        'memory_percent': process.memory_percent()
    }

@pytest.mark.timeout(30)
async def test_login_performance(
    client: AsyncClient,
    test_user: dict
):
    """Test login endpoint performance."""
    url = "/api/v1/auth/jwt/login"
    login_data = {
        "username": test_user["email"],
        "password": "testpass123"
    }
    
    # Test single request performance
    response_time = await measure_response_time(
        client, "POST", url,
        data=login_data
    )
    assert response_time < 0.5  # Should respond within 500ms
    
    # Test concurrent login requests
    response_times = await measure_concurrent_requests(
        client, "POST", url,
        num_requests=10,
        data=login_data
    )
    
    avg_time = statistics.mean(response_times)
    max_time = max(response_times)
    assert avg_time < 1.0  # Average should be under 1 second
    assert max_time < 2.0  # Max should be under 2 seconds

@pytest.mark.timeout(30)
async def test_list_businesses_performance(
    client: AsyncClient,
    superuser_token: str,
    db_session
):
    """Test business listing performance with large dataset."""
    # Create test businesses
    for _ in range(100):
        await BusinessFactory(session=db_session)
    await db_session.commit()
    
    url = "/api/v1/businesses"
    headers = {"Authorization": f"Bearer {superuser_token}"}
    
    # Test pagination performance
    for page in range(5):
        start_time = time.perf_counter()
        response = await client.get(
            url,
            headers=headers,
            params={"skip": page * 20, "limit": 20}
        )
        end_time = time.perf_counter()
        
        assert response.status_code == 200
        response_time = end_time - start_time
        assert response_time < 0.5  # Each page should load within 500ms

@pytest.mark.timeout(30)
async def test_survey_submission_performance(
    client: AsyncClient,
    user_token: str,
    test_business: dict,
    db_session
):
    """Test survey submission performance under load."""
    url = "/api/v1/surveys"
    headers = {"Authorization": f"Bearer {user_token}"}
    
    # Prepare test data
    survey_data = {
        "customer_id": "123e4567-e89b-12d3-a456-426614174000",
        "business_id": test_business["id"],
        "responses": {
            "satisfaction": 5,
            "recommendation_likelihood": 9,
            "feedback": "Performance test feedback",
            "areas_for_improvement": ["None"]
        }
    }
    
    # Test concurrent survey submissions
    start_metrics = get_process_metrics()
    
    response_times = await measure_concurrent_requests(
        client, "POST", url,
        num_requests=20,
        headers=headers,
        json=survey_data
    )
    
    end_metrics = get_process_metrics()
    
    # Analyze results
    avg_time = statistics.mean(response_times)
    percentile_95 = statistics.quantiles(response_times, n=20)[18]  # 95th percentile
    
    assert avg_time < 1.0  # Average under 1 second
    assert percentile_95 < 2.0  # 95% under 2 seconds
    
    # Check resource usage
    cpu_increase = end_metrics['cpu_percent'] - start_metrics['cpu_percent']
    memory_increase = end_metrics['memory_percent'] - start_metrics['memory_percent']
    
    assert cpu_increase < 50  # CPU usage increase should be reasonable
    assert memory_increase < 10  # Memory usage increase should be minimal

@pytest.mark.timeout(60)
async def test_api_load_test(
    client: AsyncClient,
    superuser_token: str,
    db_session
):
    """Test API performance under sustained load."""
    headers = {"Authorization": f"Bearer {superuser_token}"}
    
    # Create test data
    businesses = [
        await BusinessFactory(session=db_session)
        for _ in range(10)
    ]
    users = [
        await UserFactory(session=db_session, business=businesses[i % 10])
        for i in range(50)
    ]
    await db_session.commit()
    
    # Test endpoints under load
    endpoints = [
        ("GET", "/api/v1/businesses"),
        ("GET", "/api/v1/surveys"),
        ("GET", "/api/v1/auth/users/me")
    ]
    
    all_response_times = []
    start_metrics = get_process_metrics()
    
    # Run load test for 30 seconds
    end_time = time.time() + 30
    while time.time() < end_time:
        for method, url in endpoints:
            response_time = await measure_response_time(
                client, method, url,
                headers=headers
            )
            all_response_times.append(response_time)
        await asyncio.sleep(0.1)  # Small delay between request batches
    
    end_metrics = get_process_metrics()
    
    # Analyze results
    avg_time = statistics.mean(all_response_times)
    percentile_95 = statistics.quantiles(all_response_times, n=20)[18]
    max_time = max(all_response_times)
    
    # Performance assertions
    assert avg_time < 0.5  # Average response time under 500ms
    assert percentile_95 < 1.0  # 95th percentile under 1 second
    assert max_time < 2.0  # Maximum response time under 2 seconds
    
    # Resource usage assertions
    cpu_increase = end_metrics['cpu_percent'] - start_metrics['cpu_percent']
    memory_increase = end_metrics['memory_percent'] - start_metrics['memory_percent']
    
    assert cpu_increase < 70  # CPU usage increase should be reasonable
    assert memory_increase < 20  # Memory usage increase should be minimal 