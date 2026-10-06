"""Remotive — API publique remote, aucune clé requise.
Doc : https://remotive.com/api/remote-jobs
"""
from __future__ import annotations

from datetime import datetime, timezone

from .base import JobProvider, NormalizedJob

API_URL = "https://remotive.com/api/remote-jobs"


class RemotiveProvider(JobProvider):
    source_key = "remotive"
    needs_credentials = False

    def search(self, keywords="", location="", remote=False, category="it") -> list[NormalizedJob]:
        # Remotive est un board 100% tech : "it" ne nécessite aucun filtre extra.
        params = {"limit": 50}
        if keywords:
            params["search"] = keywords
        data = self._get(API_URL, params=params)

        jobs = []
        for item in data.get("jobs", []):
            pub = None
            raw_date = item.get("publication_date")
            if raw_date:
                try:
                    pub = datetime.fromisoformat(raw_date).replace(tzinfo=timezone.utc)
                except ValueError:
                    pub = None
            jobs.append(
                NormalizedJob(
                    source=self.source_key,
                    external_id=str(item.get("id")),
                    title=item.get("title", ""),
                    company=item.get("company_name", ""),
                    location=item.get("candidate_required_location", "") or "Remote",
                    is_remote=True,
                    contract_type=item.get("job_type", ""),
                    description=item.get("description", ""),
                    salary=item.get("salary", "") or "",
                    url=item.get("url", ""),
                    tags=item.get("tags", []) or [],
                    published_at=pub,
                )
            )
        return jobs
