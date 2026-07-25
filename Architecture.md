# NeoFactory / PWNDORA Project Architecture

## 1. Project Overview

**NeoFactory** is a simulated industrial enterprise platform with an embedded cyber-range learning layer.

The project models a smart manufacturing company where normal enterprise operations and cybersecurity training exist inside the same application. Instead of presenting isolated vulnerability challenges, the platform lets learners investigate realistic incidents across business modules such as assets, employees, search, maintenance, firmware, reports, and audit logs.

At a high level, the system combines:

- An enterprise operations platform
- A cyber-range scenario engine
- A vulnerable training surface
- A learner progress and evidence model
- A professional report-generation workflow

The core idea is:

> Learners should investigate security issues the way they appear in real enterprises: as business incidents, operational anomalies, leaked internal evidence, and chained trust failures.

## 2. High-Level Architecture

```text
NeoFactory Platform
|
|-- Frontend: React + Vite + TypeScript
|   |-- Enterprise UI
|   |-- Scenario catalog
|   |-- Lab status bar
|   |-- Mission briefing
|   |-- Evidence drawer
|   |-- Post-lab assessment UI
|
|-- Backend: FastAPI + SQLAlchemy
|   |-- Auth and users
|   |-- Employees and departments
|   |-- Assets/devices and firmware
|   |-- Maintenance tickets
|   |-- Inventory
|   |-- Search
|   |-- Reports
|   |-- Audit logs
|   |-- Scenario engine
|   |-- Stage gate and transition rules
|
|-- Database
|   |-- SQLite for local development
|   |-- PostgreSQL through Docker Compose
|
|
|-- Scenario Data
    |-- Lab 1: Operation Phantom Firmware
    |-- Lab 2: Silent Exfiltration
```

## 3. Runtime Components

### 3.1 Frontend

The frontend is located in:

```text
frontend/
```

It is built with:

- React
- TypeScript
- Vite
- Tailwind CSS
- React Query
- Axios
- React Router
- Lucide icons

The frontend provides the learner-facing and enterprise-facing experience.

Important frontend areas:

```text
frontend/src/pages/
frontend/src/components/
frontend/src/components/lab/
frontend/src/components/workspace/
frontend/src/services/
frontend/src/hooks/api/
frontend/src/contexts/
```

Key frontend responsibilities:

- Authentication flow
- Enterprise dashboard
- Asset inventory UI
- Employee directory UI
- Scenario catalog
- Scenario launch flow
- Active lab tracking
- Mission briefing display
- Evidence display
- Post-lab assessment dialog
- API communication with backend

### 3.2 Backend

The backend is located in:

```text
backend/
```

It is built with:

- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- JWT authentication
- SQLite/PostgreSQL support

The backend exposes the enterprise API and the vulnerable lab surfaces.

Important backend areas:

```text
backend/app/main.py
backend/app/api/
backend/app/api/v1/endpoints/
backend/app/models/
backend/app/schemas/
backend/app/services/
backend/app/scenarios/
backend/app/challenge_engine/
backend/app/attack_engine/
backend/app/progress_engine/
backend/app/events/
backend/app/seed/
```

Key backend responsibilities:

- User authentication
- Role checks
- CRUD services
- Enterprise module APIs
- Scenario loading
- Scenario state tracking
- Stage transition validation
- Vulnerable endpoints for labs
- Evidence/report generation support





## 4. Enterprise Domain Model

NeoFactory represents an industrial company with both IT and OT systems.

The enterprise includes:

- Employees
- Departments
- Industrial assets
- Firmware
- Maintenance tickets
- Inventory
- Network zones
- Search
- Reports
- Audit logs
- Notifications
- Scenario states

### 4.1 Employees

Employees represent internal company users and staff records.

They are relevant to the labs because industrial assets are assigned to engineers, and employee records may contain operational notes, designations, or internal references.

Security relevance:

- Employee records may expose sensitive internal details.
- Role-based access control should restrict who can view full employee profiles.
- Employee export is a high-impact data exposure surface.

### 4.2 Departments

Departments represent business structure.

Examples:

- IT
- OT Maintenance
- Finance
- Engineering
- Operations
- Security
- HR

Departments help make the environment feel like a real organization rather than a flat vulnerable app.

### 4.3 Assets / Devices

Assets represent industrial and networked devices inside NeoFactory.

Examples:

- PLCs
- HMIs
- OT gateways
- Industrial PCs
- Sensors
- Controllers
- Production-line devices

Device records may include:

- Name
- IP address
- MAC address
- Status
- Firmware relationship
- Assigned engineer
- Network zone
- Criticality
- Maintenance window
- Vendor/manufacturer
- Last patch date

Security relevance:

- Asset inventory is the starting point for industrial incident investigation.
- Outdated firmware can indicate vulnerable components.
- Assigned engineer references can lead to identity and workflow investigation.
- Device backup features can become file-access attack surfaces.

### 4.4 Firmware

Firmware represents low-level software running on industrial assets.

Security relevance:

- Outdated firmware can contain known vulnerabilities.
- Failed firmware updates can halt production.
- Unauthorized firmware pushes can affect physical operations.
- Firmware deployment logs can reveal privilege misuse.

### 4.5 Maintenance

Maintenance tickets represent operational incidents and repair workflows.

Security relevance:

- Tickets provide realistic business evidence.
- Tickets can contain clues such as affected line, device, engineer, timestamp, or symptom.
- Maintenance workflows connect operational issues to security investigation.

### 4.6 Search

Search is the global enterprise search feature.

It can conceptually index:

- Tickets
- Device records
- Employee references
- Backup metadata
- Deployment logs
- Audit fragments
- Internal notes

Security relevance:

- Search becomes dangerous when it indexes multiple systems but does not enforce result-level authorization.
- Injection in search can expose restricted internal records.
- Search is used as a discovery pivot in both labs.

### 4.7 Reports

Reports represent professional security deliverables.

The backend can generate draft vulnerability assessment content from completed scenario stages.

Report content may include:

- Executive summary
- Business context
- Findings
- Evidence
- OWASP mapping
- MITRE ATT&CK mapping
- CVSS scoring
- OWASP risk rating
- Remediation placeholders

## 5. Backend API Architecture

The main FastAPI application is created in:

```text
backend/app/main.py
```

The API router is assembled in:

```text
backend/app/api/v1/api.py
```

Major API areas include:

```text
/api/v1/auth
/api/v1/users
/api/v1/employees
/api/v1/departments
/api/v1/devices
/api/v1/firmwares
/api/v1/locations
/api/v1/tickets
/api/v1/inventory
/api/v1/notifications
/api/v1/reports
/api/v1/activity_logs
/api/v1/audit
/api/v1/timeline
/api/v1/progress
/api/v1/attack-graph
/api/v1/search
/api/v1/health
/api/v1/company
/api/v1/scenarios
/api/v1/dashboard
```

## 6. Scenario Engine Architecture

The scenario engine is responsible for loading labs, tracking progress, and advancing stages.

Important files:

```text
backend/app/scenarios/scenario_loader.py
backend/app/scenarios/scenario_registry.py
backend/app/scenarios/scenario_manager.py
backend/app/scenarios/scenario_executor.py
backend/app/scenarios/scenario_state_model.py
backend/app/scenarios/stage_gate.py
backend/app/challenge_engine/transition.py
```

### 6.1 Scenario Loading

Scenario definitions live in:

```text
backend/app/scenario_data/
```

Each scenario has a `scenario.yaml` file.

At startup, the backend loads scenario YAML files into an in-memory registry.

Current scenarios:

```text
backend/app/scenario_data/operation_phantom_firmware/scenario.yaml
backend/app/scenario_data/silent_exfiltration/scenario.yaml
```

### 6.2 Scenario Definition Structure

Each scenario contains:

- Scenario ID
- Scenario name
- Business context
- Difficulty
- Stages

Each stage contains:

- Stage ID
- Business module
- Target endpoint
- Flaw mode
- Vulnerability category
- Objective
- Discovery process
- Capability gained
- Evidence IDs
- OWASP category
- MITRE ATT&CK mapping
- CVSS metrics
- OWASP risk factors
- Enterprise layer
- Attack surface
- Technical mechanism
- Discovery surface
- Next stage

This makes scenarios report-ready and explainable.

### 6.3 Scenario State

Scenario progress is tracked with `ScenarioState`.

It stores:

- Scenario ID
- User ID
- Start time
- Completion time
- Current stage
- Status
- Completed stages
- Captured flags/evidence
- Vulnerability graph
- Metadata

### 6.4 Stage Gates

Stage advancement is handled through outcome-based checks.

Important file:

```text
backend/app/scenarios/stage_gate.py
```

Instead of simply asking whether the learner clicked a button, backend endpoints call the stage gate when meaningful actions happen.

Examples:

- Login endpoint observes brute-force pattern followed by success.
- Search endpoint observes restricted result leakage.
- Device backup endpoint observes successful traversal.
- Employee export endpoint observes stolen service key export.
- Firmware push endpoint observes privilege override success.

### 6.5 Transition Rules

Scenario-specific transition logic is defined in:

```text
backend/app/challenge_engine/transition.py
```

The transition rules check whether an observed action satisfies the current stage.

This is important because the lab should advance based on real outcomes, not vague UI clicks.

## 7. Lab 1 Architecture: Operation Phantom Firmware

### 7.1 Lab Theme

Operation Phantom Firmware is an OT incident investigation lab.

Business story:

> Production Line 2 halted after a firmware update. The learner investigates whether the failure was a normal operational issue or a security failure.

### 7.2 Lab Chain

```text
Production Line 2 halt
-> Identify affected PLC/controller
-> Follow assigned engineer clue
-> Inspect exposed employee/internal note
-> Search for deployment logs
-> Discover privilege override evidence
-> Test firmware push authorization flaw
```

### 7.3 Main Learning Goal

The learner learns to follow operational evidence until it becomes security evidence.

Meaning:

```text
Asset status -> firmware risk -> assigned engineer -> deployment logs -> privilege abuse
```

### 7.4 Vulnerability Themes

Lab 1 covers:

- Vulnerable/outdated components
- Broken access control around employee information
- Search injection leaking deployment logs
- Client-supplied role trust
- Privilege escalation in firmware operations

### 7.5 Enterprise Impact

The impact is production disruption.

The final security conclusion is:

> A firmware operation affecting physical production could be performed through weak privilege validation.

## 8. Lab 2 Architecture: Silent Exfiltration

### 8.1 Lab Theme

Silent Exfiltration is a data-breach investigation lab.

Business story:

> Finance detects unusual outbound activity, and employee personal data may have been exposed.

### 8.2 Lab Chain

```text
Weak login protection
-> Helpdesk account compromise
-> Search leaks backup metadata
-> Device backup path traversal
-> Internal service key theft
-> Employee export authorization bypass
-> Employee PII exfiltration
```

### 8.3 Main Learning Goal

The learner learns how small enterprise trust failures combine into a serious confidentiality breach.

### 8.4 Vulnerability Themes

Lab 2 covers:

- Predictable temporary credentials
- Missing brute-force protection
- Search injection
- Missing result-level authorization
- Path traversal
- Credentials stored in files
- Service-key authorization bypass
- Employee PII export

### 8.5 Enterprise Impact

The impact is employee data exposure.

The final security conclusion is:

> A non-admin attacker can chain weak authentication, internal discovery, file traversal, and stolen service credentials to export sensitive employee records.

## 9. Frontend Lab Experience

The frontend displays active lab state through:

```text
frontend/src/contexts/LabSessionContext.tsx
frontend/src/components/lab/LabStatusBar.tsx
frontend/src/components/common/dialog/MissionBriefingDialog.tsx
frontend/src/components/lab/EvidenceDrawer.tsx
frontend/src/components/lab/PostLabAssessmentDialog.tsx
```

### 9.1 Lab Session Context

The frontend polls the backend for the active scenario state.

It tracks:

- Active scenario
- Current stage
- Completed stages
- Completion status

### 9.2 Lab Status Bar

The Lab Status Bar provides:

- Scenario name
- Current stage
- Stage progress timeline
- Timer
- Mission briefing button
- Evidence drawer button
- Completion state
- Assessment flow

### 9.3 Mission Briefing

Mission briefing explains:

- Stage objective
- Technical mechanism
- OWASP category
- MITRE ATT&CK mapping
- Discovery/execution strategy

### 9.4 Evidence Drawer

The Evidence Drawer is intended to show collected evidence and help learners connect stage outcomes to report findings.

### 9.5 Post-Lab Assessment

After completion, the learner can move into assessment/reporting flow.

This reinforces the goal that learners should not only exploit issues, but also explain them professionally.

## 10. Event, Progress, And Report Architecture

### 10.1 Event Bus

The event system allows scenario progress to trigger other systems.

Important files:

```text
backend/app/events/event_bus.py
backend/app/events/event_registry.py
backend/app/events/events.py
backend/app/events/handlers.py
```

Events include:

- StageAdvanced
- ScenarioCompleted

### 10.2 Capability Tracking

Capability tracking records what the learner gained from a stage.

Important file:

```text
backend/app/progress_engine/capability_tracker.py
```

Example capability:

```text
Can exploit unsanitized query inputs to retrieve unintended data.
```

### 10.3 Vulnerability Graph

The vulnerability graph is intended to record the learner's attack path across stages.

It can include:

- Stage ID
- Objective
- OWASP category
- MITRE technique
- CVSS score
- Timestamp

### 10.4 Report Generation

Report generation is handled in:

```text
backend/app/report_generator.py
```

It builds a draft vulnerability assessment based on completed stages.

Generated report sections include:

- Executive summary
- Business context
- Finding matrix
- Enterprise layer
- Attack surface
- Discovery surface
- Technical mechanism
- Capability gained
- OWASP classification
- MITRE ATT&CK mapping
- CVSS score
- OWASP risk rating
- Evidence collected
- Analyst assessment placeholder
- Remediation placeholder

## 11. Database And Persistence

The backend uses SQLAlchemy models.

Important model areas:

```text
backend/app/models/
backend/app/scenarios/scenario_state_model.py
backend/app/audit/audit_models.py
```

Database options:

- SQLite by default for local development
- PostgreSQL through Docker Compose

Docker Compose defines:

```text
postgres
backend
```

The backend can connect to PostgreSQL through environment variables:

```text
POSTGRES_SERVER
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB
```

If PostgreSQL is not configured, the backend defaults to SQLite:

```text
sqlite:///./neofactory.db
```

## 12. Security Model

### 12.1 Authentication

Authentication uses JWT tokens.

Login endpoint:

```text
POST /api/v1/auth/login
```

Current lab behavior intentionally includes vulnerable authentication behavior for training scenarios.

### 12.2 Roles

User roles include:

```text
Employee
Engineer
Manager
Administrator
```

Role checks are enforced in some endpoints through backend dependencies.

### 12.3 Intentional Vulnerabilities

Some vulnerable behavior exists intentionally for cyber-range learning.

Examples:

- Missing login rate limiting
- Search injection behavior
- Path traversal in backup download
- Service-key bypass on employee export
- Client-supplied role trust on firmware push

These should be clearly treated as lab surfaces, not production-safe behavior.

## 13. Key Data Flows

### 13.1 Scenario Startup Flow

```text
Backend starts
-> main.py startup event runs
-> scenario_data directory is scanned
-> scenario.yaml files are loaded
-> scenarios are registered in memory
-> frontend can list scenarios
```

### 13.2 Scenario Launch Flow

```text
Learner opens scenario catalog
-> selects scenario
-> frontend calls /api/v1/scenarios/{id}/start
-> backend creates ScenarioState
-> LabSessionContext polls active state
-> LabStatusBar appears
```

### 13.3 Stage Advancement Flow

```text
Learner performs action in enterprise UI/API
-> backend endpoint executes normal or vulnerable behavior
-> endpoint calls advance_if_stage_matches
-> transition rules validate outcome
-> ScenarioState updates current_stage and completed_stages
-> StageAdvanced event is published
-> frontend polling updates lab status
```

### 13.4 Scenario Completion Flow

```text
Final stage succeeds
-> ScenarioState status becomes COMPLETED
-> ScenarioCompleted event is published
-> frontend displays completion
-> learner enters assessment/report flow
-> report generation can create draft assessment content
```

## 14. Current Strengths

- Enterprise-first cyber-range design
- Realistic business incident framing
- Multi-stage vulnerability chains
- YAML-driven scenario structure
- Outcome-based progression
- OWASP/MITRE/CVSS metadata per stage
- Frontend lab status and mission briefing system
- Report-generation direction
- Strong separation between enterprise modules and lab scenario metadata

## 15. Current Gaps And Improvement Areas

### 15.1 Documentation

The project needs stronger onboarding documentation.

Recommended docs:

- README overview
- Setup guide
- Lab authoring guide
- Scenario YAML schema guide
- Vulnerable endpoint guide
- Presentation/reporting guide

### 15.2 Scenario State Scoping

Some scenario state lookup logic should be user-scoped to avoid cross-user lab progress issues.

### 15.3 Lab 1 Stage 2 Accuracy

The employee-profile stage currently reads more like excessive employee directory exposure than clean IDOR unless a direct employee object reference is exposed and abused.

Recommended label:

```text
Broken Access Control - Excessive Employee Profile Exposure
```

Or, if the implementation is strengthened:

```text
Missing Object-Level Authorization / IDOR
```

### 15.4 Lab 2 Stage 1 Realism

Stage 1 should avoid directly giving both email and password.

Improved story:

```text
Recent SSO upgrade reset helpdesk accounts.
Temporary passwords follow a predictable pattern.
Login lacks brute-force protection.
```

### 15.5 Search Behavior Realism

Normal search terms should return normal scoped results.

Injection-style input should be required to expose restricted records.

This avoids the feeling that simple keywords magically reveal sensitive logs.

### 15.6 Seed Data

The lab-specific assets, employees, tickets, and logs should be explicitly seeded so the UI feels real.

Examples:

- PLC-Line2-Control
- HMI-7734
- Ticket #402
- Helpdesk account
- Assigned engineer
- Backup metadata
- Service credentials

## 16. Future Architecture Extensions

Recommended future extensions:

- SIEM-style alert module
- Incident timeline view
- Role-based evidence visibility
- Richer seeded enterprise data
- More OT/ICS labs
- Remediation validation stages
- Adaptive AI mentor
- Report grading
- Multi-user/team investigation mode
- Attack graph visualization
- Learner capability dashboard
- Scenario authoring UI
- Safer separation between lab-vulnerable routes and production-safe routes

## 17. Architecture Summary

NeoFactory is best understood as:

```text
A simulated industrial enterprise platform
with embedded cyber-range scenarios
where learners investigate business incidents,
follow operational evidence,
exploit realistic vulnerability chains,
and produce professional security assessments.
```

The project differs from traditional vulnerability labs because it does not stop at isolated bugs.

It connects:

```text
Enterprise context
-> operational evidence
-> technical vulnerability
-> attacker progression
-> business impact
-> professional reporting
```

That is the core architecture and educational value of the project.
