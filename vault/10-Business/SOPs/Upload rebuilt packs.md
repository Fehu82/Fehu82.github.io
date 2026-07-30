---
type: sop
status: blocked-on-owner
priority: 1
tags:
  - fehu/sop
---

# Upload the rebuilt packs to Gumroad

> [!warning] Do this before the storefront previews go live
> The site now shows preview images rendered from the packs `tools/build_packs.py`
> produces. Until those same PDFs are the files behind the Gumroad checkout
> links, a buyer sees one thing and downloads another. That is the single thing
> this whole generator was built to avoid.

Nobody has bought yet — total revenue is $0.00 — so replacing the files harms no
existing customer. That window closes the moment the first sale lands.

## Steps

1. **Build the packs.**

   ```bash
   pip install reportlab pypdf pymupdf pillow
   python3 tools/build_packs.py
   ```

   Every pack must print `verified`. That check covers page count, uniform US
   Letter mediabox, 30 unique page content streams, and no ink outside the
   printable frame. If a pack fails, fix it before uploading — do not override.

2. **Look at the pages yourself.** Open each PDF and page through it. The
   verifier catches structural faults, not ugly ones. You are the taste check.

3. **Print one page from each pack** on the printer a buyer would plausibly use.
   Confirm nothing clips at the margins and the line weights hold up.

4. **Replace the file on each Gumroad product**, keeping the same product URL so
   every link on the site and in the vault keeps working:

   | Slug | Price |
   |---|---|
   | `bold-easy-coloring-pack` | $4.99 |
   | `cat-coloring-pack` | $4.99 |
   | `celestial-coloring-pack` | $6 |
   | `sacred-geometry-coloring-pack` | $6 |
   | `rune-coloring-pack` | $7 |

5. **Re-render the previews** if you changed anything after step 1, so the site
   and the product stay in step:

   ```bash
   python3 tools/render_previews.py <slug> assets/packs/<slug>.pdf --pages 1 2 3 4 5 6
   ```

6. **Buy one yourself** at the lowest price, download it, and diff it against
   your local build. This is the only step that actually proves the loop closed.

## Definition of done

- [ ] All five packs build and verify
- [ ] Every page visually reviewed
- [ ] One page from each pack test-printed
- [ ] All five Gumroad files replaced, URLs unchanged
- [ ] Previews re-rendered from the uploaded build
- [ ] One real purchase downloaded and checked against the local file

## Note on the sixth product

`night-drift-playbook` is not a coloring pack and is not generated. It is
untouched by any of this.

Related: [[Fehu Lab MOC]], [[Publish a product]]
