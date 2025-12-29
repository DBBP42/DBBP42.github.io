document.addEventListener('DOMContentLoaded', function() {
  const cookieDisclaimer = document.getElementById('cookie-disclaimer');
  const cookieDismiss = document.getElementById('cookie-dismiss');

  if (cookieDisclaimer && cookieDismiss) {
    // Show disclaimer if not dismissed yet
    if (!localStorage.getItem('cookieDisclaimerDismissed')) {
      cookieDisclaimer.style.display = 'block';
    }

    // Dismiss and remember
    cookieDismiss.addEventListener('click', function() {
      cookieDisclaimer.style.display = 'none';
      localStorage.setItem('cookieDisclaimerDismissed', 'true');
    });
  }
});
