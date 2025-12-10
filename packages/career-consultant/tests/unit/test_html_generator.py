"""Unit tests for html_generator.py."""

from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import html_generator


class TestParseYAMLFrontmatter:
    """Tests for parse_yaml_frontmatter function."""

    def test_valid_frontmatter(self):
        """Test parsing valid frontmatter."""
        content = "---\ntitle: Test\n---\nBody content"
        frontmatter, body = html_generator.parse_yaml_frontmatter(content)
        assert frontmatter['title'] == 'Test'
        assert body == 'Body content'

    def test_no_frontmatter(self):
        """Test content without frontmatter."""
        content = "Just body content"
        frontmatter, body = html_generator.parse_yaml_frontmatter(content)
        assert frontmatter == {}
        assert body == content

    def test_malformed_yaml(self):
        """Test malformed YAML."""
        content = "---\n: invalid\n---\nBody"
        frontmatter, body = html_generator.parse_yaml_frontmatter(content)
        assert frontmatter == {}
        assert body == content


class TestLoadAllRoles:
    """Tests for load_all_roles function."""

    def test_load_roles(self):
        """Test loading roles from directory."""
        with patch('pathlib.Path.glob') as mock_glob:
            mock_file = MagicMock()
            mock_file.name = "role.md"
            mock_glob.return_value = [mock_file]
            
            content = "---\nrole_id: 1\ncompany_name: Test\n---\nBody"
            
            with patch('builtins.open', mock_open(read_data=content)):
                roles = html_generator.load_all_roles(Path('/test'))
                assert len(roles) == 1
                assert roles[0]['company_name'] == 'Test'

    def test_skip_invalid_roles(self):
        """Test skipping roles without valid frontmatter."""
        with patch('pathlib.Path.glob') as mock_glob:
            mock_file = MagicMock()
            mock_file.name = "invalid.md"
            mock_glob.return_value = [mock_file]
            
            content = "No frontmatter"
            
            with patch('builtins.open', mock_open(read_data=content)):
                roles = html_generator.load_all_roles(Path('/test'))
                assert len(roles) == 0


class TestCalculateStatistics:
    """Tests for calculate_statistics function."""

    def test_empty_roles(self):
        """Test stats with empty roles list."""
        stats = html_generator.calculate_statistics([])
        assert stats['total_jobs'] == 0
        assert stats['avg_score'] == 0

    def test_valid_stats(self):
        """Test stats calculation."""
        roles = [
            {'score_total': 80, 'priority': 'First'},
            {'score_total': 60, 'priority': 'Second'},
            {'score_total': 40, 'priority': 'Third'}
        ]
        stats = html_generator.calculate_statistics(roles)
        assert stats['total_jobs'] == 3
        assert stats['avg_score'] == 60.0
        assert stats['highest_score'] == 80.0
        assert stats['lowest_score'] == 40.0
        assert stats['median_score'] == 60.0
        assert stats['first_priority'] == 1


class TestGenerateHTMLDatabase:
    """Tests for generate_html_database function."""

    def test_generate_html(self):
        """Test HTML generation."""
        roles = [{'role_id': '1', 'company_name': 'Test', 'score_total': 80}]
        stats = {
            'total_jobs': 1, 
            'generated_date': '2025-01-01',
            'avg_score': 80,
            'highest_score': 80,
            'median_score': 80,
            'first_priority': 0,
            'second_priority': 0,
            'third_priority': 1
        }
        
        html = html_generator.generate_html_database(roles, stats)
        assert '<!DOCTYPE html>' in html
        assert 'Test' in roles[0]['company_name']
        assert '80' in str(roles[0]['score_total'])


class TestMain:
    """Tests for main function."""

    def test_main_success(self):
        """Test successful execution."""
        with patch('pathlib.Path.exists', return_value=True), \
             patch('html_generator.load_all_roles', return_value=[{'role_id': 1}]), \
             patch('html_generator.calculate_statistics', return_value={
                 'total_jobs': 1,
                 'avg_score': 80,
                 'highest_score': 80,
                 'first_priority': 0,
                 'generated_date': '2025-01-01'
             }), \
             patch('html_generator.generate_html_database', return_value='<html></html>'), \
             patch('builtins.open', mock_open()) as mock_file, \
             patch('pathlib.Path.mkdir'):
            
            html_generator.main()
            mock_file.assert_called()

    def test_main_no_roles_dir(self):
        """Test when roles directory missing."""
        with patch('pathlib.Path.exists', return_value=False):
            with patch('builtins.print') as mock_print:
                html_generator.main()
                assert any("Roles directory not found" in str(call) for call in mock_print.call_args_list)
