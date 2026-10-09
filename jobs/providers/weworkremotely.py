"""We Work Remotely — flux RSS public, aucune clé. Candidature directe employeur.
Doc : https://weworkremotely.com/remote-jobs.rss (et flux par catégorie)
"""
from __future__ import annotations

import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime

import requests

from .base import DEFAULT_TIMEOUT, USER_AGENT, JobProvider, NormalizedJob, extract_email, looks_like_it

# Catégorie programmation (tech) ; en mode "all" on prend le flux global.
FEED_IT = "https://weworkremotely.com/categories/remote-programming-jobs.rss"
FEED_ALL = "https://weworkremotely.com/remote-jobs.rss"


class WeWorkRemotelyProvider(JobProvider):
    source_key = "weworkremotely"
    needs_credentials = False

    def search(self, keywords="", location="", remote=False, category="it") -> list[NormalizedJob]:
        feed = FEED_IT if category == "it" else FEED_ALL
        resp = requests.get(
            feed, headers={"User-Agent": USER_AGENT}, timeout=DEFAULT_TIMEOUT
        )
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
        kw = keywords.lower().strip()

        jobs = []
        for item in root.findall(".//item"):
            raw_title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            desc = item.findtext("description") or ""
            region = (item.findtext("region") or "").strip()
            # WWR met "Company: Poste" dans le titre.
            if ":" in raw_title:
                company, title = [p.strip() for p in raw_title.split(":", 1)]
            else:
                company, title = "", raw_title

            if kw and kw not in f"{raw_title} {desc}".lower():
                continue
            if category == "it" and not looks_like_it(raw_title):
                continue

            pub = None
            raw_date = item.findtext("pubDate")
            if raw_date:
                try:
                    pub = parsedate_to_datetime(raw_date)
                except (TypeError, ValueError):
                    pub = None

            # external_id : dernier segment de l'URL (stable).
            ext = link.rstrip("/").rsplit("/", 1)[-1] or link

            jobs.append(
                NormalizedJob(
                    source=self.source_key,
                    external_id=ext,
                    title=title,
                    company=company,
                    location=region or "Remote",
                    is_remote=True,
                    description=desc,
                    url=link,
                    apply_email=extract_email(desc),
                    tags=[c.strip() for c in (item.findtext("category") or "").split(",") if c.strip()],
                    published_at=pub,
                )
            )
        return jobs
