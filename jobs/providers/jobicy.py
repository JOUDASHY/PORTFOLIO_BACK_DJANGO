"""Jobicy — API publique remote, aucune clé. Candidature directe (gratuite).
Doc : https://jobicy.com/jobs-rss-feed (API v2 JSON)
"""
from __future__ import annotations

from datetime import datetime

from .base import JobProvider, NormalizedJob, extract_email, looks_like_it

API_URL = "https://jobicy.com/api/v2/remote-jobs"


class JobicyProvider(JobProvider):
    source_key = "jobicy"
    needs_credentials = False

    def search(self, keywords="", location="", remote=False, category="it") -> list[NormalizedJob]:
        params = {"count": 50}
        if keywords:
            params["tag"] = keywords
        data = self._get(API_URL, params=params)

        jobs = []
        for item in data.get("jobs", []):
            title = item.get("jobTitle", "")
            tags = item.get("jobIndustry", []) or []
            if isinstance(tags, str):
                tags = [tags]
            if category == "it" and not looks_like_it(f"{title} {' '.join(tags)}"):
                continue
            pub = None
            raw = item.get("pubDate")
            if raw:
                try:
                    pub = datetime.fromisoformat(raw)
                except ValueError:
                    pub = None
            desc = item.get("jobDescription", "") or item.get("jobExcerpt", "")
            jobs.append(
                NormalizedJob(
                    source=self.source_key,
                    external_id=str(item.get("id")),
                    title=title,
                    company=item.get("companyName", ""),
                    location=item.get("jobGeo", "") or "Remote",
                    is_remote=True,
                    contract_type=item.get("jobType", "") or "",
                    description=desc,
                    url=item.get("url", ""),
                    apply_email=extract_email(desc),
                    tags=tags,
                    published_at=pub,
                )
            )
        return jobs
