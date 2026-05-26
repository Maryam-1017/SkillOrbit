"""
Controller for skill gap analysis API endpoints.
Handles request validation and orchestrates service calls.
"""

from flask import request, jsonify
from .skill_gap_service import get_analyzer


class SkillGapController:
    """Handles skill gap analysis requests."""
    
    @staticmethod
    def analyze_skill_gap():
        """
        API endpoint to analyze skill gap.
        
        Expected JSON:
        {
            "user_skills": ["Python", "HTML"],
            "career": "Frontend Developer"  (optional, use if available)
        }
        OR
        {
            "user_skills": ["Python", "HTML"],
            "required_skills": ["HTML", "CSS", "JavaScript", "React"]
        }
        
        Returns:
            JSON response with matched/missing skills and suggestions
        """
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({"error": "No data provided"}), 400
            
            user_skills = data.get("user_skills", [])
            
            if not user_skills or not isinstance(user_skills, list):
                return jsonify({"error": "user_skills must be a non-empty array"}), 400
            
            analyzer = get_analyzer()
            
            # Check if career name is provided
            career = data.get("career")
            required_skills = data.get("required_skills")
            
            if career:
                # Analyze using career name
                result = analyzer.analyze_with_career_name(user_skills, career)
                result['career'] = career
            elif required_skills and isinstance(required_skills, list):
                # Analyze using provided required skills
                result = analyzer.analyze_skill_gap(user_skills, required_skills)
            else:
                return jsonify(
                    {"error": "Either 'career' or 'required_skills' must be provided"}
                ), 400
            
            return jsonify(result), 200
        
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
