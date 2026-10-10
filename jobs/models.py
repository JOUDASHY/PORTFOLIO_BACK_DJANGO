import hashlib

from django.db import models


def make_dedup_hash(source: str, external_id: str) -> str:
    """Identifiant stable d'une offre pour éviter les doublons entre collectes."""
    raw = f"{source}:{external_id}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


class JobSearchQuery(models.Model):
    """Recherche sauvegardée, rejouée périodiquement par la commande fetch_jobs."""

    CATEGORY_CHOICES = [
        ("it", "Informatique"),
        ("all", "Tous secteurs"),
    ]

    label = models.CharField(max_length=255, help_text="Nom lisible de la veille")
    keywords = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    # "it" = ne garder que les offres informatiques (filtrage au niveau des APIs).
    category = models.CharField(max_length=8, choices=CATEGORY_CHOICES, default="it")
    remote_only = models.BooleanField(default=False)
    # Liste de clés de providers à interroger ; vide = tous les providers actifs.
    sources = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    last_run_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Recherche d'offres"
        verbose_name_plural = "Recherches d'offres"
        ordering = ["-created_at"]

    def __str__(self):
        return self.label


class JobOffer(models.Model):
    """Offre normalisée, commune à toutes les sources."""

    SOURCE_CHOICES = [
        ("remotive", "Remotive"),
        ("arbeitnow", "Arbeitnow"),
        ("remoteok", "Remote OK"),
        ("themuse", "The Muse"),
        ("france_travail", "France Travail"),
        ("adzuna", "Adzuna"),
        ("jooble", "Jooble"),
        ("jobicy", "Jobicy"),
        ("himalayas", "Himalayas"),
        ("weworkremotely", "We Work Remotely"),
        ("asako", "Asako (Madagascar)"),
        ("recruteo", "Recruteo (Madagascar)"),
    ]
    STATUS_CHOICES = [
        ("new", "Nouvelle"),
        ("seen", "Vue"),
        ("saved", "Sauvegardée"),
        ("applied", "Candidaté"),
        ("ignored", "Ignorée"),
    ]

    source = models.CharField(max_length=32, choices=SOURCE_CHOICES)
    external_id = models.CharField(max_length=255)
    dedup_hash = models.CharField(max_length=64, unique=True, db_index=True)

    title = models.CharField(max_length=500)
    company = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    is_remote = models.BooleanField(default=False)
    contract_type = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    url = models.URLField(max_length=1000)
    salary = models.CharField(max_length=255, blank=True)

    # Candidature : email direct extrait de l'annonce (si présent) et flag
    # "postulable directement / gratuitement" (faux pour les plateformes payantes).
    apply_email = models.EmailField(blank=True)
    direct_apply = models.BooleanField(default=True)

    tags = models.JSONField(default=list, blank=True)
    match_score = models.IntegerField(default=0)

    published_at = models.DateTimeField(null=True, blank=True)
    fetched_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="new")
    query = models.ForeignKey(
        JobSearchQuery,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="offers",
    )
    prospect = models.ForeignKey(
        "core.Prospect",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="job_offers",
    )

    class Meta:
        verbose_name = "Offre"
        verbose_name_plural = "Offres"
        ordering = ["-published_at", "-fetched_at"]
        indexes = [
            models.Index(fields=["status"], name="jobs_jobof_status_idx"),
            models.Index(fields=["source"], name="jobs_jobof_source_idx"),
            models.Index(fields=["is_remote"], name="jobs_jobof_remote_idx"),
        ]

    def __str__(self):
        return f"[{self.source}] {self.title} — {self.company}"
