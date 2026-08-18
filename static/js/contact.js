/**
 * Contact Form AJAX Submission - Al Bahaa Corporate Standard
 * Progressive Enhancement: Submits asynchronously without page reload
 */

document.addEventListener('DOMContentLoaded', () => {
  const formContainer = document.querySelector('.contact-form-container');
  const form = document.querySelector('.contact-form');

  if (!form || !formContainer) return;

  const submitBtn = form.querySelector('button[type="submit"]');
  const originalBtnText = submitBtn ? submitBtn.innerHTML : 'Submit Inquiry';

  function clearErrors() {
    form.querySelectorAll('.form-error-msg').forEach((el) => el.remove());
    form.querySelectorAll('.contact-form__errors').forEach((el) => el.remove());
  }

  function displayErrors(errors, generalMessage) {
    clearErrors();

    if (generalMessage) {
      const errorBanner = document.createElement('div');
      errorBanner.className = 'contact-form__errors';
      errorBanner.setAttribute('role', 'alert');
      errorBanner.textContent = generalMessage;
      form.insertBefore(errorBanner, form.querySelector('.contact-form__row'));
    }

    if (errors && typeof errors === 'object') {
      Object.keys(errors).forEach((fieldName) => {
        const input = form.querySelector(`[name="${fieldName}"]`);
        if (input) {
          const row = input.closest('.contact-form__row');
          if (row) {
            const errorMsg = document.createElement('span');
            errorMsg.className = 'form-error-msg';
            const fieldErrorArray = errors[fieldName];
            errorMsg.textContent = Array.isArray(fieldErrorArray) ? fieldErrorArray[0] : fieldErrorArray;
            row.appendChild(errorMsg);
          }
        }
      });
    }
  }

  function renderSuccessBox(message) {
    const successHtml = `
      <div class="contact-success-box" role="alert">
        <span class="contact-success-box__kicker">INQUIRY RECEIVED</span>
        <h2 class="contact-success-box__title">Thank you for reaching out.</h2>
        <span class="contact-success-box__rule" aria-hidden="true"></span>
        <p class="contact-success-box__desc">
          ${message || 'Your inquiry has been successfully transmitted to our engineering and business development committee. We will review your project requirements and respond promptly.'}
        </p>
        <a href="${window.location.href}" class="button button--solid contact-success-box__btn">Send Another Inquiry</a>
      </div>
    `;

    formContainer.innerHTML = successHtml;

    const rect = formContainer.getBoundingClientRect();
    if (rect.top < 80 || rect.bottom > window.innerHeight) {
      window.scrollTo({
        top: Math.max(0, rect.top + window.pageYOffset - 120),
        behavior: 'smooth',
      });
    }
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    clearErrors();

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = 'Submitting...';
      submitBtn.style.opacity = '0.75';
      submitBtn.style.cursor = 'not-allowed';
    }

    const formData = new FormData(form);
    const actionUrl = form.getAttribute('action') || window.location.href;
    const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]')?.value || '';

    try {
      const response = await fetch(actionUrl, {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'Accept': 'application/json',
          'X-CSRFToken': csrfToken,
        },
      });

      const data = await response.json().catch(() => ({}));

      if (response.ok && data.success) {
        renderSuccessBox(data.message);
      } else {
        displayErrors(data.errors, data.message || 'Please check the highlighted required fields.');
      }
    } catch (err) {
      console.error('Contact form submission error:', err);
      displayErrors({}, 'A network error occurred. Please verify your connection or try again.');
    } finally {
      if (submitBtn && form.isConnected) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnText;
        submitBtn.style.opacity = '1';
        submitBtn.style.cursor = 'pointer';
      }
    }
  });
});
