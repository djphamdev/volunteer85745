#!/usr/bin/env python3
"""
Generate the Volunteer 85745 clean static site - TWO CATEGORIES.
Remote + Local (10mi from 85745) volunteer listings with hours emphasis.
Non-indexed, daily cron updates, designed for Medicaid 80hrs/month requirement.
"""

import json
import re
from pathlib import Path
from datetime import datetime
from html import escape

# ===== Configuration =====
VAULT_PATH = Path("/home/donzzz/Documents/_obsidian_androidZzz")
PROJECT_PATH = VAULT_PATH / "20-PROJECTS" / "volunteer85745"
LEADS_DIR = PROJECT_PATH / "leads"
OUTPUT_DIR = Path("/home/donzzz/projects/volunteer85745")

# ===== HTML Templates =====

HTML_HEADER_ROOT = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<meta name="description" content="Volunteer opportunities near Tucson 85745 + Remote — 20hrs/week, 80hrs/month for healthcare">
<title>{title}</title>
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<link rel="stylesheet" href="assets/style.css">
<script src="assets/main.js" defer></script>
</head>
<body>
<header>
  <div>
    <h1>{page_title}</h1>
    <div class="subtitle">{subtitle}</div>
  </div>
  <button class="theme-toggle" id="themeToggle">Light</button>
</header>
"""

HTML_FOOTER = """
<button id="backToTop" aria-label="Back to top">^</button>
<footer>
  <p style="text-align: center; color: var(--text-muted); font-size: 0.85rem; padding: 24px;">
    Volunteer 85745 — Private Resource for Healthcare Hours | Updated {updated}
    <br>
    <a href="https://github.com/djphamdev/volunteer85745" style="color: var(--accent);" target="_blank">GitHub Repo</a>
    | Non-indexed · Daily updates · Built for a friend
  </p>
</footer>
</body>
</html>
"""

# ===== Helper Functions =====

def load_latest_leads():
    """Load the latest leads JSON from vault."""
    json_files = sorted(LEADS_DIR.glob("*-leads.json"), reverse=True)
    if not json_files:
        return None, None
    
    latest_file = json_files[0]
    date_str = latest_file.stem.replace("-leads", "")
    try:
        data = json.loads(latest_file.read_text())
    except Exception as e:
        print(f"  WARNING: Failed to load {latest_file}: {e}")
        return None, None
    
    return date_str, data

def load_all_cycles():
    """Load all cycles for index page history."""
    cycles = []
    for json_file in sorted(LEADS_DIR.glob("*-leads.json"), reverse=True):
        date_str = json_file.stem.replace("-leads", "")
        try:
            data = json.loads(json_file.read_text())
        except Exception as e:
            print(f"  WARNING: Failed to load {json_file}: {e}")
            continue
        
        # Count by category
        remote_count = sum(1 for e in data if e.get("category") == "remote")
        local_count = sum(1 for e in data if e.get("category") == "local")
        total = len(data)
        
        cycles.append({
            "date": date_str,
            "leads": data,
            "stats": {
                "total": total,
                "remote": remote_count,
                "local": local_count,
            }
        })
    return cycles

def format_date(date_str):
    """Format YYYY-MM-DD to readable."""
    return datetime.strptime(date_str, '%Y-%m-%d').strftime('%A, %b %d, %Y')

def hours_badge(hours_per_week):
    """Generate hours badge HTML."""
    if hours_per_week >= 20:
        return f'<span class="badge badge-hours-good">≥20 hrs/wk ✓</span>'
    elif hours_per_week >= 10:
        return f'<span class="badge badge-hours-mid">{hours_per_week} hrs/wk</span>'
    elif hours_per_week > 0:
        return f'<span class="badge badge-hours-low">{hours_per_week} hrs/wk</span>'
    return ''

def category_badge(category):
    """Generate category badge."""
    if category == "remote":
        return '<span class="badge badge-remote">🌐 REMOTE</span>'
    return '<span class="badge badge-local">📍 LOCAL (10mi)</span>'

def generate_index(cycles):
    """Generate the homepage with two-category layout."""
    if not cycles:
        return "<h1>No cycles found</h1>"
    
    latest = cycles[-1]
    total_leads = sum(c["stats"]["total"] for c in cycles)
    total_remote = sum(c["stats"]["remote"] for c in cycles)
    total_local = sum(c["stats"]["local"] for c in cycles)
    
    html_parts = [HTML_HEADER_ROOT.format(
        title="Volunteer 85745 — Tucson AZ + Remote Opportunities",
        page_title="Volunteer 85745",
        subtitle=f"10mi radius 85745 + Worldwide Remote | 20hrs/wk target · 80hrs/mo for healthcare | Updated {datetime.now().strftime('%b %d, %Y')}"
    )]
    
    # Stats bar
    html_parts.append(f"""
<div class="stats-bar">
  <div class="stat-card"><div class="num">{total_leads}</div><div class="label">Total Listings</div></div>
  <div class="stat-card"><div class="num remote">{total_remote}</div><div class="label">🌐 Remote</div></div>
  <div class="stat-card"><div class="num local">{total_local}</div><div class="label">📍 Local</div></div>
  <div class="stat-card"><div class="num">{len(cycles)}</div><div class="label">Daily Cycles</div></div>
</div>
""")
    
    # Latest cycle highlight
    if latest:
        html_parts.append(f"""
<div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: 10px; padding: 20px; margin-bottom: 24px;">
  <h2 style="margin-bottom: 12px;">NEW Latest Update - {latest['date']}</h2>
  <div class="stats-bar" style="margin-bottom: 0;">
    <div class="stat-card"><div class="num remote">{latest['stats']['remote']}</div><div class="label">🌐 Remote Listings</div></div>
    <div class="stat-card"><div class="num local">{latest['stats']['local']}</div><div class="label">📍 Local Listings</div></div>
    <div class="stat-card"><div class="num">{latest['stats']['total']}</div><div class="label">Total New</div></div>
  </div>
  <div style="margin-top: 14px;">
    <a href="cycle-{latest['date']}.html" class="action-btn primary">View All Listings -></a>
    <a href="#remote" class="action-btn secondary" style="margin-left: 12px;">Jump to Remote</a>
  </div>
</div>
""")
    
    # Two main category sections (REMOTE first, then LOCAL)
    html_parts.append("""
<h2 style="margin-bottom: 16px;">🌐 REMOTE — Worldwide Volunteer Opportunities</h2>
<div id="remote" style="display: flex; flex-direction: column; gap: 12px; margin-bottom: 32px;">
""")
    
    # Remote listings from latest cycle
    remote_leads = [e for e in latest['leads'] if e.get('category') == 'remote']
    for e in sorted(remote_leads, key=lambda x: x.get('hours_per_week', 0), reverse=True):
        html_parts.append(render_lead_card(e, latest['date']))
    
    html_parts.append("</div>")
    
    html_parts.append("""
<h2 style="margin-bottom: 16px;">📍 LOCAL — 10mi Radius from 85745 (West Tucson)</h2>
<div id="local" style="display: flex; flex-direction: column; gap: 12px; margin-bottom: 32px;">
""")
    
    # Local listings from latest cycle
    local_leads = [e for e in latest['leads'] if e.get('category') == 'local']
    for e in sorted(local_leads, key=lambda x: x.get('hours_per_week', 0), reverse=True):
        html_parts.append(render_lead_card(e, latest['date']))
    
    html_parts.append("</div>")
    
    # History section
    html_parts.append(f"""
<h2 style="margin-bottom: 16px;">📅 All Daily Cycles</h2>
<div style="display: flex; flex-wrap: wrap; gap: 8px;">
""")
    
    for c in cycles:
        date_formatted = format_date(c['date'])
        html_parts.append(f"""
<a href="cycle-{c['date']}.html" class="cycle-card">
  <div class="cycle-meta">
    <span class="cycle-date">{date_formatted}</span>
    <span class="cycle-stats">🌐 {c['stats']['remote']} Remote · 📍 {c['stats']['local']} Local · {c['stats']['total']} total</span>
  </div>
  <span class="cycle-badge">{c['stats']['total']} new</span>
</a>
""")
    
    html_parts.append('</div>\n')
    html_parts.append(HTML_FOOTER.format(updated=datetime.now().strftime('%Y-%m-%d %H:%M')))
    return ''.join(html_parts)

def render_lead_card(e, cycle_date):
    """Render a single lead card for index/category view."""
    title = e.get('title', '')
    org = e.get('organization', '')
    location = e.get('location', '')
    url = e.get('url', '')
    category = e.get('category', '')
    hours_per_week = e.get('hours_per_week', 0)
    hours_note = e.get('hours_note', '')
    schedule_flex = e.get('schedule_flexibility', '')
    description = e.get('description', '')
    requirements = e.get('requirements', '')
    contact = e.get('contact', '')
    
    badges = [category_badge(category)]
    badges.append(hours_badge(hours_per_week))
    if schedule_flex:
        badges.append(f'<span class="badge badge-flex">{escape(schedule_flex)}</span>')
    badges_html = ' '.join(badges)
    
    # Truncate description for card view
    desc_short = description[:200] + '...' if len(description) > 200 else description
    
    return f"""
<div class="lead-card" data-category="{category}">
  <div class="lead-card-header">
    <div>
      <h3>{escape(title)}</h3>
      <div class="company">{escape(org)} | {escape(location)}</div>
      <div class="meta">{badges_html}</div>
    </div>
  </div>
  <div class="lead-details">
    <div class="lead-details-grid">
      <div class="lead-detail-item">
        <div class="label">Hours / Week</div>
        <div class="value">{hours_per_week} hrs/week</div>
      </div>
      <div class="lead-detail-item">
        <div class="label">Monthly Potential</div>
        <div class="value">{hours_per_week * 4} hrs/month</div>
      </div>
      <div class="lead-detail-item">
        <div class="label">Category</div>
        <div class="value">{'🌐 Remote' if category == 'remote' else '📍 Local (10mi 85745)'}</div>
      </div>
      <div class="lead-detail-item">
        <div class="label">Schedule</div>
        <div class="value">{escape(schedule_flex or 'See listing')}</div>
      </div>
      <div class="lead-detail-item">
        <div class="label">Date Found</div>
        <div class="value">{cycle_date}</div>
      </div>
      <div class="lead-detail-item">
        <div class="label">Apply / Info</div>
        <div class="value"><a href="{escape(url)}" target="_blank" rel="noopener noreferrer">Open Listing -></a></div>
      </div>
    </div>
    {f'<div class="details-section"><div class="details-section-title">Description</div><p style="font-size:0.9rem;color:var(--text-secondary);">{escape(desc_short)}</p></div>' if description else ''}
    {f'<div class="details-section"><div class="details-section-title">Hours Note</div><p style="font-size:0.9rem;color:var(--yellow);">{escape(hours_note)}</p></div>' if hours_note else ''}
    {f'<div class="details-section"><div class="details-section-title">Requirements</div><p style="font-size:0.9rem;color:var(--text-secondary);">{escape(requirements)}</p></div>' if requirements else ''}
    <div class="action-bar">
      <a href="{escape(url)}" target="_blank" rel="noopener noreferrer" class="action-btn primary">View Full Listing</a>
    </div>
  </div>
</div>
"""

def generate_cycle_page(cycle):
    """Generate the full per-cycle listing page."""
    html_parts = [HTML_HEADER_ROOT.format(
        title=f"Volunteer Listings — {cycle['date']} — Volunteer 85745",
        page_title=f"Listings from {cycle['date']}",
        subtitle=f"🌐 {cycle['stats']['remote']} Remote · 📍 {cycle['stats']['local']} Local · {cycle['stats']['total']} Total"
    )]
    
    # Breadcrumb
    html_parts.append("""
<div class="breadcrumb">
  <a href="index.html"><- Home / All Cycles</a>
</div>
""")
    
    # Filter bar
    html_parts.append("""
<div class="filter-bar">
  <label>Category:</label>
  <select id="catFilter">
    <option value="all">All</option>
    <option value="remote">🌐 Remote Only</option>
    <option value="local">📍 Local Only</option>
  </select>
  <label>Min Hours/Week:</label>
  <select id="hoursFilter">
    <option value="0">Any</option>
    <option value="20">≥20 (Meets 80/mo target)</option>
    <option value="10">≥10</option>
    <option value="5">≥5</option>
  </select>
  <input type="text" id="searchFilter" placeholder="Search title, org, location...">
</div>
""")
    
    # Sort: Remote first, then by hours descending
    leads = sorted(cycle['leads'], key=lambda x: (x.get('category') == 'local', -x.get('hours_per_week', 0)))
    
    html_parts.append('<div class="lead-list">\n')
    for e in leads:
        title = e.get('title', '')
        org = e.get('organization', '')
        location = e.get('location', '')
        url = e.get('url', '')
        category = e.get('category', '')
        hours_per_week = e.get('hours_per_week', 0)
        hours_note = e.get('hours_note', '')
        schedule_flex = e.get('schedule_flexibility', '')
        description = e.get('description', '')
        requirements = e.get('requirements', '')
        contact = e.get('contact', '')
        source = e.get('source', '')
        
        badges = [category_badge(category)]
        badges.append(hours_badge(hours_per_week))
        if schedule_flex:
            badges.append(f'<span class="badge badge-flex">{escape(schedule_flex)}</span>')
        badges_html = ' '.join(badges)
        
        html_parts.append(f"""
<div class="lead-card" data-category="{category}" data-hours="{hours_per_week}">
  <div class="lead-card-header">
    <div>
      <h3>{escape(title)}</h3>
      <div class="company">{escape(org)} | {escape(location)}</div>
      <div class="meta">{badges_html}</div>
    </div>
  </div>
  <div class="lead-details">
    <div class="lead-details-grid">
      <div class="lead-detail-item">
        <div class="label">Hours / Week</div>
        <div class="value">{hours_per_week} hrs/week</div>
      </div>
      <div class="lead-detail-item">
        <div class="label">Monthly Potential</div>
        <div class="value">{hours_per_week * 4} hrs/month</div>
      </div>
      <div class="lead-detail-item">
        <div class="label">Meets 80hr/mo Target</div>
        <div class="value">{"✅ YES" if hours_per_week >= 20 else "❌ NO (needs multiple roles)"}</div>
      </div>
      <div class="lead-detail-item">
        <div class="label">Category</div>
        <div class="value">{'🌐 Remote' if category == 'remote' else '📍 Local (10mi 85745)'}</div>
      </div>
      <div class="lead-detail-item">
        <div class="label">Schedule Flexibility</div>
        <div class="value">{escape(schedule_flex or 'See listing')}</div>
      </div>
      <div class="lead-detail-item">
        <div class="label">Source</div>
        <div class="value">{escape(source)}</div>
      </div>
      <div class="lead-detail-item">
        <div class="label">Date Found</div>
        <div class="value">{cycle['date']}</div>
      </div>
      <div class="lead-detail-item">
        <div class="label">Apply / Info</div>
        <div class="value"><a href="{escape(url)}" target="_blank" rel="noopener noreferrer">{escape(source)} -></a></div>
      </div>
    </div>
    
    {f'<div class="details-section"><div class="details-section-title">Description</div><p style="font-size:0.95rem;color:var(--text-secondary);">{escape(description)}</p></div>' if description else ''}
    {f'<div class="details-section"><div class="details-section-title">Hours Commitment Details</div><p style="font-size:0.95rem;color:var(--yellow);font-weight:600;">{escape(hours_note)}</p></div>' if hours_note else ''}
    {f'<div class="details-section"><div class="details-section-title">Requirements</div><p style="font-size:0.95rem;color:var(--text-secondary);">{escape(requirements)}</p></div>' if requirements else ''}
    {f'<div class="details-section"><div class="details-section-title">Contact / Sign-up</div><p style="font-size:0.95rem;color:var(--accent);">{escape(contact)}</p></div>' if contact else ''}
    
    <div class="action-bar">
      <a href="{escape(url)}" target="_blank" rel="noopener noreferrer" class="action-btn primary">Open Full Listing</a>
    </div>
  </div>
</div>
""")
    
    html_parts.append('</div>\n')
    html_parts.append(HTML_FOOTER.format(updated=datetime.now().strftime('%Y-%m-%d %H:%M')))
    return ''.join(html_parts)

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "assets").mkdir(exist_ok=True)
    
    print("Generating Volunteer 85745 site (Remote + Local 10mi)...")
    
    cycles = load_all_cycles()
    
    if not cycles:
        print("  No cycles found! Creating placeholder with seeded data...")
        # Will use seeded data below
        return
    
    # Generate index
    index_html = generate_index(cycles)
    (OUTPUT_DIR / "index.html").write_text(index_html)
    print(f"  index.html -- {len(cycles)} cycles, {sum(c['stats']['total'] for c in cycles)} total listings")
    
    # Generate cycle pages
    for cycle in cycles:
        cycle_html = generate_cycle_page(cycle)
        (OUTPUT_DIR / f"cycle-{cycle['date']}.html").write_text(cycle_html)
        print(f"  cycle-{cycle['date']}.html -- {cycle['stats']['remote']} remote, {cycle['stats']['local']} local")
    
    # Generate README
    readme = """# Volunteer 85745

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
"""
    (OUTPUT_DIR / "README.md").write_text(readme)
    
    print(f"\nSite generated: {OUTPUT_DIR}")
    print(f"   {len(cycles)} cycles | {sum(c['stats']['total'] for c in cycles)} listings")

if __name__ == "__main__":
    main()