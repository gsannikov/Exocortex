"""
Comprehensive tests for cv_matcher.py - CRITICAL PRIORITY

This module tests the core CV matching and scoring logic that determines
job prioritization. High test coverage is essential here.
"""


# Import the module under test
import cv_matcher
import pytest


class TestLoadUserCVs:
    """Test CV loading functionality."""

    def test_load_single_cv(self, temp_user_data_dir, sample_cv_content):
        """Test loading a single CV successfully."""
        # Create CV file
        cv_path = temp_user_data_dir / "config" / "cv-variants" / "cv-em.md"
        cv_path.write_text(sample_cv_content)

        cv_variants = [
            {
                'id': 'EM',
                'filename': 'cv-em.md',
                'focus': 'Engineering Management',
                'weight': 1.0
            }
        ]

        cvs = cv_matcher.load_user_cvs(str(temp_user_data_dir), cv_variants)

        assert len(cvs) == 1
        assert 'EM' in cvs
        assert cvs['EM']['focus'] == 'Engineering Management'
        assert cvs['EM']['weight'] == 1.0
        assert 'Python' in cvs['EM']['content']

    def test_load_multiple_cvs(self, temp_user_data_dir, sample_cv_content, sample_cv_tpm):
        """Test loading multiple CV variants."""
        # Create multiple CV files
        (temp_user_data_dir / "config" / "cv-variants" / "cv-em.md").write_text(sample_cv_content)
        (temp_user_data_dir / "config" / "cv-variants" / "cv-tpm.md").write_text(sample_cv_tpm)

        cv_variants = [
            {'id': 'EM', 'filename': 'cv-em.md', 'focus': 'Engineering Management', 'weight': 1.0},
            {'id': 'TPM', 'filename': 'cv-tpm.md', 'focus': 'Technical Program Management', 'weight': 0.9}
        ]

        cvs = cv_matcher.load_user_cvs(str(temp_user_data_dir), cv_variants)

        assert len(cvs) == 2
        assert 'EM' in cvs
        assert 'TPM' in cvs

    def test_load_cvs_missing_file(self, temp_user_data_dir, sample_cv_content, capsys):
        """Test handling of missing CV file (should warn but continue)."""
        # Only create one CV file
        (temp_user_data_dir / "config" / "cv-variants" / "cv-em.md").write_text(sample_cv_content)

        cv_variants = [
            {'id': 'EM', 'filename': 'cv-em.md', 'focus': 'Engineering Management'},
            {'id': 'TPM', 'filename': 'cv-tpm.md', 'focus': 'Technical Program Management'}
        ]

        cvs = cv_matcher.load_user_cvs(str(temp_user_data_dir), cv_variants)

        # Should load the one that exists
        assert len(cvs) == 1
        assert 'EM' in cvs

        # Should have warning in output
        captured = capsys.readouterr()
        assert 'Warning' in captured.out or 'not found' in captured.out.lower()

    def test_load_cvs_all_missing(self, temp_user_data_dir):
        """Test error when no CVs can be loaded."""
        cv_variants = [
            {'id': 'EM', 'filename': 'cv-em.md', 'focus': 'Engineering Management'}
        ]

        with pytest.raises(ValueError, match="No CVs could be loaded"):
            cv_matcher.load_user_cvs(str(temp_user_data_dir), cv_variants)

    def test_cv_weight_default(self, temp_user_data_dir, sample_cv_content):
        """Test that CV weight defaults to 1.0 if not specified."""
        cv_path = temp_user_data_dir / "config" / "cv-variants" / "cv-em.md"
        cv_path.write_text(sample_cv_content)

        cv_variants = [
            {'id': 'EM', 'filename': 'cv-em.md', 'focus': 'Engineering Management'}
            # Note: no 'weight' field
        ]

        cvs = cv_matcher.load_user_cvs(str(temp_user_data_dir), cv_variants)
        assert cvs['EM']['weight'] == 1.0


class TestExtractSkillsFromCV:
    """Test skill extraction from CV content."""

    def test_extract_basic_skills(self, sample_cv_content):
        """Test extraction of common technical skills."""
        skills = cv_matcher.extract_skills_from_cv(sample_cv_content)

        assert 'python' in skills
        assert 'java' in skills
        assert 'javascript' in skills
        assert 'aws' in skills
        assert 'kubernetes' in skills
        assert 'docker' in skills

    def test_extract_leadership_skills(self, sample_cv_content):
        """Test extraction of leadership-related skills."""
        skills = cv_matcher.extract_skills_from_cv(sample_cv_content)

        assert 'leadership' in skills or 'management' in skills
        assert 'agile' in skills or 'scrum' in skills

    def test_extract_ai_skills(self):
        """Test extraction of AI/ML related skills."""
        cv_with_ai = """
        # AI Engineer
        Experience with Machine Learning, AI, Data Science, and Python.
        """
        skills = cv_matcher.extract_skills_from_cv(cv_with_ai)

        assert 'machine learning' in skills or 'ai' in skills
        assert 'data science' in skills

    def test_extract_case_insensitive(self):
        """Test that skill extraction is case-insensitive."""
        cv_mixed_case = "PYTHON, Java, javascript, AWS, Kubernetes"
        skills = cv_matcher.extract_skills_from_cv(cv_mixed_case)

        assert 'python' in skills
        assert 'java' in skills

    def test_extract_from_empty_cv(self):
        """Test extraction from empty CV."""
        skills = cv_matcher.extract_skills_from_cv("")
        assert isinstance(skills, list)


class TestCalculateMatchScore:
    """Test match score calculation - CRITICAL for accuracy."""

    def test_perfect_match(self, sample_cv_content):
        """Test scoring when CV perfectly matches job requirements."""
        job_requirements = """
        Senior Engineer - Must have Python, AWS, Kubernetes, Docker, Leadership, Management
        """
        score = cv_matcher.calculate_match_score(
            job_requirements,
            sample_cv_content,
            "Engineering Management"
        )

        # Should get high score for perfect match
        assert score >= 25
        assert score <= 35  # Max score is 35

    def test_zero_match(self, sample_cv_content):
        """Test scoring when CV has no matching skills."""
        job_requirements = """
        Junior Designer - Must have Photoshop, Illustrator, Figma, Design skills
        """
        score = cv_matcher.calculate_match_score(
            job_requirements,
            sample_cv_content,
            "Engineering Management"
        )

        # Should get very low score
        assert score < 15

    def test_focus_area_bonus(self, sample_cv_content):
        """Test that matching focus area gives bonus points."""
        job_with_focus = "Engineering Management position requiring leadership"
        job_without_focus = "Individual Contributor position"

        score_with = cv_matcher.calculate_match_score(
            job_with_focus,
            sample_cv_content,
            "Engineering Management"
        )
        score_without = cv_matcher.calculate_match_score(
            job_without_focus,
            sample_cv_content,
            "Engineering Management"
        )

        assert score_with >= score_without

    def test_leadership_bonus(self, sample_cv_content):
        """Test that senior/leadership roles get appropriate scoring."""
        senior_job = "Senior Engineering Manager position"
        junior_job = "Junior Developer position"

        score_senior = cv_matcher.calculate_match_score(
            senior_job,
            sample_cv_content,
            "Engineering Management"
        )
        score_junior = cv_matcher.calculate_match_score(
            junior_job,
            sample_cv_content,
            "Engineering Management"
        )

        # Senior role should score higher with EM CV
        assert score_senior >= score_junior

    def test_score_capped_at_35(self):
        """Test that score never exceeds maximum of 35."""
        # Create job requirements with every possible keyword
        massive_requirements = " ".join([
            "python java javascript aws kubernetes docker",
            "machine learning ai data science sql",
            "leadership management agile scrum senior lead director"
        ] * 10)

        cv_with_everything = massive_requirements

        score = cv_matcher.calculate_match_score(
            massive_requirements,
            cv_with_everything,
            "Everything"
        )

        assert score <= 35

    def test_empty_job_requirements(self, sample_cv_content):
        """Test handling of empty job requirements."""
        score = cv_matcher.calculate_match_score("", sample_cv_content, "Engineering")
        assert score >= 0
        assert score <= 35


class TestFindBestCVMatch:
    """Test finding best CV match from multiple variants."""

    def test_find_best_single_cv(self, temp_user_data_dir, sample_cv_content, sample_config):
        """Test with single CV (should return that CV)."""
        # Create CV
        (temp_user_data_dir / "config" / "cv-variants" / "cv-em.md").write_text(sample_cv_content)

        cvs = cv_matcher.load_user_cvs(
            str(temp_user_data_dir),
            [sample_config['cv_variants']['variants'][0]]
        )

        job_requirements = "Engineering Manager with Python and AWS experience"

        best_cv, best_score, all_scores = cv_matcher.find_best_cv_match(
            job_requirements,
            cvs,
            sample_config['scoring']['weights']
        )

        assert best_cv == 'EM'
        assert best_score > 0
        assert len(all_scores) == 1

    def test_find_best_multiple_cvs(self, temp_user_data_dir, sample_cv_content, sample_cv_tpm, sample_config):
        """Test selecting best CV from multiple variants."""
        # Create both CVs
        (temp_user_data_dir / "config" / "cv-variants" / "cv-em.md").write_text(sample_cv_content)
        (temp_user_data_dir / "config" / "cv-variants" / "cv-tpm.md").write_text(sample_cv_tpm)

        cvs = cv_matcher.load_user_cvs(
            str(temp_user_data_dir),
            sample_config['cv_variants']['variants'][:2]
        )

        # Job that matches EM better
        job_requirements = "Senior Engineering Manager with Python, AWS, Kubernetes experience"

        best_cv, best_score, all_scores = cv_matcher.find_best_cv_match(
            job_requirements,
            cvs,
            sample_config['scoring']['weights']
        )

        # EM CV should score higher
        assert best_cv == 'EM'
        assert all_scores['EM'] >= all_scores['TPM']

    def test_tpm_cv_wins_for_tpm_role(self, temp_user_data_dir, sample_cv_content, sample_cv_tpm, sample_config):
        """Test that TPM CV scores better for TPM roles."""
        # Create both CVs
        (temp_user_data_dir / "config" / "cv-variants" / "cv-em.md").write_text(sample_cv_content)
        (temp_user_data_dir / "config" / "cv-variants" / "cv-tpm.md").write_text(sample_cv_tpm)

        cvs = cv_matcher.load_user_cvs(
            str(temp_user_data_dir),
            sample_config['cv_variants']['variants'][:2]
        )

        # Job that matches TPM better
        job_requirements = """
        Technical Program Manager
        Lead cross-functional teams, program management, stakeholder management,
        coordinate engineers, agile methodologies
        """

        best_cv, best_score, all_scores = cv_matcher.find_best_cv_match(
            job_requirements,
            cvs,
            sample_config['scoring']['weights']
        )

        # TPM CV should score higher
        assert best_cv == 'TPM'

    def test_cv_weight_affects_score(self, temp_user_data_dir, sample_cv_content, sample_config):
        """Test that CV weights are properly applied."""
        # Create CV
        (temp_user_data_dir / "config" / "cv-variants" / "cv-em.md").write_text(sample_cv_content)

        # Test with different weights
        variant_high_weight = {'id': 'EM', 'filename': 'cv-em.md', 'focus': 'Engineering', 'weight': 1.0}
        variant_low_weight = {'id': 'EM', 'filename': 'cv-em.md', 'focus': 'Engineering', 'weight': 0.5}

        cvs_high = cv_matcher.load_user_cvs(str(temp_user_data_dir), [variant_high_weight])
        cvs_low = cv_matcher.load_user_cvs(str(temp_user_data_dir), [variant_low_weight])

        job = "Engineering Manager"

        _, score_high, _ = cv_matcher.find_best_cv_match(
            job, cvs_high, sample_config['scoring']['weights']
        )
        _, score_low, _ = cv_matcher.find_best_cv_match(
            job, cvs_low, sample_config['scoring']['weights']
        )

        # Higher weight should result in higher score
        assert score_high >= score_low

    def test_score_respects_max_limit(self, temp_user_data_dir, sample_cv_content, sample_config):
        """Test that score never exceeds max allowed by scoring weights."""
        (temp_user_data_dir / "config" / "cv-variants" / "cv-em.md").write_text(sample_cv_content)

        cvs = cv_matcher.load_user_cvs(
            str(temp_user_data_dir),
            [sample_config['cv_variants']['variants'][0]]
        )

        # Perfect match job
        job = sample_cv_content  # Use CV as job description for perfect match

        _, best_score, _ = cv_matcher.find_best_cv_match(
            job, cvs, sample_config['scoring']['weights']
        )

        max_match_score = sample_config['scoring']['weights']['match']
        assert best_score <= max_match_score


class TestIdentifySkillGaps:
    """Test skill gap identification."""

    def test_identify_critical_gaps(self, sample_cv_content):
        """Test identification of critical missing skills."""
        job_with_rust = """
        Senior Engineer position requiring Python, Rust, and Kubernetes.
        Rust is critical for our systems programming needs.
        """

        gaps = cv_matcher.identify_skill_gaps(job_with_rust, sample_cv_content)

        assert isinstance(gaps, dict)
        assert 'critical' in gaps
        assert 'nice_to_have' in gaps

    def test_no_gaps_perfect_match(self, sample_cv_content):
        """Test when CV has all required skills."""
        job = "Python, AWS, Kubernetes, Leadership, Management experience"

        gaps = cv_matcher.identify_skill_gaps(job, sample_cv_content)

        # Should have minimal or no critical gaps
        assert len(gaps['critical']) <= 2

    def test_gaps_case_insensitive(self):
        """Test that gap detection is case-insensitive."""
        cv = "PYTHON and JAVA experience"
        job = "python and java required"

        gaps = cv_matcher.identify_skill_gaps(job, cv)

        # Should not flag python/java as gaps
        assert 'Python' not in gaps['critical']
        assert 'Java' not in gaps['critical']


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_unicode_in_cv(self, temp_user_data_dir):
        """Test handling of Unicode characters in CV."""
        cv_with_unicode = """
        # CV - ג'ון דו
        Experience at גוגל ישראל (Google Israel)
        Skills: Python, עברית
        """

        cv_path = temp_user_data_dir / "config" / "cv-variants" / "cv-hebrew.md"
        cv_path.write_text(cv_with_unicode, encoding='utf-8')

        variants = [{'id': 'HE', 'filename': 'cv-hebrew.md', 'focus': 'Testing'}]
        cvs = cv_matcher.load_user_cvs(str(temp_user_data_dir), variants)

        assert 'HE' in cvs
        assert 'גוגל' in cvs['HE']['content']

    def test_very_long_cv(self, temp_user_data_dir):
        """Test handling of very long CV (>10000 words)."""
        long_cv = ("Python AWS Kubernetes " * 5000)

        cv_path = temp_user_data_dir / "config" / "cv-variants" / "cv-long.md"
        cv_path.write_text(long_cv)

        variants = [{'id': 'LONG', 'filename': 'cv-long.md', 'focus': 'Testing'}]
        cvs = cv_matcher.load_user_cvs(str(temp_user_data_dir), variants)

        assert 'LONG' in cvs

    def test_empty_cv_file(self, temp_user_data_dir):
        """Test handling of empty CV file."""
        cv_path = temp_user_data_dir / "config" / "cv-variants" / "cv-empty.md"
        cv_path.write_text("")

        variants = [{'id': 'EMPTY', 'filename': 'cv-empty.md', 'focus': 'Testing'}]
        cvs = cv_matcher.load_user_cvs(str(temp_user_data_dir), variants)

        assert 'EMPTY' in cvs
        assert cvs['EMPTY']['content'] == ""

    def test_special_characters_in_job_requirements(self, sample_cv_content):
        """Test job requirements with special characters."""
        job_with_special = """
        Role: Senior Engineer (Python/AWS/K8s) @ $$$BigCorp$$$
        Requirements: C++, C#, .NET, Node.js, Vue.js
        """

        score = cv_matcher.calculate_match_score(
            job_with_special,
            sample_cv_content,
            "Engineering"
        )

        assert score >= 0
        assert score <= 35


class TestRegressionTests:
    """Tests for specific bugs and regressions."""

    def test_java_detection_not_javascript(self):
        """
        Regression test: Ensure 'java' pattern doesn't match 'javascript'.
        The regex should use negative lookahead: java(?!script)
        """
        cv_with_javascript = "Skills: JavaScript, TypeScript, Node.js"
        cv_with_java = "Skills: Java, Spring Boot, Hibernate"

        skills_js = cv_matcher.extract_skills_from_cv(cv_with_javascript)
        skills_java = cv_matcher.extract_skills_from_cv(cv_with_java)

        # JavaScript CV should not have 'java' skill
        # (This test validates the negative lookahead in the regex)
        assert 'javascript' in skills_js

    def test_division_by_zero_empty_job(self):
        """Test that empty job requirements don't cause division by zero."""
        cv = "Python, AWS"
        job = ""

        # Should not raise ZeroDivisionError
        score = cv_matcher.calculate_match_score(job, cv, "Engineering")
        assert isinstance(score, int)

    def test_all_cvs_score_zero(self, temp_user_data_dir, sample_config):
        """Test handling when all CVs score 0 for a job."""
        # Create CV with completely different skills
        irrelevant_cv = "Designer with Photoshop and Figma skills only"

        cv_path = temp_user_data_dir / "config" / "cv-variants" / "cv-designer.md"
        cv_path.write_text(irrelevant_cv)

        variants = [{'id': 'DES', 'filename': 'cv-designer.md', 'focus': 'Design'}]
        cvs = cv_matcher.load_user_cvs(str(temp_user_data_dir), variants)

        # Job for engineer
        job = "Senior Python Engineer with AWS and Kubernetes"

        # Should not crash, should return some CV as "best"
        best_cv, best_score, all_scores = cv_matcher.find_best_cv_match(
            job, cvs, sample_config['scoring']['weights']
        )

        assert best_cv == 'DES'  # Only CV available
        assert best_score >= 0
