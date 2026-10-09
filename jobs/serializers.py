from rest_framework import serializers

from .models import JobOffer, JobSearchQuery


class JobOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOffer
        fields = [
            "id", "source", "title", "company", "location", "is_remote",
            "contract_type", "description", "url", "salary",
            "apply_email", "direct_apply", "tags",
            "match_score", "published_at", "fetched_at", "status",
            "query", "prospect",
        ]
        read_only_fields = [
            "id", "source", "title", "company", "location", "is_remote",
            "contract_type", "description", "url", "salary",
            "apply_email", "direct_apply", "tags",
            "match_score", "published_at", "fetched_at", "query", "prospect",
        ]


class JobSearchQuerySerializer(serializers.ModelSerializer):
    offers_count = serializers.IntegerField(source="offers.count", read_only=True)

    class Meta:
        model = JobSearchQuery
        fields = [
            "id", "label", "keywords", "location", "category", "remote_only",
            "sources", "is_active", "last_run_at", "created_at", "offers_count",
        ]
        read_only_fields = ["id", "last_run_at", "created_at", "offers_count"]


class RunSearchSerializer(serializers.Serializer):
    keywords = serializers.CharField(required=False, allow_blank=True, default="")
    location = serializers.CharField(required=False, allow_blank=True, default="")
    remote = serializers.BooleanField(required=False, default=False)
    category = serializers.ChoiceField(
        choices=["it", "all"], required=False, default="it"
    )
    sources = serializers.ListField(
        child=serializers.CharField(), required=False, default=list
    )
