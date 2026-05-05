# GridWatch CSOC
### IoT Cyber Security Operations and Incident Intelligence Platform

**Author:** Leah Machaka
**Programme:** National Diploma: ICT, 3rd Year
**Location:** Gauteng, South Africa
**GitHub:** [github.com/LeahMachaka](https://github.com/LeahMachaka)
**Status:** In Development — May 2025
**Live Demo:** [gritwatch-csoc-2.onrender.com/](https://gridwatch-csoc-1.onrender.com/)

---

## What Is GridWatch CSOC?

GridWatch CSOC is a student-built IoT Cyber Security Operations and Incident Intelligence Platform. It simulates a Dubai government campus network to demonstrate real-world IoT security monitoring, network segmentation, and an original security innovation called Passive Behavioural Anomaly Detection (PBAD).

The platform monitors 15 IoT and operational technology devices across three network security zones. When any device behaves differently from its established baseline, GridWatch CSOC raises a CSOC alert and generates a formal Incident Intelligence Report — the same type of document a security analyst would deliver to a CISO after a real incident.

---

## The Problem This Solves

Most IoT security systems verify a device identity when it connects to the network. Once authenticated, the device is trusted. The problem is that threat actors commonly compromise a legitimate IoT device so it passes authentication, then use that device to do something it should never do — exfiltrate data, communicate with external servers, or move laterally across the network.

**Zero Trust answers: who are you?**
**PBAD answers: are you still behaving as expected after we trusted you?**

This is the gap. GridWatch CSOC builds the next layer.

---

## Innovation: Passive Behavioural Anomaly Detection (PBAD)

PBAD profiles the normal communication behaviour of every IoT device after it joins the network. Each device gets a baseline covering approved destination IPs, active hours, data transfer volumes, protocols used, and connection direction.

The CSOC dashboard calculates a real-time deviation score for each device from 0 to 100. When the score crosses 80, a CRITICAL alert fires. When it crosses 60, a HIGH alert fires. The dashboard logs the event and a formal Incident Intelligence Report is generated.

This directly extends the Dubai Electronic Security Centre 2025 Zero Trust Assessment Tool launched at GISEC Global, which secures device identity at authentication. PBAD secures device behaviour after authentication — the next unsolved problem.

---

## Simulated Environment

**Name:** Al Noor Government Services Campus (Fictional, Dubai, UAE)
**Tool:** Cisco Packet Tracer 9.0.0
**Scenario:** A fictional Dubai government entity campus with three security zones, monitored continuously by GridWatch CSOC.

| Zone | VLAN | Subnet | Router Interface | Contents |
|------|------|--------|-----------------|----------|
| Zone 1 | 10 | 192.168.10.0/24 | GigabitEthernet0/0 | IoT cameras, motion sensors, entry panel, environmental monitor |
| Zone 2 | 20 | 192.168.20.0/24 | GigabitEthernet0/1 | HVAC, power meter, lighting controller, fire suppression, UPS |
| Zone 3 | 30 | 192.168.30.0/24 | GigabitEthernet0/2 | CSOC workstation, app server, SIEM server, admin workstation |
| Core | 99 | 192.168.99.0/24 | Management only | Switch management interfaces |

---

## Device Register

| Hostname | IP Address | Zone | Function |
|----------|------------|------|----------|
| IoT-MS-01 | 192.168.10.11 | Zone 1 | Motion Sensor A |
| IoT-MS-02 | 192.168.10.12 | Zone 1 | Motion Sensor B |
| IoT-CAM-01 | 192.168.10.21 | Zone 1 | IP Camera 01 |
| IoT-CAM-02 | 192.168.10.22 | Zone 1 | IP Camera 02 |
| IoT-EP-01 | 192.168.10.31 | Zone 1 | Smart Entry Panel |
| IoT-ENV-01 | 192.168.10.41 | Zone 1 | Environmental Monitor |
| OT-HVAC-01 | 192.168.20.11 | Zone 2 | HVAC Controller |
| OT-PWR-01 | 192.168.20.21 | Zone 2 | Smart Power Meter |
| OT-LGT-01 | 192.168.20.31 | Zone 2 | Lighting Controller |
| OT-FSS-01 | 192.168.20.41 | Zone 2 | Fire Suppression Sensor |
| OT-UPS-01 | 192.168.20.51 | Zone 2 | UPS Monitor |
| SRV-CSOC-01 | 192.168.30.10 | Zone 3 | CSOC Monitoring Workstation |
| SRV-APP-01 | 192.168.30.20 | Zone 3 | Government Application Server |
| SRV-SIEM-01 | 192.168.30.30 | Zone 3 | SIEM and Syslog Server |
| WS-ADM-01 | 192.168.30.40 | Zone 3 | Admin Workstation |

---

## Network Security Design

The GridWatch CSOC topology enforces strict traffic rules using two Extended Access Control Lists applied inbound on the Zone 1 and Zone 2 router interfaces.

| ACL | Rule | Action | Reason |
|-----|------|--------|--------|
| ZONE1_IN | permit icmp echo-reply to Zone 3 | PERMIT | Allows ping replies from IoT devices back to CSOC |
| ZONE1_IN | permit Zone 1 to 192.168.30.30 | PERMIT | IoT devices may send logs to SIEM server only |
| ZONE1_IN | deny Zone 1 to Zone 3 | DENY | Blocks all other Zone 1 to Zone 3 traffic |
| ZONE1_IN | deny Zone 1 to Zone 2 | DENY | Prevents IoT devices reaching OT layer |
| ZONE2_IN | permit icmp echo-reply to Zone 3 | PERMIT | Allows ping replies from OT devices back to CSOC |
| ZONE2_IN | permit Zone 2 to 192.168.30.30 | PERMIT | OT devices may send logs to SIEM server only |
| ZONE2_IN | deny Zone 2 to Zone 3 | DENY | Blocks all other Zone 2 to Zone 3 traffic |
| ZONE2_IN | deny Zone 2 to Zone 1 | DENY | Prevents OT devices reaching IoT layer |

Zone 3 (CSOC and admin) has full access to all zones for monitoring purposes.

---

## Verification Results

All tests performed from SRV-CSOC-01 in Cisco Packet Tracer 9.0.0. ACL match counts confirmed via show access-lists.

| Test | Destination | Result |
|------|-------------|--------|
| Zone 3 internal | SRV-APP-01 (192.168.30.20) | PASS |
| Zone 3 internal | SRV-SIEM-01 (192.168.30.30) | PASS |
| Zone 3 internal | WS-ADM-01 (192.168.30.40) | PASS |
| Zone 3 to Zone 1 | IoT-MS-01 (192.168.10.11) | PASS |
| Zone 3 to Zone 1 | IoT-CAM-01 (192.168.10.21) | PASS |
| Zone 3 to Zone 2 | OT-HVAC-01 (192.168.20.11) | PASS |
| Zone 3 to Zone 2 | OT-PWR-01 (192.168.20.21) | PASS |
| Zone 3 to Zone 2 | OT-FSS-01 (192.168.20.41) | PASS |
| Zone 3 to Zone 2 | OT-UPS-01 (192.168.20.51) | PASS |

---

## PBAD Device Profiles

| Device | Normal Behaviour | Anomaly Trigger | Severity |
|--------|-----------------|-----------------|----------|
| IP Camera 01/02 | Streams to SIEM only, no external IPs | Traffic to any external IP | CRITICAL |
| HVAC Controller | Internal communication only | Any external IP contact | CRITICAL |
| Fire Sensor | Silent unless triggered, one heartbeat per minute | Multiple triggers within 5 minutes | CRITICAL |
| SIEM Server | Receives syslog only, never initiates traffic | Any outbound connection initiated | CRITICAL |
| Smart Entry Panel | Max 100 events per day, 07:00 to 20:00 | Outside hours or above volume | HIGH |
| Power Meter | Within 20% of 7-day rolling average | Spike above 20% without cause | HIGH |
| UPS Monitor | Battery above 80%, charge cycle every 72 hours | Battery drops below 50% unexpectedly | HIGH |
| CSOC Workstation | Authenticated sessions only, 08:00 to 18:00 | Login outside hours or 3 failed attempts | HIGH |
| Motion Sensor A/B | Max 30 triggers per hour, 06:00 to 22:00 | Outside hours or above trigger rate | MEDIUM |
| Lighting Controller | Active 06:00 to 23:00, scheduled cycles only | Commands outside defined schedule | MEDIUM |
| Env. Monitor | Temp 18 to 26 degrees, humidity 30 to 70% | Reading outside range or 15-minute silence | LOW |

---

## Sample Incident: IIR-2025-001

The docs folder contains a full Incident Intelligence Report for the following simulated scenario.

At 02:17:43 UTC on 15 May 2025, PBAD detected that IoT-CAM-01 (192.168.10.21) initiated an outbound HTTPS connection to an external IP (185.220.101.47) and transferred 47.3 MB of data in 26 seconds during scheduled inactivity. PBAD deviation score: 94 out of 100. Severity: CRITICAL. ACL rules contained the incident to Zone 1. No lateral movement to Zone 2 or Zone 3 was possible.

---

## Repository Structure

```
gridwatch-csoc/
├── README.md
├── packet-tracer/
│   └── GridWatch_CSOC_Topology_LeahMachaka.pkt
├── dashboard/
│   ├── index.html
│   ├── style.css
│   └── dashboard.js
└── docs/
    ├── GridWatch_PacketTracer_BuildGuide.docx
    └── GridWatch_Incident_Intelligence_Report.docx
```

---

## Technology Stack

| Layer | Technology |
|-------|------------|
| Network Simulation | Cisco Packet Tracer 9.0.0 |
| Routing | Static inter-VLAN routing, one interface per zone |
| Security | Extended ACLs (ZONE1_IN, ZONE2_IN) on Cisco 2911 |
| Segmentation | VLANs 10, 20, 30, 99 on Cisco 2960 switches |
| Dashboard | HTML, CSS, JavaScript |
| Backend (planned) | Python, Django |
| Innovation | PBAD (Passive Behavioural Anomaly Detection) |

---

## DESC Compliance Alignment

This project was designed with reference to the Dubai Electronic Security Centre published frameworks.

- **DESC IoT Security Standard** — mandatory controls for IoT device security in Dubai government entities
- **DESC Zero Trust Assessment Tool (GISEC 2025)** — PBAD extends this into the post-authentication behavioural layer
- **DESC ISR Version 3** — incident response structure follows ISR protocol
- **DESC CSOC Monitoring Standard** — continuous PBAD monitoring with real-time alerting
- **DESC ICS and OT Security Standard** — Zone 2 OT devices profiled separately with appropriate baselines

---

## Certifications

| Certificate | Provider | Status |
|-------------|----------|--------|
| Introduction to IoT | Cisco NetAcad | Completed — May 2025 |
| Networking Basics | Cisco NetAcad | In Progress |
| Introduction to Cybersecurity | Cisco NetAcad | In Progress |

---

## Contact

**Leah Machaka**
National Diploma: ICT, 3rd Year
Gauteng, South Africa
GitHub: [github.com/LeahMachaka](https://github.com/LeahMachaka)

---

*GridWatch CSOC — Securing What Zero Trust Cannot See*
*PBAD is an original innovation developed by Leah Machaka as part of this portfolio project.*
