"""Adzuna — agrégateur mondial. Clé gratuite (app_id + app_key).
Doc : https://developer.adzuna.com/
"""
from __future__ import annotations

import os
from datetime import datetime, timezone

from .base import JobProvider, NormalizedJob

# Pays par défaut (code ISO sur 2 lettres, minuscule). "fr" pour la France.
DEFAULT_COUNTRY = os.getenv("ADZUNA_COUNTRY", "fr")


class AdzunaProvider(JobProvider):
    source_key = "adzuna"
    needs_credentials = True

    def __init__(self):
        self.app_id = os.getenv("ADZUNA_APP_ID", "")
        self.app_key = os.getenv("ADZUNA_APP_KEY", "")
        self.country = DEFAULT_COUNTRY

    def is_configured(self) -> bool:
        return bool(self.app_id and self.app_key)

    def search(self, keywords="", location="", remote=False, category="it") -> list[NormalizedJob]:
        url = f"https://api.adzuna.com/v1/api/jobs/{self.country}/search/1"
        params = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "results_per_page": 50,
            "content-type": "application/json",
        }
        if category == "it":
            # Catégorie officielle Adzuna pour l'informatique.
            params["category"] = "it-jobs"
        if keywords:
            params["what"] = keywords
        if location:
            params["where"] = location
        data = self._get(url, params=params)

        jobs = []
        for item in data.get("results", []):
            pub = None
            raw_date = item.get("created")
            if raw_date:
                try:
                    pub = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
                except ValueError:
                    pub = None
            loc = (item.get("location") or {}).get("display_name", "")
            salary = ""
            if item.get("salary_min") and item.get("salary_max"):
                salary = f"{int(item['salary_min'])} - {int(item['salary_max'])}"

            jobs.append(
                NormalizedJob(
                    source=self.source_key,
                    external_id=str(item.get("id")),
                    title=item.get("title", ""),
                    company=(item.get("company") or {}).get("display_name", ""),
                    location=loc,
                    is_remote="remote" in f"{item.get('title','')} {loc}".lower(),
                    contract_type=item.get("contract_time", "") or "",
                    description=item.get("description", ""),
                    salary=salary,
                    url=item.get("redirect_url", ""),
                    tags=[c.get("label") for c in [item.get("category", {})] if c.get("label")],
                    published_at=pub if not pub or pub.tzinfo else pub.replace(tzinfo=timezone.utc),
                )
            )
        return jobs
