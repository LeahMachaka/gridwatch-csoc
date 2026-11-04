from django.contrib import admin

from events.models import Event, Source


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("name", "source_type", "is_active", "last_seen", "created_at")
    list_filter = ("source_type", "is_active")
    search_fields = ("name",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "event_time",
        "source",
        "source_type",
        "category",
        "action",
        "outcome",
        "severity",
        "host_or_device",
    )
    list_filter = ("source_type", "domain", "category", "outcome", "severity")
    search_fields = ("host_or_device", "user", "action", "raw")
