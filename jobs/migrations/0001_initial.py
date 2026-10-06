import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core", "0051_add_education_to_award"),
    ]

    operations = [
        migrations.CreateModel(
            name="JobSearchQuery",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(help_text="Nom lisible de la veille", max_length=255)),
                ("keywords", models.CharField(blank=True, max_length=255)),
                ("location", models.CharField(blank=True, max_length=255)),
                ("category", models.CharField(choices=[("it", "Informatique"), ("all", "Tous secteurs")], default="it", max_length=8)),
                ("remote_only", models.BooleanField(default=False)),
                ("sources", models.JSONField(blank=True, default=list)),
                ("is_active", models.BooleanField(default=True)),
                ("last_run_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Recherche d'offres",
                "verbose_name_plural": "Recherches d'offres",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="JobOffer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("source", models.CharField(choices=[("remotive", "Remotive"), ("arbeitnow", "Arbeitnow"), ("remoteok", "Remote OK"), ("themuse", "The Muse"), ("france_travail", "France Travail"), ("adzuna", "Adzuna"), ("jooble", "Jooble")], max_length=32)),
                ("external_id", models.CharField(max_length=255)),
                ("dedup_hash", models.CharField(db_index=True, max_length=64, unique=True)),
                ("title", models.CharField(max_length=500)),
                ("company", models.CharField(blank=True, max_length=255)),
                ("location", models.CharField(blank=True, max_length=255)),
                ("is_remote", models.BooleanField(default=False)),
                ("contract_type", models.CharField(blank=True, max_length=100)),
                ("description", models.TextField(blank=True)),
                ("url", models.URLField(max_length=1000)),
                ("salary", models.CharField(blank=True, max_length=255)),
                ("tags", models.JSONField(blank=True, default=list)),
                ("match_score", models.IntegerField(default=0)),
                ("published_at", models.DateTimeField(blank=True, null=True)),
                ("fetched_at", models.DateTimeField(auto_now_add=True)),
                ("status", models.CharField(choices=[("new", "Nouvelle"), ("seen", "Vue"), ("saved", "Sauvegardée"), ("applied", "Candidaté"), ("ignored", "Ignorée")], default="new", max_length=16)),
                ("prospect", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="job_offers", to="core.prospect")),
                ("query", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="offers", to="jobs.jobsearchquery")),
            ],
            options={
                "verbose_name": "Offre",
                "verbose_name_plural": "Offres",
                "ordering": ["-published_at", "-fetched_at"],
            },
        ),
        migrations.AddIndex(
            model_name="joboffer",
            index=models.Index(fields=["status"], name="jobs_jobof_status_idx"),
        ),
        migrations.AddIndex(
            model_name="joboffer",
            index=models.Index(fields=["source"], name="jobs_jobof_source_idx"),
        ),
        migrations.AddIndex(
            model_name="joboffer",
            index=models.Index(fields=["is_remote"], name="jobs_jobof_remote_idx"),
        ),
    ]
