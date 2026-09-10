# www.teekaudio.com

Static site for **Teek Audio** — a tube amplifier workshop in Fond du Lac, Wisconsin.

Built from JSON content by a dependency-free Python script. Hosted on GitHub Pages.

## Build

```bash
python3 build.py
```

Requires Python 3.9+. Nothing to install.

Preview locally:

```bash
python3 build.py && python3 -m http.server 8000 --directory dist
```

## Editing

| What | Where |
|---|---|
| Business name, contact details, About copy | `content/site.json` |
| Service cards | `content/services.json` |
| Colours and type | top of `static/css/site.css` |
| Images | `static/img/` |

Push to `main` and GitHub Actions builds and deploys automatically. `dist/` is
generated, not committed.

## Heads up

The phone number and email address in `content/site.json` are **placeholders**
inherited from the old WordPress theme. They are deliberately excluded from the
site's structured data and flagged on the contact page until real details arrive.
See `CLAUDE.md`.

## Deployment

GitHub Pages via `.github/workflows/deploy.yml`. The repository must remain public.

DNS stays in Microsoft 365 — only two record types point here:

```
A     @     185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
CNAME www   galoryber.github.io
```
