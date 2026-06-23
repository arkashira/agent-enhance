import json
from dataclasses import dataclass
from typing import Dict

@dataclass
class AuthConfig:
    token: str

class AuthMiddleware:
    def __init__(self, config: AuthConfig):
        self.config = config

    def authenticate(self, request: Dict) -> bool:
        return request.get("token") == self.config.token

class RateLimitMiddleware:
    def __init__(self, max_requests: int):
        self.max_requests = max_requests
        self.requests = 0

    def allow_request(self) -> bool:
        if self.requests < self.max_requests:
            self.requests += 1
            return True
        return False

class HealthCheckMiddleware:
    def check(self) -> bool:
        return True

def register_middleware(config: AuthConfig, max_requests: int) -> Dict:
    auth_middleware = AuthMiddleware(config)
    rate_limit_middleware = RateLimitMiddleware(max_requests)
    health_check_middleware = HealthCheckMiddleware()
    return {
        "auth": auth_middleware,
        "rate_limit": rate_limit_middleware,
        "health_check": health_check_middleware,
    }
