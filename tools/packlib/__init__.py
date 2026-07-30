"""packlib — generative line art for Fehu Lab printable coloring packs.

Every page is clean black outline on white: no fills, no grayscale, no shading.
Output is vector, so it stays crisp at any home-printer resolution.

Generation is deterministic. A pack built from the same seed is byte-comparable
page for page, which is what makes "the previews are real pages from the product"
a checkable claim rather than a promise.
"""

from .page import Page, LETTER_W, LETTER_H, W_OUTLINE, W_DETAIL, W_ACCENT

__all__ = ["Page", "LETTER_W", "LETTER_H", "W_OUTLINE", "W_DETAIL", "W_ACCENT"]
