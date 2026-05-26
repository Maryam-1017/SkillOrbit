"""
Service layer for skill gap analysis.
Contains core business logic for comparing skills.
"""

import sys
import os
from .skill_gap_utils import normalize_skills, remove_duplicates, categorize_skill_priority

# Add parent directory to path for accessing ML module
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)

from ML.recommender import get_matches


class SkillGapAnalyzer:
    """Analyzes skill gaps between user skills and career requirements."""
    
    def __init__(self):
        pass
    
    def get_career_required_skills(self, career_name):
        """
        Fetch required skills for a specific career from the recommender module.
        
        Args:
            career_name (str): Career title to fetch skills for
        
        Returns:
            list: List of required skills or empty list if career not found
        """
        try:
            # Get matches using the career title as a query
            matches = get_matches(career_name.lower(), top_n=1)
            
            if matches and len(matches) > 0:
                # Check if the top match is the exact career
                if matches[0]['career'].lower() == career_name.lower():
                    return matches[0]['required_skills']
            
            # If not exact match, search through all matches
            matches = get_matches(career_name.lower(), top_n=50)
            for match in matches:
                if match['career'].lower() == career_name.lower():
                    return match['required_skills']
            
            return []
        except Exception as e:
            print(f"Error fetching career skills: {e}")
            return []
    
    def analyze_skill_gap(self, user_skills, required_skills):
        """
        Analyze the gap between user skills and required skills.
        
        Args:
            user_skills (list): List of skills user has
            required_skills (list): List of skills required for the career
        
        Returns:
            dict: Analysis result with matched_skills, missing_skills, etc.
        """
        # Normalize and deduplicate both lists
        user_skills_normalized = remove_duplicates(normalize_skills(user_skills))
        required_skills_normalized = remove_duplicates(normalize_skills(required_skills))
        
        # Convert to sets for efficient comparison
        user_set = set(user_skills_normalized)
        required_set = set(required_skills_normalized)
        
        # Calculate matched and missing skills
        matched_skills = list(user_set.intersection(required_set))
        missing_skills = list(required_set - user_set)
        
        # Sort by priority
        missing_skills_with_priority = [
            {
                'skill': skill,
                'priority': categorize_skill_priority(skill)
            }
            for skill in missing_skills
        ]
        
        # Sort by priority (High > Medium > Low)
        priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
        missing_skills_with_priority.sort(key=lambda x: priority_order[x['priority']])
        
        # Generate learning suggestions based on missing skills
        suggestions = self._generate_suggestions(missing_skills_with_priority)
        
        return {
            'matched_skills': sorted(matched_skills),
            'missing_skills': missing_skills_with_priority,
            'missing_count': len(missing_skills),
            'matched_count': len(matched_skills),
            'total_required': len(required_skills_normalized),
            'proficiency_percentage': round(
                (len(matched_skills) / len(required_skills_normalized) * 100) if required_skills_normalized else 0,
                1
            ),
            'suggestions': suggestions
        }
    
    def _generate_suggestions(self, missing_skills_with_priority):
        """
        Generate learning suggestions based on missing skills.
        
        Args:
            missing_skills_with_priority (list): List of missing skills with priority
        
        Returns:
            list: List of learning suggestions
        """
        suggestions = []
        
        # Group skills by priority
        high_priority = [s['skill'] for s in missing_skills_with_priority if s['priority'] == 'High']
        medium_priority = [s['skill'] for s in missing_skills_with_priority if s['priority'] == 'Medium']
        low_priority = [s['skill'] for s in missing_skills_with_priority if s['priority'] == 'Low']
        
        # Generate suggestions for high priority skills
        if high_priority:
            if len(high_priority) == 1:
                suggestions.append(f"Master {high_priority[0]} - this is critical for your career")
            else:
                skill_list = ', '.join(high_priority[:3])
                suggestions.append(f"Focus on learning {skill_list} - these are highly important")
        
        # Generate suggestions for medium priority skills
        if medium_priority:
            if len(medium_priority) <= 2:
                skill_list = ' and '.join(medium_priority)
                suggestions.append(f"Build proficiency in {skill_list}")
            else:
                skill_list = ', '.join(medium_priority[:3])
                suggestions.append(f"Develop skills in {skill_list}, among others")
        
        # Generate suggestions for low priority skills
        if low_priority and len(suggestions) < 5:
            if len(low_priority) <= 2:
                skill_list = ' and '.join(low_priority)
                suggestions.append(f"Learn {skill_list} to strengthen your profile")
            else:
                suggestions.append(f"Explore additional tools and frameworks like {low_priority[0]}")
        
        # Add generic suggestions if needed
        if not suggestions:
            suggestions.append("You have all the required skills for this career!")
        
        return suggestions[:5]  # Return max 5 suggestions
    
    def analyze_with_career_name(self, user_skills, career_name):
        """
        Analyze skill gap using user skills and a career name.
        
        Args:
            user_skills (list): List of skills user has
            career_name (str): Name of the career
        
        Returns:
            dict: Analysis result with matched_skills, missing_skills, etc.
        """
        required_skills = self.get_career_required_skills(career_name)
        
        if not required_skills:
            raise ValueError(f"Career '{career_name}' not found in database")
        
        return self.analyze_skill_gap(user_skills, required_skills)


# Create singleton instance
_analyzer_instance = None


def get_analyzer():
    """Get or create the singleton SkillGapAnalyzer instance."""
    global _analyzer_instance
    if _analyzer_instance is None:
        _analyzer_instance = SkillGapAnalyzer()
    return _analyzer_instance
