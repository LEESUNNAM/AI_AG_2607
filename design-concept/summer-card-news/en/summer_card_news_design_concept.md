# Design Concept: Summer (여름) — 3-Frame Card News

## 1. Overview

- **Topic**: Summer (여름)
- **Deliverable**: A 3-frame 카드뉴스 (card news) carousel for social media (Instagram-style square/portrait format)
- **Assumed audience/tone**: No specific brand or audience was given, so this concept assumes a general SNS audience for a promotional or editorial summer post (the most common use case for a standalone 3-frame 카드뉴스). The direction is bright and energetic but not childish or generically "tropical" — grounded in 2026's actual summer color and social-carousel trends rather than stock clichés.
- **Format assumption**: 1080×1080 (1:1) primary, adaptable to 1080×1350 (4:5) — the two dominant Instagram carousel formats.

## 2. Trend & Reference Research

**Social carousel trends (2026)**: Two trends stand out as directly relevant to a 3-frame format. First, "authenticity over polish" — as AI makes glossy content effortless, raw/textured, slightly imperfect design (grain, hand-drawn accents) is what earns attention in 2026, a shift most industry forecasts name as the defining one of the year. Second, carousels are increasingly built as one continuous visual thread across slides (the "seamless panoramic carousel" trend) rather than three disconnected cards — even at just 3 frames, this argues for one consistent color/motif system running through all three rather than treating each frame as a separate design.

**Summer color system (2026)**: DepositPhotos' 2026 summer color trend report gives a genuinely useful *system*, not just a mood board — four colors, each with a distinct functional role: Concrete (#D5D5D7, "quiet structure"), Poolside Blue (#539DB6, "freshness, clarity, digital calm"), Chartreuse (#AEB73A, "energy, acidity, standout detail"), and Sunset Blaze (#FF5F21, "heat, urgency, conversion-focused accent"). That last color is explicitly framed as a conversion/CTA color — directly useful for a card news' closing frame.

**Korean-market summer campaign references (July 2026)**: Two real, currently-running Korean campaigns validate the direction. 신세계백화점's "Letters from Summer" campaign expresses sunlight and travel through illustration and animation rather than photography. Red Velvet's "Velvet Summer" concept splits into two moods — "Big Wave" (vintage collage, surf imagery) and "High Tide" (mermaid, dreamlike) — both leaning into a slightly retro, hand-crafted illustration treatment rather than glossy 3D-rendered tropical imagery. This lines up with the "authenticity over polish" trend above and gives a concrete, non-generic illustration direction to point to instead of default beach-stock-photo tropes.

**Layout reference**: A curated Pinterest board of 220 카드뉴스 reference/layout ideas (kr.pinterest.com/y2s1224) was used to confirm common card news layout conventions — large single-focus headline on the hook frame, consistent margin/logo placement across frames, and restrained copy per frame (kept to well under 20 words per slide, consistent with general carousel copywriting guidance).

Coverage note: dedicated design-award sites (Awwwards, GDWEB) don't meaningfully cover the 카드뉴스 format, since it's a social/print-adjacent deliverable rather than a web page — reference material here instead draws on color/trend reports, real brand campaigns, and a curated layout collection, which is a better fit for this deliverable type.

## 3. Design Concept Statement

**"Cool Heat" (시원함과 뜨거움의 대비)**

The concept is built directly from the DepositPhotos color system's own internal logic: one color for calm, one for energy, one for heat, one for structure. Rather than defaulting to a single "bright tropical" mood, the concept leans into the *contrast* those four colors already encode — the relief of shade (Poolside Blue, Concrete) against the intensity of midday heat (Chartreuse, Sunset Blaze). That contrast is also what summer itself is about: the pleasure of a pool, a shaded café, or an iced drink is only meaningful *because* of the heat around it. Frame 1 opens on the "heat" (a scroll-stopping hook), Frame 2 settles into the "cool" (the calm, information-dense middle), and Frame 3 returns to heat as a conversion/CTA moment — giving the 3-frame structure a built-in emotional arc instead of three visually identical cards.

Illustration treatment follows the "authenticity over polish" trend and the Red Velvet/신세계 references: slightly textured, hand-drawn-feeling summer motifs (sun, waves, citrus slices) rather than glossy 3D renders or default stock photography.

## 4. Color Palette

| Role | Color | Hex | Rationale |
|---|---|---|---|
| Background (neutral) | Warm Ivory | `#FAF7F2` | A warm off-white keeps the bright accent colors legible and prevents the palette from feeling cold or clinical — practical necessity for text-heavy card news frames. |
| Structure / secondary neutral | Concrete | `#D5D5D7` | Directly from the 2026 trend report's "quiet structure" role — used for dividers, secondary text blocks, and Frame 2's calmer background. |
| Primary / cool accent | Poolside Blue | `#539DB6` | The "digital calm" color from the trend system — used for Frame 2's dominant color and for headline text needing a cool, credible tone. |
| Energy accent | Chartreuse | `#AEB73A` | The trend system's "standout detail" color — used sparingly for tags, small icons, and highlight underlines, not as a dominant field color (it's too intense for large areas). |
| Heat / CTA accent | Sunset Blaze | `#FF5F21` | Explicitly framed by the source trend report as a "conversion-focused accent" — reserved for Frame 1's hook treatment and Frame 3's CTA button/highlight, so it retains urgency instead of being diluted everywhere. |
| Text ink | Warm Charcoal | `#2B2B2B` | A warm dark neutral (not pure black) for body copy — keeps long-form Frame 2 text legible without feeling harsh against Warm Ivory. |

## 5. Typography

**Pretendard** (전체 웨이트 활용: Black/ExtraBold for headlines, Medium/Regular for body) — a single free, commercially-licensed variable Korean web font spanning Thin (100) to Black (900). Using one type family across all three frames, distinguished only by weight, keeps the carousel visually unified (supporting the "one continuous thread" carousel trend from §2) while still giving Frame 1's hook enough visual weight to stop a scroll. It's also a practical choice for a fast-turnaround deliverable like card news, since there's only one font file to manage rather than a display/body pairing.

## 6. Layout & UI Patterns

Designed for 1080×1080 primary, safe-area-adjusted for 1080×1350:

- **Frame 1 (Hook)**: Sunset Blaze or a Sunset Blaze-tinted illustration as the dominant field, one large Pretendard Black headline (under ~8 words), minimal supporting copy. Job is purely to stop the scroll.
- **Frame 2 (Body/Detail)**: Poolside Blue or Concrete background, 2-3 supporting points laid out in a spacious, single-column or simple grid (not dense) — Chartreuse used only as small icon/underline accents to draw the eye to each point without competing with the headline color from Frame 1.
- **Frame 3 (CTA/Close)**: Returns to a Sunset Blaze accent block (button or banner) against a Warm Ivory field, restating the core message in one line plus a clear call-to-action.
- **Cross-frame consistency**: identical logo/handle placement (e.g. bottom-right) and identical outer margin on all three frames — this is what makes a 3-frame set read as one continuous carousel rather than three unrelated cards, per the "seamless" carousel trend.
- **Responsive note**: keep all text and the logo mark inside the safe area common to both 1:1 and 4:5 crops (roughly the center 1080×1080 of a 1080×1350 canvas) so the same source file works for either aspect ratio without redesigning.

## 7. Imagery & Iconography

- **Style**: Hand-drawn-feeling illustration (sun rays, wave lines, citrus-slice motifs) with a light grain/texture overlay — deliberately avoiding glossy 3D renders and generic tropical stock photography, per the "authenticity over polish" trend and the Red Velvet/신세계 references.
- **Color treatment**: Illustrations rendered in the palette above (Poolside Blue + Sunset Blaze as the two dominant illustration colors, Chartreuse reserved for small details) rather than full-color realistic imagery — keeps illustration and UI color consistent.
- **Icons**: Simple line icons, single-color-filled in either Chartreuse or Sunset Blaze depending on which frame they sit on — avoid multi-color icon sets, which would compete with the illustration accents.

## 8. Motion/Interaction Notes

This is a static carousel, so motion is intentionally minimal — the main "interaction" consideration is the swipe itself: keeping the logo mark and outer margin in an identical position across all three frames means the swipe transition feels continuous rather than jarring, which is the practical, static-deliverable equivalent of the "seamless carousel" trend referenced in §2.

## 9. Sources

- [DepositPhotos — Summer Color Trends 2026](https://blog.depositphotos.com/summer-color-trends-2026.html) — source of the four core hex values and their functional roles.
- [Versa Creative — Top Social Media Design Trends 2026](https://versacreative.com/blog/top-social-media-design-trends-2026/) — "authenticity over polish" trend.
- [CarouselPost.io — Summer Carousel Ideas Trending on Instagram, July 2026](https://carouselpost.io/digest/summer-carousel-ideas-instagram-july-2026) — carousel copy/structure guidance (hook → points → CTA, under 20 words/slide).
- [Lady Learner — 2026년 7월 디자인 트렌드 & 레퍼런스](https://theladylearner.com/3965/) — 신세계백화점 "Letters from Summer" and Red Velvet "Velvet Summer" campaign references.
- [Pinterest — 220 카드뉴스 레퍼런스 및 카드 레이아웃 아이디어](https://kr.pinterest.com/y2s1224/%EC%B9%B4%EB%93%9C%EB%89%B4%EC%8A%A4-%EB%A0%88%ED%8D%BC%EB%9F%B0%EC%8A%A4/) — layout-convention reference.
- [Pretendard (GitHub)](https://github.com/orioncactus/pretendard) — typeface specification and free commercial licensing.
