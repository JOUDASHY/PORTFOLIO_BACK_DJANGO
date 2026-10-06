"""Remote OK — flux public, aucune clé requise.
Doc : https://remoteok.com/api
Le premier élément du tableau est une entrée de légende, on le saute.
"""
from __future__ import annotations

from datetime import datetime, timezone

from .base import JobProvider, NormalizedJob

API_URL = "https://remoteok.com/api"


class RemoteOkProvider(JobProvider):
    source_key = "remoteok"
    needs_credentials = False

    def search(self, keywords="", location="", remote=False, category="it") -> list[NormalizedJob]:
        # Remote OK est un board remote tech : "it" ne nécessite aucun filtre extra.
        data = self._get(API_URL)
        if not isinstance(data, list):
            return []
        kw = keywords.lower().strip()

        jobs = []
        for item in data:
            # La première entrée est un objet de métadonnées (clé "legal").
            if not isinstance(item, dict) or "position" not in item:
                continue
            title = item.get("position", "") or item.get("title", "")
            company = item.get("company", "")
            tags = item.get("tags", []) or []

            haystack = f"{title} {company} {' '.join(tags)}".lower()
            if kw and kw not in haystack:
                continue

            pub = None
            raw_date = item.get("date")
            if raw_date:
                try:
                    pub = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
                except (ValueError, AttributeError):
                    pub = None

            jobs.append(
                NormalizedJob(
                    source=self.source_key,
                    external_id=str(item.get("id", item.get("slug", ""))),
                    title=title,
                    company=company,
                    location=item.get("location", "") or "Remote",
                    is_remote=True,
                    description=item.get("description", ""),
                    salary=self._salary(item),
                    url=item.get("url", ""),
                    tags=tags,
                    published_at=pub if pub and pub.tzinfo else (pub.replace(tzinfo=timezone.utc) if pub else None),
                )
            )
        return jobs

    @staticmethod
    def _salary(item: dict) -> str:
        lo, hi = item.get("salary_min"), item.get("salary_max")
        if lo and hi:
            return f"{lo} - {hi} USD"
        return ""
