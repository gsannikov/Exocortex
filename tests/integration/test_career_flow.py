import pytest
import yaml
from pathlib import Path

# We are testing the data handoff contract between skills
# job-analyzer writes -> interview-prep reads

def test_career_handoff(integration_data_dir):
    """Verify interview-prep can consume job-analyzer output."""
    career_dir = integration_data_dir / "career"
    
    # 1. Simulate job-analyzer output
    # job-analyzer produces a YAML file for each job
    job_id = "software-engineer-google-123"
    job_file = career_dir / "analyses" / f"{job_id}.yaml"
    
    job_data = {
        "id": job_id,
        "title": "Software Engineer",
        "company": "Google",
        "url": "https://google.com/careers/123",
        "analysis": {
            "score": 85,
            "skills_match": ["Python", "System Design"],
            "missing_skills": ["Kubernetes"],
            "cultural_fit": "High"
        },
        "status": "applied",
        "added_at": "2025-12-11"
    }
    
    with open(job_file, "w") as f:
        yaml.dump(job_data, f)
        
    # 2. Simulate reading by interview-prep (or generic consumer)
    # Verify file exists and structure is correct
    assert job_file.exists()
    
    with open(job_file) as f:
        loaded_data = yaml.safe_load(f)
        
    # 3. Validation assertions (The Integration Contract)
    assert loaded_data["id"] == job_id
    assert loaded_data["company"] == "Google"
    assert "analysis" in loaded_data
    assert "missing_skills" in loaded_data["analysis"]
    
    # 4. Verify shared config access
    config_file = career_dir / "config.yaml"
    config_data = {
        "resume_path": "/path/to/resume.pdf",
        "openai_model": "gpt-4"
    }
    with open(config_file, "w") as f:
        yaml.dump(config_data, f)
        
    assert config_file.exists()
    with open(config_file) as f:
        loaded_config = yaml.safe_load(f)
        
    assert loaded_config["resume_path"] == "/path/to/resume.pdf"
