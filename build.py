#!/usr/bin/env python3
"""
Teek Audio static site builder.

Reads JSON from content/, copies static/, writes finished HTML to dist/.
Pure standard library — no pip install, no node_modules, nothing to rot.

    python3 build.py
"""

from __future__ import annotations

import datetime as dt
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
STATIC = ROOT / "static"
DIST = ROOT / "dist"

NAV = [("/", "Home"), ("/about/", "About"), ("/services/", "Services"), ("/contact/", "Contact")]


def load(name: str):
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))


def e(text) -> str:
    return html.escape(str(text if text is not None else ""), quote=True)


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def layout(*, site, title, description, path, body):
    nav = "\n".join(
        f'          <a href="{href}"{" aria-current=\"page\"" if href == path else ""}>{e(label)}</a>'
        for href, label in NAV
    )
    footer_nav = "\n".join(f'            <a href="{href}">{e(label)}</a>' for href, label in NAV)
    canonical = site["url"].rstrip("/") + path
    year = dt.date.today().year

    jsonld = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": site["name"],
        "url": site["url"],
        "description": site["description"],
        "address": {"@type": "PostalAddress", "addressLocality": "Fond du Lac",
                    "addressRegion": "WI", "addressCountry": "US"},
    }
    # Contact details are placeholders until the client supplies real ones. Publishing
    # them as structured data would feed a fake phone number to search engines and
    # map listings, which is far harder to walk back than a line of page text.
    if not site.get("contact_details_are_placeholders"):
        jsonld["telephone"] = site["phone_href"]
        jsonld["email"] = site["email"]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">
  <link rel="canonical" href="{e(canonical)}">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{e(site["name"])}">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:url" content="{e(canonical)}">
  <meta property="og:image" content="{e(site["url"])}/img/og-image.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#0d0b0a">

  <link rel="icon" href="/img/favicon.svg" type="image/svg+xml">
  <link rel="preload" href="/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/css/site.css">
  <script type="application/ld+json">
{json.dumps(jsonld, indent=2)}
  </script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>

  <header class="site-header">
    <div class="wrap">
      <a class="brand" href="/">
        <span class="brand-mark">Teek<em>Audio</em></span>
        <span class="brand-sub">Fond du Lac, WI</span>
      </a>
      <nav class="nav" aria-label="Main">
{nav}
      </nav>
    </div>
  </header>

  <main id="main">
{body}
  </main>

  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-grid">
        <div>
          <p style="margin:0 0 6px"><strong>{e(site["name"])}</strong> — {e(site["hometown"])}</p>
          <p style="margin:0">Tube amp builds, repairs, and restoration.</p>
        </div>
        <nav class="nav" aria-label="Footer">
{footer_nav}
        </nav>
      </div>
      <p class="footer-legal">© {year} {e(site["name"])}. All rights reserved.</p>
    </div>
  </footer>
</body>
</html>
"""


def cta(site):
    return f"""    <section class="cta">
      <div class="wrap">
        <h2>Let's amplify your sound</h2>
        <p>Whether you are chasing a tone you can already hear in your head or trying to
           bring a tired amp back to life, tell us what you are after.</p>
        <a class="btn btn-primary" href="/contact/">Start a conversation</a>
      </div>
    </section>"""


def page_home(site, services):
    cards = "\n".join(f"""        <article class="card">
          <img src="/img/{e(s["image"])}" alt="" loading="lazy" width="1600" height="1067">
          <div class="card-body">
            <h3>{e(s["name"])}</h3>
            <p class="summary">{e(s["summary"])}</p>
            <p>{e(s["body"])}</p>
          </div>
        </article>""" for s in services[:2])

    reasons = "\n".join(f"""        <li>
          <span class="n">{i:02d}</span>
          <span><strong>{e(t)}</strong><span class="text">{e(d)}</span></span>
        </li>""" for i, (t, d) in enumerate(site["why_us"], 1))

    body = f"""    <section class="hero">
      <div class="hero-bg">
        <img src="/img/hero-tubes.jpg" alt="" fetchpriority="high" width="2400" height="1631">
      </div>
      <div class="wrap">
        <p class="eyebrow">Fond du Lac, Wisconsin</p>
        <h1>Unleash the <span class="glow">power of sound</span></h1>
        <p class="lede">{e(site["intro_lede"])}</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="/services/">What we do</a>
          <a class="btn btn-ghost" href="/contact/">Get in touch</a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="eyebrow">Our expertise</p>
        <h2>What we build, and what we bring back</h2>
        <p class="sub">Two things we do more than anything else.</p>
        <div class="grid grid-2">
{cards}
        </div>
        <p style="margin-top:30px"><a class="btn btn-ghost" href="/services/">All services</a></p>
      </div>
    </section>

    <section class="section section-alt">
      <div class="wrap">
        <p class="eyebrow">Why choose us</p>
        <h2>Five things you can count on</h2>
        <ul class="reasons">
{reasons}
        </ul>
      </div>
    </section>

{cta(site)}"""

    return layout(site=site, path="/",
                  title=f'{site["name"]} — {site["tagline"]}',
                  description=site["description"], body=body)


def page_about(site):
    paras = "\n".join(f"          <p>{e(p)}</p>" for p in site["about"])
    body = f"""    <div class="page-head">
      <div class="wrap">
        <p class="eyebrow">About</p>
        <h1>What we do</h1>
        <p>Custom builds, repairs, and restoration out of Fond du Lac, Wisconsin.</p>
      </div>
    </div>

    <section class="section">
      <div class="wrap">
        <div class="split">
          <div class="prose">
{paras}
          </div>
          <img src="/img/tubes-blue.jpg" alt="Vacuum tubes glowing in a darkened amplifier chassis"
               loading="lazy" width="1600" height="951">
        </div>
      </div>
    </section>

{cta(site)}"""
    return layout(site=site, path="/about/",
                  title=f'About — {site["name"]}',
                  description=f'Teek Audio is a tube amplifier workshop in {site["hometown"]}, building custom amps and repairing vintage and modern gear.',
                  body=body)


def page_services(site, services):
    cards = "\n".join(f"""        <article class="card">
          <img src="/img/{e(s["image"])}" alt="" loading="lazy" width="1600" height="1067">
          <div class="card-body">
            <h3>{e(s["name"])}</h3>
            <p class="summary">{e(s["summary"])}</p>
            <p>{e(s["body"])}</p>
          </div>
        </article>""" for s in services)

    body = f"""    <div class="page-head">
      <div class="wrap">
        <p class="eyebrow">Services</p>
        <h1>Everything we take on</h1>
        <p>From a one-off build to a rack of amplifiers that has to work every night.</p>
      </div>
    </div>

    <section class="section">
      <div class="wrap">
        <div class="grid grid-2">
{cards}
        </div>
      </div>
    </section>

{cta(site)}"""
    return layout(site=site, path="/services/",
                  title=f'Services — {site["name"]}',
                  description="Custom tube amplifier builds, repairs, and residential and commercial amplification services from Teek Audio.",
                  body=body)


def page_contact(site):
    placeholder_notice = ""
    if site.get("contact_details_are_placeholders"):
        placeholder_notice = """
          <p class="notice"><strong>Note:</strong> these contact details are
          placeholders and are not yet live. Replace them in
          <code>content/site.json</code> before this site goes to production.</p>"""

    body = f"""    <div class="page-head">
      <div class="wrap">
        <p class="eyebrow">Contact</p>
        <h1>Start a conversation</h1>
        <p>Tell us what you are working with and what you want it to sound like. The more
           detail you can give us up front, the more useful our first reply will be.</p>
      </div>
    </div>

    <section class="section">
      <div class="wrap">
        <div class="split" style="align-items:start">
          <div>
            <ul class="contact-list">
              <li>
                <span class="label">Phone</span>
                <span class="value"><a href="tel:{e(site["phone_href"])}">{e(site["phone_display"])}</a></span>
              </li>
              <li>
                <span class="label">Email</span>
                <span class="value"><a href="mailto:{e(site["email"])}">{e(site["email"])}</a></span>
              </li>
              <li>
                <span class="label">Based in</span>
                <span class="value">{e(site["hometown"])}</span>
              </li>
            </ul>
{placeholder_notice}
          </div>
          <div>
            <h2 style="font-family:var(--display);font-weight:700;font-size:1.2rem;margin:0 0 12px">
              What to include</h2>
            <ul style="color:var(--text-muted);padding-left:20px;margin:0 0 24px">
              <li>Make and model, if you know it</li>
              <li>What it is doing now — hum, crackle, no sound, or nothing wrong at all</li>
              <li>For a build: the sound you are chasing, and what you play</li>
              <li>Whether you can drop it off or need to ship it</li>
            </ul>
            <a class="btn btn-primary" href="mailto:{e(site["email"])}">Email us</a>
          </div>
        </div>
      </div>
    </section>"""
    return layout(site=site, path="/contact/",
                  title=f'Contact — {site["name"]}',
                  description=f'Get in touch with Teek Audio about a custom tube amplifier build or a repair. Based in {site["hometown"]}.',
                  body=body)


def page_404(site):
    body = """    <section class="section" style="padding:120px 0;text-align:center">
      <div class="wrap">
        <p class="eyebrow" style="margin-bottom:8px">404</p>
        <h2 style="font-family:var(--display);font-weight:800;font-size:clamp(2rem,6vw,3rem);margin:0 0 12px">
          This page isn't here</h2>
        <p class="sub" style="margin:0 auto 28px">Something came unplugged. Let's get you back.</p>
        <a class="btn btn-primary" href="/">Back to the front</a>
      </div>
    </section>"""
    return layout(site=site, path="/404", title="Page not found — Teek Audio",
                  description="Page not found.", body=body)


FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="10" fill="#0d0b0a"/>
  <rect x="24" y="14" width="16" height="30" rx="8" fill="none" stroke="#7b8ede" stroke-width="2.5"/>
  <path d="M29 40 v-12 l3 -5 l3 5 v12" fill="none" stroke="#ff9a3c" stroke-width="2.5"
        stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="26" y="44" width="12" height="5" rx="1.5" fill="#4d3c2c"/>
</svg>
"""


def build():
    site = load("site.json")
    services = load("services.json")

    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(STATIC, DIST)

    write(DIST / "img" / "favicon.svg", FAVICON)
    shutil.copy2(DIST / "img" / "hero-tubes.jpg", DIST / "img" / "og-image.jpg")

    write(DIST / "index.html", page_home(site, services))
    write(DIST / "about" / "index.html", page_about(site))
    write(DIST / "services" / "index.html", page_services(site, services))
    write(DIST / "contact" / "index.html", page_contact(site))
    write(DIST / "404.html", page_404(site))

    base = site["url"].rstrip("/")
    urls = "\n".join(f"  <url><loc>{base}{p}</loc></url>" for p, _ in NAV)
    write(DIST / "sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          f"{urls}\n</urlset>\n")
    write(DIST / "robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n")

    # GitHub Pages needs this file to serve the custom domain, and needs
    # .nojekyll so it does not try to run the output through Jekyll.
    write(DIST / "CNAME", "www.teekaudio.com\n")
    write(DIST / ".nojekyll", "")

    print(f"Built -> {DIST}")
    print(f"  {len(services)} services")
    if site.get("contact_details_are_placeholders"):
        print("  note: contact details are PLACEHOLDERS — omitted from structured data")


if __name__ == "__main__":
    build()
