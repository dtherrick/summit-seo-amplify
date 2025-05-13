/home/runner/work/summit-seo-amplify/summit-seo-amplify/backend/.venv/lib/python3.13/site-packages/pytest_asyncio/plugin.py:217: PytestDeprecationWarning: The configuration option "asyncio_default_fixture_loop_scope" is unset.
The event loop scope for asynchronous fixtures will default to the fixture caching scope. Future versions of pytest-asyncio will default the loop scope for asynchronous fixtures to function scope. Set the default fixture loop scope explicitly in order to avoid unexpected behavior in the future. Valid fixture loop scopes are: "function", "class", "module", "package", "session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET))
============================= test session starts ==============================
platform linux -- Python 3.13.1, pytest-8.3.5, pluggy-1.5.0 -- /home/runner/work/summit-seo-amplify/summit-seo-amplify/backend/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /home/runner/work/summit-seo-amplify/summit-seo-amplify/backend
configfile: pyproject.toml
plugins: mock-3.14.0, asyncio-0.26.0, cov-6.1.1, anyio-4.9.0
asyncio: mode=Mode.STRICT, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 6 items

backend/app/tests/api/endpoints/test_users.py::test_read_users_me_success PASSED [ 16%]
backend/app/tests/api/endpoints/test_users.py::test_read_users_me_not_found PASSED [ 33%]
backend/app/tests/api/endpoints/test_users.py::test_update_users_me_partial_update PASSED [ 50%]
backend/app/tests/api/endpoints/test_users.py::test_update_users_me_noop PASSED [ 66%]
backend/app/tests/api/endpoints/test_users.py::test_update_users_me_not_found PASSED [ 83%]
backend/app/tests/api/endpoints/test_users.py::test_update_users_me_dynamodb_error FAILED [100%]

=================================== FAILURES ===================================
_____________________ test_update_users_me_dynamodb_error ______________________

patch_users_table = <MagicMock name='users_table' id='140674271789808'>
override_get_current_user = None

    def test_update_users_me_dynamodb_error(patch_users_table, override_get_current_user):
        patch_users_table.query.return_value = {"Items": [MOCK_USER.copy()]}
        mock_error_response = {'Error': {'Code': 'InternalServerError', 'Message': 'DynamoDB broke'}}
        patch_users_table.update_item.side_effect = ClientError(mock_error_response, 'UpdateItem')
>       response = client.put("/api/v1/users/me", json={"full_name": "Jane Doe"})

backend/app/tests/api/endpoints/test_users.py:82: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
backend/.venv/lib/python3.13/site-packages/starlette/testclient.py:569: in put
    return super().put(
backend/.venv/lib/python3.13/site-packages/httpx/_client.py:1181: in put
    return self.request(
backend/.venv/lib/python3.13/site-packages/starlette/testclient.py:437: in request
    return super().request(
backend/.venv/lib/python3.13/site-packages/httpx/_client.py:825: in request
    return self.send(request, auth=auth, follow_redirects=follow_redirects)
backend/.venv/lib/python3.13/site-packages/httpx/_client.py:914: in send
    response = self._send_handling_auth(
backend/.venv/lib/python3.13/site-packages/httpx/_client.py:942: in _send_handling_auth
    response = self._send_handling_redirects(
backend/.venv/lib/python3.13/site-packages/httpx/_client.py:979: in _send_handling_redirects
    response = self._send_single_request(request)
backend/.venv/lib/python3.13/site-packages/httpx/_client.py:1014: in _send_single_request
    response = transport.handle_request(request)
backend/.venv/lib/python3.13/site-packages/starlette/testclient.py:340: in handle_request
    raise exc
backend/.venv/lib/python3.13/site-packages/starlette/testclient.py:337: in handle_request
    portal.call(self.app, scope, receive, send)
backend/.venv/lib/python3.13/site-packages/anyio/from_thread.py:290: in call
    return cast(T_Retval, self.start_task_soon(func, *args).result())
../../../.local/share/uv/python/cpython-3.13.1-linux-x86_64-gnu/lib/python3.13/concurrent/futures/_base.py:449: in result
    return self.__get_result()
../../../.local/share/uv/python/cpython-3.13.1-linux-x86_64-gnu/lib/python3.13/concurrent/futures/_base.py:401: in __get_result
    raise self._exception
backend/.venv/lib/python3.13/site-packages/anyio/from_thread.py:221: in _call_func
    retval = await retval_or_awaitable
backend/.venv/lib/python3.13/site-packages/fastapi/applications.py:1054: in __call__
    await super().__call__(scope, receive, send)
backend/.venv/lib/python3.13/site-packages/starlette/applications.py:112: in __call__
    await self.middleware_stack(scope, receive, send)
backend/.venv/lib/python3.13/site-packages/starlette/middleware/errors.py:187: in __call__
    raise exc
backend/.venv/lib/python3.13/site-packages/starlette/middleware/errors.py:165: in __call__
    await self.app(scope, receive, _send)
backend/.venv/lib/python3.13/site-packages/starlette/middleware/cors.py:85: in __call__
    await self.app(scope, receive, send)
backend/.venv/lib/python3.13/site-packages/starlette/middleware/exceptions.py:62: in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
backend/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
backend/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
backend/.venv/lib/python3.13/site-packages/starlette/routing.py:714: in __call__
    await self.middleware_stack(scope, receive, send)
backend/.venv/lib/python3.13/site-packages/starlette/routing.py:734: in app
    await route.handle(scope, receive, send)
backend/.venv/lib/python3.13/site-packages/starlette/routing.py:288: in handle
    await self.app(scope, receive, send)
backend/.venv/lib/python3.13/site-packages/starlette/routing.py:76: in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
backend/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py:53: in wrapped_app
    raise exc
backend/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py:42: in wrapped_app
    await app(scope, receive, sender)
backend/.venv/lib/python3.13/site-packages/starlette/routing.py:73: in app
    response = await f(request)
backend/.venv/lib/python3.13/site-packages/fastapi/routing.py:301: in app
    raw_response = await run_endpoint_function(
backend/.venv/lib/python3.13/site-packages/fastapi/routing.py:212: in run_endpoint_function
    return await dependant.call(**values)
backend/app/api/endpoints/users.py:36: in update_users_me
    updated_user = await update_user(user["id"], update_data)
backend/app/db/dynamodb.py:72: in update_user
    response = users_table.update_item(
../../../.local/share/uv/python/cpython-3.13.1-linux-x86_64-gnu/lib/python3.13/unittest/mock.py:1167: in __call__
    return self._mock_call(*args, **kwargs)
../../../.local/share/uv/python/cpython-3.13.1-linux-x86_64-gnu/lib/python3.13/unittest/mock.py:1171: in _mock_call
    return self._execute_mock_call(*args, **kwargs)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <MagicMock name='users_table.update_item' id='140674232073392'>
args = ()
kwargs = {'ExpressionAttributeValues': {':full_name': 'Jane Doe'}, 'Key': {'id': 'user-123'}, 'ReturnValues': 'ALL_NEW', 'UpdateExpression': 'SET full_name = :full_name'}
effect = ClientError('An error occurred (InternalServerError) when calling the UpdateItem operation: DynamoDB broke')

    def _execute_mock_call(self, /, *args, **kwargs):
        # separate from _increment_mock_call so that awaited functions are
        # executed separately from their call, also AsyncMock overrides this method
    
        effect = self.side_effect
        if effect is not None:
            if _is_exception(effect):
>               raise effect
E               botocore.exceptions.ClientError: An error occurred (InternalServerError) when calling the UpdateItem operation: DynamoDB broke

../../../.local/share/uv/python/cpython-3.13.1-linux-x86_64-gnu/lib/python3.13/unittest/mock.py:1226: ClientError
------------------------------ Captured log call -------------------------------
ERROR    backend.app.db.dynamodb:dynamodb.py:80 Error updating user: An error occurred (InternalServerError) when calling the UpdateItem operation: DynamoDB broke
=============================== warnings summary ===============================
backend/.venv/lib/python3.13/site-packages/pydantic/_internal/_config.py:323
  /home/runner/work/summit-seo-amplify/summit-seo-amplify/backend/.venv/lib/python3.13/site-packages/pydantic/_internal/_config.py:323: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.11/migration/
    warnings.warn(DEPRECATION_MESSAGE, DeprecationWarning)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
FAILED backend/app/tests/api/endpoints/test_users.py::test_update_users_me_dynamodb_error - botocore.exceptions.ClientError: An error occurred (InternalServerError) when calling the UpdateItem operation: DynamoDB broke
==================== 1 failed, 5 passed, 1 warning in 1.96s ====================