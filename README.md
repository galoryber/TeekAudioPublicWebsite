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

There is **no phone number** on this site. The one in the old WordPress theme was a
placeholder (`+1-800-123-4567`) and was removed rather than published. Contact is by
email only until the client supplies a real number — at which point adding
`phone_display` and `phone_href` to `content/site.json` is all that is needed.

## Deployment

GitHub Pages via `.github/workflows/deploy.yml`. The repository must remain public.

DNS stays in Microsoft 365 — only two record types point here:

```
A     @     185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
CNAME www   galoryber.github.io
```
