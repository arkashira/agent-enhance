import json
from dataclasses import dataclass
from typing import List

@dataclass
class Integration:
    name: str
    config: dict

class AgentReachPro:
    def __init__(self):
        self.integrations = []

    def add_integration(self, integration: Integration):
        self.integrations.append(integration)

    def get_integrations(self):
        return self.integrations

    def configure_integration(self, name: str, config: dict):
        for integration in self.integrations:
            if integration.name == name:
                integration.config = config
                return
        if name == "":
            raise ValueError("Integration name cannot be empty")
        raise ValueError(f"Integration {name} not found")

    def test_integration(self, name: str):
        for integration in self.integrations:
            if integration.name == name:
                # Simulate testing the integration
                return True
        raise ValueError(f"Integration {name} not found")

    def to_json(self):
        return json.dumps([{"name": i.name, "config": i.config} for i in self.integrations])

    @staticmethod
    def from_json(json_str: str):
        agent_reach_pro = AgentReachPro()
        integrations = json.loads(json_str)
        for integration in integrations:
            agent_reach_pro.add_integration(Integration(integration["name"], integration["config"]))
        return agent_reach_pro
