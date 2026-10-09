"""Logique métier : collecte multi-sources, dédoublonnage, scoring, persistance."""
from __future__ import annotations

import logging
from urllib.parse import urlparse

from django.conf import settings
from django.utils import timezone

from .models import JobOffer, JobSearchQuery, make_dedup_hash
from .providers import NormalizedJob, get_providers

logger = logging.getLogger("jobs")

# Plateformes où postuler est verrouillé / payant (marketplaces, pas de candidature
# directe gratuite). Surchargeables via settings.JOB_BLACKLIST_DOMAINS.
DEFAULT_BLACKLIST = ["lemon.io", "toptal.com", "arc.dev", "turing.com", "gun.io"]


def _blacklist_domains() -> set[str]:
    return {d.lower() for d in getattr(settings, "JOB_BLACKLIST_DOMAINS", DEFAULT_BLACKLIST)}


def is_blacklisted(url: str) -> bool:
    """Vrai si l'URL appartient à une plateforme payante/verrouillée."""
    try:
        host = urlparse(url).netloc.lower()
    except Exception:
        return False
    return any(host == d or host.endswith("." + d) for d in _blacklist_domains())


def competence_terms() -> list[str]:
    """Noms des compétences du profil (pour scorer la pertinence vs ton CV)."""
    try:
        from core.models import Competence

        return [
            c.strip().lower()
            for c in Competence.objects.values_list("name", flat=True)
            if c and c.strip()
        ]
    except Exception:  # BDD indisponible / app non migrée
        return []


def score_offer(
    job: NormalizedJob, keywords: str, competences: list[str] | None = None
) -> int:
    """Score de pertinence : mots-clés + compétences du profil + remote."""
    score = 0
    title = job.title.lower()
    haystack = f"{job.title} {job.company} {' '.join(job.tags)} {job.description}".lower()
    for word in {w.strip().lower() for w in keywords.split() if len(w.strip()) > 2}:
        if word in title:
            score += 10
        elif word in haystack:
            score += 4
    # Bonus si l'offre matche tes compétences réelles.
    for comp in competences or []:
        if comp in title:
            score += 8
        elif comp in haystack:
            score += 3
    if job.is_remote:
        score += 3
    return score


def persist_jobs(
    jobs: list[NormalizedJob],
    keywords: str = "",
    query: JobSearchQuery | None = None,
    competences: list[str] | None = None,
) -> dict:
    """Enregistre/actualise une liste d'offres. Renvoie un récap chiffré."""
    created = updated = blacklisted = 0
    for job in jobs:
        if not job.external_id or not job.url:
            continue
        dedup = make_dedup_hash(job.source, job.external_id)
        blocked = is_blacklisted(job.url)
        if blocked:
            blacklisted += 1
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
            "apply_email": (job.apply_email or "")[:254],
            "direct_apply": not blocked,
            "tags": job.tags or [],
            "match_score": score_offer(job, keywords, competences),
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
    return {
        "created": created,
        "updated": updated,
        "received": len(jobs),
        "blacklisted": blacklisted,
    }


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

    competences = competence_terms()  # chargé une seule fois
    stats = persist_jobs(
        all_jobs, keywords=keywords, query=query, competences=competences
    )
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
