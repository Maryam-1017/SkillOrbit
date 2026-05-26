/**
 * Skill Gap Analyzer - Event Delegation Handler
 * 
 * Uses event delegation to handle Skill Gap button clicks on ALL career cards
 * (both existing and future dynamically created cards).
 * 
 * Single listener pattern:
 * - One listener attached to career cards container
 * - Detects clicks on .skill-gap-btn buttons
 * - Reads career name from data-career attribute
 * - Calls API and renders results
 */

/**
 * Initialize skill gap analyzer event delegation
 * 
 * Must be called once when page loads.
 * Automatically handles all current and future career cards.
 * 
 * @param {string} containerSelector - Selector for career cards container
 * @param {string} resultsSelector - Selector for results container
 * @param {Array<string>} userSkills - Current user skills array
 * 
 * @example
 * initSkillGapHandler('#results-container', '#skill-gap-results', ['Python', 'HTML']);
 */
function initSkillGapHandler(containerSelector, resultsSelector, userSkills = []) {
  const container = document.querySelector(containerSelector);

  if (!container) {
    console.error(`Container "${containerSelector}" not found. Skill Gap handler not initialized.`);
    return;
  }

  // Use event delegation: attach ONE listener to the container
  // This handles ALL current and future .skill-gap-btn buttons
  container.addEventListener('click', async (event) => {
    const button = event.target.closest('.skill-gap-btn');

    // Only handle clicks on skill gap buttons
    if (!button) return;

    event.preventDefault();

    // Get career name from data attribute on closest career card
    const careerCard = button.closest('[data-career]');
    if (!careerCard) {
      console.error('Career card with data-career attribute not found');
      return;
    }

    const careerName = careerCard.getAttribute('data-career');

    if (!careerName) {
      console.error('Career name not found in data-career attribute');
      return;
    }

    // Handle button state during loading
    const originalText = button.textContent;
    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Analyzing...';

    try {
      // Validate user skills
      if (!userSkills || userSkills.length === 0) {
        console.warn('No user skills provided for analysis');
        alert('Please add at least one skill first.');
        return;
      }

      // Call API
      const result = await analyzeSkillGap({
        user_skills: userSkills,
        career: careerName
      });

      // Add career name to result
      result.career = careerName;

      // Render results
      renderSkillGapResults(result, careerName, resultsSelector);

    } catch (error) {
      console.error('Skill Gap Analysis Error:', error);
      alert(`Failed to analyze skill gap: ${error.message}`);
    } finally {
      // Restore button state
      button.disabled = false;
      button.innerHTML = originalText;
    }
  });

  console.log('✓ Skill Gap Handler initialized with event delegation');
}

/**
 * Update user skills for skill gap analyzer
 * Typically called after user modifies their skills
 * 
 * @param {Array<string>} newSkills - Updated skills array
 * 
 * @example
 * updateSkillGapUserSkills(['Python', 'JavaScript', 'React']);
 */
function updateSkillGapUserSkills(newSkills) {
  // Store skills in global scope for handler to access
  if (window.skillGapUserSkills) {
    window.skillGapUserSkills = newSkills;
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { initSkillGapHandler, updateSkillGapUserSkills };
}
