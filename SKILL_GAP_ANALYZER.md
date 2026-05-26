# Skill Gap Analyzer Module

The Skill Gap Analyzer is Module 3 of SkillOrbit. It compares user skills with career requirements and provides:
- **Matched Skills**: Skills user already has ( Green)
- **Missing Skills**: Skills user needs to learn ( Red, prioritized)
- **Learning Suggestions**: Actionable next steps ( Blue)

Server runs at: `http://localhost:5000`

**Description**: Analyze skill gap between user skills and career requirements.

## Architecture

### Module Structure
```
/backend/modules/skill_gap/
├── __init__.py                 # Blueprint initialization
├── skill_gap_utils.py          # Utility functions
├── skill_gap_service.py        # Core business logic
├── skill_gap_controller.py     # Request handlers
└── skill_gap_routes.py         # Route definitions
```

### Data Flow
```
User Input (Frontend)
    ↓
/api/skill-gap/analyze (Route)
    ↓
skill_gap_controller.py (Request validation)
    ↓
skill_gap_service.py (Core logic)
    ├── Get career required skills
    ├── Normalize user skills
    ├── Normalize required skills
    ├── Compare sets (intersection/difference)
    ├── Categorize priorities
    └── Generate suggestions
    ↓
skill_gap_utils.py (Helper functions)
    ↓
JSON Response (Frontend)
```

## Key Components

### 1. skill_gap_utils.py

**Functions**:
- `normalize_skill(skill)` - Converts skill to lowercase, strips whitespace
- `normalize_skills(skills_list)` - Batch normalization
- `remove_duplicates(skills)` - Removes duplicates while preserving order
- `case_insensitive_match(skill, skills_list)` - Flexible matching
- `categorize_skill_priority(skill)` - Assigns High/Medium/Low priority

**Usage Example**:
```python
from backend.modules.skill_gap.skill_gap_utils import normalize_skills, remove_duplicates

user_input = ["Python", "PYTHON", "HTML"]
normalized = normalize_skills(user_input)  # ["python", "html"]
deduped = remove_duplicates(normalized)    # ["python", "html"]
```

### 2. skill_gap_service.py

**SkillGapAnalyzer Class**:

```python
from backend.modules.skill_gap.skill_gap_service import get_analyzer

analyzer = get_analyzer()  # Singleton instance

# Option 1: With career name
result = analyzer.analyze_with_career_name(
    user_skills=["Python", "SQL"],
    career_name="Data Scientist"
)

# Option 2: With required skills array
result = analyzer.analyze_skill_gap(
    user_skills=["Python", "SQL"],
    required_skills=["Python", "SQL", "Machine Learning", "Statistics"]
)

# Result contains:
# - matched_skills: list of matched skills
# - missing_skills: list of dicts with {skill, priority}
# - suggestions: list of learning suggestions
# - proficiency_percentage: float (0-100)
```

### 3. skill_gap_controller.py

**SkillGapController.analyze_skill_gap()**:
- Validates request JSON
- Ensures user_skills is provided
- Checks for either career or required_skills
- Calls service layer
- Returns JSON response with proper status codes

### 4. skill_gap_routes.py

**Routes**:
- `POST /api/skill-gap/analyze` → `analyze()`
- `GET /api/skill-gap/health` → `health()`

## Frontend Integration

### Career Advisor Page (/advisor)

**New Button** on each career card:
```html
<button class="btn btn-outline-custom rounded-pill" 
        onclick="analyzeSkillGap('Frontend Developer', event)">
    Skill Gap
</button>
```

**JavaScript Function**:
```javascript
// Analyze skill gap
analyzeSkillGap(careerName, event)

// Display results
displaySkillGapResults(data, careerName)
```

**Result Display**:
3-column responsive grid showing:
1. **Matched Skills** (Green badge with ✓)
2. **Missing Skills** (Red badges, darker = higher priority)
3. **Learning Path** (Blue suggestions with 📚 icon)

## Priority Categorization

### High Priority Skills
Framework/Language cores: `react, javascript, python, java, c++, ...`
Advanced concepts: `system design, machine learning, deep learning, ...`
Important tools: `docker, kubernetes, aws, gcp, azure, ...`

### Medium Priority Skills
`html, css, git, testing, rest api, linux, excel, tableau, agile, ...`

### Low Priority Skills
Everything else (tools, frameworks, niche technologies)

## Error Handling

### Expected Error Cases

1. **No data provided** (400)
```json
{"error": "No data provided"}
```

2. **Empty user_skills** (400)
```json
{"error": "user_skills must be a non-empty array"}
```

3. **Neither career nor required_skills** (400)
```json
{"error": "Either 'career' or 'required_skills' must be provided"}
```

4. **Career not found** (404)
```json
{"error": "Career 'NonExistentCareer' not found in database"}
```

5. **Server error** (500)
```json
{"error": "An error occurred: <error_details>"}
```

## Support & Questions

For issues or questions:
1. Check error logs: `flask debug=True`
2. Review test cases: `/tmp/test_skill_gap.sh`
3. Check implementation: `/backend/modules/skill_gap/`
4. Review this guide: `SKILL_GAP_ANALYZER.md`

## License & Credits

Part of SkillOrbit - AI-Powered Career Guidance Platform
Implementation: Module 3: Skill Gap Analyzer
