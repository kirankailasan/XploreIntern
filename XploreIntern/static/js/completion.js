document.addEventListener('DOMContentLoaded', function() {
  const progressCircles = document.querySelectorAll('.circular-progress');

  progressCircles.forEach(function(progressCircle) {
      const percentage = parseInt(progressCircle.dataset.percentage) || 0;
      const degrees = percentage * 3.6;  // Convert percentage to degrees

      // Get data attributes for colors
      const progressColor = progressCircle.dataset.progressColor || 'crimson';
      const bgColor = progressCircle.dataset.bgColor || 'lightgrey';

      // Update the percentage text
      const percentageText = progressCircle.querySelector('.percentage');
      if (percentageText) {
          percentageText.textContent = `${percentage}%`;
      }

      // Apply the conic-gradient for the circular progress
      progressCircle.style.background = `conic-gradient(${progressColor} ${degrees}deg, ${bgColor} ${degrees}deg)`;
  });
});
