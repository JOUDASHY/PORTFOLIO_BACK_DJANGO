from django.contrib import admin

from .models import JobOffer, JobSearchQuery


@admin.register(JobSearchQuery)
class JobSearchQueryAdmin(admin.ModelAdmin):
    list_display = ("label", "keywords", "location", "category", "remote_only", "is_active", "last_run_at")
    list_filter = ("is_active", "category", "remote_only")
    search_fields = ("label", "keywords", "location")


@admin.register(JobOffer)
class JobOfferAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "source", "location", "is_remote",
                    "match_score", "status", "published_at")
    list_filter = ("source", "status", "is_remote")
    search_fields = ("title", "company", "location", "description")
    ordering = ("-match_score", "-published_at")
    list_editable = ("status",)
    readonly_fields = ("dedup_hash", "external_id", "fetched_at")
