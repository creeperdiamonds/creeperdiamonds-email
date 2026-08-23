# Creeperdiamonds Studios — email templates

Two files, one shared `assets/` folder.

| File | For |
|---|---|
| `creeperdiamonds-email.html` | Campaign / announcement sends. Modular blocks, merge tags, full footer. |
| `personal-note.html` | A one-to-one email you write yourself. |

Both are 600px, table-based and dark: a textured card floating on a starfield page, with an
emerald/cyan accent. See `preview.png` (campaign) and `preview-note.png` (note).

---

## `personal-note.html`

Everything that makes an email look automated is gone: no hero, no feature cards, no pull quote,
no eyebrow, no view-in-browser, no merge tags, and no unsubscribe/preferences/address block.
Those last three exist for commercial bulk mail; putting them on a genuine one-to-one note makes
it read as a mailshot, which defeats the purpose. (Not legal advice — if you're using it for
anything promotional to a list, use the campaign template instead, which has them.)

**It survives being pasted into Gmail or Outlook compose.** Those strip `<style>` blocks, so every
colour, size and space that matters is set inline on the elements themselves. The `<style>` block
holds only dark mode, the mobile media query, and client resets — nice to have, not load-bearing.
Verified: no element depends on a class without an inline equivalent. If you edit it, keep it that
way — don't hoist inline styles up into `<style>`.

Tuned for business correspondence rather than a casual note:

- **Linen surface, not facets** — see Textures below.
- **Animated logo mark.** Outlook on Windows freezes GIFs on frame 1, and frame 1 is a full
  legible composition, so it degrades to exactly the still. `logo-mark.png` is that still, left
  commented in the file if you want to drop the 137 KB.
- **The faceted stripe**, full-bleed under the letterhead — same seven segments and same palette
  as the campaign template, at 4px instead of 5px. Pure table cells, no image, so it renders
  identically everywhere including Outlook and with images blocked.
- **A real signature block**: name, role, studio, contact line.
- Quieter type: 15/27 body, tighter letterhead, more generous margins.

**Footer links** — website, GitHub and Discord, on one line below the closing rule. They replaced
the "Creeperdiamonds Studios" line that used to sit there; the studio name already appears in the
letterhead and in your role line, so repeating it a third time was noise.

**Recommended product block** — a bordered card appended *after* the signature, so it reads as
supplementary rather than interrupting the letter's argument. Label, product name, two-line
description, and a "Check it out" link.

Placeholder URLs to replace before sending:

| Placeholder | Where |
|---|---|
| `https://creeperdiamonds.xyz` | footer |
| `https://github.com/creeperdiamonds` | footer |
| `https://discord.gg/your-invite` | footer |
| `https://appealy.example/` | recommended product |
| `https://example.com` | the sample inline link in the body |

These are plain URLs, not merge tags — the note is hand-sent, and a `{{tag}}` pasted into Gmail
would arrive as literal text.

Fill in: greeting, three body paragraphs, and the signature. For maximum formality, delete the
`background`/`background-image` on `<body>` and the wrapper table plus the VML block — flat
`#060B18` is a perfectly good letterhead. There's an optional button commented out, but a plain
inline link reads better in a personal email.

To send it: open in a browser, select all, copy, paste into your compose window. Images need to be
hosted first, or the avatar arrives broken — see "Before you send" below.

---

## Before you send: two things that will bite you

**1. Images are hosted — already done.** Both templates now reference absolute URLs served by
GitHub Pages from this repo:

```
https://creeperdiamonds.github.io/creeperdiamonds-email/assets/<filename>
```

That means they load anywhere — on your phone, in a forwarded copy, in any inbox. Relative paths
would only have resolved when the HTML sat beside its `assets/` folder, which is never true in an
inbox.

Do **not** use `github.com/creeperdiamonds/creeperdiamonds-email/tree/main/assets/...` — that is
GitHub's web UI page for a directory and returns HTML, so a mail client gets a webpage instead of
a PNG. Only Pages (above) and `raw.githubusercontent.com` serve real image bytes; Pages is
preferred because raw is rate-limited and GitHub discourages hotlinking it.

`host-assets.py` switches where the images point, rewriting all 33 references in place across all
four reference types — `src`, the `background` attribute, inline `background-image`, and the
Outlook VML `v:fill src`, which is easy to miss by hand:

```
python host-assets.py            # show where they currently point
python host-assets.py pages      # GitHub Pages (current)
python host-assets.py raw        # raw.githubusercontent.com
python host-assets.py local      # back to relative, for offline editing
python host-assets.py https://your.cdn/path
```

It refuses a non-HTTPS base and warns if a referenced file is missing from `assets/`.

### Preview on your phone

Pages serves the templates themselves too, so you can open either one in a phone browser without
sending anything:

- https://creeperdiamonds.github.io/creeperdiamonds-email/personal-note.html
- https://creeperdiamonds.github.io/creeperdiamonds-email/creeperdiamonds-email.html

That is a browser preview, not an inbox preview — a real client will still strip the `<style>`
block and may block the images. It is the fastest way to check layout and the animated mark on a
real screen.

Even correctly hosted, **many clients block remote images until the recipient clicks "show
images."** That is expected, and it's why every textured surface carries a flat `bgcolor` fallback.
The email is designed to read properly with zero images loaded.

The campaign hero is real key art now: `assets/hero-keyart.jpg`, composed from the CapCut master.
The master is square 1080×1080, so a straight crop to 1200×630 would have cut off either the
character's head or the caption. Instead the artwork sits sharp and full-height in the centre, on
a heavily blurred and darkened copy of itself scaled to fill the width, with the two vertical
seams feathered so the centre panel doesn't look pasted on. JPEG at q78 — 79 KB, 8× smaller than
the PNG, and it's photographic content so JPEG is the right format.

**2. Do not hotlink the Google avatar URL.** The `lh3.googleusercontent.com/ogw/...` URL is a
Google *account* avatar endpoint. Those tokens rotate, and when one does, every email you have
ever sent shows a broken image forever. It also serves the older, watermarked cut of the artwork.
Host the files in `assets/` instead — they come from the CapCut master.

---

## Merge tags

Written in generic `{{ handlebars }}`. Find-and-replace for your platform:

| In the file | Mailchimp | SendGrid | Brevo | Klaviyo |
|---|---|---|---|---|
| `{{first_name}}` | `*|FNAME|*` | `{{first_name}}` | `{{contact.FIRSTNAME}}` | `{{ first_name }}` |
| `{{view_in_browser_url}}` | `*|ARCHIVE|*` | `<%asm_group_unsubscribe_raw_url%>` † | `{{ mirror }}` | `{% web_view %}` |
| `{{unsubscribe_url}}` | `*|UNSUB|*` | `<%asm_group_unsubscribe_raw_url%>` | `{{ unsubscribe }}` | `{% unsubscribe %}` |
| `{{preferences_url}}` | `*|UPDATE_PROFILE|*` | `<%asm_preferences_raw_url%>` | `{{ update_profile }}` | `{% manage_preferences %}` |
| `{{company_address}}` | `*|LIST:ADDRESS|*` | `<%asm_address%>` | *(set in sender profile)* | `{% organization %}` |
| `{{current_year}}` | `*|CURRENT_YEAR|*` | *(hardcode)* | *(hardcode)* | `{{ now|date:"Y" }}` |
| `{{issue_label}}` | *(free text)* | *(free text)* | *(free text)* | *(free text)* |
| `{{cta_url}}`, `{{card_1_url}}`, `{{card_2_url}}` | *(free text)* | *(free text)* | *(free text)* | *(free text)* |
| `{{url_site}}`, `{{url_discord}}`, `{{url_youtube}}`, `{{url_press}}` | *(free text)* | *(free text)* | *(free text)* | *(free text)* |

† SendGrid has no first-class view-in-browser tag; most people drop that line or link to a hosted
copy of the campaign.

`{{first_name}}` needs a fallback or the greeting reads "Hey ," for anyone missing the field.
Mailchimp: `*|IF:FNAME|*Hey *|FNAME|* — *|ELSE:|*Hey — *|END:IF|*`.

---

## Blocks

Every section is a top-level `<tr>` marked `<!-- BLOCK: ... -->`. Delete or duplicate whole `<tr>`s.

| Block | What it is |
|---|---|
| Preheader | The grey preview line next to the subject. **Rewrite this every send** — it is the second-most-read text in the email after the subject line. The `&#847;&zwnj;` run after it stops Gmail from padding the preview with body copy. |
| View in browser | Optional. Drop it if your ESP has no archive tag. |
| Header | Avatar + wordmark. |
| Faceted stripe | Brand device. Pure table cells — no image, renders everywhere. |
| Hero | Image, eyebrow, H1, two paragraphs, CTA button. |
| Two-up cards | Stacks to one column under 620px. Duplicate the whole `<tr>` pair for more rows. |
| Callout | Pull quote with an accent rule. |
| Footer | Wordmark, links, legal, unsubscribe. |

## Textures

Both templates are dark and textured. `preview.png` shows the result.

| Surface | Texture | Flat fallback | Bytes |
|---|---|---|---|
| Page (both files) | `assets/bg-stars.png` — seamless starfield with faint nebula | `#060B18` | 22 KB |
| Campaign card | `assets/bg-panel.png` — seamless low-poly facets | `#151F34` | 12 KB |
| Note card | `assets/bg-linen.png` — seamless fine weave | `#121A2B` | 2 KB |

The note uses linen rather than facets on purpose: a low-poly pattern under body copy reads as a
game asset, which is the wrong note for business correspondence. Linen's luminance range is 8
levels (facets are 14), so it registers as material rather than pattern.

Both are generated, seamlessly tiling, and deliberately low-contrast. The panel's entire luminance
range is 23–37 out of 255 — narrow enough that no facet can swallow text. Verified by measuring
the seam against a normal neighbouring column: 0.04 vs 0.05, i.e. the wrap is indistinguishable
from anywhere else in the tile.

### The three-part pattern

Every textured `<td>` carries all three of these. Do not drop any one of them:

```html
<td background="assets/bg-panel.png"        <!-- Gmail, Yahoo            -->
    bgcolor="#151F34"                       <!-- Outlook, images blocked -->
    style="background-color:#151F34; background-image:url('assets/bg-panel.png'); background-repeat:repeat;">
```

The `bgcolor` is the one that matters most. Outlook desktop ignores CSS background images
completely, and images are blocked by default in much of Gmail and Outlook — in both cases the
flat colour is all anyone sees. Each fallback is the measured mean of its own texture (`#151F34`
is literally the panel's average pixel), so the flat version reads as a deliberate design rather
than a broken one.

The page background additionally has a VML `<v:background>` block for Outlook. Its `src` needs an
absolute `https://` URL to work at all; unhosted, Outlook shows flat `#060B18`, which is fine.

## Colours

| Token | Value | Contrast on panel |
|---|---|---|
| Page | `#060B18` | — |
| Card | `#151F34` | — |
| Heading | `#E9EEF9` | 12.6:1 |
| Body | `#C2CCDF` / `#C8D2E4` | 9.1:1 |
| Muted | `#94A2BC` | 5.7:1 |
| Accent | `#2DD4A7` | 7.8:1 |
| Separators | `#5F6E8C` | 2.9:1 (decorative only) |
| Button | `#2DD4A7` fill, `#06231A` label | 8.8:1 |

Every ratio above is measured against the texture's **lightest** pixel, not its average — that's
the worst case a glyph can land on. All body and heading text clears AAA; muted text clears AA.

The button inverted when the design went dark: bright accent fill with a near-black label, rather
than white on dark green. White on `#2DD4A7` is only 2.5:1 and would have failed outright.

## What's already handled

- Outlook 2016–2021 (Word engine): VML `roundrect` CTA, ghost table wrapper, `mso-table-lspace`
  resets, `mso-line-height-rule:exactly` on type, 96 DPI pinned so it doesn't scale up 25%.
- Dark mode via `prefers-color-scheme` plus `[data-ogsc]` for Outlook.com.
- iOS/Gmail auto-link suppression (stops dates and addresses turning brand-blue).
- Mobile stacking at 620px; single-column, 24px gutters.
- `role="presentation"` on layout tables, real `alt` text, `role="article"` landmark.
- Images-off: the hero has a dark `background-color` behind it and the wordmark, footer mark and
  all nav links are live text, so nothing structural depends on an image loading.

## Assets

Both are built from the CapCut master (`1080×1080`, 30 fps, 3.02 s), not from the Google avatar
GIF. No imgPlay watermark, no crop needed — the master's caption already reads "CREEPERDIAMONDS
STUDIOS", so the same mark works for server sends and everything else.

| File | Display | Bytes | Use |
|---|---|---|---|
| `assets/logo-animated.gif` | 52×52 | 133 KB | 160×160, 28 frames. **Wired in by default.** |
| `assets/logo-mark.png` | 52×52 | 39 KB | Frame 1 as a still. Swap comment in either header. |
| `assets/hero-keyart.jpg` | 600×315 | 79 KB | Campaign hero, 1200×630 source for retina. |
| `assets/appealy-icon.png` | 40×40 | 3 KB | Appealy's own icon, from `brand/icon.svg` in its repo, rasterised because Gmail and Outlook strip SVG. |

### Timeline

The GIF is retimed to match the original avatar GIF exactly: **28 frames × 30 ms = 840 ms**, looping
forever. That is a ~3.6× speed-up over the 3.02 s master, which is what the original did too.

The frame mapping was measured, not assumed — each of the original GIF's 28 frames was matched
against all 90 master frames by lowest mean-squared error over the region above the caption (the
caption text differs between versions, so including it would have poisoned the match). The result
was a clean linear fit: original frame *n* → master frame `7 + 3.037n`, stepping by 3 every time.
So the original sampled master frames **7 → 89**, and this GIF samples exactly those same frames.
Frames 0–6 are just more sparkles — no intro or fade is being clipped.

30 ms is exactly 3 centiseconds, and GIF stores delays in centiseconds, so the timing is exact
rather than rounded.

### Encoding

Two-pass ffmpeg `palettegen`/`paletteuse`, 128 colours, `diff_mode=rectangle`, **dithering off**.
Turning dithering off halved the file (266 KB → 133 KB): the background is nearly static, and
dither noise destroys the inter-frame redundancy GIF depends on. Cost is a mean error of 4.36/255
against the source — about 1.7%, with no visible banding on the Earth gradient.

Smaller versions are a one-line change if you want them: 128×128 is 94 KB, 104×104 is 65 KB.
104 is still 2× the 52px display slot, so it stays sharp on retina screens.

Outlook on Windows shows frame 1 and ignores the rest — that's why frame 1 is a full, legible
composition rather than a mid-animation frame.

## Test before you send

Litmus or Email on Acid if you have one. If not, the cheap version that catches most of it:
Gmail web, Gmail Android app, Apple Mail on iPhone, and Outlook 2019+ on Windows. That last one
is where table-based layouts actually break.
