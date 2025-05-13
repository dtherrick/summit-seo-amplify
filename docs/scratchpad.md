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

backend/app/tests/api/endpoints/test_users.py::test_read_users_me_success FAILED [ 16%]
backend/app/tests/api/endpoints/test_users.py::test_read_users_me_not_found FAILED [ 33%]
backend/app/tests/api/endpoints/test_users.py::test_update_users_me_partial_update FAILED [ 50%]
backend/app/tests/api/endpoints/test_users.py::test_update_users_me_noop FAILED [ 66%]
backend/app/tests/api/endpoints/test_users.py::test_update_users_me_not_found FAILED [ 83%]
backend/app/tests/api/endpoints/test_users.py::test_update_users_me_dynamodb_error FAILED [100%]

=================================== FAILURES ===================================
__________________________ test_read_users_me_success __________________________

mock_get_user = <AsyncMock name='get_user_by_cognito_id' id='139782176927968'>
override_get_current_user = None

    @patch("backend.app.db.dynamodb.get_user_by_cognito_id", new_callable=AsyncMock)
    def test_read_users_me_success(mock_get_user, override_get_current_user):
        mock_get_user.return_value = MOCK_USER
>       response = client.get("/api/v1/users/me")

backend/app/tests/api/endpoints/test_users.py:36: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
backend/.venv/lib/python3.13/site-packages/starlette/testclient.py:465: in get
    return super().get(
backend/.venv/lib/python3.13/site-packages/httpx/_client.py:1053: in get
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
backend/app/api/endpoints/users.py:16: in read_users_me
    user = await get_user_by_cognito_id(current_user["cognito_id"])
backend/app/db/dynamodb.py:38: in get_user_by_cognito_id
    response = users_table.query(
backend/.venv/lib/python3.13/site-packages/boto3/resources/factory.py:581: in do_action
    response = action(self, *args, **kwargs)
backend/.venv/lib/python3.13/site-packages/boto3/resources/action.py:88: in __call__
    response = getattr(parent.meta.client, operation_name)(*args, **params)
backend/.venv/lib/python3.13/site-packages/botocore/client.py:570: in _api_call
    return self._make_api_call(operation_name, kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/context.py:123: in wrapper
    return func(*args, **kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/client.py:1013: in _make_api_call
    http, parsed_response = self._make_request(
backend/.venv/lib/python3.13/site-packages/botocore/client.py:1037: in _make_request
    return self._endpoint.make_request(operation_model, request_dict)
backend/.venv/lib/python3.13/site-packages/botocore/endpoint.py:119: in make_request
    return self._send_request(request_dict, operation_model)
backend/.venv/lib/python3.13/site-packages/botocore/endpoint.py:196: in _send_request
    request = self.create_request(request_dict, operation_model)
backend/.venv/lib/python3.13/site-packages/botocore/endpoint.py:132: in create_request
    self._event_emitter.emit(
backend/.venv/lib/python3.13/site-packages/botocore/hooks.py:412: in emit
    return self._emitter.emit(aliased_event_name, **kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/hooks.py:256: in emit
    return self._emit(event_name, kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/hooks.py:239: in _emit
    response = handler(**kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/signers.py:106: in handler
    return self.sign(operation_name, request)
backend/.venv/lib/python3.13/site-packages/botocore/signers.py:198: in sign
    auth.add_auth(request)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <botocore.auth.SigV4Auth object at 0x7f2191a85be0>
request = <botocore.awsrequest.AWSRequest object at 0x7f2191a82d70>

    def add_auth(self, request):
        if self.credentials is None:
>           raise NoCredentialsError()
E           botocore.exceptions.NoCredentialsError: Unable to locate credentials

backend/.venv/lib/python3.13/site-packages/botocore/auth.py:424: NoCredentialsError
_________________________ test_read_users_me_not_found _________________________

mock_get_user = <AsyncMock name='get_user_by_cognito_id' id='139782154374512'>
override_get_current_user = None

    @patch("backend.app.db.dynamodb.get_user_by_cognito_id", new_callable=AsyncMock)
    def test_read_users_me_not_found(mock_get_user, override_get_current_user):
        mock_get_user.return_value = None
>       response = client.get("/api/v1/users/me")

backend/app/tests/api/endpoints/test_users.py:45: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
backend/.venv/lib/python3.13/site-packages/starlette/testclient.py:465: in get
    return super().get(
backend/.venv/lib/python3.13/site-packages/httpx/_client.py:1053: in get
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
../../../.local/share/uv/python/cpython-3.13.1-linux-x86_64-gnu/lib/python3.13/concurrent/futures/_base.py:456: in result
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
backend/app/api/endpoints/users.py:16: in read_users_me
    user = await get_user_by_cognito_id(current_user["cognito_id"])
backend/app/db/dynamodb.py:38: in get_user_by_cognito_id
    response = users_table.query(
backend/.venv/lib/python3.13/site-packages/boto3/resources/factory.py:581: in do_action
    response = action(self, *args, **kwargs)
backend/.venv/lib/python3.13/site-packages/boto3/resources/action.py:88: in __call__
    response = getattr(parent.meta.client, operation_name)(*args, **params)
backend/.venv/lib/python3.13/site-packages/botocore/client.py:570: in _api_call
    return self._make_api_call(operation_name, kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/context.py:123: in wrapper
    return func(*args, **kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/client.py:1013: in _make_api_call
    http, parsed_response = self._make_request(
backend/.venv/lib/python3.13/site-packages/botocore/client.py:1037: in _make_request
    return self._endpoint.make_request(operation_model, request_dict)
backend/.venv/lib/python3.13/site-packages/botocore/endpoint.py:119: in make_request
    return self._send_request(request_dict, operation_model)
backend/.venv/lib/python3.13/site-packages/botocore/endpoint.py:196: in _send_request
    request = self.create_request(request_dict, operation_model)
backend/.venv/lib/python3.13/site-packages/botocore/endpoint.py:132: in create_request
    self._event_emitter.emit(
backend/.venv/lib/python3.13/site-packages/botocore/hooks.py:412: in emit
    return self._emitter.emit(aliased_event_name, **kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/hooks.py:256: in emit
    return self._emit(event_name, kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/hooks.py:239: in _emit
    response = handler(**kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/signers.py:106: in handler
    return self.sign(operation_name, request)
backend/.venv/lib/python3.13/site-packages/botocore/signers.py:198: in sign
    auth.add_auth(request)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <botocore.auth.SigV4Auth object at 0x7f21918c2c10>
request = <botocore.awsrequest.AWSRequest object at 0x7f2191a83230>

    def add_auth(self, request):
        if self.credentials is None:
>           raise NoCredentialsError()
E           botocore.exceptions.NoCredentialsError: Unable to locate credentials

backend/.venv/lib/python3.13/site-packages/botocore/auth.py:424: NoCredentialsError
_____________________ test_update_users_me_partial_update ______________________

mock_update_user = <AsyncMock name='update_user' id='139782154380896'>
mock_get_user = <AsyncMock name='get_user_by_cognito_id' id='139782154381568'>
override_get_current_user = None

    @patch("backend.app.db.dynamodb.get_user_by_cognito_id", new_callable=AsyncMock)
    @patch("backend.app.db.dynamodb.update_user", new_callable=AsyncMock)
    def test_update_users_me_partial_update(mock_update_user, mock_get_user, override_get_current_user):
        mock_get_user.return_value = MOCK_USER.copy()
        updated = MOCK_USER.copy()
        updated["full_name"] = "Jane Doe"
        mock_update_user.return_value = updated
>       response = client.put("/api/v1/users/me", json={"full_name": "Jane Doe"})

backend/app/tests/api/endpoints/test_users.py:55: 
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
../../../.local/share/uv/python/cpython-3.13.1-linux-x86_64-gnu/lib/python3.13/concurrent/futures/_base.py:456: in result
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
backend/app/api/endpoints/users.py:29: in update_users_me
    user = await get_user_by_cognito_id(current_user["cognito_id"])
backend/app/db/dynamodb.py:38: in get_user_by_cognito_id
    response = users_table.query(
backend/.venv/lib/python3.13/site-packages/boto3/resources/factory.py:581: in do_action
    response = action(self, *args, **kwargs)
backend/.venv/lib/python3.13/site-packages/boto3/resources/action.py:88: in __call__
    response = getattr(parent.meta.client, operation_name)(*args, **params)
backend/.venv/lib/python3.13/site-packages/botocore/client.py:570: in _api_call
    return self._make_api_call(operation_name, kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/context.py:123: in wrapper
    return func(*args, **kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/client.py:1013: in _make_api_call
    http, parsed_response = self._make_request(
backend/.venv/lib/python3.13/site-packages/botocore/client.py:1037: in _make_request
    return self._endpoint.make_request(operation_model, request_dict)
backend/.venv/lib/python3.13/site-packages/botocore/endpoint.py:119: in make_request
    return self._send_request(request_dict, operation_model)
backend/.venv/lib/python3.13/site-packages/botocore/endpoint.py:196: in _send_request
    request = self.create_request(request_dict, operation_model)
backend/.venv/lib/python3.13/site-packages/botocore/endpoint.py:132: in create_request
    self._event_emitter.emit(
backend/.venv/lib/python3.13/site-packages/botocore/hooks.py:412: in emit
    return self._emitter.emit(aliased_event_name, **kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/hooks.py:256: in emit
    return self._emit(event_name, kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/hooks.py:239: in _emit
    response = handler(**kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/signers.py:106: in handler
    return self.sign(operation_name, request)
backend/.venv/lib/python3.13/site-packages/botocore/signers.py:198: in sign
    auth.add_auth(request)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <botocore.auth.SigV4Auth object at 0x7f2191618190>
request = <botocore.awsrequest.AWSRequest object at 0x7f21918aee70>

    def add_auth(self, request):
        if self.credentials is None:
>           raise NoCredentialsError()
E           botocore.exceptions.NoCredentialsError: Unable to locate credentials

backend/.venv/lib/python3.13/site-packages/botocore/auth.py:424: NoCredentialsError
__________________________ test_update_users_me_noop ___________________________

mock_update_user = <AsyncMock name='update_user' id='139782176927968'>
mock_get_user = <AsyncMock name='get_user_by_cognito_id' id='139782176929312'>
override_get_current_user = None

    @patch("backend.app.db.dynamodb.get_user_by_cognito_id", new_callable=AsyncMock)
    @patch("backend.app.db.dynamodb.update_user", new_callable=AsyncMock)
    def test_update_users_me_noop(mock_update_user, mock_get_user, override_get_current_user):
        mock_get_user.return_value = MOCK_USER.copy()
>       response = client.put("/api/v1/users/me", json={})

backend/app/tests/api/endpoints/test_users.py:65: 
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
backend/app/api/endpoints/users.py:29: in update_users_me
    user = await get_user_by_cognito_id(current_user["cognito_id"])
backend/app/db/dynamodb.py:38: in get_user_by_cognito_id
    response = users_table.query(
backend/.venv/lib/python3.13/site-packages/boto3/resources/factory.py:581: in do_action
    response = action(self, *args, **kwargs)
backend/.venv/lib/python3.13/site-packages/boto3/resources/action.py:88: in __call__
    response = getattr(parent.meta.client, operation_name)(*args, **params)
backend/.venv/lib/python3.13/site-packages/botocore/client.py:570: in _api_call
    return self._make_api_call(operation_name, kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/context.py:123: in wrapper
    return func(*args, **kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/client.py:1013: in _make_api_call
    http, parsed_response = self._make_request(
backend/.venv/lib/python3.13/site-packages/botocore/client.py:1037: in _make_request
    return self._endpoint.make_request(operation_model, request_dict)
backend/.venv/lib/python3.13/site-packages/botocore/endpoint.py:119: in make_request
    return self._send_request(request_dict, operation_model)
backend/.venv/lib/python3.13/site-packages/botocore/endpoint.py:196: in _send_request
    request = self.create_request(request_dict, operation_model)
backend/.venv/lib/python3.13/site-packages/botocore/endpoint.py:132: in create_request
    self._event_emitter.emit(
backend/.venv/lib/python3.13/site-packages/botocore/hooks.py:412: in emit
    return self._emitter.emit(aliased_event_name, **kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/hooks.py:256: in emit
    return self._emit(event_name, kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/hooks.py:239: in _emit
    response = handler(**kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/signers.py:106: in handler
    return self.sign(operation_name, request)
backend/.venv/lib/python3.13/site-packages/botocore/signers.py:198: in sign
    auth.add_auth(request)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <botocore.auth.SigV4Auth object at 0x7f2191a816e0>
request = <botocore.awsrequest.AWSRequest object at 0x7f2192f4d040>

    def add_auth(self, request):
        if self.credentials is None:
>           raise NoCredentialsError()
E           botocore.exceptions.NoCredentialsError: Unable to locate credentials

backend/.venv/lib/python3.13/site-packages/botocore/auth.py:424: NoCredentialsError
________________________ test_update_users_me_not_found ________________________

mock_get_user = <AsyncMock name='get_user_by_cognito_id' id='139782176930656'>
override_get_current_user = None

    @patch("backend.app.db.dynamodb.get_user_by_cognito_id", new_callable=AsyncMock)
    def test_update_users_me_not_found(mock_get_user, override_get_current_user):
        mock_get_user.return_value = None
>       response = client.put("/api/v1/users/me", json={"full_name": "Jane Doe"})

backend/app/tests/api/endpoints/test_users.py:74: 
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
backend/app/api/endpoints/users.py:29: in update_users_me
    user = await get_user_by_cognito_id(current_user["cognito_id"])
backend/app/db/dynamodb.py:38: in get_user_by_cognito_id
    response = users_table.query(
backend/.venv/lib/python3.13/site-packages/boto3/resources/factory.py:581: in do_action
    response = action(self, *args, **kwargs)
backend/.venv/lib/python3.13/site-packages/boto3/resources/action.py:88: in __call__
    response = getattr(parent.meta.client, operation_name)(*args, **params)
backend/.venv/lib/python3.13/site-packages/botocore/client.py:570: in _api_call
    return self._make_api_call(operation_name, kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/context.py:123: in wrapper
    return func(*args, **kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/client.py:1013: in _make_api_call
    http, parsed_response = self._make_request(
backend/.venv/lib/python3.13/site-packages/botocore/client.py:1037: in _make_request
    return self._endpoint.make_request(operation_model, request_dict)
backend/.venv/lib/python3.13/site-packages/botocore/endpoint.py:119: in make_request
    return self._send_request(request_dict, operation_model)
backend/.venv/lib/python3.13/site-packages/botocore/endpoint.py:196: in _send_request
    request = self.create_request(request_dict, operation_model)
backend/.venv/lib/python3.13/site-packages/botocore/endpoint.py:132: in create_request
    self._event_emitter.emit(
backend/.venv/lib/python3.13/site-packages/botocore/hooks.py:412: in emit
    return self._emitter.emit(aliased_event_name, **kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/hooks.py:256: in emit
    return self._emit(event_name, kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/hooks.py:239: in _emit
    response = handler(**kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/signers.py:106: in handler
    return self.sign(operation_name, request)
backend/.venv/lib/python3.13/site-packages/botocore/signers.py:198: in sign
    auth.add_auth(request)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <botocore.auth.SigV4Auth object at 0x7f219198c180>
request = <botocore.awsrequest.AWSRequest object at 0x7f2192fcc490>

    def add_auth(self, request):
        if self.credentials is None:
>           raise NoCredentialsError()
E           botocore.exceptions.NoCredentialsError: Unable to locate credentials

backend/.venv/lib/python3.13/site-packages/botocore/auth.py:424: NoCredentialsError
_____________________ test_update_users_me_dynamodb_error ______________________

mock_update_user = <AsyncMock name='update_user' id='139782176930992'>
mock_get_user = <AsyncMock name='get_user_by_cognito_id' id='139782154374512'>
override_get_current_user = None

    @patch("backend.app.db.dynamodb.get_user_by_cognito_id", new_callable=AsyncMock)
    @patch("backend.app.db.dynamodb.update_user", new_callable=AsyncMock)
    def test_update_users_me_dynamodb_error(mock_update_user, mock_get_user, override_get_current_user):
        mock_get_user.return_value = MOCK_USER.copy()
        mock_update_user.side_effect = Exception("DynamoDB error")
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
backend/app/api/endpoints/users.py:29: in update_users_me
    user = await get_user_by_cognito_id(current_user["cognito_id"])
backend/app/db/dynamodb.py:38: in get_user_by_cognito_id
    response = users_table.query(
backend/.venv/lib/python3.13/site-packages/boto3/resources/factory.py:581: in do_action
    response = action(self, *args, **kwargs)
backend/.venv/lib/python3.13/site-packages/boto3/resources/action.py:88: in __call__
    response = getattr(parent.meta.client, operation_name)(*args, **params)
backend/.venv/lib/python3.13/site-packages/botocore/client.py:570: in _api_call
    return self._make_api_call(operation_name, kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/context.py:123: in wrapper
    return func(*args, **kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/client.py:1013: in _make_api_call
    http, parsed_response = self._make_request(
backend/.venv/lib/python3.13/site-packages/botocore/client.py:1037: in _make_request
    return self._endpoint.make_request(operation_model, request_dict)
backend/.venv/lib/python3.13/site-packages/botocore/endpoint.py:119: in make_request
    return self._send_request(request_dict, operation_model)
backend/.venv/lib/python3.13/site-packages/botocore/endpoint.py:196: in _send_request
    request = self.create_request(request_dict, operation_model)
backend/.venv/lib/python3.13/site-packages/botocore/endpoint.py:132: in create_request
    self._event_emitter.emit(
backend/.venv/lib/python3.13/site-packages/botocore/hooks.py:412: in emit
    return self._emitter.emit(aliased_event_name, **kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/hooks.py:256: in emit
    return self._emit(event_name, kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/hooks.py:239: in _emit
    response = handler(**kwargs)
backend/.venv/lib/python3.13/site-packages/botocore/signers.py:106: in handler
    return self.sign(operation_name, request)
backend/.venv/lib/python3.13/site-packages/botocore/signers.py:198: in sign
    auth.add_auth(request)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <botocore.auth.SigV4Auth object at 0x7f21918aed50>
request = <botocore.awsrequest.AWSRequest object at 0x7f2192fc2150>

    def add_auth(self, request):
        if self.credentials is None:
>           raise NoCredentialsError()
E           botocore.exceptions.NoCredentialsError: Unable to locate credentials

backend/.venv/lib/python3.13/site-packages/botocore/auth.py:424: NoCredentialsError
=============================== warnings summary ===============================
backend/.venv/lib/python3.13/site-packages/pydantic/_internal/_config.py:323
  /home/runner/work/summit-seo-amplify/summit-seo-amplify/backend/.venv/lib/python3.13/site-packages/pydantic/_internal/_config.py:323: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.11/migration/
    warnings.warn(DEPRECATION_MESSAGE, DeprecationWarning)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
FAILED backend/app/tests/api/endpoints/test_users.py::test_read_users_me_success - botocore.exceptions.NoCredentialsError: Unable to locate credentials
FAILED backend/app/tests/api/endpoints/test_users.py::test_read_users_me_not_found - botocore.exceptions.NoCredentialsError: Unable to locate credentials
FAILED backend/app/tests/api/endpoints/test_users.py::test_update_users_me_partial_update - botocore.exceptions.NoCredentialsError: Unable to locate credentials
FAILED backend/app/tests/api/endpoints/test_users.py::test_update_users_me_noop - botocore.exceptions.NoCredentialsError: Unable to locate credentials
FAILED backend/app/tests/api/endpoints/test_users.py::test_update_users_me_not_found - botocore.exceptions.NoCredentialsError: Unable to locate credentials
FAILED backend/app/tests/api/endpoints/test_users.py::test_update_users_me_dynamodb_error - botocore.exceptions.NoCredentialsError: Unable to locate credentials
========================= 6 failed, 1 warning in 3.17s =========================