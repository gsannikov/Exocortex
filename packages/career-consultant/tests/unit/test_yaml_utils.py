"""
Comprehensive tests for yaml_utils.py - HIGH PRIORITY

This module tests YAML frontmatter handling which is critical for data integrity.
"""

import pytest
import tempfile
from pathlib import Path

import yaml_utils


class TestCreateYAMLDocument:
    """Test YAML document creation."""

    def test_basic_document_creation(self):
        """Test creating a document with simple frontmatter."""
        frontmatter = {'title': 'Test', 'date': '2025-01-01'}
        content = '# Test Content'

        doc = yaml_utils.create_yaml_document(frontmatter, content)

        assert doc.startswith('---\n')
        assert 'title: Test' in doc
        assert 'date:' in doc and '2025-01-01' in doc
        assert '# Test Content' in doc
        assert doc.count('---') == 2

    def test_empty_frontmatter(self):
        """Test creating document with empty frontmatter."""
        frontmatter = {}
        content = '# Content Only'

        doc = yaml_utils.create_yaml_document(frontmatter, content)

        assert doc.startswith('---\n')
        assert '# Content Only' in doc

    def test_nested_structures(self):
        """Test nested dictionaries and lists in frontmatter."""
        frontmatter = {
            'company': 'Test Corp',
            'scores': {'match': 35, 'income': 25},
            'tags': ['python', 'aws', 'kubernetes'],
            'metadata': {
                'tier': 1,
                'validated': True
            }
        }
        content = '# Company Profile'

        doc = yaml_utils.create_yaml_document(frontmatter, content)

        # Re-parse to verify structure
        parsed, _ = yaml_utils.parse_yaml_frontmatter(doc)

        assert parsed['scores']['match'] == 35
        assert 'python' in parsed['tags']
        assert parsed['metadata']['tier'] == 1

    def test_unicode_in_frontmatter(self):
        """Test handling of Unicode characters."""
        frontmatter = {
            'company': 'גוגל ישראל',
            'location': 'תל אביב',
            'notes': 'Company in Tel Aviv 🚀'
        }
        content = '# Hebrew Company'

        doc = yaml_utils.create_yaml_document(frontmatter, content)

        assert 'גוגל ישראל' in doc
        parsed, _ = yaml_utils.parse_yaml_frontmatter(doc)
        assert parsed['company'] == 'גוגל ישראל'

    def test_special_yaml_characters(self):
        """Test handling of special YAML characters that need quoting."""
        frontmatter = {
            'title': 'Company: Test',
            'description': 'Role @ Company (2024)',
            'note': 'Value with "quotes" and \'apostrophes\''
        }
        content = '# Content'

        doc = yaml_utils.create_yaml_document(frontmatter, content)

        # Should handle special characters properly
        parsed, _ = yaml_utils.parse_yaml_frontmatter(doc)
        assert parsed['title'] == 'Company: Test'
        assert parsed['description'] == 'Role @ Company (2024)'

    def test_multiline_content(self):
        """Test document with multi-line markdown content."""
        frontmatter = {'title': 'Test'}
        content = """# Heading 1

## Heading 2

Paragraph with multiple lines.

- List item 1
- List item 2

```python
code block
```
"""
        doc = yaml_utils.create_yaml_document(frontmatter, content)

        _, parsed_content = yaml_utils.parse_yaml_frontmatter(doc)
        assert '# Heading 1' in parsed_content
        assert 'code block' in parsed_content

    def test_boolean_and_null_values(self):
        """Test YAML boolean and null values."""
        frontmatter = {
            'published': True,
            'draft': False,
            'archived': None,
            'count': 0
        }
        content = '# Content'

        doc = yaml_utils.create_yaml_document(frontmatter, content)

        parsed, _ = yaml_utils.parse_yaml_frontmatter(doc)
        assert parsed['published'] is True
        assert parsed['draft'] is False
        assert parsed['archived'] is None
        assert parsed['count'] == 0


class TestParseYAMLFrontmatter:
    """Test YAML frontmatter parsing."""

    def test_valid_frontmatter(self):
        """Test parsing valid YAML frontmatter."""
        doc = """---
title: Test Document
date: 2025-01-01
score: 85
---

# Content Starts Here
"""
        frontmatter, content = yaml_utils.parse_yaml_frontmatter(doc)

        assert frontmatter['title'] == 'Test Document'
        import datetime
        assert frontmatter['date'] == datetime.date(2025, 1, 1)
        assert frontmatter['score'] == 85
        assert '# Content Starts Here' in content

    def test_missing_frontmatter(self):
        """Test documents without frontmatter."""
        doc = "# Just Regular Markdown\n\nNo frontmatter here."

        frontmatter, content = yaml_utils.parse_yaml_frontmatter(doc)

        assert frontmatter == {}
        assert content == doc

    def test_empty_frontmatter(self):
        """Test document with empty frontmatter section."""
        doc = "---\n---\n\n# Content"

        frontmatter, content = yaml_utils.parse_yaml_frontmatter(doc)

        assert frontmatter == {}
        assert '# Content' in content

    def test_malformed_yaml(self):
        """Test handling of malformed YAML (should not crash)."""
        doc = """---
invalid: yaml: structure: here:
  bad indentation
missing: quote '
---

# Content
"""
        frontmatter, content = yaml_utils.parse_yaml_frontmatter(doc)

        # Should handle gracefully and return empty dict
        assert isinstance(frontmatter, dict)
        assert '# Content' in content

    def test_yaml_with_three_dashes_in_content(self):
        """Test that --- in content doesn't confuse parser."""
        doc = """---
title: Test
---

# Content

Some text here

---

More content after separator
"""
        frontmatter, content = yaml_utils.parse_yaml_frontmatter(doc)

        assert frontmatter['title'] == 'Test'
        # Content should include the --- separator
        assert '---' in content
        assert 'More content after separator' in content

    def test_complex_nested_structure(self, sample_role_frontmatter):
        """Test parsing complex nested YAML."""
        # Create document from fixture
        content = "# Role Analysis"
        doc = yaml_utils.create_yaml_document(sample_role_frontmatter, content)

        # Parse it back
        parsed, _ = yaml_utils.parse_yaml_frontmatter(doc)

        assert parsed['role_id'] == sample_role_frontmatter['role_id']
        assert parsed['cv_scores']['EM'] == sample_role_frontmatter['cv_scores']['EM']
        assert parsed['priority'] == sample_role_frontmatter['priority']

    def test_preserve_data_types(self):
        """Test that data types are preserved through create/parse cycle."""
        original = {
            'string': 'text',
            'integer': 42,
            'float': 3.14,
            'boolean': True,
            'null': None,
            'list': [1, 2, 3],
            'dict': {'key': 'value'}
        }
        content = '# Test'

        doc = yaml_utils.create_yaml_document(original, content)
        parsed, _ = yaml_utils.parse_yaml_frontmatter(doc)

        assert parsed['string'] == 'text'
        assert parsed['integer'] == 42
        assert abs(parsed['float'] - 3.14) < 0.001
        assert parsed['boolean'] is True
        assert parsed['null'] is None
        assert parsed['list'] == [1, 2, 3]
        assert parsed['dict']['key'] == 'value'


class TestGetYAMLField:
    """Test getting specific fields from frontmatter."""

    def test_get_existing_field(self):
        """Test retrieving an existing field."""
        doc = "---\ntitle: Test\nscore: 85\n---\n\n# Content"

        title = yaml_utils.get_yaml_field(doc, 'title')
        score = yaml_utils.get_yaml_field(doc, 'score')

        assert title == 'Test'
        assert score == 85

    def test_get_nonexistent_field(self):
        """Test retrieving a field that doesn't exist."""
        doc = "---\ntitle: Test\n---\n\n# Content"

        result = yaml_utils.get_yaml_field(doc, 'nonexistent')

        assert result is None

    def test_get_nested_field(self):
        """Test getting nested field values."""
        doc = """---
metadata:
  tier: 1
  score: 85
---

# Content
"""
        # Note: get_yaml_field doesn't support nested access directly
        # We need to get the parent dict first
        metadata = yaml_utils.get_yaml_field(doc, 'metadata')

        assert metadata is not None
        assert metadata['tier'] == 1
        assert metadata['score'] == 85


class TestUpdateYAMLField:
    """Test updating fields in frontmatter."""

    def test_update_existing_field(self):
        """Test updating an existing field value."""
        doc = "---\ntitle: Old Title\nscore: 50\n---\n\n# Content"

        updated = yaml_utils.update_yaml_field(doc, 'title', 'New Title')

        title = yaml_utils.get_yaml_field(updated, 'title')
        assert title == 'New Title'

        # Content should be preserved
        assert '# Content' in updated

    def test_add_new_field(self):
        """Test adding a new field to frontmatter."""
        doc = "---\ntitle: Test\n---\n\n# Content"

        updated = yaml_utils.update_yaml_field(doc, 'new_field', 'new value')

        new_value = yaml_utils.get_yaml_field(updated, 'new_field')
        assert new_value == 'new value'

        # Old field should still exist
        title = yaml_utils.get_yaml_field(updated, 'title')
        assert title == 'Test'

    def test_update_preserves_other_fields(self):
        """Test that updating one field doesn't affect others."""
        doc = """---
field1: value1
field2: value2
field3: value3
---

# Content
"""
        updated = yaml_utils.update_yaml_field(doc, 'field2', 'new_value2')

        frontmatter, _ = yaml_utils.parse_yaml_frontmatter(updated)

        assert frontmatter['field1'] == 'value1'
        assert frontmatter['field2'] == 'new_value2'
        assert frontmatter['field3'] == 'value3'

    def test_update_with_complex_value(self):
        """Test updating field with complex value (dict, list)."""
        doc = "---\ntitle: Test\n---\n\n# Content"

        updated = yaml_utils.update_yaml_field(doc, 'scores', {'match': 35, 'income': 25})

        scores = yaml_utils.get_yaml_field(updated, 'scores')
        assert scores['match'] == 35
        assert scores['income'] == 25


class TestMergeYAMLFrontmatter:
    """Test merging updates into frontmatter."""

    def test_merge_multiple_fields(self):
        """Test merging multiple field updates at once."""
        doc = """---
field1: old1
field2: old2
---

# Content
"""
        updates = {
            'field2': 'new2',
            'field3': 'added3',
            'field4': 'added4'
        }

        merged = yaml_utils.merge_yaml_frontmatter(doc, updates)

        frontmatter, _ = yaml_utils.parse_yaml_frontmatter(merged)

        assert frontmatter['field1'] == 'old1'  # Unchanged
        assert frontmatter['field2'] == 'new2'  # Updated
        assert frontmatter['field3'] == 'added3'  # Added
        assert frontmatter['field4'] == 'added4'  # Added

    def test_merge_empty_updates(self):
        """Test merging empty updates (should not change document)."""
        original = "---\ntitle: Test\n---\n\n# Content"

        merged = yaml_utils.merge_yaml_frontmatter(original, {})

        assert merged.strip() == original.strip()

    def test_merge_overwrites_existing(self):
        """Test that merge overwrites existing values."""
        doc = "---\nscore: 50\n---\n\n# Content"

        merged = yaml_utils.merge_yaml_frontmatter(doc, {'score': 100})

        score = yaml_utils.get_yaml_field(merged, 'score')
        assert score == 100


class TestValidateYAMLFrontmatter:
    """Test frontmatter validation."""

    def test_validate_all_required_present(self):
        """Test validation passes when all required fields present."""
        doc = """---
field1: value1
field2: value2
field3: value3
---

# Content
"""
        required = ['field1', 'field2', 'field3']

        # Should not raise
        result = yaml_utils.validate_yaml_frontmatter(doc, required)
        assert result is True

    def test_validate_missing_required_field(self):
        """Test validation fails when required field missing."""
        doc = """---
field1: value1
field2: value2
---

# Content
"""
        required = ['field1', 'field2', 'field3']

        with pytest.raises(ValueError, match="Missing required fields: field3"):
            yaml_utils.validate_yaml_frontmatter(doc, required)

    def test_validate_multiple_missing_fields(self):
        """Test error message lists all missing fields."""
        doc = "---\nfield1: value1\n---\n\n# Content"
        required = ['field1', 'field2', 'field3', 'field4']

        with pytest.raises(ValueError) as exc_info:
            yaml_utils.validate_yaml_frontmatter(doc, required)

        error_message = str(exc_info.value)
        assert 'field2' in error_message
        assert 'field3' in error_message
        assert 'field4' in error_message

    def test_validate_empty_required_list(self):
        """Test validation with no required fields."""
        doc = "---\nfield: value\n---\n\n# Content"

        result = yaml_utils.validate_yaml_frontmatter(doc, [])
        assert result is True

    def test_validate_no_frontmatter(self):
        """Test validation fails when document has no frontmatter."""
        doc = "# Just content, no frontmatter"
        required = ['field1']

        with pytest.raises(ValueError):
            yaml_utils.validate_yaml_frontmatter(doc, required)


class TestYAMLFileOperations:
    """Test file-based YAML operations."""

    def test_yaml_to_dict(self, tmp_path):
        """Test loading YAML file to dictionary."""
        yaml_file = tmp_path / "test.yaml"
        yaml_content = """
title: Test
score: 85
items:
  - item1
  - item2
"""
        yaml_file.write_text(yaml_content)

        data = yaml_utils.yaml_to_dict(str(yaml_file))

        assert data['title'] == 'Test'
        assert data['score'] == 85
        assert data['items'] == ['item1', 'item2']

    def test_dict_to_yaml(self, tmp_path):
        """Test saving dictionary to YAML file."""
        data = {
            'title': 'Test Document',
            'score': 85,
            'tags': ['python', 'testing']
        }

        yaml_file = tmp_path / "output.yaml"
        yaml_utils.dict_to_yaml(data, str(yaml_file))

        # Verify file was created
        assert yaml_file.exists()

        # Reload and verify
        loaded = yaml_utils.yaml_to_dict(str(yaml_file))
        assert loaded['title'] == 'Test Document'
        assert loaded['score'] == 85
        assert loaded['tags'] == ['python', 'testing']

    def test_round_trip_yaml_file(self, tmp_path, sample_company_frontmatter):
        """Test saving and loading preserves data."""
        yaml_file = tmp_path / "company.yaml"

        # Save
        yaml_utils.dict_to_yaml(sample_company_frontmatter, str(yaml_file))

        # Load
        loaded = yaml_utils.yaml_to_dict(str(yaml_file))

        # Verify
        assert loaded['company_id'] == sample_company_frontmatter['company_id']
        assert loaded['tier'] == sample_company_frontmatter['tier']
        assert loaded['key_products'] == sample_company_frontmatter['key_products']

    def test_yaml_file_unicode(self, tmp_path):
        """Test YAML files with Unicode content."""
        data = {
            'company': 'גוגל ישראל',
            'location': 'תל אביב',
            'emoji': '🚀'
        }

        yaml_file = tmp_path / "hebrew.yaml"
        yaml_utils.dict_to_yaml(data, str(yaml_file))

        loaded = yaml_utils.yaml_to_dict(str(yaml_file))
        assert loaded['company'] == 'גוגל ישראל'
        assert loaded['emoji'] == '🚀'


class TestEdgeCases:
    """Test edge cases and unusual scenarios."""

    def test_very_large_frontmatter(self):
        """Test handling of very large frontmatter (>1000 fields)."""
        large_frontmatter = {f'field{i}': f'value{i}' for i in range(1000)}
        content = '# Content'

        doc = yaml_utils.create_yaml_document(large_frontmatter, content)

        parsed, _ = yaml_utils.parse_yaml_frontmatter(doc)
        assert len(parsed) == 1000
        assert parsed['field500'] == 'value500'

    def test_deeply_nested_structure(self):
        """Test deeply nested YAML structures."""
        nested = {
            'level1': {
                'level2': {
                    'level3': {
                        'level4': {
                            'value': 'deep'
                        }
                    }
                }
            }
        }
        content = '# Content'

        doc = yaml_utils.create_yaml_document(nested, content)

        parsed, _ = yaml_utils.parse_yaml_frontmatter(doc)
        assert parsed['level1']['level2']['level3']['level4']['value'] == 'deep'

    def test_content_with_yaml_delimiters(self):
        """Test content that looks like YAML but isn't."""
        frontmatter = {'title': 'Test'}
        content = """# Content

Here's some content with YAML-like structure:

```yaml
---
fake: frontmatter
---
```

This should not confuse the parser.
"""
        doc = yaml_utils.create_yaml_document(frontmatter, content)

        parsed_fm, parsed_content = yaml_utils.parse_yaml_frontmatter(doc)

        assert parsed_fm['title'] == 'Test'
        assert 'fake: frontmatter' in parsed_content

    def test_empty_content(self):
        """Test document with frontmatter but no content."""
        frontmatter = {'title': 'Test'}
        content = ''

        doc = yaml_utils.create_yaml_document(frontmatter, content)

        parsed_fm, parsed_content = yaml_utils.parse_yaml_frontmatter(doc)

        assert parsed_fm['title'] == 'Test'
        assert parsed_content == ''

    def test_special_string_values(self):
        """Test YAML special string values that need quoting."""
        frontmatter = {
            'version': '1.0.0',
            'date': '2025-01-01',
            'time': '12:00:00',
            'boolean_string': 'yes',  # Could be interpreted as boolean
            'null_string': 'null',  # Could be interpreted as null
        }
        content = '# Test'

        doc = yaml_utils.create_yaml_document(frontmatter, content)

        parsed, _ = yaml_utils.parse_yaml_frontmatter(doc)

        # Strings should remain as strings
        assert isinstance(parsed['version'], str)
        assert isinstance(parsed['date'], str) or isinstance(parsed['date'], str)
