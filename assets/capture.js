/* Fehu Lab email capture — one config block for the whole site.
 *
 * Three modes. Set exactly one of the two constants below.
 *
 * ── Mode A: CAPTURE_TO ────────────────────────────────────────────────────
 * Zero-signup. Point it at an inbox and FormSubmit relays each address there:
 *
 *     const CAPTURE_TO = 'you@example.com';
 *
 * The very first submission triggers a one-time confirmation email to that
 * address; click the link in it and capture is live forever. No account, no
 * dashboard, no card.
 *
 * Two things to know before choosing this:
 *   1. The address is visible in this file, which is public. Harvesters will
 *      find it. Use a dedicated address, not your main one — a Gmail alias
 *      like you+fehulab@gmail.com works and can be filtered.
 *   2. FormSubmit collects addresses; it does not send newsletters or deliver
 *      the free-pages PDF automatically. You reply, or you export and import
 *      into a real provider later. Good enough to stop losing leads today.
 *   After activating, FormSubmit gives you a hashed endpoint that hides the
 *   address — swap it into FORM_ENDPOINT below and delete CAPTURE_TO.
 *
 * ── Mode B: FORM_ENDPOINT ─────────────────────────────────────────────────
 * Any real provider's form-action URL. Better long-term: these deliver the
 * lead magnet and run the welcome sequence for you.
 *
 *   Kit (ConvertKit)  https://app.kit.com/forms/<form-id>/subscriptions
 *   MailerLite        https://assets.mailerlite.com/jsonp/<acct>/forms/<id>/subscribe
 *   Buttondown        https://buttondown.email/api/emails/embed-subscribe/<user>
 *   FormSubmit hashed https://formsubmit.co/ajax/<hash>
 *
 * ── Mode C: neither set ───────────────────────────────────────────────────
 * Capture is off. The form refuses to submit and says so plainly, rather than
 * silently discarding an address someone typed in.
 *
 * Runbook: vault/10-Business/SOPs/Wire email capture.md
 */
const CAPTURE_TO = '';
const FORM_ENDPOINT = '';

(function () {
  'use strict';

  var forms = document.querySelectorAll('form.capture');
  if (!forms.length) return;

  var MESSAGES = {
    notWired:
      '<strong>Not wired yet</strong> — the owner still has to connect the email ' +
      'provider, so nothing was sent and nothing was stored. The 3 free pages go ' +
      'live here as soon as it is.',
    sending: 'Sending…',
    ok:
      '<strong>Check your inbox.</strong> Your free pages are on the way. If ' +
      'nothing arrives in a few minutes, look in spam — then tell us and we will ' +
      'send them by hand.',
    failed:
      '<strong>That did not go through.</strong> Nothing was stored. Please try ' +
      'again in a moment.'
  };

  function noteFor(form) {
    return (
      form.parentNode.querySelector('#capture-note, .capture-note') ||
      document.getElementById('capture-note')
    );
  }

  function say(form, html) {
    var note = noteFor(form);
    if (!note) return;
    note.innerHTML = html;
    // Screen readers should hear the result; the note is not focused.
    note.setAttribute('role', 'status');
    note.setAttribute('aria-live', 'polite');
  }

  function setBusy(form, busy) {
    var button = form.querySelector('button[type=submit]');
    if (!button) return;
    button.disabled = busy;
    button.style.opacity = busy ? '0.6' : '';
  }

  // Bot bait. Real people never see it, so anything that fills it is a bot.
  function addHoneypot(form) {
    if (form.querySelector('input[name=_honey]')) return;
    var honey = document.createElement('input');
    honey.type = 'text';
    honey.name = '_honey';
    honey.tabIndex = -1;
    honey.setAttribute('autocomplete', 'off');
    honey.setAttribute('aria-hidden', 'true');
    honey.style.cssText =
      'position:absolute;left:-9999px;width:1px;height:1px;opacity:0';
    form.appendChild(honey);
  }

  function ajaxEndpoint() {
    if (CAPTURE_TO) return 'https://formsubmit.co/ajax/' + encodeURIComponent(CAPTURE_TO);
    if (FORM_ENDPOINT && FORM_ENDPOINT.indexOf('formsubmit.co/ajax/') !== -1) {
      return FORM_ENDPOINT;
    }
    return null;
  }

  Array.prototype.forEach.call(forms, function (form) {
    addHoneypot(form);

    var endpoint = ajaxEndpoint();

    // Mode B with a non-AJAX provider: plain form POST, browser handles it.
    if (!endpoint && FORM_ENDPOINT) {
      form.setAttribute('action', FORM_ENDPOINT);
      return;
    }

    form.addEventListener('submit', function (event) {
      event.preventDefault();

      // Mode C — nothing configured.
      if (!endpoint) {
        say(form, MESSAGES.notWired);
        return;
      }

      // Honeypot tripped: pretend it worked, store nothing.
      if ((form.querySelector('input[name=_honey]') || {}).value) {
        say(form, MESSAGES.ok);
        return;
      }

      var email = (form.querySelector('input[type=email]') || {}).value || '';
      if (!email) return;

      setBusy(form, true);
      say(form, MESSAGES.sending);

      fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({
          email: email,
          _subject: 'Fehu Lab — free pages request',
          _template: 'table',
          _captcha: 'false',
          source: window.location.pathname
        })
      })
        .then(function (response) {
          if (!response.ok) throw new Error('HTTP ' + response.status);
          return response.json();
        })
        .then(function () {
          form.reset();
          say(form, MESSAGES.ok);
        })
        .catch(function () {
          say(form, MESSAGES.failed);
        })
        .then(function () {
          setBusy(form, false);
        });
    });
  });
})();
