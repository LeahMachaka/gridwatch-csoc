from collections import Counter

from django.shortcuts import render


def dashboard(request):
    """
    This is the main dashboard view.
    It holds all the data that will appear on the screen.
    We use plain Python lists and dictionaries — easy to read and explain.
    """
 
    # ---------------------------------------------------------------
    # KPI CARDS — the four summary numbers at the top of the dashboard
    # ---------------------------------------------------------------
    kpi_cards = [
        {
            "label": "Total Devices",
            "value": "15",
            "icon": "server",
            "color": "blue",
            "sub": "Across 3 zones",
        },
        {
            "label": "Active Alerts",
            "value": "3",
            "icon": "alert-triangle",
            "color": "red",
            "sub": "1 CRITICAL, 2 HIGH",
        },
        {
            "label": "Incidents Today",
            "value": "1",
            "icon": "file-text",
            "color": "orange",
            "sub": "IIR-2025-001 open",
        },
        {
            "label": "Zones Monitored",
            "value": "3",
            "icon": "layers",
            "color": "green",
            "sub": "All zones healthy",
        },
    ]
 
    # ---------------------------------------------------------------
    # PBAD ALERT FEED — recent security events shown in the left column
    # ---------------------------------------------------------------
    alerts = [
        {
            "id": "IIR-2025-001",
            "time": "02:17:43",
            "date": "15 May 2025",
            "device": "IoT-CAM-01",
            "ip": "192.168.10.21",
            "zone": "Zone 1",
            "severity": "CRITICAL",
            "score": 94,
            "message": "External HTTPS connection to 185.220.101.47. 47.3 MB exfiltrated in 26 seconds. Device isolated.",
            "status": "CONTAINED",
        },
        {
            "id": "ALT-2025-019",
            "time": "14:03:11",
            "date": "14 May 2025",
            "device": "IoT-EP-01",
            "ip": "192.168.10.31",
            "zone": "Zone 1",
            "severity": "HIGH",
            "score": 67,
            "message": "Entry panel triggered 134 events between 23:00 and 01:00 UTC. Exceeds daily limit of 100.",
            "status": "INVESTIGATING",
        },
        {
            "id": "ALT-2025-018",
            "time": "09:45:22",
            "date": "13 May 2025",
            "device": "OT-UPS-01",
            "ip": "192.168.20.51",
            "zone": "Zone 2",
            "severity": "HIGH",
            "score": 61,
            "message": "UPS battery dropped to 43% without scheduled load event. Unexpected charge cycle initiated.",
            "status": "RESOLVED",
        },
        {
            "id": "ALT-2025-017",
            "time": "06:12:55",
            "date": "12 May 2025",
            "device": "IoT-MS-02",
            "ip": "192.168.10.12",
            "zone": "Zone 1",
            "severity": "MEDIUM",
            "score": 44,
            "message": "Motion sensor triggered 38 times in one hour between 04:00 and 05:00. Outside normal window.",
            "status": "RESOLVED",
        },
        {
            "id": "ALT-2025-016",
            "time": "22:58:01",
            "date": "11 May 2025",
            "device": "OT-LGT-01",
            "ip": "192.168.20.31",
            "zone": "Zone 2",
            "severity": "MEDIUM",
            "score": 38,
            "message": "Lighting controller received command at 23:47 UTC outside its defined schedule window.",
            "status": "RESOLVED",
        },
    ]
 
    # ---------------------------------------------------------------
    # DEVICE TABLE — all 15 monitored devices with their current status
    # ---------------------------------------------------------------
    devices = [
        # Zone 1 — IoT Devices
        {"hostname": "IoT-MS-01",   "ip": "192.168.10.11", "zone": "Zone 1", "function": "Motion Sensor A",        "score": 4,  "status": "ONLINE"},
        {"hostname": "IoT-MS-02",   "ip": "192.168.10.12", "zone": "Zone 1", "function": "Motion Sensor B",        "score": 12, "status": "ONLINE"},
        {"hostname": "IoT-CAM-01",  "ip": "192.168.10.21", "zone": "Zone 1", "function": "IP Camera 01",           "score": 94, "status": "ISOLATED"},
        {"hostname": "IoT-CAM-02",  "ip": "192.168.10.22", "zone": "Zone 1", "function": "IP Camera 02",           "score": 8,  "status": "ONLINE"},
        {"hostname": "IoT-EP-01",   "ip": "192.168.10.31", "zone": "Zone 1", "function": "Smart Entry Panel",      "score": 67, "status": "ALERT"},
        {"hostname": "IoT-ENV-01",  "ip": "192.168.10.41", "zone": "Zone 1", "function": "Environmental Monitor",  "score": 5,  "status": "ONLINE"},
        # Zone 2 — OT Devices
        {"hostname": "OT-HVAC-01",  "ip": "192.168.20.11", "zone": "Zone 2", "function": "HVAC Controller",        "score": 9,  "status": "ONLINE"},
        {"hostname": "OT-PWR-01",   "ip": "192.168.20.21", "zone": "Zone 2", "function": "Smart Power Meter",      "score": 17, "status": "ONLINE"},
        {"hostname": "OT-LGT-01",   "ip": "192.168.20.31", "zone": "Zone 2", "function": "Lighting Controller",    "score": 22, "status": "ONLINE"},
        {"hostname": "OT-FSS-01",   "ip": "192.168.20.41", "zone": "Zone 2", "function": "Fire Suppression Sensor","score": 3,  "status": "ONLINE"},
        {"hostname": "OT-UPS-01",   "ip": "192.168.20.51", "zone": "Zone 2", "function": "UPS Monitor",            "score": 61, "status": "ALERT"},
        # Zone 3 — CSOC and Admin
        {"hostname": "SRV-CSOC-01", "ip": "192.168.30.10", "zone": "Zone 3", "function": "CSOC Workstation",       "score": 2,  "status": "ONLINE"},
        {"hostname": "SRV-APP-01",  "ip": "192.168.30.20", "zone": "Zone 3", "function": "Application Server",     "score": 6,  "status": "ONLINE"},
        {"hostname": "SRV-SIEM-01", "ip": "192.168.30.30", "zone": "Zone 3", "function": "SIEM and Syslog Server", "score": 11, "status": "ONLINE"},
        {"hostname": "WS-ADM-01",   "ip": "192.168.30.40", "zone": "Zone 3", "function": "Admin Workstation",      "score": 7,  "status": "ONLINE"},
    ]
 
    # ---------------------------------------------------------------
    # ZONE HEALTH — status cards shown at the bottom of the dashboard
    # ---------------------------------------------------------------
    zones = [
        {
            "name": "Zone 1",
            "label": "IoT Perimeter",
            "vlan": "VLAN 10",
            "subnet": "192.168.10.0/24",
            "device_count": 6,
            "online": 4,
            "alert": 1,
            "isolated": 1,
            "health": "DEGRADED",
            "health_color": "orange",
            "description": "IP cameras, motion sensors, entry panel, environmental monitor",
        },
        {
            "name": "Zone 2",
            "label": "OT Operations",
            "vlan": "VLAN 20",
            "subnet": "192.168.20.0/24",
            "device_count": 5,
            "online": 4,
            "alert": 1,
            "isolated": 0,
            "health": "DEGRADED",
            "health_color": "orange",
            "description": "HVAC, power meter, lighting, fire suppression, UPS",
        },
        {
            "name": "Zone 3",
            "label": "CSOC Secure",
            "vlan": "VLAN 30",
            "subnet": "192.168.30.0/24",
            "device_count": 4,
            "online": 4,
            "alert": 0,
            "isolated": 0,
            "health": "HEALTHY",
            "health_color": "green",
            "description": "CSOC workstation, app server, SIEM, admin workstation",
        },
    ]
 
    # ---------------------------------------------------------------
    # SEVERITY BREAKDOWN — used to draw the bar chart on the right
    # ---------------------------------------------------------------
    severity_counts = [
        {"level": "CRITICAL", "count": 1, "color": "#ef4444"},
        {"level": "HIGH",     "count": 2, "color": "#f97316"},
        {"level": "MEDIUM",   "count": 2, "color": "#eab308"},
        {"level": "LOW",      "count": 0, "color": "#22c55e"},
    ]

    thumbs = ("img/thumb-1.svg", "img/thumb-2.svg", "img/thumb-3.svg")
    alerts = [{**row, "thumb": thumbs[i % len(thumbs)]} for i, row in enumerate(alerts)]

    zone_order = ("Zone 1", "Zone 2", "Zone 3")
    zone_totals = Counter(d["zone"] for d in devices)
    chart_zones = {
        "labels": [z for z in zone_order if z in zone_totals],
        "values": [zone_totals[z] for z in zone_order if z in zone_totals],
    }
    chart_severity = {
        "labels": [row["level"] for row in severity_counts],
        "values": [row["count"] for row in severity_counts],
        "colors": [row["color"] for row in severity_counts],
    }

    # ---------------------------------------------------------------
    # Send all the data to the template using the context dictionary.
    # The keys on the left are what the template will use.
    # ---------------------------------------------------------------
    context = {
        "kpi_cards": kpi_cards,
        "alerts": alerts,
        "devices": devices,
        "zones": zones,
        "severity_counts": severity_counts,
        "chart_zones": chart_zones,
        "chart_severity": chart_severity,
        "analyst": "Leah Machaka",
        "campus": "Al Noor Government Services Campus",
        "page_title": "GridWatch CSOC",
    }
 
    # Render means: take this data, put it into the HTML template, return the page.
    return render(request, "dashboard/index.html", context)
 
 
def incident_report(request):
    """
    This view shows the full Incident Intelligence Report IIR-2025-001.
    It uses the same data that was gathered during the simulated incident.
    """
 
    timeline = [
        {"time": "02:00:00", "event": "System",       "description": "Scheduled quiet period begins. No Zone 1 activity expected until 06:00 UTC."},
        {"time": "02:17:43", "event": "PBAD Alert",   "description": "Outbound TCP connection from 192.168.10.21 to 185.220.101.47 on port 443 detected."},
        {"time": "02:17:45", "event": "Triage",        "description": "Automated severity scoring assigns CRITICAL. Alert escalated. IIR-2025-001 created."},
        {"time": "02:18:10", "event": "Analysis",      "description": "PBAD logs record 47.3 MB of outbound data in 26 seconds. Pattern consistent with exfiltration."},
        {"time": "02:19:00", "event": "Analyst",       "description": "CSOC analyst LM-CSOC-01 acknowledges alert. PBAD deviation score confirmed at 94/100."},
        {"time": "02:21:30", "event": "Containment",   "description": "Deny rule applied on RTR-CORE-01. IoT-CAM-01 isolated from the network."},
        {"time": "02:24:00", "event": "Escalation",    "description": "Incident escalated to Infrastructure Security Lead and CISO duty officer."},
        {"time": "02:30:00", "event": "Forensic Hold", "description": "SRV-SIEM-01 captures and write-protects all IoT-CAM-01 traffic logs."},
        {"time": "06:00:00", "event": "Status Update", "description": "Device remains isolated. Physical inspection scheduled. Replacement camera being sourced."},
    ]
 
    recommendations = [
        {"ref": "R01", "text": "Implement mandatory firmware update policy. Critical CVE patches within 72 hours of release.", "priority": "CRITICAL"},
        {"ref": "R02", "text": "Change all IoT device credentials from factory defaults. Store in privileged access management system.", "priority": "CRITICAL"},
        {"ref": "R03", "text": "Implement automated PBAD isolation. Score above 85 should auto-apply deny ACL without analyst confirmation.", "priority": "HIGH"},
        {"ref": "R04", "text": "Add outbound filtering on RTR-GW-01 blocking Zone 1 and Zone 2 from initiating external connections.", "priority": "HIGH"},
        {"ref": "R05", "text": "Conduct full Zone 1 audit to verify firmware versions, credentials, and PBAD baselines.", "priority": "HIGH"},
        {"ref": "R06", "text": "Enrich SIEM correlation rules with IoT-CAM-01 pattern to improve detection of similar attempts.", "priority": "MEDIUM"},
        {"ref": "R07", "text": "Review and update PBAD baselines for all campus devices on a quarterly schedule.", "priority": "MEDIUM"},
    ]
 
    context = {
        "timeline": timeline,
        "recommendations": recommendations,
        "page_title": "IIR-2025-001 — Incident Intelligence Report",
    }
 
    return render(request, "dashboard/incident_report.html", context)
 