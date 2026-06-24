from agent_reach_pro import AgentReachPro, Integration

def test_add_integration():
    agent_reach_pro = AgentReachPro()
    integration = Integration("Test Integration", {"key": "value"})
    agent_reach_pro.add_integration(integration)
    assert len(agent_reach_pro.get_integrations()) == 1

def test_get_integrations():
    agent_reach_pro = AgentReachPro()
    integration1 = Integration("Test Integration 1", {"key": "value"})
    integration2 = Integration("Test Integration 2", {"key": "value"})
    agent_reach_pro.add_integration(integration1)
    agent_reach_pro.add_integration(integration2)
    assert len(agent_reach_pro.get_integrations()) == 2

def test_configure_integration():
    agent_reach_pro = AgentReachPro()
    integration = Integration("Test Integration", {"key": "value"})
    agent_reach_pro.add_integration(integration)
    agent_reach_pro.configure_integration("Test Integration", {"new_key": "new_value"})
    assert agent_reach_pro.get_integrations()[0].config == {"new_key": "new_value"}

def test_test_integration():
    agent_reach_pro = AgentReachPro()
    integration = Integration("Test Integration", {"key": "value"})
    agent_reach_pro.add_integration(integration)
    assert agent_reach_pro.test_integration("Test Integration") is True

def test_to_json():
    agent_reach_pro = AgentReachPro()
    integration = Integration("Test Integration", {"key": "value"})
    agent_reach_pro.add_integration(integration)
    json_str = agent_reach_pro.to_json()
    assert json_str == '[{"name": "Test Integration", "config": {"key": "value"}}]'

def test_from_json():
    json_str = '[{"name": "Test Integration", "config": {"key": "value"}}]'
    agent_reach_pro = AgentReachPro.from_json(json_str)
    assert len(agent_reach_pro.get_integrations()) == 1

def test_edge_case_add_integration():
    agent_reach_pro = AgentReachPro()
    integration = Integration("", {"key": "value"})
    agent_reach_pro.add_integration(integration)
    assert len(agent_reach_pro.get_integrations()) == 1

def test_edge_case_configure_integration():
    agent_reach_pro = AgentReachPro()
    integration = Integration("Test Integration", {"key": "value"})
    agent_reach_pro.add_integration(integration)
    try:
        agent_reach_pro.configure_integration("", {"new_key": "new_value"})
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == "Integration name cannot be empty"
