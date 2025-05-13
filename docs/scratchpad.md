============================= test session starts ==============================
platform linux -- Python 3.13.1, pytest-8.3.5, pluggy-1.5.0 -- /home/runner/work/summit-seo-amplify/summit-seo-amplify/backend/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /home/runner/work/summit-seo-amplify/summit-seo-amplify/backend
configfile: pyproject.toml
plugins: mock-3.14.0, asyncio-0.26.0, cov-6.1.1, anyio-4.9.0
asyncio: mode=Mode.STRICT, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 6 items

backend/app/tests/api/endpoints/test_users.py::test_read_users_me_success PASSED [ 16%]
backend/app/tests/api/endpoints/test_users.py::test_read_users_me_not_found FAILED [ 33%]
backend/app/tests/api/endpoints/test_users.py::test_update_users_me_partial_update FAILED [ 50%]
backend/app/tests/api/endpoints/test_users.py::test_update_users_me_noop PASSED [ 66%]
backend/app/tests/api/endpoints/test_users.py::test_update_users_me_not_found FAILED [ 83%]
backend/app/tests/api/endpoints/test_users.py::test_update_users_me_dynamodb_error FAILED [100%]

=================================== FAILURES ===================================
_________________________ test_read_users_me_not_found _________________________

mock_get_user = <AsyncMock name='get_user_by_cognito_id' id='139981928192656'>
override_get_current_user = None

    @patch("backend.app.db.dynamodb.get_user_by_cognito_id", new_callable=AsyncMock)
    def test_read_users_me_not_found(mock_get_user, override_get_current_user):
        mock_get_user.return_value = None
        response = client.get("/api/v1/users/me")
>       assert response.status_code == 404
E       assert 200 == 404
E        +  where 200 = <Response [200 OK]>.status_code

backend/app/tests/api/endpoints/test_users.py:59: AssertionError
_____________________ test_update_users_me_partial_update ______________________

mock_update_user = <AsyncMock name='update_user' id='139981928197024'>
mock_get_user = <AsyncMock name='get_user_by_cognito_id' id='139981928197696'>
override_get_current_user = None

    @patch("backend.app.db.dynamodb.get_user_by_cognito_id", new_callable=AsyncMock)
    @patch("backend.app.db.dynamodb.update_user", new_callable=AsyncMock)
    def test_update_users_me_partial_update(mock_update_user, mock_get_user, override_get_current_user):
        mock_get_user.return_value = MOCK_USER.copy()
        updated = MOCK_USER.copy()
        updated["full_name"] = "Jane Doe"
        mock_update_user.return_value = updated
        response = client.put("/api/v1/users/me", json={"full_name": "Jane Doe"})
        assert response.status_code == 200
        data = response.json()
>       assert data["full_name"] == "Jane Doe"
E       AssertionError: assert 'John Doe' == 'Jane Doe'
E         
E         - Jane Doe
E         ?  ^ -
E         + John Doe
E         ?  ^^

backend/app/tests/api/endpoints/test_users.py:71: AssertionError
________________________ test_update_users_me_not_found ________________________

mock_get_user = <AsyncMock name='get_user_by_cognito_id' id='139981928199040'>
override_get_current_user = None

    @patch("backend.app.db.dynamodb.get_user_by_cognito_id", new_callable=AsyncMock)
    def test_update_users_me_not_found(mock_get_user, override_get_current_user):
        mock_get_user.return_value = None
        response = client.put("/api/v1/users/me", json={"full_name": "Jane Doe"})
>       assert response.status_code == 404
E       assert 200 == 404
E        +  where 200 = <Response [200 OK]>.status_code

backend/app/tests/api/endpoints/test_users.py:88: AssertionError
_____________________ test_update_users_me_dynamodb_error ______________________

mock_update_user = <AsyncMock name='update_user' id='139981928659472'>
mock_get_user = <AsyncMock name='get_user_by_cognito_id' id='139981928658128'>
override_get_current_user = None

    @patch("backend.app.db.dynamodb.get_user_by_cognito_id", new_callable=AsyncMock)
    @patch("backend.app.db.dynamodb.update_user", new_callable=AsyncMock)
    def test_update_users_me_dynamodb_error(mock_update_user, mock_get_user, override_get_current_user):
        mock_get_user.return_value = MOCK_USER.copy()
        mock_update_user.side_effect = Exception("DynamoDB error")
        response = client.put("/api/v1/users/me", json={"full_name": "Jane Doe"})
>       assert response.status_code == 500 or response.status_code == 422
E       assert (200 == 500 or 200 == 422)
E        +  where 200 = <Response [200 OK]>.status_code
E        +  and   200 = <Response [200 OK]>.status_code

backend/app/tests/api/endpoints/test_users.py:96: AssertionError
=============================== warnings summary ===============================
backend/.venv/lib/python3.13/site-packages/pydantic/_internal/_config.py:323
  /home/runner/work/summit-seo-amplify/summit-seo-amplify/backend/.venv/lib/python3.13/site-packages/pydantic/_internal/_config.py:323: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.11/migration/
    warnings.warn(DEPRECATION_MESSAGE, DeprecationWarning)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
FAILED backend/app/tests/api/endpoints/test_users.py::test_read_users_me_not_found - assert 200 == 404
 +  where 200 = <Response [200 OK]>.status_code
FAILED backend/app/tests/api/endpoints/test_users.py::test_update_users_me_partial_update - AssertionError: assert 'John Doe' == 'Jane Doe'
  
  - Jane Doe
  ?  ^ -
  + John Doe
  ?  ^^
FAILED backend/app/tests/api/endpoints/test_users.py::test_update_users_me_not_found - assert 200 == 404
 +  where 200 = <Response [200 OK]>.status_code
FAILED backend/app/tests/api/endpoints/test_users.py::test_update_users_me_dynamodb_error - assert (200 == 500 or 200 == 422)
 +  where 200 = <Response [200 OK]>.status_code
 +  and   200 = <Response [200 OK]>.status_code
==================== 4 failed, 2 passed, 1 warning in 1.71s ====================