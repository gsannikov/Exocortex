import pytest
import shutil
import tempfile
from pathlib import Path
import os
import sys

# Add repo root to path
REPO_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

@pytest.fixture(scope="function")
def integration_data_dir():
    """Create a temporary directory for integration tests acting as exocortex-data."""
    temp_dir = tempfile.mkdtemp(prefix="exo-integration-")
    exocortex_data = Path(temp_dir)
    
    # Create structure
    (exocortex_data / "career" / "analyses").mkdir(parents=True)
    
    yield exocortex_data
    
    shutil.rmtree(temp_dir)
