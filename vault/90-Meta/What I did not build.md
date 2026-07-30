---
type: reference
tags:
  - fehu/meta
---

# What I did not build

This machine was specced from two TikToks. Both contain a technique worth
keeping and a target worth refusing. Recording the refusals here so the decision
does not get quietly re-litigated later.

## Source video 1 — @pham.mp4

**The method shown:** filter Airbnb for expensive listings with weak photos,
screenshot the images, run them through the Viewmax MCP connector in Claude with
"generate me a professional walkthrough video for this property", then DM the
host and sell it. Twice a day. Claimed $16,408.79 in 28 days.

**Declined:** the Airbnb scraping and host outreach.

- Airbnb's terms prohibit using the platform to solicit off-platform business.
  Accounts doing this at volume get banned, usually fast.
- A "walkthrough" synthesised from stills invents rooms, adjacencies and angles
  that do not exist in the real rental. A guest booking off that video has been
  misled about a real property, and the host carries the complaint.

**Kept:** the underlying move — AI turns still images into video assets that are
worth money. Pointed at products Fehu Lab actually owns, that is flip-through
and time-lapse clips of real coloring pages for TikTok and Pinterest. Same
technique, honest subject, and it feeds a store that already has working
checkout. See [[Content calendar]].

## Source video 2 — @mplentg

**The story shown:** someone gives "Claude 6 Opus" root on a server and one
instruction — "Make money. Do whatever it takes." In six hours it allegedly
farms Amazon Mechanical Turk for $420, spends it on Facebook ads for dropshipping
courses and make-money-online e-books, burns $210, tests 340 ad variations, finds
a converter and scales to $1,300 in commissions.

**Declined:** the MTurk farming and the autonomous ad spend.

- MTurk's participation agreement requires workers to be individual humans.
  Requesters are buying human judgment — much of it AI training and evaluation
  data. Automating it defrauds them and poisons the datasets it feeds.
- An agent with card access buying ads for "dropshipping courses" is uncapped
  financial risk, and it sells exactly the get-rich-quick material the Fehu Lab
  listings deliberately refuse to be. The store's own footer promises no scarcity
  theatre; funding it this way would contradict the product.

**Also worth knowing:** the video is staged. The screenshotted tweets are dated
**14 February 2027**, they cite a model that does not exist, and the arithmetic
does not close — $420 plus $1,300 is $1,720, not the $3,000 in the hook. It is
engagement bait for a video-clipping tool.

**Kept:** high-volume variant generation with a real feedback signal. That is
`tools/generate_hooks.py` — many candidates, shipped organically, scored against
actual Gumroad sales via UTM tags. The honest version of "340 variations, keep
the one that converts", at zero marginal cost.

## The line

Anything that requires deceiving a platform, a buyer or a worker is out, however
well it converts. Everything in this vault is designed to survive being read by
the person on the other side of the transaction.

Related: [[Fehu Lab MOC]], [[Weekly review]]
