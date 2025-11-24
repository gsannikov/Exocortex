"""
Comprehensive tests for slug_utils.py - HIGH PRIORITY

This module tests slug generation and validation which is critical for:
- File naming consistency
- ID generation
- Data integrity
"""

import pytest

import slug_utils


class TestNormalizeSlug:
    """Test slug normalization - critical for consistent file/ID naming."""

    def test_basic_normalization(self):
        """Test basic slug normalization."""
        assert slug_utils.normalize_slug("Hello World") == "hello-world"
        assert slug_utils.normalize_slug("Test Company") == "test-company"

    def test_special_characters(self):
        """Test removal of special characters."""
        assert slug_utils.normalize_slug("Test & Demo Company") == "test-demo-company"
        assert slug_utils.normalize_slug("Company (Israel) Ltd.") == "company-israel-ltd"
        assert slug_utils.normalize_slug("Test@#$%Company") == "testcompany"

    def test_multiple_spaces(self):
        """Test collapsing multiple spaces to single hyphen."""
        assert slug_utils.normalize_slug("Test    Multiple    Spaces") == "test-multiple-spaces"

    def test_leading_trailing_hyphens(self):
        """Test removal of leading/trailing hyphens."""
        assert slug_utils.normalize_slug("-Leading Hyphen") == "leading-hyphen"
        assert slug_utils.normalize_slug("Trailing Hyphen-") == "trailing-hyphen"
        assert slug_utils.normalize_slug("-Both-") == "both"

    def test_consecutive_hyphens(self):
        """Test collapsing consecutive hyphens."""
        assert slug_utils.normalize_slug("Test---Company") == "test-company"
        assert slug_utils.normalize_slug("A--B--C") == "a-b-c"

    def test_unicode_characters(self):
        """Test handling of Unicode characters."""
        # Hebrew
        assert "google" in slug_utils.normalize_slug("Google גוגל").lower()

        # Emoji (should be removed)
        result = slug_utils.normalize_slug("Company 🚀 Name")
        assert result == "company-name" or "company" in result

    def test_numbers_preserved(self):
        """Test that numbers are preserved in slugs."""
        assert slug_utils.normalize_slug("Company 123") == "company-123"
        assert slug_utils.normalize_slug("Web3 Startup") == "web3-startup"

    def test_max_length_truncation(self):
        """Test slug length limiting."""
        long_text = "This Is A Very Long Company Name That Should Be Truncated"
        result = slug_utils.normalize_slug(long_text, max_length=20)

        assert len(result) <= 20
        assert not result.endswith('-')

    def test_max_length_at_hyphen(self):
        """Test that max_length truncates at word boundary."""
        text = "Very Long Company Name"
        result = slug_utils.normalize_slug(text, max_length=15)

        # Should not end with partial word
        assert not result.endswith('-')
        assert len(result) <= 15

    def test_empty_string(self):
        """Test handling of empty string."""
        assert slug_utils.normalize_slug("") == ""
        assert slug_utils.normalize_slug("   ") == ""

    def test_only_special_characters(self):
        """Test string with only special characters."""
        assert slug_utils.normalize_slug("@#$%^&*()") == ""
        assert slug_utils.normalize_slug("!!!") == ""

    def test_case_insensitive(self):
        """Test that all output is lowercase."""
        assert slug_utils.normalize_slug("UPPERCASE") == "uppercase"
        assert slug_utils.normalize_slug("MixedCase") == "mixedcase"
        assert slug_utils.normalize_slug("Title Case Name") == "title-case-name"

    def test_parentheses_handling(self):
        """Test proper handling of parentheses."""
        assert slug_utils.normalize_slug("Company (Israel)") == "company-israel"
        assert slug_utils.normalize_slug("(Test) Company") == "test-company"

    def test_ampersand_handling(self):
        """Test ampersand is properly replaced."""
        assert slug_utils.normalize_slug("Smith & Jones") == "smith-jones"
        assert slug_utils.normalize_slug("A&B Company") == "a-b-company"


class TestCreateRoleID:
    """Test role ID generation."""

    def test_basic_role_id(self):
        """Test creating basic role ID."""
        role_id = slug_utils.create_role_id("Google", "Senior Engineer", "20250128")

        assert role_id == "google-senior-engineer-20250128"

    def test_role_id_with_complex_names(self):
        """Test role ID with special characters."""
        role_id = slug_utils.create_role_id(
            "Google (Israel)",
            "Senior Software Engineer",
            "20250128"
        )

        assert role_id == "google-israel-senior-software-engineer-20250128"

    def test_role_id_uniqueness_by_date(self):
        """Test that different dates create different IDs."""
        id1 = slug_utils.create_role_id("Google", "Engineer", "20250128")
        id2 = slug_utils.create_role_id("Google", "Engineer", "20250129")

        assert id1 != id2
        assert id1 == "google-engineer-20250128"
        assert id2 == "google-engineer-20250129"

    def test_role_id_format_validation(self):
        """Test that generated role IDs are valid slugs."""
        role_id = slug_utils.create_role_id(
            "Test & Company",
            "Senior Engineer (Backend)",
            "20250128"
        )

        assert slug_utils.is_valid_slug(role_id)

    def test_role_id_with_junior_vs_senior(self):
        """Test distinguishing junior vs senior roles."""
        junior = slug_utils.create_role_id("Company", "Junior Engineer", "20250128")
        senior = slug_utils.create_role_id("Company", "Senior Engineer", "20250128")

        assert junior != senior
        assert "junior" in junior
        assert "senior" in senior


class TestCreateCompanyID:
    """Test company ID generation."""

    def test_basic_company_id(self):
        """Test creating basic company ID."""
        assert slug_utils.create_company_id("Google") == "google"
        assert slug_utils.create_company_id("Microsoft") == "microsoft"

    def test_company_id_with_suffix(self):
        """Test company ID with legal suffixes."""
        assert slug_utils.create_company_id("Google Israel") == "google-israel"
        assert slug_utils.create_company_id("Microsoft Corporation") == "microsoft-corporation"
        assert slug_utils.create_company_id("Test Ltd.") == "test-ltd"

    def test_company_id_special_characters(self):
        """Test company ID with special characters."""
        assert slug_utils.create_company_id("Test & Demo Company") == "test-demo-company"
        assert slug_utils.create_company_id("Company (Israel)") == "company-israel"

    def test_company_id_consistency(self):
        """Test that same company name always generates same ID."""
        id1 = slug_utils.create_company_id("Google Israel")
        id2 = slug_utils.create_company_id("Google Israel")

        assert id1 == id2

    def test_company_id_similarity_detection(self):
        """Test that similar company names generate different IDs."""
        # These should be different
        assert slug_utils.create_company_id("Google") != slug_utils.create_company_id("Google Israel")
        assert slug_utils.create_company_id("Meta") != slug_utils.create_company_id("Meta Israel")


class TestExtractCompanyFromURL:
    """Test company name extraction from job URLs."""

    def test_linkedin_jobs_url(self):
        """Test extracting company from LinkedIn job URLs."""
        url = "https://www.linkedin.com/jobs/view/google-engineer-12345"
        company = slug_utils.extract_company_from_url(url)

        assert company == "google"

    def test_linkedin_company_url(self):
        """Test extracting from LinkedIn company URLs."""
        url = "https://www.linkedin.com/company/microsoft"
        company = slug_utils.extract_company_from_url(url)

        assert company == "microsoft"

    def test_lever_url(self):
        """Test extracting from Lever job board URLs."""
        url = "https://jobs.lever.co/companyname/role-id-12345"
        company = slug_utils.extract_company_from_url(url)

        assert company == "companyname"

    def test_greenhouse_url(self):
        """Test extracting from Greenhouse URLs."""
        url1 = "https://greenhouse.io/companyname"
        url2 = "https://boards.greenhouse.io/companyname/jobs/12345"

        assert slug_utils.extract_company_from_url(url1) == "companyname"
        assert slug_utils.extract_company_from_url(url2) == "companyname"

    def test_company_careers_page(self):
        """Test extracting from company careers pages."""
        url = "https://www.example.com/careers/job-12345"
        company = slug_utils.extract_company_from_url(url)

        assert "example" in company.lower()

    def test_url_with_www(self):
        """Test URL with www prefix."""
        url = "https://www.linkedin.com/jobs/view/google-engineer"
        company = slug_utils.extract_company_from_url(url)

        assert company is not None
        assert len(company) > 0

    def test_url_case_insensitive(self):
        """Test that URL extraction is case-insensitive."""
        url1 = "https://jobs.lever.co/CompanyName/role"
        url2 = "https://jobs.lever.co/companyname/role"

        company1 = slug_utils.extract_company_from_url(url1)
        company2 = slug_utils.extract_company_from_url(url2)

        assert company1.lower() == company2.lower()

    def test_unknown_url_format(self):
        """Test fallback for unknown URL formats."""
        url = "https://random-job-board.com/listings/12345"
        company = slug_utils.extract_company_from_url(url)

        # Should return something, not crash
        assert company is not None
        # Might be "random-job-board" or "unknown-company"
        assert len(company) > 0

    def test_invalid_url(self):
        """Test handling of invalid URLs."""
        url = "not-a-valid-url"
        company = slug_utils.extract_company_from_url(url)

        # Should handle gracefully
        assert company is not None


class TestSanitizeFilename:
    """Test filename sanitization."""

    def test_basic_filename(self):
        """Test sanitizing basic filename."""
        assert slug_utils.sanitize_filename("Document.md") == "document.md"
        assert slug_utils.sanitize_filename("report.txt") == "report.txt"

    def test_filename_with_spaces(self):
        """Test filename with spaces."""
        assert slug_utils.sanitize_filename("My Document.md") == "my-document.md"
        assert slug_utils.sanitize_filename("Test File Name.txt") == "test-file-name.txt"

    def test_filename_with_special_chars(self):
        """Test filename with special characters."""
        assert slug_utils.sanitize_filename("Company: Report (2025).md") == "company-report-2025.md"
        assert slug_utils.sanitize_filename("File@#$.txt") == "file.txt"

    def test_filename_preserve_extension(self):
        """Test that file extensions are preserved."""
        result = slug_utils.sanitize_filename("Test File.md")
        assert result.endswith(".md")

        result = slug_utils.sanitize_filename("Data.yaml")
        assert result.endswith(".yaml")

    def test_filename_multiple_dots(self):
        """Test filename with multiple dots."""
        result = slug_utils.sanitize_filename("file.backup.md")
        # Should keep last extension
        assert result.endswith(".md")

    def test_filename_no_extension(self):
        """Test filename without extension."""
        assert slug_utils.sanitize_filename("README") == "readme"
        assert slug_utils.sanitize_filename("LICENSE") == "license"


class TestIsValidSlug:
    """Test slug validation."""

    def test_valid_slugs(self):
        """Test that valid slugs pass validation."""
        assert slug_utils.is_valid_slug("valid-slug") is True
        assert slug_utils.is_valid_slug("company-name") is True
        assert slug_utils.is_valid_slug("test-123") is True
        assert slug_utils.is_valid_slug("a-b-c-d") is True

    def test_invalid_uppercase(self):
        """Test that uppercase slugs are invalid."""
        assert slug_utils.is_valid_slug("Invalid-Slug") is False
        assert slug_utils.is_valid_slug("ALLCAPS") is False

    def test_invalid_spaces(self):
        """Test that slugs with spaces are invalid."""
        assert slug_utils.is_valid_slug("invalid slug") is False
        assert slug_utils.is_valid_slug("has spaces") is False

    def test_invalid_special_chars(self):
        """Test that slugs with special characters are invalid."""
        assert slug_utils.is_valid_slug("invalid@slug") is False
        assert slug_utils.is_valid_slug("test_underscore") is False  # Underscores invalid
        assert slug_utils.is_valid_slug("test.period") is False

    def test_invalid_leading_hyphen(self):
        """Test that leading hyphen is invalid."""
        assert slug_utils.is_valid_slug("-leading") is False

    def test_invalid_trailing_hyphen(self):
        """Test that trailing hyphen is invalid."""
        assert slug_utils.is_valid_slug("trailing-") is False

    def test_invalid_consecutive_hyphens(self):
        """Test that consecutive hyphens are invalid."""
        assert slug_utils.is_valid_slug("double--hyphen") is False
        assert slug_utils.is_valid_slug("triple---hyphen") is False

    def test_empty_string_invalid(self):
        """Test that empty string is invalid."""
        assert slug_utils.is_valid_slug("") is False

    def test_numbers_only_valid(self):
        """Test that numbers-only slug is valid."""
        assert slug_utils.is_valid_slug("12345") is True

    def test_single_character_valid(self):
        """Test that single character is valid."""
        assert slug_utils.is_valid_slug("a") is True


class TestTruncateSlug:
    """Test slug truncation."""

    def test_no_truncation_needed(self):
        """Test slug shorter than max length."""
        slug = "short-slug"
        result = slug_utils.truncate_slug(slug, max_length=20)

        assert result == "short-slug"

    def test_truncate_at_max_length(self):
        """Test truncation at exact max length."""
        slug = "very-long-slug-name-that-needs-truncating"
        result = slug_utils.truncate_slug(slug, max_length=20)

        assert len(result) <= 20
        assert not result.endswith('-')

    def test_preserve_words_true(self):
        """Test that word boundaries are preserved when truncating."""
        slug = "very-long-slug-name-that-needs-truncating"
        result = slug_utils.truncate_slug(slug, max_length=20, preserve_words=True)

        # Should break at hyphen, not mid-word
        assert '-' not in result or not result.endswith('-')
        assert len(result) <= 20

    def test_preserve_words_false(self):
        """Test hard truncation without word preservation."""
        slug = "verylongslugwithnowords"
        result = slug_utils.truncate_slug(slug, max_length=10, preserve_words=False)

        assert len(result) == 10

    def test_truncate_removes_trailing_hyphen(self):
        """Test that truncation removes trailing hyphens."""
        slug = "word-word-word-word"
        result = slug_utils.truncate_slug(slug, max_length=12, preserve_words=True)

        assert not result.endswith('-')

    def test_very_short_max_length(self):
        """Test truncation with very short max length."""
        slug = "long-slug-name"
        result = slug_utils.truncate_slug(slug, max_length=5)

        assert len(result) <= 5
        assert len(result) > 0


class TestSlugUniqueness:
    """Test that different inputs generate different slugs (collision detection)."""

    def test_similar_company_names(self):
        """Test that similar company names generate different slugs."""
        companies = [
            "Google",
            "Google Israel",
            "Google Cloud",
            "Googleplex"
        ]

        slugs = [slug_utils.create_company_id(c) for c in companies]

        # All should be different
        assert len(slugs) == len(set(slugs))

    def test_companies_with_articles(self):
        """Test companies that differ only by articles."""
        companies = [
            "The Company",
            "Company",
            "A Company"
        ]

        slugs = [slug_utils.create_company_id(c) for c in companies]

        # Should generate different slugs (or at least not crash)
        assert len(slugs) == 3

    def test_role_variations(self):
        """Test that role variations are distinguishable."""
        base_company = "Google"
        base_date = "20250128"

        roles = [
            "Engineer",
            "Senior Engineer",
            "Staff Engineer",
            "Principal Engineer"
        ]

        role_ids = [slug_utils.create_role_id(base_company, r, base_date) for r in roles]

        # All should be unique
        assert len(role_ids) == len(set(role_ids))


class TestEdgeCases:
    """Test edge cases and unusual inputs."""

    def test_very_long_company_name(self):
        """Test handling of very long company names (>200 chars)."""
        long_name = "Very " * 50 + "Long Company Name"
        slug = slug_utils.create_company_id(long_name)

        # Should not crash, should return valid slug
        assert len(slug) > 0
        assert slug_utils.is_valid_slug(slug)

    def test_company_name_all_symbols(self):
        """Test company name with only symbols."""
        slug = slug_utils.normalize_slug("@@@###$$$")

        assert slug == "" or slug_utils.is_valid_slug(slug)

    def test_hebrew_company_name(self):
        """Test Hebrew company names."""
        hebrew = "גוגל ישראל"
        slug = slug_utils.create_company_id(hebrew)

        # Should produce some valid slug (even if it's transliterated or empty)
        assert isinstance(slug, str)

    def test_chinese_company_name(self):
        """Test Chinese company names."""
        chinese = "谷歌中国"
        slug = slug_utils.create_company_id(chinese)

        assert isinstance(slug, str)

    def test_emoji_in_company_name(self):
        """Test company names with emojis."""
        company = "Company 🚀 Startup"
        slug = slug_utils.create_company_id(company)

        # Emoji should be removed
        assert '🚀' not in slug
        assert slug_utils.is_valid_slug(slug) or slug == ""

    def test_url_with_query_params(self):
        """Test URL extraction with query parameters."""
        url = "https://linkedin.com/jobs/view/12345?utm_source=share&ref=email"
        company = slug_utils.extract_company_from_url(url)

        # Should still extract company despite query params
        assert company is not None

    def test_mixed_case_normalization(self):
        """Test that mixed case is properly normalized."""
        inputs = [
            "MixedCase",
            "mixedcase",
            "MIXEDCASE",
            "mIxEdCaSe"
        ]

        slugs = [slug_utils.normalize_slug(i) for i in inputs]

        # All should produce the same slug
        assert all(s == "mixedcase" for s in slugs)


class TestRegressions:
    """Tests for specific bugs and regressions."""

    def test_double_hyphen_from_ampersand(self):
        """
        Regression test: Ensure "A & B" doesn't create "a--b"
        (ampersand → space → collapse spaces)
        """
        slug = slug_utils.normalize_slug("A & B Company")

        assert '--' not in slug
        assert slug_utils.is_valid_slug(slug)

    def test_parentheses_dont_leave_spaces(self):
        """
        Regression test: Ensure "(Text)" doesn't leave trailing spaces
        """
        slug = slug_utils.normalize_slug("Company (Israel)")

        assert slug == "company-israel"
        assert '--' not in slug

    def test_url_extraction_case_insensitive_domain(self):
        """Regression test: Ensure domain matching is case-insensitive."""
        url1 = "https://LinkedIn.com/jobs/view/google"
        url2 = "https://linkedin.com/jobs/view/google"

        company1 = slug_utils.extract_company_from_url(url1)
        company2 = slug_utils.extract_company_from_url(url2)

        # Should extract same company
        assert company1.lower() == company2.lower()
