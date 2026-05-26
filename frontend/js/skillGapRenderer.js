/**
 * Skill Gap Analyzer - Results Rendering Module
 * 
 * Handles all UI rendering for skill gap analysis results.
 * Provides reusable rendering logic independent of career card implementation.
 */

/**
 * Render skill gap analysis results to specified container
 * 
 * @param {Object} data - Analysis result from API
 * @param {Array<string>} data.matched_skills - Skills user already has
 * @param {Array<Object>} data.missing_skills - Missing skills with priority levels
 * @param {number} data.proficiency_percentage - Overall proficiency percentage
 * @param {number} data.matched_count - Number of matched skills
 * @param {number} data.total_required - Total required skills
 * @param {Array<string>} data.suggestions - Learning suggestions
 * @param {string} careerName - Name of the career analyzed
 * @param {string} containerId - ID of container to render results in
 * 
 * @returns {void}
 * 
 * @example
 * renderSkillGapResults(apiData, "Frontend Developer", "skill-gap-results");
 */
function renderSkillGapResults(data, careerName, containerId) {
  const container = document.getElementById(containerId);

  if (!container) {
    console.error(`Container with ID "${containerId}" not found`);
    return;
  }

  // Clear previous results
  container.innerHTML = '';

  // Create header section
  const header = document.createElement('div');
  header.className = 'mb-4';
  header.innerHTML = `
    <div class="d-flex align-items-center justify-content-between mb-3">
      <h3 class="mb-0">
        <span class="material-symbols-outlined" style="color: var(--secondary); vertical-align: middle; margin-right: 0.5rem;">analytics</span>
        Skill Gap Analysis for ${careerName}
      </h3>
      <button class="btn btn-sm btn-outline-secondary" onclick="document.getElementById('${containerId}').innerHTML = '';">Close</button>
    </div>
    <div class="skill-gap-proficiency">
      <span class="skill-gap-proficiency-text">Your Current Proficiency:</span>
      <span class="skill-gap-proficiency-percent">${data.proficiency_percentage}%</span>
      <span class="skill-gap-proficiency-text"> (${data.matched_count}/${data.total_required} skills)</span>
    </div>
  `;
  container.appendChild(header);

  // Create three-column grid
  const cardsContainer = document.createElement('div');
  cardsContainer.className = 'skill-gap-row';

  // Matched Skills Card
  const matchedCard = document.createElement('div');
  matchedCard.className = 'glass-card skill-gap-card skill-gap-card-matched fade-in';
  matchedCard.style.animationDelay = '0s';
  matchedCard.innerHTML = `
    <div class="skill-gap-card-header">
      <span class="material-symbols-outlined">check_circle</span>
      <h5 class="skill-gap-card-title">Matched Skills (${data.matched_skills.length})</h5>
    </div>
    <div class="skill-gap-skills">
      ${data.matched_skills.length > 0
      ? data.matched_skills.map(skill => `<span class="skill-gap-skill-item skill-gap-skill-matched">✓ ${skill}</span>`).join('')
      : '<p style="color: var(--text-secondary); font-size: 0.85rem; margin: 0;">No matching skills yet. Start learning!</p>'
    }
    </div>
  `;
  cardsContainer.appendChild(matchedCard);

  // Missing Skills Card
  const missingCard = document.createElement('div');
  missingCard.className = 'glass-card skill-gap-card skill-gap-card-missing fade-in';
  missingCard.style.animationDelay = '0.1s';
  const missingSkillsHtml = data.missing_skills
    .map(s => `<span class="skill-gap-skill-item skill-gap-skill-missing ${s.priority === 'High' ? 'skill-gap-skill-high-priority' : ''}">${s.skill}</span>`)
    .join('');
  missingCard.innerHTML = `
    <div class="skill-gap-card-header">
      <span class="material-symbols-outlined">warning</span>
      <h5 class="skill-gap-card-title">Missing Skills (${data.missing_skills.length})</h5>
    </div>
    <div class="skill-gap-skills">
      ${missingSkillsHtml}
    </div>
    <small style="color: var(--text-secondary); margin-top: 0.5rem;">
      <strong>Darker red</strong> = High Priority | <strong>Light red</strong> = Medium/Low Priority
    </small>
  `;
  cardsContainer.appendChild(missingCard);

  // Suggestions Card
  const suggestionsCard = document.createElement('div');
  suggestionsCard.className = 'glass-card skill-gap-card skill-gap-card-suggestions fade-in';
  suggestionsCard.style.animationDelay = '0.2s';
  suggestionsCard.innerHTML = `
    <div class="skill-gap-card-header">
      <span class="material-symbols-outlined">lightbulb</span>
      <h5 class="skill-gap-card-title">Learning Path</h5>
    </div>
    <div>
      ${data.suggestions.map(suggestion => `<div class="skill-gap-suggestion-item">📚 ${suggestion}</div>`).join('')}
    </div>
  `;
  cardsContainer.appendChild(suggestionsCard);

  container.appendChild(cardsContainer);

  // Scroll to results
  container.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { renderSkillGapResults };
}
