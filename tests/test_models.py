from datetime import datetime, timezone

import pytest

from events.models import Event, Source, SourceType


@pytest.mark.django_db
def test_event_saves_and_reads_back():
    source = Source.objects.create(
        name="server-01",
        source_type=SourceType.LINUX_AUTH,
        token_hash="a" * 64,
    )
    event_time = datetime(2026, 11, 4, 18, 25, tzinfo=timezone.utc)
    event = Event.objects.create(
        event_time=event_time,
        domain=Event.Domain.IT,
        source=source,
        source_type=source.source_type,
        host_or_device="server-01",
        category="authentication",
        action="login_failed",
        outcome=Event.Outcome.FAILURE,
        user="admin",
        src_ip="192.0.2.10",
        severity=5,
        raw="Failed password for admin from 192.0.2.10 port 54321 ssh2",
        extra={"port": 54321, "protocol": "ssh2"},
    )

    saved_event = Event.objects.get(pk=event.pk)

    assert saved_event.source == source
    assert saved_event.event_time == event_time
    assert saved_event.ingest_time is not None
    assert saved_event.action == "login_failed"
    assert saved_event.user == "admin"
    assert saved_event.src_ip == "192.0.2.10"
    assert saved_event.extra == {"port": 54321, "protocol": "ssh2"}
