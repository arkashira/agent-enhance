import pytest
import sys
sys.path.insert(0, '../src')
from agent_reach_pro import AuthConfig, AuthMiddleware, RateLimitMiddleware, HealthCheckMiddleware, register_middleware

def test_auth_middleware():
    config = AuthConfig(token="test_token")
    auth_middleware = AuthMiddleware(config)
    request_with_token = {"token": "test_token"}
    request_without_token = {}
    assert auth_middleware.authenticate(request_with_token)
    assert not auth_middleware.authenticate(request_without_token)

def test_rate_limit_middleware():
    max_requests = 5
    rate_limit_middleware = RateLimitMiddleware(max_requests)
    for _ in range(max_requests):
        assert rate_limit_middleware.allow_request()
    assert not rate_limit_middleware.allow_request()

def test_health_check_middleware():
    health_check_middleware = HealthCheckMiddleware()
    assert health_check_middleware.check()

def test_register_middleware():
    config = AuthConfig(token="test_token")
    max_requests = 5
    middleware = register_middleware(config, max_requests)
    assert isinstance(middleware["auth"], AuthMiddleware)
    assert isinstance(middleware["rate_limit"], RateLimitMiddleware)
    assert isinstance(middleware["health_check"], HealthCheckMiddleware)
