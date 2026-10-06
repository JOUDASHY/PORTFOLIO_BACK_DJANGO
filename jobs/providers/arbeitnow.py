"""Arbeitnow — API publique (Europe, beaucoup de remote), aucune clé requise.
Doc : https://www.arbeitnow.com/api/job-board-api
"""
from __future__ import annotations

from datetime import datetime, timezone

from .base import JobProvider, NormalizedJob, looks_like_it

API_URL = "https://www.arbeitnow.com/api/job-board-api"


class ArbeitnowProvider(JobProvider):
    source_key = "arbeitnow"
    needs_credentials = False

    def search(self, keywords="", location="", remote=False, category="it") -> list[NormalizedJob]:
        data = self._get(API_URL)
        kw = keywords.lower().strip()
        loc = location.lower().strip()

        jobs = []
        for item in data.get("data", []):
            title = item.get("title", "")
            company = item.get("company_name", "")
            item_remote = bool(item.get("remote"))
            item_loc = item.get("location", "")
            tags = item.get("tags", []) or []

            # L'API ne filtre pas côté serveur : on filtre localement.
            haystack = f"{title} {company} {' '.join(tags)}".lower()
            if kw and kw not in haystack:
                continue
            if loc and loc not in item_loc.lower():
                continue
            if remote and not item_remote:
                continue
            # Arbeitnow est généraliste : en catégorie "it", on écarte le non-tech.
            if category == "it" and not looks_like_it(f"{title} {' '.join(tags)}"):
                continue

            pub = None
            ts = item.get("created_at")
            if ts:
                try:
                    pub = datetime.fromtimestamp(int(ts), tz=timezone.utc)
                except (ValueError, TypeError):
                    pub = None

            jobs.append(
                NormalizedJob(
                    source=self.source_key,
                    external_id=str(item.get("slug", "")),
                    title=title,
                    company=company,
                    location=item_loc,
                    is_remote=item_remote,
                    contract_type=", ".join(item.get("job_types", []) or []),
                    description=item.get("description", ""),
                    url=item.get("url", ""),
                    tags=tags,
                    published_at=pub,
                )
            )
        return jobs
