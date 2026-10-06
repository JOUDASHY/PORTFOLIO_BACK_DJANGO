"""Collecte les offres d'emploi depuis les sources configurées.

Exemples :
    python manage.py fetch_jobs                       # rejoue les recherches sauvegardées actives
    python manage.py fetch_jobs --keywords "django" --remote
    python manage.py fetch_jobs --keywords "react" --location "Paris" --sources remotive adzuna
    python manage.py fetch_jobs --query 3             # une JobSearchQuery précise

À planifier via cron / tâche planifiée Windows / GitHub Action.
"""
from django.core.management.base import BaseCommand, CommandError

from jobs.models import JobSearchQuery
from jobs.services import run_all_active_queries, run_search


class Command(BaseCommand):
    help = "Collecte les offres depuis les APIs (Remotive, Adzuna, France Travail, ...)."

    def add_arguments(self, parser):
        parser.add_argument("--keywords", type=str, default="")
        parser.add_argument("--location", type=str, default="")
        parser.add_argument("--remote", action="store_true")
        parser.add_argument("--sources", nargs="*", default=None,
                            help="Clés de providers (ex: remotive adzuna). Vide = toutes.")
        parser.add_argument("--category", choices=["it", "all"], default="it",
                            help="'it' (défaut) = offres informatiques uniquement.")
        parser.add_argument("--all-categories", action="store_true",
                            help="Raccourci pour --category all (tous secteurs).")
        parser.add_argument("--query", type=int, default=None,
                            help="ID d'une JobSearchQuery à rejouer.")

    def handle(self, *args, **opts):
        category = "all" if opts["all_categories"] else opts["category"]
        if opts["query"] is not None:
            try:
                q = JobSearchQuery.objects.get(pk=opts["query"])
            except JobSearchQuery.DoesNotExist:
                raise CommandError(f"JobSearchQuery #{opts['query']} introuvable.")
            recap = run_search(
                keywords=q.keywords, location=q.location, remote=q.remote_only,
                sources=q.sources or None, category=q.category, query=q,
            )
            self._report(q.label, recap)
            return

        has_adhoc = opts["keywords"] or opts["location"] or opts["sources"]
        if has_adhoc:
            recap = run_search(
                keywords=opts["keywords"], location=opts["location"],
                remote=opts["remote"], sources=opts["sources"], category=category,
            )
            self._report(f"recherche ad hoc ({category})", recap)
            return

        recaps = run_all_active_queries()
        if not recaps:
            self.stdout.write(self.style.WARNING(
                "Aucune recherche active. Crée une JobSearchQuery ou passe --keywords."
            ))
            return
        for recap in recaps:
            self._report(recap.get("query", "?"), recap)

    def _report(self, label, recap):
        self.stdout.write(self.style.SUCCESS(
            f"[{label}] reçues={recap['received']} "
            f"nouvelles={recap['created']} maj={recap['updated']}"
        ))
        for src, n in (recap.get("per_source") or {}).items():
            self.stdout.write(f"    - {src}: {n}")
