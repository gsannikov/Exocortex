"""Unit tests for storage_utils.py."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
import storage_utils

class TestDetectStorageType:
    """Tests for detect_storage_type function."""

    def test_detect_google_drive(self):
        """Test detection when Google Drive path exists."""
        with patch("pathlib.Path.exists") as mock_exists:
            # First check (MyDrive) returns True
            mock_exists.side_effect = [True]
            assert storage_utils.detect_storage_type() == "google_drive"

    def test_detect_local(self):
        """Test detection when no Google Drive path exists."""
        with patch("pathlib.Path.exists") as mock_exists:
            # All checks return False
            mock_exists.return_value = False
            assert storage_utils.detect_storage_type() == "local"


class TestResolveBasePath:
    """Tests for resolve_base_path function."""

    def test_explicit_base_path(self):
        """Test when base_path is explicitly configured."""
        config = {'storage': {'base_path': '/custom/path'}}
        path = storage_utils.resolve_base_path(config)
        assert str(path) == '/custom/path'

    def test_auto_detect_google_drive(self):
        """Test auto-detection for Google Drive."""
        config = {
            'storage': {
                'type': 'google_drive',
                'base_path': 'auto',
                'google_drive': {'mount_point': '/Volumes/GoogleDrive'}
            }
        }
        path = storage_utils.resolve_base_path(config)
        assert str(path) == '/Volumes/GoogleDrive/career-consultant.skill'

    def test_auto_detect_local(self):
        """Test auto-detection for local storage."""
        config = {
            'storage': {
                'type': 'local',
                'base_path': 'auto',
                'local': {'base_dir': '/Users/test/Documents/career-consultant'}
            }
        }
        path = storage_utils.resolve_base_path(config)
        assert str(path) == '/Users/test/Documents/career-consultant'


class TestResolveStoragePaths:
    """Tests for resolve_storage_paths function."""

    def test_resolve_all_paths(self, sample_config):
        """Test that all required paths are resolved correctly."""
        # Mock base path resolution to return a fixed path
        with patch('storage_utils.resolve_base_path') as mock_resolve:
            base = Path('/test/base')
            mock_resolve.return_value = base
            
            paths = storage_utils.resolve_storage_paths(sample_config)
            
            assert paths['BASE_PATH'] == str(base)
            assert paths['USER_DATA_BASE'] == str(base / 'user-data')
            assert paths['CV_BASE'].endswith('config/cv-variants')
            assert paths['COMPANIES_DIR'].endswith('db/companies')


class TestVerifyStorage:
    """Tests for verify_storage function."""

    def test_verify_valid_storage(self, sample_config):
        """Test verification with valid structure."""
        with patch('storage_utils.resolve_base_path') as mock_resolve:
            base = Path('/test/base')
            mock_resolve.return_value = base
            
            # Mock existence of all checked paths
            with patch('pathlib.Path.exists') as mock_exists:
                mock_exists.return_value = True
                
                is_valid, msg = storage_utils.verify_storage(sample_config)
                assert is_valid is True
                assert "Storage verified" in msg

    def test_verify_missing_base_path(self, sample_config):
        """Test verification when base path doesn't exist."""
        with patch('storage_utils.resolve_base_path') as mock_resolve:
            base = Path('/test/base')
            mock_resolve.return_value = base
            
            with patch('pathlib.Path.exists') as mock_exists:
                mock_exists.return_value = False
                
                is_valid, msg = storage_utils.verify_storage(sample_config)
                assert is_valid is False
                assert "Base path does not exist" in msg

    def test_verify_google_drive_not_mounted(self, sample_config):
        """Test verification when Google Drive is not mounted."""
        sample_config['storage'] = {
            'type': 'google_drive',
            'google_drive': {'verify_mounted': True, 'mount_point': '/Volumes/Drive'}
        }
        
        with patch('storage_utils.resolve_base_path') as mock_resolve:
            base = Path('/Volumes/Drive/career-consultant.skill')
            mock_resolve.return_value = base
            
            # Mock base path exists but mount point doesn't
            def side_effect(*args, **kwargs):
                # When called on an instance, the instance is the first arg
                if args and str(args[0]) == '/Volumes/Drive':
                    return False
                return True
                
            with patch('pathlib.Path.exists', side_effect=side_effect, autospec=True):
                is_valid, msg = storage_utils.verify_storage(sample_config)
                assert is_valid is False
                assert "Google Drive not mounted" in msg

    def test_verify_missing_config(self, sample_config):
        """Test verification when settings.yaml is missing."""
        with patch('storage_utils.resolve_base_path') as mock_resolve:
            base = Path('/test/base')
            mock_resolve.return_value = base
            
            def mock_exists_side_effect(*args, **kwargs):
                if args and 'settings.yaml' in str(args[0]):
                    return False
                return True
            
            with patch('pathlib.Path.exists', side_effect=mock_exists_side_effect, autospec=True):
                is_valid, msg = storage_utils.verify_storage(sample_config)
                assert is_valid is False
                assert "Configuration file not found" in msg


class TestInitStorage:
    """Tests for init_storage function."""

    def test_init_storage_success(self, sample_config):
        """Test successful initialization."""
        with patch('storage_utils.resolve_base_path') as mock_resolve, \
             patch('storage_utils.verify_google_drive_mounted') as mock_mount, \
             patch('storage_utils.verify_storage') as mock_verify:
            
            mock_resolve.return_value = Path('/test/base')
            mock_mount.return_value = (True, Path('/Volumes/Drive'))
            mock_verify.return_value = (True, "Verified")
            
            with patch('pathlib.Path.exists', return_value=True):
                success, msg = storage_utils.init_storage(sample_config)
                assert success is True
                assert "initialized successfully" in msg


class TestVerifyGoogleDriveMounted:
    """Tests for verify_google_drive_mounted function."""

    def test_drive_mounted(self):
        """Test when Drive is mounted."""
        with patch('pathlib.Path.exists', return_value=True):
            is_mounted, path = storage_utils.verify_google_drive_mounted()
            assert is_mounted is True
            assert path is not None

    def test_drive_not_mounted(self):
        """Test when Drive is not mounted."""
        with patch('pathlib.Path.exists', return_value=False):
            is_mounted, path = storage_utils.verify_google_drive_mounted()
            assert is_mounted is False
            assert path is None


class TestGetStorageInfo:
    """Tests for get_storage_info function."""

    def test_get_info_local(self, sample_config):
        """Test getting info for local storage."""
        sample_config['storage'] = {'type': 'local'}
        
        with patch('storage_utils.resolve_base_path') as mock_resolve:
            base = Path('/test/base')
            mock_resolve.return_value = base
            
            with patch('pathlib.Path.exists', return_value=True):
                info = storage_utils.get_storage_info(sample_config)
                assert info['type'] == 'local'
                assert info['exists'] is True
                assert info['is_local'] is True

    def test_get_info_drive(self, sample_config):
        """Test getting info for Drive storage."""
        with patch('storage_utils.resolve_base_path') as mock_resolve, \
             patch('storage_utils.verify_google_drive_mounted') as mock_mount:
            
            base = Path('/test/base')
            mock_resolve.return_value = base
            mock_mount.return_value = (True, Path('/Volumes/Drive'))
            
            with patch('pathlib.Path.exists', return_value=True):
                info = storage_utils.get_storage_info(sample_config)
                assert info['type'] == 'google_drive'
                assert info['drive_mounted'] is True


class TestLoadConfigWithStorage:
    """Tests for load_config_with_storage function."""

    def test_load_explicit_path(self, sample_config):
        """Test loading from explicit path."""
        with patch('builtins.open', mock_open(read_data="storage: {type: local}")), \
             patch('yaml.safe_load', return_value=sample_config), \
             patch('storage_utils.resolve_storage_paths') as mock_resolve:
            
            mock_resolve.return_value = {'BASE_PATH': '/test'}
            
            config, paths = storage_utils.load_config_with_storage(Path('/test/config.yaml'))
            assert config == sample_config
            assert paths['BASE_PATH'] == '/test'

    def test_auto_detect_config(self, sample_config):
        """Test auto-detecting config file."""
        with patch('pathlib.Path.exists') as mock_exists, \
             patch('builtins.open', mock_open(read_data="storage: {type: local}")), \
             patch('yaml.safe_load', return_value=sample_config), \
             patch('storage_utils.resolve_storage_paths') as mock_resolve:
            
            # First path exists
            mock_exists.side_effect = [True]
            mock_resolve.return_value = {'BASE_PATH': '/test'}
            
            config, paths = storage_utils.load_config_with_storage()
            assert config == sample_config

    def test_config_not_found(self):
        """Test error when config not found."""
        with patch('pathlib.Path.exists', return_value=False):
            with pytest.raises(FileNotFoundError):
                storage_utils.load_config_with_storage()

