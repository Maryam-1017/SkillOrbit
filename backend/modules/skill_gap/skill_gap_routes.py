"""
Routes for skill gap analysis module.
"""

from flask import Blueprint
from .skill_gap_controller import SkillGapController

# Create blueprint for skill gap module
skill_gap_bp = Blueprint('skill_gap', __name__, url_prefix='/api/skill-gap')


@skill_gap_bp.route('/analyze', methods=['POST'])
def analyze():
    """Endpoint to analyze skill gap between user skills and career requirements."""
    return SkillGapController.analyze_skill_gap()


@skill_gap_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint for the skill gap module."""
    return {'status': 'ok', 'module': 'skill_gap'}, 200
