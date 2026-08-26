---
name: reference
description: Given a design concept, mood/style keywords, a color palette, a brand or product topic — or a path to a design-concept document (e.g. one produced by the design-concept skill) — this skill searches the web for matching visual reference images and downloads them to a local folder along with a source manifest, like assembling a real mood board. Use this whenever the user wants actual reference images collected and saved, not just a list of reference websites to read — phrases like "레퍼런스 이미지 찾아서 저장해줘", "이 디자인 컨셉에 맞는 이미지 좀 모아줘", "무드보드 이미지 저장해줘", "find and save some reference images for X", "download some visual references matching this style" — even if they don't say "mood board" or "레퍼런스" explicitly, as long as they want image files saved locally rather than a text description. This is a natural follow-up after using the design-concept skill (its concept keywords, palette, and imagery-direction notes are ideal search input here), but also works standalone from a bare topic or mood description. Do NOT use this when the user only wants reference *sites* named/linked for reading, with no image files saved — that's plain WebSearch or the 웹디자인 agent's job.

---

# Reference Image Collector

Turn a design concept, mood, or topic into an actual folder of saved reference images with a source manifest — the digital equivalent of pinning real examples to a mood board, not just describing what they might look like.

## Why this shape

A design concept document says what the palette and mood *should* be; this skill goes and finds real images that already embody it, so the user has something to look at and compare against, not just adjectives. The manifest matters as much as the images themselves — a folder of unlabeled pictures is much less useful later than one where each image is traceable back to where it came from and why it was picked, especially since the user may later need to check a specific image's license before using it in a real deliverable.

## 1. Figure out the search input

- **If given a file path** (e.g. a design-concept skill output like `design-concept/<topic>/en/<topic>_design_concept.md`), read it and pull out the concept keywords, color palette, and imagery/iconography direction — use those as the actual search vocabulary instead of asking the user to restate them.
- **If given a bare topic or mood description** ("미니멀 스칸디나비아 인테리어", "playful fintech app for Gen Z"), work directly from that.
- **Clarify only what changes the search meaningfully**: roughly how many images (default ~12-15 — enough to feel like a real board without being a dump), and whether this is for a website/app UI, a brand/product, or general mood/aesthetic reference (this changes which sites are worth searching). Infer a sensible default and state the assumption rather than blocking on it.

## 2. Build targeted search queries

Turn the concept into 3-6 specific queries rather than one vague one — specific queries surface specific, usable images while a vague query surfaces generic stock-photo noise. Combine the mood/style keywords with a source or format hint, e.g.:
- "<style keyword> web design mood board"
- "<industry> app UI screenshot <style keyword>"
- "<style keyword> color palette photography"
- "<topic> branding pinterest"
- "<style keyword> interior/product/editorial photography" (pick whichever medium fits the topic)

## 3. Find real image sources with WebSearch

Use `WebSearch` to find candidate pages, prioritizing sites that are actually built around browsable, high-quality images rather than link-farm article pages:
- **General visual/mood reference**: Pinterest, Unsplash, Pexels
- **Web/app UI reference**: Dribbble, Behance, Awwwards, Mobbin
- **Product/brand reference**: the brand's own site, Behance case studies

Unsplash and Pexels are free-to-use and licensing-safe by default, which makes them the safest pick whenever the topic doesn't specifically need Pinterest/Dribbble-style curation — lean on them when either would serve the search equally well.

## 4. Extract real image URLs with WebFetch

For each promising source page, use `WebFetch` to load it and find the actual image URLs — don't guess a URL from the page's title. Look for:
- `og:image` meta tags (usually a solid, full-size representative image)
- `<img src>` / `srcset` attributes — prefer the largest resolution offered, not a thumbnail
- Direct `.jpg`/`.png`/`.webp` links visible in the page content

If a source page is too JavaScript-heavy for WebFetch to yield real image URLs (common on Pinterest search results), fall back to search results from a site that renders more statically (Unsplash/Pexels/Dribbble often do), or note the gap rather than saving a broken/placeholder link.

## 5. Download and verify each image

Download images with `curl` via Bash (e.g. `curl -sL -o <path> "<url>"`) rather than treating a found URL as good enough on its own — a wrong or dead link produces a 0-byte file or an HTML error page saved with an image extension, which is worse than skipping it. After each download:
- Check the file is non-trivial in size (a real photo/screenshot is rarely under a few KB; an error page saved as `.jpg` often is)
- If a download fails or looks broken, drop it and move to the next candidate rather than leaving a broken file in the folder

This skill's whole purpose is fetching and saving images on the user's behalf — that's the explicit intent behind asking for it, so there's no need to pause for confirmation on each individual image. Do mention up front, before a large batch, roughly how many images you're about to fetch and from which sites, so the user isn't surprised by the result.

## 6. Save and organize

Save into `reference-images/<topic>/`:
- The image files themselves, named descriptively (e.g. `01_warm-minimalist-hero.jpg`) rather than left as opaque hashes from the source URL
- A `sources.md` manifest listing, for every saved image: filename, source URL, and a one-line note on why it was picked (which mood/keyword it matches)

If the source pages were rendered via the Playwright MCP browser instead of WebFetch (e.g. to screenshot a page that resists fetching), save those raw screenshots under `output2/playwright/` per this project's convention, and still copy/reference the final curated images into `reference-images/<topic>/` with the manifest.

After saving, report back: the folder path, how many images were saved, which sites they came from, and any gaps (fewer images than targeted, a mood/keyword that came up thin).

## Constraints

- Never fabricate an image URL or claim an image was saved when the download failed — verify each file actually landed and looks like a real image before listing it in the manifest.
- These images are for internal design reference/mood-boarding, not guaranteed-cleared assets for a shipped deliverable. Note in the manifest or final report that any image used in a real, public-facing product should have its license checked first (Unsplash/Pexels images are generally safe for this; Pinterest/Dribbble/Behance images usually are not without checking).
- Don't pad the folder with near-duplicate or barely-relevant images just to hit a target count — a smaller set of genuinely on-concept images beats a larger set of filler.
