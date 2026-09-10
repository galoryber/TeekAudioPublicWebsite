# Teek Audio — site guide for Claude

Static site for **www.teekaudio.com**. A tube amplifier workshop in Fond du Lac,
Wisconsin: custom builds, repairs, and restoration.

This replaces a WordPress 6.8.8 site that ran on an EC2 instance.

## The one thing to know

**All content lives in `content/*.json`.** Edit JSON, run the build, commit.

```bash
python3 build.py     # content/ + static/  ->  dist/
```

Pure standard library. No pip install, no node_modules.

`dist/` is **gitignored here** — GitHub Actions builds it on every push. That is
the opposite of the Random Riot repo, which commits `dist/` because Cloudflare
serves the directory as-is. Don't copy that pattern over; it isn't needed when
the runner does the build, and it means a JSON edit from github.com or a phone
is enough to publish.

## Contact details are placeholders — read this before touching them

`+1-800-123-4567` and `info@teekaudio.com` in `content/site.json` are **not real**.
They came from the original WordPress theme. The client knows and is expected to
supply real details; until then the placeholders ship deliberately.

Two guards exist because of this, and both must stay:

1. `contact_details_are_placeholders: true` in `site.json` **omits phone and email
   from the LocalBusiness JSON-LD**. Publishing a fake phone number as structured
   data feeds it to Google Business listings and map providers, which is much
   harder to walk back than a line of page text.
2. The contact page renders a visible note saying the details are not yet live.

When the real details arrive: replace the values, set the flag to `false`, and
delete the `PLACEHOLDER_NOTE` key. Both guards then switch off on their own.

**Do not invent a phone number or email.** If asked to make the site look
finished, leave these alone and say why.

## Content

- `content/site.json` — name, tagline, contact details, About copy, the
  "why choose us" list.
- `content/services.json` — service cards. Each needs `name`, `image`, `summary`,
  `body`. `image` is a filename in `static/img/`.

Copy was carried over from the WordPress site and lightly tightened. It is the
client's own marketing language — don't rewrite it wholesale without asking.

## Design

Palette is derived from the subject: the amber glow of a heated filament, the
blue-violet cast inside the glass, and the near-black of a workshop with the
lights down. Tokens at the top of `static/css/site.css`:

- ground `#0d0b0a` · amber `#ff9a3c` / `#ffb867` · violet `#7b8ede` · cream `#f4ede3`

Amber is the action colour — buttons, links, the eyebrow labels. Violet is used
sparingly (the numbered list, the placeholder notice) so it stays a secondary
note rather than competing.

Fonts are **self-hosted** in `static/fonts/`: Archivo for display, Barlow for
body. Do not swap these for a Google Fonts `<link>`.

## Images

All images are stock photographs inherited from the WordPress site, downsized and
stripped of metadata. **There are no real photos of the client's work yet.** If any
arrive they should replace the stock immediately — a photo of an actual amp on an
actual bench is worth more than every stock tube on the site.

The WordPress site also used clip-art waveform glyphs. Those were deliberately
dropped.

## Deployment

GitHub Pages, built and deployed by `.github/workflows/deploy.yml` on every push
to `main`. The repo must stay **public** — Pages on the Free plan cannot publish
from a private repo.

DNS lives in Microsoft 365 (`ns*.bdm.microsoftonline.com`) and **stays there**.
M365 has no API for arbitrary DNS records, so those are edited by hand. The
records that point the domain here:

```
A     @     185.199.108.153 / .109.153 / .110.153 / .111.153
CNAME www   galoryber.github.io
```

`www` is the canonical hostname (matching what WordPress did), and GitHub Pages
redirects the apex to it automatically. `dist/CNAME` must keep saying
`www.teekaudio.com`.

Nothing about the Microsoft 365 mail records (MX, SPF, autodiscover, Teams) is
touched by any of this. Leave them alone.

## Gotchas

- The old WordPress site had a working contact form. A static site cannot process
  form posts — the contact page uses `mailto:` instead. If the client wants a real
  form, that needs a third-party endpoint (Formspree or similar), not a rewrite.
- The original copy invites visitors to "browse our portfolio". There is no
  portfolio page, because there is no work to show yet. That line was cut rather
  than linking somewhere empty.
- teekaudio.com has no DMARC record. Unrelated to this site, but worth raising.
