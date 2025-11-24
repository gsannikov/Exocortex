"""Pytest configuration and shared fixtures."""

import os
import sys
from pathlib import Path

import pytest

# Add skill-package/scripts to path for imports
REPO_ROOT = Path(__file__).parent.parent
SKILL_SCRIPTS_DIR = REPO_ROOT / "skill-package" / "scripts"
sys.path.insert(0, str(SKILL_SCRIPTS_DIR))


@pytest.fixture
def sample_cv_content():
    """Sample CV content for testing."""
    return """# Senior Engineering Manager CV

## Professional Summary
Experienced engineering leader with 10+ years in software development and team management.

## Skills
- **Languages**: Python, Java, JavaScript, Go
- **Cloud**: AWS (EC2, S3, Lambda), Kubernetes, Docker
- **Leadership**: Engineering Management, Agile, Scrum
- **AI/ML**: Machine Learning, Data Science, TensorFlow

## Experience

### Senior Engineering Manager - Google Israel (2020-2024)
- Led team of 12 engineers building cloud infrastructure
- Implemented Kubernetes-based deployment pipeline
- Managed $2M annual budget
- Delivered 15+ major features

### Engineering Manager - Microsoft (2017-2020)
- Led team of 8 engineers on Azure services
- Implemented agile methodologies
- Mentored 5 engineers to senior roles

### Senior Software Engineer - Amazon (2014-2017)
- Built AWS Lambda features
- Python and Java backend development
- Led technical design for 3 major projects
"""


@pytest.fixture
def sample_cv_tpm():
    """Sample TPM-focused CV."""
    return """# Technical Program Manager CV

## Professional Summary
Technical Program Manager with expertise in cross-functional program delivery.

## Skills
- **Program Management**: Agile, Scrum, Project Planning
- **Technical**: Python, SQL, APIs, System Design
- **Leadership**: Stakeholder Management, Team Coordination

## Experience

### Technical Program Manager - Meta (2021-2024)
- Led 5 cross-functional teams (40+ people)
- Delivered infrastructure migration project ($5M budget)
- Reduced deployment time by 60%

### Senior TPM - Apple (2018-2021)
- Managed iOS feature releases
- Coordinated 30+ engineers across 4 teams
"""


@pytest.fixture
def sample_job_requirements_senior_em():
    """Sample job requirements for Senior Engineering Manager."""
    return """Senior Engineering Manager - Cloud Infrastructure

Requirements:
- 8+ years of software engineering experience
- 3+ years of engineering management experience
- Strong experience with Python and cloud technologies (AWS/GCP)
- Experience with Kubernetes and containerization
- Proven track record of leading teams of 10+ engineers
- Experience with agile methodologies
- Excellent leadership and communication skills

Nice to have:
- Experience with machine learning infrastructure
- Previous experience at tech giants (Google, Amazon, Microsoft)
- Israeli tech market experience
"""


@pytest.fixture
def sample_job_requirements_ai_engineer():
    """Sample job requirements for AI Engineer."""
    return """Senior AI/ML Engineer

Requirements:
- 5+ years of machine learning experience
- Strong Python programming skills
- Experience with TensorFlow, PyTorch, or similar frameworks
- Experience deploying ML models to production
- Strong understanding of data science and statistics
- Experience with AWS or GCP for ML workloads

Nice to have:
- PhD in Computer Science or related field
- Experience with large language models
- Research publications
"""


@pytest.fixture
def sample_config():
    """Sample user configuration."""
    return {
        'cv_variants': {
            'enabled': True,
            'count': 3,
            'variants': [
                {
                    'id': 'EM',
                    'filename': 'cv-em.md',
                    'focus': 'Engineering Management',
                    'weight': 1.0
                },
                {
                    'id': 'TPM',
                    'filename': 'cv-tpm.md',
                    'focus': 'Technical Program Management',
                    'weight': 0.9
                },
                {
                    'id': 'AI',
                    'filename': 'cv-ai.md',
                    'focus': 'AI/ML Engineering',
                    'weight': 0.85
                }
            ]
        },
        'scoring': {
            'weights': {
                'match': 35,
                'income': 15,
                'growth': 20,
                'lowprep': 15,
                'stress': 10,
                'location': 5
            },
            'thresholds': {
                'first_priority': 70,
                'second_priority': 50
            },
            'bonuses': {
                'tech_giant_experience': 5,
                'startup_experience': 3,
                'relevant_domain': 2
            }
        },
        'preferences': {
            'min_salary_annual_ils': 450000,
            'preferred_locations': ['Tel Aviv', 'Remote', 'Herzliya'],
            'avoid_keywords': ['relocation required', 'on-call 24/7']
        },
        'paths': {
            'cv_base': 'config/cv-variants',
            'companies_db': 'db/companies',
            'roles_db': 'db/roles'
        }
    }


@pytest.fixture
def sample_company_frontmatter():
    """Sample company YAML frontmatter."""
    return {
        'company_id': 'google-israel',
        'company_name': 'Google Israel',
        'tier': 1,
        'tier_score': 25,
        'employees_global': 150000,
        'employees_israel': 2000,
        'glassdoor_rating': 4.5,
        'revenue_usd': '280B',
        'funding_stage': 'Public',
        'key_products': ['Search', 'Cloud', 'Android'],
        'updated': True
    }


@pytest.fixture
def sample_role_frontmatter():
    """Sample role YAML frontmatter."""
    return {
        'role_id': 'google-israel-senior-engineer-20250128',
        'company_id': 'google-israel',
        'role_title': 'Senior Software Engineer',
        'application_date': '2025-01-28',
        'score_total': 78,
        'score_match': 32,
        'score_income': 23,
        'score_growth': 18,
        'score_lowprep': 12,
        'score_stress': 8,
        'score_location': 5,
        'priority': 'First',
        'best_cv': 'EM',
        'cv_scores': {
            'EM': 32,
            'TPM': 28,
            'AI': 25
        },
        'status': 'Applied',
        'notes': 'Strong team, interesting project'
    }


@pytest.fixture
def temp_user_data_dir(tmp_path):
    """Create temporary user-data directory structure."""
    user_data = tmp_path / "user-data"
    user_data.mkdir()

    # Create subdirectories
    (user_data / "config").mkdir()
    (user_data / "config" / "cv-variants").mkdir()
    (user_data / "db").mkdir()
    (user_data / "db" / "companies").mkdir()
    (user_data / "db" / "roles").mkdir()

    return user_data
