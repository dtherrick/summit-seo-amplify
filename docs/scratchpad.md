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

mock_get_user = <AsyncMock name='get_user_by_cognito_id' id='139925511074016'>
override_get_current_user = None

    @patch("backend.app.db.dynamodb.get_user_by_cognito_id", new_callable=AsyncMock)
    def test_read_users_me_success(mock_get_user, override_get_current_user):
        mock_get_user.return_value = MOCK_USER
>       response = client.get("/api/v1/users/me")

backend/app/tests/api/endpoints/test_users.py:41: 
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
backend/.venv/lib/python3.13/site-packages/fastapi/routing.py:327: in app
    content = await serialize_response(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    async def serialize_response(
        *,
        field: Optional[ModelField] = None,
        response_content: Any,
        include: Optional[IncEx] = None,
        exclude: Optional[IncEx] = None,
        by_alias: bool = True,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        is_coroutine: bool = True,
    ) -> Any:
        if field:
            errors = []
            if not hasattr(field, "serialize"):
                # pydantic v1
                response_content = _prepare_response_content(
                    response_content,
                    exclude_unset=exclude_unset,
                    exclude_defaults=exclude_defaults,
                    exclude_none=exclude_none,
                )
            if is_coroutine:
                value, errors_ = field.validate(response_content, {}, loc=("response",))
            else:
                value, errors_ = await run_in_threadpool(
                    field.validate, response_content, {}, loc=("response",)
                )
            if isinstance(errors_, list):
                errors.extend(errors_)
            elif errors_:
                errors.append(errors_)
            if errors:
>               raise ResponseValidationError(
                    errors=_normalize_errors(errors), body=response_content
                )
E               fastapi.exceptions.ResponseValidationError: 7 validation errors:
E                 {'type': 'string_type', 'loc': ('response', 'email'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().email' id='139925486463232'>}
E                 {'type': 'string_type', 'loc': ('response', 'full_name'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().full_name' id='139925486463568'>}
E                 {'type': 'string_type', 'loc': ('response', 'id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().id' id='139925486464576'>}
E                 {'type': 'string_type', 'loc': ('response', 'tenant_id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().tenant_id' id='139925486464912'>}
E                 {'type': 'string_type', 'loc': ('response', 'cognito_id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().cognito_id' id='139925486465248'>}
E                 {'type': 'string_type', 'loc': ('response', 'user_type'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().user_type' id='139925486466928'>}
E                 {'type': 'string_type', 'loc': ('response', 'subscription_tier'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().subscription_tier' id='139925486467264'>}

backend/.venv/lib/python3.13/site-packages/fastapi/routing.py:176: ResponseValidationError
_________________________ test_read_users_me_not_found _________________________

mock_get_user = <AsyncMock name='get_user_by_cognito_id' id='139925489469488'>
override_get_current_user = None

    @patch("backend.app.db.dynamodb.get_user_by_cognito_id", new_callable=AsyncMock)
    def test_read_users_me_not_found(mock_get_user, override_get_current_user):
        mock_get_user.return_value = None
>       response = client.get("/api/v1/users/me")

backend/app/tests/api/endpoints/test_users.py:50: 
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
backend/.venv/lib/python3.13/site-packages/fastapi/routing.py:327: in app
    content = await serialize_response(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    async def serialize_response(
        *,
        field: Optional[ModelField] = None,
        response_content: Any,
        include: Optional[IncEx] = None,
        exclude: Optional[IncEx] = None,
        by_alias: bool = True,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        is_coroutine: bool = True,
    ) -> Any:
        if field:
            errors = []
            if not hasattr(field, "serialize"):
                # pydantic v1
                response_content = _prepare_response_content(
                    response_content,
                    exclude_unset=exclude_unset,
                    exclude_defaults=exclude_defaults,
                    exclude_none=exclude_none,
                )
            if is_coroutine:
                value, errors_ = field.validate(response_content, {}, loc=("response",))
            else:
                value, errors_ = await run_in_threadpool(
                    field.validate, response_content, {}, loc=("response",)
                )
            if isinstance(errors_, list):
                errors.extend(errors_)
            elif errors_:
                errors.append(errors_)
            if errors:
>               raise ResponseValidationError(
                    errors=_normalize_errors(errors), body=response_content
                )
E               fastapi.exceptions.ResponseValidationError: 7 validation errors:
E                 {'type': 'string_type', 'loc': ('response', 'email'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().email' id='139925489471840'>}
E                 {'type': 'string_type', 'loc': ('response', 'full_name'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().full_name' id='139925489472176'>}
E                 {'type': 'string_type', 'loc': ('response', 'id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().id' id='139925489473184'>}
E                 {'type': 'string_type', 'loc': ('response', 'tenant_id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().tenant_id' id='139925489473520'>}
E                 {'type': 'string_type', 'loc': ('response', 'cognito_id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().cognito_id' id='139925489473856'>}
E                 {'type': 'string_type', 'loc': ('response', 'user_type'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().user_type' id='139925489475536'>}
E                 {'type': 'string_type', 'loc': ('response', 'subscription_tier'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().subscription_tier' id='139925489475872'>}

backend/.venv/lib/python3.13/site-packages/fastapi/routing.py:176: ResponseValidationError
_____________________ test_update_users_me_partial_update ______________________

mock_update_user = <AsyncMock name='update_user' id='139925489479232'>
mock_get_user = <AsyncMock name='get_user_by_cognito_id' id='139925489471504'>
override_get_current_user = None

    @patch("backend.app.db.dynamodb.get_user_by_cognito_id", new_callable=AsyncMock)
    @patch("backend.app.db.dynamodb.update_user", new_callable=AsyncMock)
    def test_update_users_me_partial_update(mock_update_user, mock_get_user, override_get_current_user):
        mock_get_user.return_value = MOCK_USER.copy()
        updated = MOCK_USER.copy()
        updated["full_name"] = "Jane Doe"
        mock_update_user.return_value = updated
>       response = client.put("/api/v1/users/me", json={"full_name": "Jane Doe"})

backend/app/tests/api/endpoints/test_users.py:60: 
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
backend/.venv/lib/python3.13/site-packages/fastapi/routing.py:327: in app
    content = await serialize_response(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    async def serialize_response(
        *,
        field: Optional[ModelField] = None,
        response_content: Any,
        include: Optional[IncEx] = None,
        exclude: Optional[IncEx] = None,
        by_alias: bool = True,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        is_coroutine: bool = True,
    ) -> Any:
        if field:
            errors = []
            if not hasattr(field, "serialize"):
                # pydantic v1
                response_content = _prepare_response_content(
                    response_content,
                    exclude_unset=exclude_unset,
                    exclude_defaults=exclude_defaults,
                    exclude_none=exclude_none,
                )
            if is_coroutine:
                value, errors_ = field.validate(response_content, {}, loc=("response",))
            else:
                value, errors_ = await run_in_threadpool(
                    field.validate, response_content, {}, loc=("response",)
                )
            if isinstance(errors_, list):
                errors.extend(errors_)
            elif errors_:
                errors.append(errors_)
            if errors:
>               raise ResponseValidationError(
                    errors=_normalize_errors(errors), body=response_content
                )
E               fastapi.exceptions.ResponseValidationError: 7 validation errors:
E                 {'type': 'string_type', 'loc': ('response', 'email'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().email' id='139925489482928'>}
E                 {'type': 'string_type', 'loc': ('response', 'full_name'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().full_name' id='139925489483264'>}
E                 {'type': 'string_type', 'loc': ('response', 'id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().id' id='139925486076656'>}
E                 {'type': 'string_type', 'loc': ('response', 'tenant_id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().tenant_id' id='139925486076992'>}
E                 {'type': 'string_type', 'loc': ('response', 'cognito_id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().cognito_id' id='139925486077328'>}
E                 {'type': 'string_type', 'loc': ('response', 'user_type'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().user_type' id='139925486079008'>}
E                 {'type': 'string_type', 'loc': ('response', 'subscription_tier'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().subscription_tier' id='139925486079344'>}

backend/.venv/lib/python3.13/site-packages/fastapi/routing.py:176: ResponseValidationError
__________________________ test_update_users_me_noop ___________________________

mock_update_user = <AsyncMock name='update_user' id='139925486083040'>
mock_get_user = <AsyncMock name='get_user_by_cognito_id' id='139925486080016'>
override_get_current_user = None

    @patch("backend.app.db.dynamodb.get_user_by_cognito_id", new_callable=AsyncMock)
    @patch("backend.app.db.dynamodb.update_user", new_callable=AsyncMock)
    def test_update_users_me_noop(mock_update_user, mock_get_user, override_get_current_user):
        mock_get_user.return_value = MOCK_USER.copy()
>       response = client.put("/api/v1/users/me", json={})

backend/app/tests/api/endpoints/test_users.py:70: 
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
backend/.venv/lib/python3.13/site-packages/fastapi/routing.py:327: in app
    content = await serialize_response(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    async def serialize_response(
        *,
        field: Optional[ModelField] = None,
        response_content: Any,
        include: Optional[IncEx] = None,
        exclude: Optional[IncEx] = None,
        by_alias: bool = True,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        is_coroutine: bool = True,
    ) -> Any:
        if field:
            errors = []
            if not hasattr(field, "serialize"):
                # pydantic v1
                response_content = _prepare_response_content(
                    response_content,
                    exclude_unset=exclude_unset,
                    exclude_defaults=exclude_defaults,
                    exclude_none=exclude_none,
                )
            if is_coroutine:
                value, errors_ = field.validate(response_content, {}, loc=("response",))
            else:
                value, errors_ = await run_in_threadpool(
                    field.validate, response_content, {}, loc=("response",)
                )
            if isinstance(errors_, list):
                errors.extend(errors_)
            elif errors_:
                errors.append(errors_)
            if errors:
>               raise ResponseValidationError(
                    errors=_normalize_errors(errors), body=response_content
                )
E               fastapi.exceptions.ResponseValidationError: 7 validation errors:
E                 {'type': 'string_type', 'loc': ('response', 'email'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().email' id='139925486084720'>}
E                 {'type': 'string_type', 'loc': ('response', 'full_name'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().full_name' id='139925486085056'>}
E                 {'type': 'string_type', 'loc': ('response', 'id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().id' id='139925486086064'>}
E                 {'type': 'string_type', 'loc': ('response', 'tenant_id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().tenant_id' id='139925486086400'>}
E                 {'type': 'string_type', 'loc': ('response', 'cognito_id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().cognito_id' id='139925486086736'>}
E                 {'type': 'string_type', 'loc': ('response', 'user_type'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().user_type' id='139925486088416'>}
E                 {'type': 'string_type', 'loc': ('response', 'subscription_tier'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().subscription_tier' id='139925486088752'>}

backend/.venv/lib/python3.13/site-packages/fastapi/routing.py:176: ResponseValidationError
________________________ test_update_users_me_not_found ________________________

mock_get_user = <AsyncMock name='get_user_by_cognito_id' id='139925489471504'>
override_get_current_user = None

    @patch("backend.app.db.dynamodb.get_user_by_cognito_id", new_callable=AsyncMock)
    def test_update_users_me_not_found(mock_get_user, override_get_current_user):
        mock_get_user.return_value = None
>       response = client.put("/api/v1/users/me", json={"full_name": "Jane Doe"})

backend/app/tests/api/endpoints/test_users.py:79: 
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
backend/.venv/lib/python3.13/site-packages/fastapi/routing.py:327: in app
    content = await serialize_response(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    async def serialize_response(
        *,
        field: Optional[ModelField] = None,
        response_content: Any,
        include: Optional[IncEx] = None,
        exclude: Optional[IncEx] = None,
        by_alias: bool = True,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        is_coroutine: bool = True,
    ) -> Any:
        if field:
            errors = []
            if not hasattr(field, "serialize"):
                # pydantic v1
                response_content = _prepare_response_content(
                    response_content,
                    exclude_unset=exclude_unset,
                    exclude_defaults=exclude_defaults,
                    exclude_none=exclude_none,
                )
            if is_coroutine:
                value, errors_ = field.validate(response_content, {}, loc=("response",))
            else:
                value, errors_ = await run_in_threadpool(
                    field.validate, response_content, {}, loc=("response",)
                )
            if isinstance(errors_, list):
                errors.extend(errors_)
            elif errors_:
                errors.append(errors_)
            if errors:
>               raise ResponseValidationError(
                    errors=_normalize_errors(errors), body=response_content
                )
E               fastapi.exceptions.ResponseValidationError: 7 validation errors:
E                 {'type': 'string_type', 'loc': ('response', 'email'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().email' id='139925489477888'>}
E                 {'type': 'string_type', 'loc': ('response', 'full_name'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().full_name' id='139925489481584'>}
E                 {'type': 'string_type', 'loc': ('response', 'id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().id' id='139925489475200'>}
E                 {'type': 'string_type', 'loc': ('response', 'tenant_id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().tenant_id' id='139925489474528'>}
E                 {'type': 'string_type', 'loc': ('response', 'cognito_id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().cognito_id' id='139925489472848'>}
E                 {'type': 'string_type', 'loc': ('response', 'user_type'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().user_type' id='139925489472176'>}
E                 {'type': 'string_type', 'loc': ('response', 'subscription_tier'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().subscription_tier' id='139925489473184'>}

backend/.venv/lib/python3.13/site-packages/fastapi/routing.py:176: ResponseValidationError
_____________________ test_update_users_me_dynamodb_error ______________________

mock_update_user = <AsyncMock name='update_user' id='139925489469152'>
mock_get_user = <AsyncMock name='get_user_by_cognito_id' id='139925489478896'>
override_get_current_user = None

    @patch("backend.app.db.dynamodb.get_user_by_cognito_id", new_callable=AsyncMock)
    @patch("backend.app.db.dynamodb.update_user", new_callable=AsyncMock)
    def test_update_users_me_dynamodb_error(mock_update_user, mock_get_user, override_get_current_user):
        mock_get_user.return_value = MOCK_USER.copy()
        mock_update_user.side_effect = Exception("DynamoDB error")
>       response = client.put("/api/v1/users/me", json={"full_name": "Jane Doe"})

backend/app/tests/api/endpoints/test_users.py:87: 
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
backend/.venv/lib/python3.13/site-packages/fastapi/routing.py:327: in app
    content = await serialize_response(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    async def serialize_response(
        *,
        field: Optional[ModelField] = None,
        response_content: Any,
        include: Optional[IncEx] = None,
        exclude: Optional[IncEx] = None,
        by_alias: bool = True,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        is_coroutine: bool = True,
    ) -> Any:
        if field:
            errors = []
            if not hasattr(field, "serialize"):
                # pydantic v1
                response_content = _prepare_response_content(
                    response_content,
                    exclude_unset=exclude_unset,
                    exclude_defaults=exclude_defaults,
                    exclude_none=exclude_none,
                )
            if is_coroutine:
                value, errors_ = field.validate(response_content, {}, loc=("response",))
            else:
                value, errors_ = await run_in_threadpool(
                    field.validate, response_content, {}, loc=("response",)
                )
            if isinstance(errors_, list):
                errors.extend(errors_)
            elif errors_:
                errors.append(errors_)
            if errors:
>               raise ResponseValidationError(
                    errors=_normalize_errors(errors), body=response_content
                )
E               fastapi.exceptions.ResponseValidationError: 7 validation errors:
E                 {'type': 'string_type', 'loc': ('response', 'email'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().email' id='139925486465584'>}
E                 {'type': 'string_type', 'loc': ('response', 'full_name'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().full_name' id='139925486463904'>}
E                 {'type': 'string_type', 'loc': ('response', 'id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().id' id='139925486464576'>}
E                 {'type': 'string_type', 'loc': ('response', 'tenant_id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().tenant_id' id='139925486464912'>}
E                 {'type': 'string_type', 'loc': ('response', 'cognito_id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().cognito_id' id='139925486465248'>}
E                 {'type': 'string_type', 'loc': ('response', 'user_type'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().user_type' id='139925486461888'>}
E                 {'type': 'string_type', 'loc': ('response', 'subscription_tier'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().subscription_tier' id='139925486461552'>}

backend/.venv/lib/python3.13/site-packages/fastapi/routing.py:176: ResponseValidationError
=============================== warnings summary ===============================
backend/.venv/lib/python3.13/site-packages/pydantic/_internal/_config.py:323
  /home/runner/work/summit-seo-amplify/summit-seo-amplify/backend/.venv/lib/python3.13/site-packages/pydantic/_internal/_config.py:323: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.11/migration/
    warnings.warn(DEPRECATION_MESSAGE, DeprecationWarning)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
FAILED backend/app/tests/api/endpoints/test_users.py::test_read_users_me_success - fastapi.exceptions.ResponseValidationError: 7 validation errors:
  {'type': 'string_type', 'loc': ('response', 'email'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().email' id='139925486463232'>}
  {'type': 'string_type', 'loc': ('response', 'full_name'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().full_name' id='139925486463568'>}
  {'type': 'string_type', 'loc': ('response', 'id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().id' id='139925486464576'>}
  {'type': 'string_type', 'loc': ('response', 'tenant_id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().tenant_id' id='139925486464912'>}
  {'type': 'string_type', 'loc': ('response', 'cognito_id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().cognito_id' id='139925486465248'>}
  {'type': 'string_type', 'loc': ('response', 'user_type'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().user_type' id='139925486466928'>}
  {'type': 'string_type', 'loc': ('response', 'subscription_tier'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().subscription_tier' id='139925486467264'>}
FAILED backend/app/tests/api/endpoints/test_users.py::test_read_users_me_not_found - fastapi.exceptions.ResponseValidationError: 7 validation errors:
  {'type': 'string_type', 'loc': ('response', 'email'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().email' id='139925489471840'>}
  {'type': 'string_type', 'loc': ('response', 'full_name'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().full_name' id='139925489472176'>}
  {'type': 'string_type', 'loc': ('response', 'id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().id' id='139925489473184'>}
  {'type': 'string_type', 'loc': ('response', 'tenant_id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().tenant_id' id='139925489473520'>}
  {'type': 'string_type', 'loc': ('response', 'cognito_id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().cognito_id' id='139925489473856'>}
  {'type': 'string_type', 'loc': ('response', 'user_type'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().user_type' id='139925489475536'>}
  {'type': 'string_type', 'loc': ('response', 'subscription_tier'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().subscription_tier' id='139925489475872'>}
FAILED backend/app/tests/api/endpoints/test_users.py::test_update_users_me_partial_update - fastapi.exceptions.ResponseValidationError: 7 validation errors:
  {'type': 'string_type', 'loc': ('response', 'email'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().email' id='139925489482928'>}
  {'type': 'string_type', 'loc': ('response', 'full_name'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().full_name' id='139925489483264'>}
  {'type': 'string_type', 'loc': ('response', 'id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().id' id='139925486076656'>}
  {'type': 'string_type', 'loc': ('response', 'tenant_id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().tenant_id' id='139925486076992'>}
  {'type': 'string_type', 'loc': ('response', 'cognito_id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().cognito_id' id='139925486077328'>}
  {'type': 'string_type', 'loc': ('response', 'user_type'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().user_type' id='139925486079008'>}
  {'type': 'string_type', 'loc': ('response', 'subscription_tier'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().subscription_tier' id='139925486079344'>}
FAILED backend/app/tests/api/endpoints/test_users.py::test_update_users_me_noop - fastapi.exceptions.ResponseValidationError: 7 validation errors:
  {'type': 'string_type', 'loc': ('response', 'email'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().email' id='139925486084720'>}
  {'type': 'string_type', 'loc': ('response', 'full_name'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().full_name' id='139925486085056'>}
  {'type': 'string_type', 'loc': ('response', 'id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().id' id='139925486086064'>}
  {'type': 'string_type', 'loc': ('response', 'tenant_id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().tenant_id' id='139925486086400'>}
  {'type': 'string_type', 'loc': ('response', 'cognito_id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().cognito_id' id='139925486086736'>}
  {'type': 'string_type', 'loc': ('response', 'user_type'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().user_type' id='139925486088416'>}
  {'type': 'string_type', 'loc': ('response', 'subscription_tier'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.query().get().__getitem__().subscription_tier' id='139925486088752'>}
FAILED backend/app/tests/api/endpoints/test_users.py::test_update_users_me_not_found - fastapi.exceptions.ResponseValidationError: 7 validation errors:
  {'type': 'string_type', 'loc': ('response', 'email'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().email' id='139925489477888'>}
  {'type': 'string_type', 'loc': ('response', 'full_name'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().full_name' id='139925489481584'>}
  {'type': 'string_type', 'loc': ('response', 'id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().id' id='139925489475200'>}
  {'type': 'string_type', 'loc': ('response', 'tenant_id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().tenant_id' id='139925489474528'>}
  {'type': 'string_type', 'loc': ('response', 'cognito_id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().cognito_id' id='139925489472848'>}
  {'type': 'string_type', 'loc': ('response', 'user_type'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().user_type' id='139925489472176'>}
  {'type': 'string_type', 'loc': ('response', 'subscription_tier'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().subscription_tier' id='139925489473184'>}
FAILED backend/app/tests/api/endpoints/test_users.py::test_update_users_me_dynamodb_error - fastapi.exceptions.ResponseValidationError: 7 validation errors:
  {'type': 'string_type', 'loc': ('response', 'email'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().email' id='139925486465584'>}
  {'type': 'string_type', 'loc': ('response', 'full_name'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().full_name' id='139925486463904'>}
  {'type': 'string_type', 'loc': ('response', 'id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().id' id='139925486464576'>}
  {'type': 'string_type', 'loc': ('response', 'tenant_id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().tenant_id' id='139925486464912'>}
  {'type': 'string_type', 'loc': ('response', 'cognito_id'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().cognito_id' id='139925486465248'>}
  {'type': 'string_type', 'loc': ('response', 'user_type'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().user_type' id='139925486461888'>}
  {'type': 'string_type', 'loc': ('response', 'subscription_tier'), 'msg': 'Input should be a valid string', 'input': <MagicMock name='mock.update_item().get().subscription_tier' id='139925486461552'>}
========================= 6 failed, 1 warning in 2.75s =========================