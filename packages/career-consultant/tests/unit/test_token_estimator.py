"""Unit tests for token_estimator.py."""

import pytest
from unittest.mock import mock_open, patch
import token_estimator

class TestEstimateTokens:
    """Tests for estimate_tokens function."""

    def test_empty_text(self):
        """Test empty text returns 0."""
        assert token_estimator.estimate_tokens("") == 0
        assert token_estimator.estimate_tokens(None) == 0

    def test_basic_estimation(self):
        """Test basic token estimation."""
        text = "Hello world"
        # 11 chars / 4 = 2 tokens
        assert token_estimator.estimate_tokens(text) == 2

    def test_special_chars(self):
        """Test special characters add to token count."""
        text = "{Hello}"
        # 7 chars / 4 = 1 token + 2 special chars = 3
        assert token_estimator.estimate_tokens(text) == 3

    def test_whitespace_normalization(self):
        """Test whitespace is normalized."""
        text = "Hello    world"
        # Should be treated as "Hello world" (11 chars) -> 2 tokens
        assert token_estimator.estimate_tokens(text) == 2


class TestEstimateFileTokens:
    """Tests for estimate_file_tokens function."""

    def test_valid_file(self):
        """Test estimating tokens from file."""
        content = "Hello world"
        with patch("builtins.open", mock_open(read_data=content)):
            assert token_estimator.estimate_file_tokens("test.txt") == 2

    def test_file_error(self):
        """Test error handling when reading file."""
        with patch("builtins.open", side_effect=FileNotFoundError):
            assert token_estimator.estimate_file_tokens("nonexistent.txt") == 0


class TestEstimateModuleTokens:
    """Tests for estimate_module_tokens function."""

    def test_multiple_modules(self):
        """Test estimating tokens for multiple modules."""
        modules = {
            "mod1": "Hello",
            "mod2": "World"
        }
        counts = token_estimator.estimate_module_tokens(modules)
        assert counts["mod1"] == 1
        assert counts["mod2"] == 1


class TestCheckTokenBudget:
    """Tests for check_token_budget function."""

    def test_budget_ok(self):
        """Test OK status."""
        result = token_estimator.check_token_budget(1000, 10000)
        assert result['status'] == 'OK'
        assert result['percentage_used'] == 10.0

    def test_budget_warning(self):
        """Test WARNING status."""
        result = token_estimator.check_token_budget(6500, 10000)
        assert result['status'] == 'WARNING'

    def test_budget_critical(self):
        """Test CRITICAL status."""
        result = token_estimator.check_token_budget(8500, 10000)
        assert result['status'] == 'CRITICAL'


class TestEstimatePhaseTokens:
    """Tests for estimate_phase_tokens function."""

    def test_known_phases(self):
        """Test known phases return correct values."""
        assert token_estimator.estimate_phase_tokens('init') == 5000
        assert token_estimator.estimate_phase_tokens('research') == 15000

    def test_unknown_phase(self):
        """Test unknown phase returns default."""
        assert token_estimator.estimate_phase_tokens('unknown') == 10000


class TestCanFitInBudget:
    """Tests for can_fit_in_budget function."""

    def test_fits(self):
        """Test when content fits."""
        # 1000 + 1000 <= 10000 - 1000
        assert token_estimator.can_fit_in_budget(1000, 1000, 10000, 1000) is True

    def test_does_not_fit(self):
        """Test when content does not fit."""
        # 8500 + 1000 > 10000 - 1000
        assert token_estimator.can_fit_in_budget(8500, 1000, 10000, 1000) is False


class TestFormatTokenReport:
    """Tests for format_token_report function."""

    def test_format_report(self):
        """Test report formatting."""
        data = {
            'used': 1000,
            'remaining': 9000,
            'percentage_used': 10.0,
            'status': 'OK',
            'recommendation': 'Good'
        }
        report = token_estimator.format_token_report(data)
        assert "Used: 1,000 tokens" in report
        assert "Status: ✅ OK" in report


class TestEstimateTotalWorkflowTokens:
    """Tests for estimate_total_workflow_tokens function."""

    def test_workflow_existing_company(self):
        """Test workflow estimation for existing company."""
        result = token_estimator.estimate_total_workflow_tokens(cv_count=2, is_new_company=False)
        # init(5000) + cvs(4000) + modules(8000) + analysis(5000) + excel(2000) = 24000
        assert result['total'] == 24000
        assert 'research' not in result['breakdown']

    def test_workflow_new_company(self):
        """Test workflow estimation for new company."""
        result = token_estimator.estimate_total_workflow_tokens(cv_count=2, is_new_company=True)
        # 24000 + research(15000) = 39000
        assert result['total'] == 39000
        assert result['breakdown']['research'] == 15000
