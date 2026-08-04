# Trivago MCP — Available Features

This document describes the capabilities exposed by the Trivago MCP (Model Context Protocol) server that are available in this environment. It provides two tools for searching accommodations and hotels through trivago.

## Overview

| Tool | Purpose |
|---|---|
| `trivago-accommodation-search` | Search accommodations by destination name or point of interest (e.g. a city, region, or landmark name). |
| `trivago-accommodation-radius-search` | Search accommodations near a specific geographic point using latitude/longitude coordinates. |

Both tools return hotel/accommodation listings with pricing, availability, and metadata based on the given search criteria and filters.

## 1. Destination Search — `trivago-accommodation-search`

Searches accommodations by a free-text destination or point of interest (e.g. "Paris", "Times Square, New York", "Gangnam, Seoul").

### Required parameters
- `query` — Destination or point of interest (string).
- `arrival` — Check-in date, `YYYY-MM-DD`. Must be a future date and before `departure`.
- `departure` — Check-out date, `YYYY-MM-DD`. Must be after `arrival`.

### Optional parameters
- `adults` — Number of adults (min 1).
- `children` — Number of children (min 0).
- `children_ages` — Dash-separated list of children's ages (e.g. `10-12-14`).
- `rooms` — Number of rooms (must be ≤ number of adults).
- `country` — ISO alpha-2 market/country code for pricing and content (default `US`).
- `currency` — ISO 4217 currency code (default `USD`).
- `language` — Content language code (default `EN_US`).
- `hotel_rating` — Filter by star rating: `1star` through `5star` (booleans, multiple selectable).
- `review_rating` — Filter by guest review score: `rating70`, `rating75`, `rating80`, `rating85`.
- `filters` — Amenity filters (all booleans): `airConditioning`, `breakfastIncluded`, `freeCancellation`, `freeWiFi`, `gym`, `kitchen`, `parking`, `petFriendly`, `pool`, `spa`.

## 2. Radius Search — `trivago-accommodation-radius-search`

Searches accommodations near a specific geographic location using coordinates, useful when searching around a precise landmark or address rather than a named destination.

### Required parameters
- `latitude` — Latitude of the target location.
- `longitude` — Longitude of the target location.
- `arrival` — Check-in date, `YYYY-MM-DD`. Must be a future date and before `departure`.
- `departure` — Check-out date, `YYYY-MM-DD`. Must be after `arrival`.

### Optional parameters
Same set as the destination search tool: `adults`, `children`, `children_ages`, `rooms`, `country`, `currency`, `language`, `hotel_rating`, `review_rating`, `filters`.

## Common Use Cases

- Find hotels in a specific city or neighborhood for given travel dates.
- Find hotels within a radius of a landmark, venue, or address (e.g. near a conference center or airport).
- Filter results by star rating, guest review score, or amenities (Wi-Fi, breakfast, pool, pet-friendly, etc.).
- Get market-specific pricing and content by specifying country, currency, and language.
- Plan for groups by specifying multiple adults, children (with ages), and rooms.

## Notes / Constraints

- Dates must be in `YYYY-MM-DD` format; `arrival` must be a future date and strictly before `departure`.
- `rooms` cannot exceed the number of `adults`.
- Use `trivago-accommodation-search` when the destination can be described by name; use `trivago-accommodation-radius-search` when precise coordinates are known and a radius-based search around a specific point is preferred.
