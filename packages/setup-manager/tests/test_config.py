"""
Test script for MCP Configuration Manager.
Verifies path detection and config updates.
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add package root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from setup_manager.config_manager import add_mcp_server, get_config_path


def test_path_detection():
    print("\nTesting Path Detection...")
    
    # Test Mac
    with patch("setup_manager.config_manager.platform.system", return_value="Darwin"):
        path = get_config_path()
        print(f"Mac Path: {path}")
        assert "Library" in str(path) and "Application Support" in str(path)
        
    # Test Windows
    with patch("setup_manager.config_manager.platform.system", return_value="Windows"):
        # Patch os.environ.get specifically for the module or just os.environ
        with patch("setup_manager.config_manager.os.environ.get", return_value="C:\\Users\\Test\\AppData\\Roaming"):
            path = get_config_path()
            print(f"Windows Path: {path}")
            # On non-Windows systems, Path will be PosixPath, so backslashes might be preserved as characters
            # or treated as separators depending on implementation. 
            # We just check that the path string contains the expected parts.
            path_str = str(path)
            assert "AppData" in path_str and "Roaming" in path_str and "Claude" in path_str
            
    print("✅ Path detection passed.")

def test_config_update():
    print("\nTesting Config Update...")
    
    # Mock reading config
    mock_config = {
        "mcpServers": {
            "existing-server": {
                "command": "echo",
                "args": ["hello"]
            }
        }
    }
    
    with patch("setup_manager.config_manager.read_config", return_value=mock_config):
        with patch("setup_manager.config_manager.get_config_path", return_value=Path("/tmp/claude_config.json")):
            
            # Test Preview (Diff)
            print("Testing Preview Mode...")
            success, msg = add_mcp_server(
                name="new-server",
                command="uv",
                args=["run", "server.py"],
                preview_only=True
            )
            print(f"Preview Result: {msg}")
            assert success
            assert "Proposed changes" in msg
            assert "+    \"new-server\": {" in msg
            
            # Test Apply (Write)
            print("\nTesting Apply Mode...")
            with patch("builtins.open", MagicMock()) as mock_open:
                with patch("json.dump") as mock_dump:
                    success, msg = add_mcp_server(
                        name="new-server",
                        command="uv",
                        args=["run", "server.py"],
                        preview_only=False
                    )
                    print(f"Apply Result: {msg}")
                    assert success
                    assert "Successfully updated" in msg
                    mock_dump.assert_called_once()
                    
    print("✅ Config update passed.")

if __name__ == "__main__":
    test_path_detection()
    test_config_update()
