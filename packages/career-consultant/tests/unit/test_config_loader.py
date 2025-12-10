"""Unit tests for config_loader.py."""

from unittest.mock import mock_open, patch

import config_loader
import pytest
import yaml


class TestLoadUserConfig:
    """Tests for load_user_config function."""

    def test_load_valid_config(self, sample_config):
        """Test loading a valid configuration file."""
        yaml_content = yaml.dump(sample_config)
        
        with patch("builtins.open", mock_open(read_data=yaml_content)):
            config = config_loader.load_user_config("/fake/path")
            assert config == sample_config

    def test_config_file_not_found(self):
        """Test error when config file doesn't exist."""
        with patch("builtins.open", side_effect=FileNotFoundError):
            with pytest.raises(FileNotFoundError, match="User config not found"):
                config_loader.load_user_config("/fake/path")

    def test_invalid_yaml_content(self):
        """Test error when config file contains invalid YAML."""
        with patch("builtins.open", mock_open(read_data="invalid: [yaml")):
            with pytest.raises(ValueError, match="Invalid YAML"):
                config_loader.load_user_config("/fake/path")

    def test_missing_required_fields(self, sample_config):
        """Test error when required fields are missing."""
        del sample_config['cv_variants']
        yaml_content = yaml.dump(sample_config)
        
        with patch("builtins.open", mock_open(read_data=yaml_content)):
            with pytest.raises(ValueError, match="Missing required config field"):
                config_loader.load_user_config("/fake/path")


class TestGetHelpers:
    """Tests for helper getter functions."""

    def test_get_cv_variants(self, sample_config):
        """Test extracting CV variants."""
        variants = config_loader.get_cv_variants(sample_config)
        assert len(variants) == 3
        assert variants[0]['id'] == 'EM'

    def test_get_cv_variants_disabled(self, sample_config):
        """Test error when CV variants are disabled."""
        sample_config['cv_variants']['enabled'] = False
        with pytest.raises(ValueError, match="CV variants not enabled"):
            config_loader.get_cv_variants(sample_config)

    def test_get_cv_variants_empty(self, sample_config):
        """Test error when variants list is empty."""
        sample_config['cv_variants']['variants'] = []
        with pytest.raises(ValueError, match="No CV variants defined"):
            config_loader.get_cv_variants(sample_config)

    def test_get_scoring_weights(self, sample_config):
        """Test extracting scoring weights."""
        weights = config_loader.get_scoring_weights(sample_config)
        assert weights['match'] == 35
        assert sum(weights.values()) == 100

    def test_get_scoring_weights_invalid_sum(self, sample_config, capsys):
        """Test warning when weights don't sum to 100."""
        sample_config['scoring']['weights']['match'] = 10
        config_loader.get_scoring_weights(sample_config)
        captured = capsys.readouterr()
        assert "Warning: Scoring weights sum to" in captured.out

    def test_get_scoring_thresholds(self, sample_config):
        """Test extracting scoring thresholds."""
        thresholds = config_loader.get_scoring_thresholds(sample_config)
        assert thresholds['first_priority'] == 70

    def test_get_scoring_bonuses(self, sample_config):
        """Test extracting scoring bonuses."""
        bonuses = config_loader.get_scoring_bonuses(sample_config)
        assert bonuses['tech_giant_experience'] == 5

    def test_get_preferences(self, sample_config):
        """Test extracting preferences."""
        prefs = config_loader.get_preferences(sample_config)
        assert prefs['min_salary_annual_ils'] == 450000

    def test_get_paths(self, sample_config):
        """Test extracting paths."""
        paths = config_loader.get_paths(sample_config)
        assert paths['cv_base'] == 'config/cv-variants'


class TestValidateConfig:
    """Tests for validate_config function."""

    def test_valid_config(self, sample_config):
        """Test validation of a correct configuration."""
        assert config_loader.validate_config(sample_config) is True

    def test_missing_cv_variants_config(self, sample_config):
        """Test validation failure when CV variants config is missing."""
        sample_config['cv_variants']['enabled'] = False
        with pytest.raises(ValueError, match="CV variants not enabled"):
            config_loader.validate_config(sample_config)

    def test_invalid_variant_structure(self, sample_config):
        """Test validation failure when variant is missing fields."""
        del sample_config['cv_variants']['variants'][0]['id']
        with pytest.raises(ValueError, match="CV variant missing field"):
            config_loader.validate_config(sample_config)

    def test_missing_scoring_weight(self, sample_config):
        """Test validation failure when a scoring weight is missing."""
        del sample_config['scoring']['weights']['match']
        with pytest.raises(ValueError, match="Missing scoring weight"):
            config_loader.validate_config(sample_config)

    def test_missing_threshold(self, sample_config):
        """Test validation failure when a threshold is missing."""
        del sample_config['scoring']['thresholds']['first_priority']
        with pytest.raises(ValueError, match="Missing threshold"):
            config_loader.validate_config(sample_config)
