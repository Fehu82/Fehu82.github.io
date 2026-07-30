/* Fehu Lab email capture — one switch for the whole site.
 *
 * TO GO LIVE: paste your email provider's form-action URL into FORM_ENDPOINT
 * below. That single edit turns capture on across every page, because every
 * page loads this one file.
 *
 * Kit (ConvertKit):  https://app.kit.com/forms/<form-id>/subscriptions
 * MailerLite:        https://assets.mailerlite.com/jsonp/<account>/forms/<id>/subscribe
 * Buttondown:        https://buttondown.email/api/emails/embed-subscribe/<user>
 *
 * Full runbook: vault/10-Business/SOPs/Wire email capture.md
 *
 * Empty string = not wired. The form then refuses to submit and says so
 * plainly, rather than silently discarding an address someone typed in.
 */
const FORM_ENDPOINT = '';

(function () {
  var forms = document.querySelectorAll('form.capture');
  if (!forms.length) return;

  var NOT_WIRED =
    '<strong>Not wired yet</strong> — the owner still has to connect the email ' +
    'provider, so nothing was sent and nothing was stored. The 3 free pages go ' +
    'live here as soon as it is.';

  Array.prototype.forEach.call(forms, function (form) {
    if (FORM_ENDPOINT) {
      form.setAttribute('action', FORM_ENDPOINT);
      return;
    }
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      var note =
        form.parentNode.querySelector('#capture-note, .capture-note') ||
        document.getElementById('capture-note');
      if (note) note.innerHTML = NOT_WIRED;
    });
  });
})();
