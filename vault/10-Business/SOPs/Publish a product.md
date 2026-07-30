---
type: sop
tags:
  - fehu/sop
---

# Publish a product

From finished PDF to live listing. Follow in order; step 6 is the one that is
easy to skip and expensive to skip.

## 1. Verify the file

- Correct page count, uniform page size, every page unique
- Opens in a normal PDF reader and prints clean on US Letter at home-printer DPI
- Record the verification in the product note's `## Notes` section

## 2. Create the Gumroad product

Slug must match the site directory exactly — `tools/sync_products.py` and every
UTM link depend on that. Set the price, upload the PDF, publish.

## 3. Build the page

Copy the closest existing product directory (`rune-coloring-pack/` is the fullest
example) and update:

- `<title>`, `<meta name="description">`, canonical, OG tags
- The JSON-LD `Product` block — **name, description, price and offer URL must
  match Gumroad exactly**, or the structured data is wrong and search engines
  will eventually notice
- Hero copy, "what's inside", details table
- The AI disclosure — every Fehu Lab product carries it

## 4. Render real previews

```bash
python3 tools/render_previews.py <slug> path/to/real.pdf --pages 1 4 7 16 22 30
```

Paste the printed `<figure>` block into the page's gallery. **Previews must be
pages from the file the buyer downloads.** Generated look-alike art that is not
in the product misrepresents what is being sold.

## 5. Wire it into the site

- Add a card to `index.html`
- Add `<loc>` to `sitemap.xml` with today's `lastmod`
- Add it to the related-products strip on the other product pages
- Confirm the Gumroad link carries `?utm_source=site&utm_medium=product-page&utm_content=<slug>`

## 6. Sync and generate

```bash
python3 tools/sync_products.py
python3 tools/generate_hooks.py <slug>
python3 tools/generate_pins.py <slug>
```

Add it to [[Content calendar]].

## Definition of done

- [ ] Live on Gumroad, checkout tested with a real card or a $0 test
- [ ] Page live, previews real, no blank figures
- [ ] JSON-LD matches Gumroad
- [ ] In sitemap, in landing page, in cross-links
- [ ] Vault note exists, hooks and pins generated

Related: [[Fehu Lab MOC]], [[Weekly review]]
