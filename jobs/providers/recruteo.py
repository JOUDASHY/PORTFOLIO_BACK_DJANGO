"""Recruteo (recruteo.mg) — site d'emploi malgache. Candidature directe, gratuite.

Même approche fiable qu'Asako : le listing filtre les offres IT côté serveur
(`?secteur=Informatique`), et chaque page d'offre embarque un JSON-LD
`JobPosting` (schema.org) → extraction robuste.

robots.txt autorise /offres (seuls /admin, /api, /recruteur, /espace-membre bloqués).
On s'identifie via User-Agent et on plafonne les pages visitées.
"""
from __future__ import annotations

import os
import re
import time
from datetime import datetime

import requests

from .base import (
    DEFAULT_TIMEOUT,
    USER_AGENT,
    JobProvider,
    NormalizedJob,
    extract_email,
    extract_jobposting,
    jsonld_location,
    looks_like_it,
)

BASE = "https://recruteo.mg"
LISTING_IT = BASE + "/offres?secteur=Informatique"
LISTING_ALL = BASE + "/offres"
_LINK_RE = re.compile(r'href="(/offres/annonce/[^"#]+)"')
_HTML_TAG_RE = re.compile(r"<[^>]+>")
MAX_PAGES = int(os.getenv("RECRUTEO_MAX_PAGES", "30"))
REQUEST_DELAY = 0.25


class RecruteoProvider(JobProvider):
    source_key = "recruteo"
    needs_credentials = False

    def search(self, keywords="", location="", remote=False, category="it") -> list[NormalizedJob]:
        listing_url = LISTING_IT if category == "it" else LISTING_ALL
        try:
            resp = requests.get(
                listing_url, headers={"User-Agent": USER_AGENT}, timeout=DEFAULT_TIMEOUT
            )
            resp.raise_for_status()
        except requests.RequestException:
            return []

        links = list(dict.fromkeys(_LINK_RE.findall(resp.content.decode("utf-8", "replace"))))
        kw_terms = [w.strip().lower() for w in keywords.split() if len(w.strip()) > 2]
        links = links[:MAX_PAGES]

        jobs = []
        for href in links:
            url = requests.compat.urljoin(BASE, href)
            job = self._parse_offer(url)
            if not job:
                continue
            blob = f"{job.title} {job.description[:400]}".lower()
            if kw_terms and not any(t in f"{job.title} {job.description}".lower() for t in kw_terms):
                continue
            if category == "it" and not looks_like_it(blob):
                continue
            jobs.append(job)
            time.sleep(REQUEST_DELAY)
        return jobs

    def _parse_offer(self, url: str) -> NormalizedJob | None:
        try:
            resp = requests.get(
                url, headers={"User-Agent": USER_AGENT}, timeout=DEFAULT_TIMEOUT
            )
            resp.raise_for_status()
        except requests.RequestException:
            return None

        posting = extract_jobposting(resp.content.decode("utf-8", errors="replace"))
        if not posting:
            return None

        title = (posting.get("title") or "").strip()
        description = posting.get("description") or ""
        org = posting.get("hiringOrganization")
        company = (org.get("name") or "").strip() if isinstance(org, dict) else ""
        location = jsonld_location(posting.get("jobLocation"))
        emp = posting.get("employmentType") or ""
        if isinstance(emp, list):
            emp = ", ".join(emp)

        pub = None
        raw_date = posting.get("datePosted")
        if raw_date:
            try:
                pub = datetime.fromisoformat(str(raw_date).replace("Z", "+00:00"))
            except ValueError:
                pub = None

        slug = url.rstrip("/").rsplit("/", 1)[-1]
        blob = f"{title} {location} {slug}".lower()
        is_remote = any(k in blob for k in ("télétravail", "teletravail", "remote"))

        return NormalizedJob(
            source=self.source_key,
            external_id=slug,
            title=title,
            company=company,
            location=location or "Madagascar",
            is_remote=is_remote,
            contract_type=str(emp),
            description=description,
            url=url,
            apply_email=extract_email(_HTML_TAG_RE.sub(" ", description)),
            tags=[],
            published_at=pub,
        )
