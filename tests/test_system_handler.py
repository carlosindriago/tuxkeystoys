from unittest.mock import patch, mock_open
from tuxkeystoys.infrastructure.system_handler import SystemHandler

def test_read_existing_rules_file_not_found():
    handler = SystemHandler("/non/existent/path.conf")
    assert handler.read_existing_rules() == []

@patch("os.path.exists", return_value=True)
def test_read_existing_rules_valid_file(mock_exists):
    config_data = """
[ids]
0001:0001

[main]
a = b
c = d
# comment = e
f = g
"""
    handler = SystemHandler("/fake/path.conf")
    with patch("builtins.open", mock_open(read_data=config_data)):
        rules = handler.read_existing_rules()
    
    assert rules == [("a", "b"), ("c", "d"), ("f", "g")]

@patch("subprocess.run")
def test_write_config(mock_run):
    handler = SystemHandler("/fake/path.conf")
    with patch("builtins.open", mock_open()) as mocked_file:
        handler.write_config("test content")
        
    mocked_file.assert_called_once_with("/tmp/laptop_remap.conf", "w")
    mocked_file().write.assert_called_once_with("test content")
    mock_run.assert_called_once()
    assert "sudo" in mock_run.call_args[0][0]
    assert "mv" in mock_run.call_args[0][0]

@patch("subprocess.run")
def test_reload_keyd(mock_run):
    handler = SystemHandler()
    handler.reload_keyd()
    mock_run.assert_called_once_with(["sudo", "keyd", "reload"], check=True)
