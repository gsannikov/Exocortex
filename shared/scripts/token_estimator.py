"""
Token Estimator for Career Consultant Skill
Estimates token usage to prevent context window overflow

This script runs in Claude's container.
"""

import re
from typing import Dict


def estimate_tokens(text: str) -> int:
    """
    Estimate number of tokens in text.
    
    This is a rough approximation based on common tokenization rules.
    Actual token count may vary.
    
    Args:
        text: Text to estimate tokens for
        
    Returns:
        Estimated token count
        
    Note:
        Uses ~4 characters per token as rough estimate
    """
    if not text:
        return 0
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Rough estimate: ~4 characters per token
    char_count = len(text)
    estimated_tokens = char_count // 4
    
    # Add tokens for special characters and formatting
    special_chars = text.count('{') + text.count('}') + text.count('[') + text.count(']')
    estimated_tokens += special_chars
    
    return estimated_tokens


def estimate_file_tokens(file_path: str) -> int:
    """
    Estimate tokens in a file.
    
    Args:
        file_path: Path to file
        
    Returns:
        Estimated token count
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return estimate_tokens(content)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return 0


def estimate_module_tokens(module_dict: Dict[str, str]) -> Dict[str, int]:
    """
    Estimate tokens for multiple modules.
    
    Args:
        module_dict: Dictionary mapping module names to content
        
    Returns:
        Dictionary mapping module names to token counts
    """
    token_counts = {}
    for module_name, content in module_dict.items():
        token_counts[module_name] = estimate_tokens(content)
    return token_counts


def check_token_budget(current_tokens: int, max_tokens: int = 190000) -> Dict:
    """
    Check if within token budget.
    
    Args:
        current_tokens: Current token count
        max_tokens: Maximum allowed tokens
        
    Returns:
        Dictionary with budget status
    """
    remaining = max_tokens - current_tokens
    percentage_used = (current_tokens / max_tokens) * 100
    
    if percentage_used > 80:
        status = "CRITICAL"
        recommendation = "Start new conversation immediately"
    elif percentage_used > 60:
        status = "WARNING"
        recommendation = "Consider starting new conversation soon"
    else:
        status = "OK"
        recommendation = "Plenty of room to continue"
    
    return {
        'used': current_tokens,
        'remaining': remaining,
        'max': max_tokens,
        'percentage_used': round(percentage_used, 1),
        'status': status,
        'recommendation': recommendation
    }


def estimate_phase_tokens(phase: str) -> int:
    """
    Estimate token usage for different workflow phases.
    
    Args:
        phase: Workflow phase ('init', 'research', 'analysis', 'excel')
        
    Returns:
        Estimated token usage
    """
    phase_estimates = {
        'init': 5000,           # Load config
        'research': 15000,      # Company research
        'analysis': 20000,      # Job analysis with CVs
        'excel': 5000,          # Excel generation
    }
    
    return phase_estimates.get(phase, 10000)


def can_fit_in_budget(
    current_tokens: int,
    additional_tokens: int,
    max_tokens: int = 190000,
    safety_margin: int = 10000
) -> bool:
    """
    Check if additional content fits in budget with safety margin.
    
    Args:
        current_tokens: Current token count
        additional_tokens: Tokens to add
        max_tokens: Maximum allowed tokens
        safety_margin: Safety margin to maintain
        
    Returns:
        True if fits within budget
    """
    total = current_tokens + additional_tokens
    return total <= (max_tokens - safety_margin)


def format_token_report(token_data: Dict) -> str:
    """
    Format token usage report for display.
    
    Args:
        token_data: Token data from check_token_budget
        
    Returns:
        Formatted report string
    """
    status_icons = {
        'OK': '✅',
        'WARNING': '⚠️',
        'CRITICAL': '🚨'
    }
    
    icon = status_icons.get(token_data['status'], '❓')
    
    report = f"""
📊 Token Status Check
Used: {token_data['used']:,} tokens ({token_data['percentage_used']}%)
Remaining: {token_data['remaining']:,} tokens ({100 - token_data['percentage_used']:.1f}%)
Status: {icon} {token_data['status']}
Recommendation: {token_data['recommendation']}
"""
    return report.strip()


def estimate_cv_load_tokens(cv_count: int, avg_cv_size: int = 2000) -> int:
    """
    Estimate tokens needed to load CVs.
    
    Args:
        cv_count: Number of CVs
        avg_cv_size: Average tokens per CV
        
    Returns:
        Estimated total tokens
    """
    return cv_count * avg_cv_size


def estimate_total_workflow_tokens(cv_count: int, is_new_company: bool = False) -> Dict:
    """
    Estimate total tokens for complete workflow.
    
    Args:
        cv_count: Number of CV variants
        is_new_company: Whether company needs research
        
    Returns:
        Dictionary with token breakdown
    """
    tokens = {
        'init': 5000,
        'cvs': estimate_cv_load_tokens(cv_count),
        'modules': 8000,
        'analysis': 5000,
        'excel': 2000
    }
    
    if is_new_company:
        tokens['research'] = 15000
    
    total = sum(tokens.values())
    
    return {
        'breakdown': tokens,
        'total': total,
        'cv_count': cv_count,
        'is_new_company': is_new_company
    }


# Example usage
if __name__ == "__main__":
    # Test token estimation
    test_text = """
    This is a test document with multiple lines.
    It contains various types of content including:
    - Lists
    - Code snippets
    - Regular text
    
    Let's estimate how many tokens this might use.
    """
    
    tokens = estimate_tokens(test_text)
    print(f"Estimated tokens: {tokens}")
    print("\n" + "="*50 + "\n")
    
    # Test budget check
    current = 75000
    budget_status = check_token_budget(current)
    print(format_token_report(budget_status))
    print("\n" + "="*50 + "\n")
    
    # Test workflow estimation
    workflow_tokens = estimate_total_workflow_tokens(cv_count=4, is_new_company=True)
    print("Workflow Token Estimate:")
    for phase, tokens in workflow_tokens['breakdown'].items():
        print(f"  {phase}: {tokens:,} tokens")
    print(f"\nTotal: {workflow_tokens['total']:,} tokens")
    
    # Check if fits in budget
    fits = can_fit_in_budget(75000, workflow_tokens['total'])
    print(f"\nFits in budget: {'Yes ✅' if fits else 'No ❌'}")
