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

All seven pages carry the same capture form and the same one-line switch:

```js
const FORM_ENDPOINT = '';
```

Empty means the form refuses to submit and says so honestly. It never pretends to
have captured an address it dropped.

## Steps

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

- [ ] Provider account exists
- [ ] `FORM_ENDPOINT` set in `assets/capture.js`
- [ ] Free-pages PDF uploaded and delivering
- [ ] "Not wired yet" copy replaced on all 7 pages
- [ ] Live end-to-end test passed with a real inbox
- [ ] First subscriber count recorded in `vault/private/ledger.md`

Related: [[Fehu Lab MOC]], [[Weekly review]]
