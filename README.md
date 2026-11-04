# GridWatch

## Overview

GridWatch is a SIEM I am building as a hands-on portfolio project. It collects logs from Linux servers, web servers and Windows hosts, along with events from physical infrastructure sensors, normalises them into one schema, and applies detection and correlation rules to raise alerts for investigation. Rules are mapped to MITRE ATT&CK. Treating physical sensor events as a first-class log source is the main design focus.

## Scope

The project scope and exclusions are documented in [docs/scope.md](docs/scope.md). Ideas outside that scope are tracked in [docs/backlog.md](docs/backlog.md).

## Planned architecture

Log and sensor sources will send events to collection components, where events will be normalised before detection and correlation rules evaluate them. Matching events will produce alerts for investigation through cases, timelines, notes, and incident reports. A diagram will be added later.

## Tech stack

- Python 3.12 and Django 5.2
- PostgreSQL 16
- Redis 7 and Celery
- Docker Compose
- pytest and Ruff

## Quick start

1. Clone this repository and change into its directory:

   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Copy the example environment file:

   ```sh
   cp .env.example .env
   ```

3. Build and start the services:

   ```sh
   docker compose up --build
   ```

4. Open [http://localhost:8000/health/](http://localhost:8000/health/) to check service health.

## Project status

Phase 0 complete, ongoing build.

## Limitations

This is an early-stage portfolio project, not a production-ready SIEM. Collection, normalisation, detection, and investigation capabilities are planned and are not all implemented yet. Supported devices and log formats will be limited. The health endpoint currently checks database and Redis connectivity only.
