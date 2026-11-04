from django.core.validators import MaxValueValidator
from django.db import models


class SourceType(models.TextChoices):
    LINUX_AUTH = "linux_auth", "Linux authentication"
    WEB_ACCESS = "web_access", "Web access"
    WINDOWS_SECURITY = "windows_security", "Windows security"
    SYSMON = "sysmon", "Sysmon"
    FIREWALL = "firewall", "Firewall"
    SENSOR = "sensor", "Sensor"


class Source(models.Model):
    name = models.CharField(max_length=255, unique=True)
    source_type = models.CharField(max_length=32, choices=SourceType.choices)
    token_hash = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    class Domain(models.TextChoices):
        IT = "it", "IT"
        PHYSICAL = "physical", "Physical"

    class Outcome(models.TextChoices):
        SUCCESS = "success", "Success"
        FAILURE = "failure", "Failure"
        UNKNOWN = "unknown", "Unknown"

    event_time = models.DateTimeField()
    ingest_time = models.DateTimeField(auto_now_add=True)
    domain = models.CharField(max_length=16, choices=Domain.choices)
    source = models.ForeignKey(Source, on_delete=models.PROTECT)
    source_type = models.CharField(max_length=32, choices=SourceType.choices)
    host_or_device = models.CharField(max_length=255)
    category = models.CharField(max_length=64)
    action = models.CharField(max_length=128)
    outcome = models.CharField(
        max_length=16, choices=Outcome.choices, default=Outcome.UNKNOWN
    )
    user = models.CharField(max_length=255, blank=True, null=True)
    src_ip = models.GenericIPAddressField(null=True, blank=True)
    dst_ip = models.GenericIPAddressField(null=True, blank=True)
    severity = models.PositiveSmallIntegerField(
        default=0, validators=[MaxValueValidator(10)]
    )
    raw = models.TextField()
    extra = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-event_time"]
        indexes = [
            models.Index(fields=["event_time"], name="events_event_time_idx"),
            models.Index(
                fields=["host_or_device", "event_time"],
                name="events_host_time_idx",
            ),
            models.Index(
                fields=["source_type", "event_time"],
                name="events_type_time_idx",
            ),
            models.Index(fields=["user"], name="events_user_idx"),
            models.Index(fields=["src_ip"], name="events_src_ip_idx"),
        ]

    def __str__(self):
        return f"{self.action} on {self.host_or_device} at {self.event_time}"
