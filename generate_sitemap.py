#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate OSRS Guru sitemap (sitemap index + sub-sitemaps)."""

import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import date

BASE = "https://osrsguru.com"
TODAY = str(date.today())  # 2026-07-03
ROOT = r"C:\Users\Lenovo\osrs-guide-site"

EXCLUDE = {
    "css_override_complete.html",
    "ga4_dashboard.html",
    "googlef2d4bacd14fcdb05.html",
    "index-backup-2026-07-03.html",
    "index-redesign-plan.html",
    "medium-article-formatted.html",
    "medium-osrs-money-making-2026.html",
    os.path.join("blog", "shippage_simple.html"),
    os.path.join("guides", "osrs-weekly-pain-points-template.html"),
    os.path.join("pt-br", "promo-landing.html"),
}


def get_priority(rel_path):
    p = rel_path.replace(os.sep, "/")

    if p == "index.html" or p == "":
        return "1.0", "weekly"
    if p in ("about.html", "privacy-policy.html", "contact.html"):
        return "0.7", "monthly"
    if p in ("community.html",):
        return "0.7", "monthly"
    if p in ("money-making.html", "skill-training.html", "quest-guides.html", "boss-guides.html"):
        return "0.9", "weekly"
    if p in ("weekly-updates.html", "monthly-updates.html"):
        return "0.8", "weekly"
    if p in ("new-player.html", "returning-player.html", "members.html", "mid-to-high.html"):
        return "0.85", "weekly"

    if p.startswith("guides/") and not p.startswith("guides/crimson-desert/") and not p.startswith("guides/windrose/"):
        return "0.85", "weekly"
    if p.startswith("guides/crimson-desert/"):
        return "0.8", "weekly"
    if p.startswith("guides/windrose/"):
        return "0.8", "weekly"
    if p.startswith("blog/"):
        return "0.7", "monthly"
    if p.startswith("zh/") and not p.startswith("zh/guides/"):
        return "0.8", "weekly"
    if p.startswith("zh/guides/"):
        return "0.85", "weekly"
    if p.startswith("pt-br/") and not p.startswith("pt-br/guides/"):
        return "0.8", "weekly"
    if p.startswith("pt-br/guides/"):
        return "0.85", "weekly"

    return "0.8", "monthly"


def prettify(elem):
    rough = ET.tostring(elem, encoding="unicode")
    parsed = minidom.parseString(rough.encode())
    return parsed.toprettyxml(indent="  ", encoding="UTF-8").decode("UTF-8")


def collect_urls(base_dir, exclude_set):
    groups = {
        "core": [], "guides": [], "cd": [], "windrose": [],
        "blog": [], "zh": [], "pt": [],
    }

    for dirpath, _, filenames in os.walk(base_dir):
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, base_dir)

            # Skip excluded
            if any(rel.endswith(ex) for ex in exclude_set):
                continue
            # Skip infrastructure dirs
            parts = rel.split(os.sep)
            if any(p in ("node_modules", ".workbuddy", ".git") for p in parts):
                continue

            url = f"{BASE}/{rel.replace(os.sep, '/')}"

            if rel.startswith(os.path.join("guides", "crimson-desert")):
                groups["cd"].append(url)
            elif rel.startswith(os.path.join("guides", "windrose")):
                groups["windrose"].append(url)
            elif rel.startswith("guides"):
                groups["guides"].append(url)
            elif rel.startswith("zh"):
                groups["zh"].append(url)
            elif rel.startswith("pt-br"):
                groups["pt"].append(url)
            elif rel.startswith("blog"):
                groups["blog"].append(url)
            else:
                groups["core"].append(url)

    return groups


def write_urlset(urls, filename, base_dir):
    root = ET.Element("urlset")
    root.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

    for url_str in sorted(urls):
        rel_part = url_str.replace(BASE + "/", "")
        prio, freq = get_priority(rel_part)
        u = ET.SubElement(root, "url")
        ET.SubElement(u, "loc").text = url_str
        ET.SubElement(u, "lastmod").text = TODAY
        ET.SubElement(u, "changefreq").text = freq
        ET.SubElement(u, "priority").text = prio

    xml_str = prettify(root)
    print(f"  FILE:{filename}")
    print(f"  LEN:{len(urls)}")
    print(xml_str)
    print(f"  /FILE:{filename}")


def write_sitemap_index(groups_meta, base_dir):
    index = ET.Element("sitemapindex")
    index.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

    for meta in groups_meta:
        sm = ET.SubElement(index, "sitemap")
        ET.SubElement(sm, "loc").text = f"{BASE}/{meta['filename']}"
        ET.SubElement(sm, "lastmod").text = TODAY

    xml_str = prettify(index)
    print(f"  FILE:sitemap.xml")
    print(f"  LEN:{len(groups_meta)}")
    print(xml_str)
    print(f"  /FILE:sitemap.xml")


if __name__ == "__main__":
    print(f"Generating OSRS Guru Sitemap - {TODAY}\n")

    groups = collect_urls(ROOT, EXCLUDE)

    configs = [
        ("sitemap-core.xml", "core",      "Core Pages"),
        ("sitemap-guides.xml", "guides",  "OSRS Guides"),
        ("sitemap-cd.xml", "cd",          "Crimson Desert"),
        ("sitemap-windrose.xml", "windrose", "Windrose"),
        ("sitemap-zh.xml", "zh",          "Chinese Station"),
        ("sitemap-pt.xml", "pt",          "Brazilian Station"),
        ("sitemap-blog.xml", "blog",      "Blog"),
    ]

    # Sitemap Index mode: write sub-sitemaps + index
    total = 0
    meta = []
    for filename, key, label in configs:
        urls = sorted(groups[key])
        if not urls:
            print(f"  SKIP {filename}: empty")
            continue
        write_urlset(urls, filename, ROOT)
        total += len(urls)
        meta.append({"filename": filename, "label": label, "count": len(urls)})

    write_sitemap_index(meta, ROOT)

    print(f"\n{'='*50}")
    print(f"Sitemap Summary")
    print(f"{'='*50}")
    for m in meta:
        print(f"  {m['label']:25s} -> {m['filename']:20s}  {m['count']:4d} URLs")
    print(f"  {'-'*50}")
    print(f"  {'TOTAL':25s}                    {total:4d} URLs")
    print(f"\nDone! Submit sitemap.xml to Google Search Console.")
