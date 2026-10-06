"""The Muse — API gratuite. Clé optionnelle (augmente le quota) via THEMUSE_API_KEY.
Doc : https://www.themuse.com/developers/api/v2
"""
from __future__ import annotations

import os
import re
from datetime import datetime

from .base import JobProvider, NormalizedJob

API_URL = "https://www.themuse.com/api/public/jobs"
_TAG_RE = re.compile(r"<[^>]+>")

# Catégories The Muse correspondant à l'informatique.
IT_CATEGORIES = ["Software Engineering", "Data Science", "Computer and IT", "UX"]


class TheMuseProvider(JobProvider):
    source_key = "themuse"
    needs_credentials = False  # fonctionne sans clé (quota réduit)

    def __init__(self):
        self.api_key = os.getenv("THEMUSE_API_KEY", "")

    def search(self, keywords="", location="", remote=False, category="it") -> list[NormalizedJob]:
        params = {"page": 0}
        if category == "it":
            params["category"] = IT_CATEGORIES  # requests répète la clé
        if self.api_key:
            params["api_key"] = self.api_key
        if location:
            params["location"] = location
        if remote:
            params["location"] = "Flexible / Remote"
        data = self._get(API_URL, params=params)
        kw = keywords.lower().strip()

        jobs = []
        for item in data.get("results", []):
            title = item.get("name", "")
            company = (item.get("company") or {}).get("name", "")
            if kw and kw not in f"{title} {company}".lower():
                continue
            locs = ", ".join(loc.get("name", "") for loc in item.get("locations", []))
            pub = None
            raw_date = item.get("publication_date")
            if raw_date:
                try:
                    pub = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
                except ValueError:
                    pub = None
            refs = item.get("refs") or {}

            jobs.append(
                NormalizedJob(
                    source=self.source_key,
                    external_id=str(item.get("id")),
                    title=title,
                    company=company,
                    location=locs,
                    is_remote="remote" in locs.lower() or "flexible" in locs.lower(),
                    contract_type=item.get("type", ""),
                    description=_TAG_RE.sub("", item.get("contents", "") or ""),
                    url=refs.get("landing_page", ""),
                    tags=[c.get("name") for c in item.get("categories", []) if c.get("name")],
                    published_at=pub,
                )
            )
        return jobs
