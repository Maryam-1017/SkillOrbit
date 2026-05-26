"""
Utility functions for skill normalization and comparison.
"""


def normalize_skill(skill):
    """
    Normalize a single skill: lowercase, strip whitespace, remove extra spaces.
    
    Args:
        skill (str): Raw skill string
    
    Returns:
        str: Normalized skill
    """
    return skill.strip().lower()


def normalize_skills(skills):
    """
    Normalize a list of skills.
    
    Args:
        skills (list): List of skill strings
    
    Returns:
        list: List of normalized skills
    """
    if not isinstance(skills, list):
        return []
    return [normalize_skill(s) for s in skills if isinstance(s, str) and s.strip()]


def remove_duplicates(skills):
    """
    Remove duplicate skills while preserving order.
    
    Args:
        skills (list): List of skills
    
    Returns:
        list: List with duplicates removed
    """
    seen = set()
    result = []
    for skill in skills:
        if skill not in seen:
            seen.add(skill)
            result.append(skill)
    return result


def case_insensitive_match(skill, skills_list):
    """
    Check if a skill exists in a list (case-insensitive).
    
    Args:
        skill (str): Skill to search for (normalized)
        skills_list (list): List of normalized skills
    
    Returns:
        bool: True if skill found, False otherwise
    """
    normalized_skill = normalize_skill(skill)
    return normalized_skill in skills_list


def categorize_skill_priority(skill):
    """
    Assign priority level to a skill (High/Medium/Low).
    
    Args:
        skill (str): Normalized skill name
    
    Returns:
        str: Priority level ('High', 'Medium', or 'Low')
    """
    high_priority_keywords = [
        'react', 'javascript', 'python', 'java', 'c++', 'system design',
        'machine learning', 'deep learning', 'tensorflow', 'pytorch',
        'docker', 'kubernetes', 'aws', 'gcp', 'azure', 'sql', 'leadership',
        'communication'
    ]
    
    medium_priority_keywords = [
        'html', 'css', 'rest api', 'git', 'testing', 'debugging',
        'linux', 'windows', 'excel', 'tableau', 'power bi', 'agile'
    ]
    
    skill_lower = skill.lower()
    
    for keyword in high_priority_keywords:
        if keyword in skill_lower:
            return 'High'
    
    for keyword in medium_priority_keywords:
        if keyword in skill_lower:
            return 'Medium'
    
    return 'Low'
