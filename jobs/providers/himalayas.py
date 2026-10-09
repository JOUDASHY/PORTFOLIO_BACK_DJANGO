"""Himalayas — API publique remote, aucune clé. Lien de candidature direct.
Doc : https://himalayas.app/jobs/api
"""
from __future__ import annotations

from datetime import datetime, timezone

from .base import JobProvider, NormalizedJob, extract_email, looks_like_it

API_URL = "https://himalayas.app/jobs/api"


class HimalayasProvider(JobProvider):
    source_key = "himalayas"
    needs_credentials = False

    def search(self, keywords="", location="", remote=False, category="it") -> list[NormalizedJob]:
        data = self._get(API_URL, params={"limit": 50})
        kw = keywords.lower().strip()

        jobs = []
        for item in data.get("jobs", []):
            title = item.get("title", "")
            company = item.get("companyName", "")
            cats = item.get("categories", []) or []
            if isinstance(cats, str):
                cats = [cats]
            desc_preview = item.get("description", "") or item.get("excerpt", "")
            haystack = f"{title} {company} {' '.join(cats)} {desc_preview}".lower()
            if kw and kw not in haystack:
                continue
            if category == "it" and not looks_like_it(f"{title} {' '.join(cats)}"):
                continue

            pub = None
            raw = item.get("pubDate")
            if raw:
                try:
                    pub = datetime.fromtimestamp(int(raw), tz=timezone.utc)
                except (ValueError, TypeError):
                    pub = None

            locs = item.get("locationRestrictions", []) or []
            if isinstance(locs, str):
                locs = [locs]
            desc = item.get("description", "") or item.get("excerpt", "")

            salary = ""
            if item.get("minSalary") and item.get("maxSalary"):
                cur = item.get("currency", "") or ""
                salary = f"{item['minSalary']} - {item['maxSalary']} {cur}".strip()

            jobs.append(
                NormalizedJob(
                    source=self.source_key,
                    external_id=str(item.get("guid") or item.get("applicationLink", "")),
                    title=title,
                    company=company,
                    location=", ".join(locs) or "Remote",
                    is_remote=True,
                    contract_type=item.get("employmentType", "") or "",
                    description=desc,
                    salary=salary,
                    url=item.get("applicationLink", ""),
                    apply_email=extract_email(desc),
                    tags=cats,
                    published_at=pub,
                )
            )
        return jobs
