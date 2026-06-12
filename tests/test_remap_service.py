import pytest
from unittest.mock import MagicMock
from tuxkeystoys.core.remap_service import RemapService

@pytest.fixture
def mock_system_handler():
    return MagicMock()

@pytest.fixture
def remap_service(mock_system_handler):
    return RemapService(mock_system_handler)

def test_get_existing_rules(remap_service, mock_system_handler):
    expected_rules = [("a", "b"), ("c", "d")]
    mock_system_handler.read_existing_rules.return_value = expected_rules
    
    rules = remap_service.get_existing_rules()
    
    assert rules == expected_rules
    mock_system_handler.read_existing_rules.assert_called_once()

def test_apply_remap_with_rules(remap_service, mock_system_handler):
    rules = [("a", "b"), ("c", "")]
    
    active = remap_service.apply_remap(rules)
    
    assert active == 1
    mock_system_handler.write_config.assert_called_once()
    mock_system_handler.reload_keyd.assert_called_once()
    
    args, _ = mock_system_handler.write_config.call_args
    config_content = args[0]
    assert "a = b" in config_content
    assert "c =" not in config_content

def test_apply_remap_no_active_rules(remap_service, mock_system_handler):
    rules = [("", "b"), ("c", "")]
    
    active = remap_service.apply_remap(rules)
    
    assert active == 0
    mock_system_handler.write_config.assert_called_once()
    mock_system_handler.reload_keyd.assert_called_once()
    
    args, _ = mock_system_handler.write_config.call_args
    config_content = args[0]
    assert "# No hay reglas activas" in config_content
