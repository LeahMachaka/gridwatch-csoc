# Common event schema

Every log source is parsed into this one schema so that detection rules and search work the same on all sources.

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| `event_time` | datetime UTC | Yes | Time the event occurred. | `2026-11-04T18:25:00Z` |
| `ingest_time` | datetime UTC | No, set by the server | Time the server received the event. | `2026-11-04T18:25:02Z` |
| `domain` | string | Yes | Event domain. Allowed values: `it`, `physical`. | `it` |
| `source_type` | string | Yes | Source format or collector type. Allowed values: `linux_auth`, `web_access`, `windows_security`, `sysmon`, `firewall`, `sensor`. | `linux_auth` |
| `host_or_device` | string | Yes | Name or identifier of the originating host or device. | `server-01` |
| `category` | string | Yes | Broad event category. Allowed values: `authentication`, `web`, `process`, `network`, `device_health`, `tamper`, `system`. | `authentication` |
| `action` | string | Yes | Specific event action. | `login_failed` |
| `outcome` | string | Yes | Result of the action. Allowed values: `success`, `failure`, `unknown`. | `failure` |
| `user` | string | No | User associated with the event. | `admin` |
| `src_ip` | IP address | No | Source IP address, when available. | `192.0.2.10` |
| `dst_ip` | IP address | No | Destination IP address, when available. | `192.0.2.20` |
| `severity` | integer from 0 to 10 | Yes | Normalised severity, from lowest (`0`) to highest (`10`). | `5` |
| `raw` | string | Yes | Original source text, stored untouched. | `Failed password for admin from 192.0.2.10 port 54321 ssh2` |
| `extra` | JSON object | Yes | Source-specific fields that do not have a common schema field. | `{"port": 54321}` |

## Design rules

- Store `raw` untouched as received from the source.
- Represent all timestamps in UTC.
- Represent unknown values as `null` or `"unknown"` rather than guessing.
- Put new source-specific fields in `extra` first.

## Worked example

Raw sshd log line:

```text
Nov  4 18:25:00 server-01 sshd[1234]: Failed password for admin from 192.0.2.10 port 54321 ssh2
```

Normalised event:

```json
{
  "event_time": "2026-11-04T18:25:00Z",
  "ingest_time": "2026-11-04T18:25:02Z",
  "domain": "it",
  "source_type": "linux_auth",
  "host_or_device": "server-01",
  "category": "authentication",
  "action": "login_failed",
  "outcome": "failure",
  "user": "admin",
  "src_ip": "192.0.2.10",
  "dst_ip": null,
  "severity": 5,
  "raw": "Nov  4 18:25:00 server-01 sshd[1234]: Failed password for admin from 192.0.2.10 port 54321 ssh2",
  "extra": {
    "port": 54321,
    "protocol": "ssh2"
  }
}
```
