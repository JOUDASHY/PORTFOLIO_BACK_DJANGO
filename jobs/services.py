"""Logique métier : collecte multi-sources, dédoublonnage, scoring, persistance."""
from __future__ import annotations

import logging

from django.utils import timezone

from .models import JobOffer, JobSearchQuery, make_dedup_hash
from .providers import NormalizedJob, get_providers

logger = logging.getLogger("jobs")


def score_offer(job: NormalizedJob, keywords: str) -> int:
    """Score de pertinence simple : présence des mots-clés + bonus remote."""
    score = 0
    haystack = f"{job.title} {job.company} {' '.join(job.tags)} {job.description}".lower()
    for word in {w.strip().lower() for w in keywords.split() if len(w.strip()) > 2}:
        if word in job.title.lower():
            score += 10
        elif word in haystack:
            score += 4
    if job.is_remote:
        score += 3
    return score


def persist_jobs(
    jobs: list[NormalizedJob],
    keywords: str = "",
    query: JobSearchQuery | None = None,
) -> dict:
    """Enregistre/actualise une liste d'offres. Renvoie un récap chiffré."""
    created = updated = 0
    for job in jobs:
        if not job.external_id or not job.url:
            continue
        dedup = make_dedup_hash(job.source, job.external_id)
        defaults = {
            "source": job.source,
            "external_id": job.external_id,
            "title": job.title[:500],
            "company": job.company[:255],
            "location": job.location[:255],
            "is_remote": job.is_remote,
            "contract_type": (job.contract_type or "")[:100],
            "description": job.description or "",
            "url": job.url[:1000],
            "salary": (job.salary or "")[:255],
            "tags": job.tags or [],
            "match_score": score_offer(job, keywords),
            "published_at": job.published_at,
            "query": query,
        }
        obj, was_created = JobOffer.objects.update_or_create(
            dedup_hash=dedup, defaults=defaults
        )
        # On ne réécrase pas un statut manuel (saved/applied/ignored) sur un refetch.
        if was_created:
            created += 1
        else:
            updated += 1
    return {"created": created, "updated": updated, "received": len(jobs)}


def run_search(
    keywords: str = "",
    location: str = "",
    remote: bool = False,
    sources: list[str] | None = None,
    category: str = "it",
    query: JobSearchQuery | None = None,
) -> dict:
    """Interroge les providers, agrège, persiste. Tolérant aux pannes de source.

    `category="it"` (défaut) ne remonte que les offres informatiques.
    """
    providers = get_providers(sources)
    all_jobs: list[NormalizedJob] = []
    per_source: dict[str, int] = {}

    for provider in providers:
        results = provider.safe_search(
            keywords=keywords, location=location, remote=remote, category=category
        )
        per_source[provider.source_key] = len(results)
        all_jobs.extend(results)

    stats = persist_jobs(all_jobs, keywords=keywords, query=query)
    stats["per_source"] = per_source

    if query is not None:
        query.last_run_at = timezone.now()
        query.save(update_fields=["last_run_at"])

    logger.info("run_search terminé : %s", stats)
    return stats


def run_all_active_queries() -> list[dict]:
    """Rejoue toutes les JobSearchQuery actives (appelé par le cron)."""
    recaps = []
    for query in JobSearchQuery.objects.filter(is_active=True):
        recap = run_search(
            keywords=query.keywords,
            location=query.location,
            remote=query.remote_only,
            sources=query.sources or None,
            category=query.category,
            query=query,
        )
        recap["query"] = query.label
        recaps.append(recap)
    return recaps
