/**
 * Skill Gap Analyzer - API Communication Module
 * 
 * Handles all backend communication for skill gap analysis.
 * Separates API logic from UI rendering.
 */

/**
 * Analyze skill gap by calling backend API
 * 
 * @param {Object} data - Request payload
 * @param {Array<string>} data.user_skills - User's current skills
 * @param {string} data.career - Career name (or provide required_skills instead)
 * @param {Array<string>} [data.required_skills] - Required skills array (alternative to career)
 * 
 * @returns {Promise<Object>} API response with analysis results
 * @throws {Error} If API call fails
 * 
 * @example
 * const result = await analyzeSkillGap({
 *   user_skills: ["Python", "HTML"],
 *   career: "Frontend Developer"
 * });
 */
async function analyzeSkillGap(data) {
  try {
    const response = await fetch('/api/skill-gap/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `API Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Skill Gap API Error:', error);
    throw error;
  }
}

/**
 * Health check for skill gap module
 * 
 * @returns {Promise<Object>} Health status
 * 
 * @example
 * const health = await checkSkillGapHealth();
 * console.log(health.status); // 'ok'
 */
async function checkSkillGapHealth() {
  try {
    const response = await fetch('/api/skill-gap/health');
    if (!response.ok) {
      throw new Error(`Health check failed: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Skill Gap Health Check Error:', error);
    throw error;
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { analyzeSkillGap, checkSkillGapHealth };
}
