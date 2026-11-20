# Volunteer 85745

**Live Site: https://djphamdev.github.io/volunteer85745/**

Private volunteer opportunity aggregator for Tucson AZ 85745 (10mi radius) + Worldwide Remote.
Built for a friend needing 20hrs/week (80hrs/month) to maintain Medicaid eligibility starting Jan 2027.

## Site Structure
- index.html - Homepage with two-category layout (Remote first, then Local)
- cycle-YYYY-MM-DD.html - Per-day listings with full details
- assets/style.css - Dark-mode-default theme with light toggle
- assets/main.js - Theme toggle, back-to-top, category/hours filters
- assets/favicon.svg - Heart icon

## Data Source
Obsidian vault: `20-PROJECTS/volunteer85745/leads/`
- *-leads.json: Curated volunteer listings (no PII)

## Categories
- **🌐 REMOTE** - Worldwide volunteer-from-home opportunities
- **📍 LOCAL** - Within 10 miles of zip code 85745 (West Tucson)

## Key Features
- Hours/week prominently displayed (target: ≥20 hrs/wk = 80hrs/mo)
- Monthly potential calculated automatically
- "Meets 80hr/mo target" indicator per listing
- Category filter (Remote/Local/All)
- Min-hours filter (≥20, ≥10, ≥5, Any)
- Search filter
- Non-indexed (noindex, nofollow meta)

## Auto-Update
Cron runs daily, rebuilds site, pushes to GitHub Pages.
