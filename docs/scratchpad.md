[ERROR]	2025-05-18T22:44:25.729Z	06ceef41-cfd6-47d5-bc27-4f9718b67713	An error occurred running the application.
Traceback (most recent call last):
  File "/var/task/mangum/protocols/http.py", line 58, in run
    await app(self.scope, self.receive, self.send)
  File "/var/task/fastapi/applications.py", line 1054, in __call__
    await super().__call__(scope, receive, send)
  File "/var/task/starlette/applications.py", line 112, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/var/task/starlette/middleware/errors.py", line 187, in __call__
    raise exc
  File "/var/task/starlette/middleware/errors.py", line 165, in __call__
    await self.app(scope, receive, _send)
  File "/var/task/starlette/middleware/exceptions.py", line 62, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "/var/task/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "/var/task/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/var/task/starlette/routing.py", line 714, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/var/task/starlette/routing.py", line 734, in app
    await route.handle(scope, receive, send)
  File "/var/task/starlette/routing.py", line 288, in handle
    await self.app(scope, receive, send)
  File "/var/task/starlette/routing.py", line 76, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "/var/task/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "/var/task/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/var/task/starlette/routing.py", line 73, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "/var/task/fastapi/routing.py", line 327, in app
    content = await serialize_response(
              ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/var/task/fastapi/routing.py", line 176, in serialize_response
    raise ResponseValidationError(
fastapi.exceptions.ResponseValidationError: 2 validation errors:
  {'type': 'missing', 'loc': ('response', 'id'), 'msg': 'Field required', 'input': {'updated_at': '2025-05-11T02:35:29.603464', 'user_id': 'c3933f85-813a-42dd-894a-739459648904', 'created_at': '2025-05-11T02:35:29.603464', 'cognito_id': 'f468e498-f051-705f-e684-d15444d72ae5', 'subscription_tier': 'free', 'user_type': 'user', 'email': 'damian.herrick@gmail.com'}}
  {'type': 'missing', 'loc': ('response', 'tenant_id'), 'msg': 'Field required', 'input': {'updated_at': '2025-05-11T02:35:29.603464', 'user_id': 'c3933f85-813a-42dd-894a-739459648904', 'created_at': '2025-05-11T02:35:29.603464', 'cognito_id': 'f468e498-f051-705f-e684-d15444d72ae5', 'subscription_tier': 'free', 'user_type': 'user', 'email': 'damian.herrick@gmail.com'}}