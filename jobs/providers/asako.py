"""Asako (asako.mg) — site d'emploi malgache. Candidature directe, gratuite.

Scraping *respectueux* et robuste :
  1. On lit le sitemap des offres (sitemap-jobs.xml) → URLs + date.
  2. On pré-filtre sur le slug (mots-clés / tech) pour NE PAS télécharger
     des pages inutiles.
  3. Pour chaque offre retenue (plafonnée), on lit le JSON-LD `JobPosting`
     embarqué dans la page (standard schema.org, stable) → extraction fiable.

robots.txt d'Asako autorise /emploi et /annonces ; on s'identifie via User-Agent
et on plafonne le nombre de requêtes.
"""
from __future__ import annotations

import json
import os
import re
import time
import xml.etree.ElementTree as ET
from datetime import datetime

import requests

from .base import (
    DEFAULT_TIMEOUT,
    USER_AGENT,
    JobProvider,
    NormalizedJob,
    extract_email,
    looks_like_it,
)

SITEMAP_URL = "https://www.asako.mg/sitemap-jobs.xml"
_LD_RE = re.compile(
    r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', re.S
)
_HTML_TAG_RE = re.compile(r"<[^>]+>")
# Plafond de pages téléchargées par collecte (respect du serveur).
MAX_PAGES = int(os.getenv("ASAKO_MAX_PAGES", "30"))
REQUEST_DELAY = 0.25  # secondes entre deux pages


class AsakoProvider(JobProvider):
    source_key = "asako"
    needs_credentials = False

    def search(self, keywords="", location="", remote=False, category="it") -> list[NormalizedJob]:
        entries = self._sitemap_entries()
        kw_terms = [w.strip().lower() for w in keywords.split() if len(w.strip()) > 2]

        # Pré-filtrage sur le slug pour limiter les téléchargements.
        selected = []
        for url, lastmod in entries:
            slug = url.rstrip("/").rsplit("/", 1)[-1].replace("-", " ").lower()
            if kw_terms and not any(t in slug for t in kw_terms):
                continue
            if category == "it" and not kw_terms and not looks_like_it(slug):
                continue
            selected.append((url, lastmod))

        # Plus récentes d'abord, puis plafond.
        selected.sort(key=lambda x: x[1] or "", reverse=True)
        selected = selected[:MAX_PAGES]

        jobs = []
        for url, _ in selected:
            job = self._parse_offer(url)
            if not job:
                continue
            # Garde-fou catégorie sur le contenu réel.
            if category == "it" and not looks_like_it(f"{job.title} {job.description[:400]}"):
                continue
            jobs.append(job)
            time.sleep(REQUEST_DELAY)
        return jobs

    # ------------------------------------------------------------------

    def _sitemap_entries(self) -> list[tuple[str, str]]:
        resp = requests.get(
            SITEMAP_URL, headers={"User-Agent": USER_AGENT}, timeout=DEFAULT_TIMEOUT
        )
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        out = []
        for url_el in root.findall(".//sm:url", ns):
            loc = url_el.findtext("sm:loc", default="", namespaces=ns)
            lastmod = url_el.findtext("sm:lastmod", default="", namespaces=ns)
            if loc:
                out.append((loc.strip(), (lastmod or "").strip()))
        return out

    def _parse_offer(self, url: str) -> NormalizedJob | None:
        try:
            resp = requests.get(
                url, headers={"User-Agent": USER_AGENT}, timeout=DEFAULT_TIMEOUT
            )
            resp.raise_for_status()
        except requests.RequestException:
            return None

        html = resp.content.decode("utf-8", errors="replace")
        posting = None
        for block in _LD_RE.findall(html):
            try:
                data = json.loads(block.strip())
            except json.JSONDecodeError:
                continue
            items = data if isinstance(data, list) else [data]
            for item in items:
                if isinstance(item, dict) and item.get("@type") == "JobPosting":
                    posting = item
                    break
            if posting:
                break
        if not posting:
            return None

        title = (posting.get("title") or "").strip()
        description = posting.get("description") or ""
        company = ""
        org = posting.get("hiringOrganization")
        if isinstance(org, dict):
            company = (org.get("name") or "").strip()

        location = self._location(posting.get("jobLocation"))
        emp = posting.get("employmentType") or ""
        if isinstance(emp, list):
            emp = ", ".join(emp)

        pub = None
        raw_date = posting.get("datePosted")
        if raw_date:
            try:
                pub = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
            except ValueError:
                pub = None

        slug = url.rstrip("/").rsplit("/", 1)[-1]
        blob = f"{title} {location} {slug}".lower()
        is_remote = any(k in blob for k in ("télétravail", "teletravail", "remote", "télé-travail"))

        salary = self._salary(posting.get("baseSalary"))

        return NormalizedJob(
            source=self.source_key,
            external_id=slug,
            title=title,
            company=company,
            location=location or "Madagascar",
            is_remote=is_remote,
            contract_type=str(emp),
            description=description,
            salary=salary,
            url=url,
            apply_email=extract_email(_HTML_TAG_RE.sub(" ", description)),
            tags=[],
            published_at=pub,
        )

    @staticmethod
    def _location(job_location) -> str:
        loc = job_location[0] if isinstance(job_location, list) and job_location else job_location
        if not isinstance(loc, dict):
            return ""
        addr = loc.get("address")
        if isinstance(addr, dict):
            parts = [
                addr.get("addressLocality"),
                addr.get("addressRegion"),
                addr.get("addressCountry"),
            ]
            return ", ".join(p for p in parts if isinstance(p, str) and p)
        if isinstance(addr, str):
            return addr
        return ""

    @staticmethod
    def _salary(base_salary) -> str:
        if not isinstance(base_salary, dict):
            return ""
        value = base_salary.get("value")
        cur = base_salary.get("currency", "") or ""
        if isinstance(value, dict):
            lo, hi = value.get("minValue"), value.get("maxValue")
            if lo and hi:
                return f"{lo} - {hi} {cur}".strip()
            if value.get("value"):
                return f"{value['value']} {cur}".strip()
        return ""
