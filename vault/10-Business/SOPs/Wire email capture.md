---
type: sop
status: blocked-on-owner
priority: 1
tags:
  - fehu/sop
---

# Wire email capture

**This is the highest-value unfinished job on the site.** Every visitor who wants
the three free pages currently hits a form that stores nothing. The lead magnet
exists, the copy exists, the form exists — only the endpoint is missing.

## What is in place

All seven pages carry the same capture form and load one shared module,
`assets/capture.js`, with two constants at the top:

```js
const CAPTURE_TO = '';      // Mode A — zero signup
const FORM_ENDPOINT = '';   // Mode B — a real provider
```

Both empty means the form refuses to submit and says so honestly. It never
pretends to have captured an address it dropped. A honeypot field is injected
into every form, so bots that fill it are silently discarded without a request.

## Mode A — fastest, no account (about 2 minutes)

FormSubmit relays each address to an inbox you already own. No signup, no
dashboard, no card.

1. Set one line in `assets/capture.js`:

   ```js
   const CAPTURE_TO = 'you+fehulab@gmail.com';
   ```

   Use a dedicated address or a `+` alias. **That address is visible in a public
   file and harvesters will find it** — do not use your main one.

2. Push, then submit the form once on the live site. FormSubmit emails you a
   one-time confirmation link. Click it. Capture is live from that moment.

3. After activating, FormSubmit gives you a **hashed endpoint** that hides the
   address. Move it into `FORM_ENDPOINT` and clear `CAPTURE_TO`:

   ```js
   const CAPTURE_TO = '';
   const FORM_ENDPOINT = 'https://formsubmit.co/ajax/<your-hash>';
   ```

**What this does not do:** it collects addresses, it does not send the welcome
email or deliver the free-pages PDF. You reply by hand, or export and import into
a real provider later. That is fine — it stops the bleeding today, and a list of
50 addresses you email by hand beats a dead form.

## Mode B — the real thing

Worth doing once the list justifies it: these deliver the lead magnet and run the
welcome sequence for you, which Mode A does not.

1. **Pick a provider.** Any of these give a hosted form URL on a free tier:
   - **Kit (formerly ConvertKit)** — free to 10,000 subscribers, and it can
     auto-deliver a PDF on signup, which is exactly what this lead magnet needs.
     Recommended.
   - **MailerLite** — free to 1,000 subscribers, file delivery included.
   - **Buttondown** — plain-text feel that matches the Fehu Lab tone, smaller
     free tier.

2. **Build the form** in that provider and copy its **form action URL**. In Kit
   this looks like `https://app.kit.com/forms/<id>/subscriptions`.

3. **Set the endpoint once.** Edit `assets/capture.js` at the repo root:

   ```js
   const FORM_ENDPOINT = 'https://app.kit.com/forms/1234567/subscriptions';
   ```

   Every page loads that one file, so this single edit switches capture on
   site-wide. Nothing else needs touching.

4. **Upload the actual free-pages PDF** as the provider's incentive/delivery
   file. It must contain the three pages the copy promises: the Fehu wealth-rune
   mandala, the serpent-coil knotwork medallion, and the star-tetrahedron
   construction. If those exact pages are not what you send, change the copy on
   the site to match what you do send.

5. **Update the honest-status note.** With capture live, the "not wired yet"
   paragraph in each page is no longer true. Replace it with the privacy line:
   *"One welcome email with your pages, then only real product news.
   Unsubscribe anytime."*

6. **Test it end to end.** Submit your own address on the live site. Confirm the
   welcome email arrives and the PDF opens. Do not skip this — a broken delivery
   is worse than no form.

## Definition of done

Mode A (do this today):

- [ ] `CAPTURE_TO` set to a dedicated address in `assets/capture.js`
- [ ] Pushed, submitted once on the live site, confirmation link clicked
- [ ] Hashed endpoint swapped into `FORM_ENDPOINT`, `CAPTURE_TO` cleared
- [ ] "Not wired yet" copy replaced on all 7 pages
- [ ] First subscriber count recorded in `vault/private/ledger.md`

Mode B (when the list justifies it):

- [ ] Provider account exists
- [ ] `FORM_ENDPOINT` set in `assets/capture.js`
- [ ] Free-pages PDF uploaded and delivering
- [ ] Mode A addresses exported and imported
- [ ] Live end-to-end test passed with a real inbox

Related: [[Fehu Lab MOC]], [[Weekly review]]
