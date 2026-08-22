# GridPortfolio

> **An open-source operating system for integrating energy data, teams, decisions, and execution.**

GridPortfolio connects **Data & Analytics, Asset Management, Energy Origination, Wholesale, Procurement, Sustainability, Finance, and Leadership** through a shared portfolio model, continuous portfolio-health monitoring, AI-assisted decision support, and cross-functional execution tracking.

---

# 1. Why This Project Exists

Modern energy organizations increasingly have strong specialist teams and sophisticated tools.

The problem is often not a lack of data, analytics, market expertise, asset expertise, or procurement expertise.

The problem is the **connective tissue between them**.

Different teams may have:

* different source systems
* different definitions
* different metrics
* different reporting cadences
* different assumptions
* different priorities
* different owners
* different views of risk
* different workflows for turning information into action

This can create a gap between:

```text
DATA
  ↓
ANALYSIS
  ↓
TEAM INSIGHT
  ↓
CROSS-FUNCTIONAL ALIGNMENT
  ↓
DECISION
  ↓
PROCUREMENT
  ↓
EXECUTION
  ↓
OUTCOME
```

GridPortfolio exists to make that chain visible, connected, and measurable.

---

# 2. Guiding Thesis

The central design thesis of GridPortfolio is:

> **“The problem isn't that Asset Management, Origination, Wholesale, or Analytics lack sophisticated tools. The problem is what happens between those tools. GridPortfolio is built around that connective tissue — a shared semantic model, common portfolio metrics, cross-team dependencies, continuous health monitoring, AI-assisted investigation, decision traceability, and an operating cadence that takes signals all the way through procurement and execution.”**

Every major product and architecture decision should support this thesis.

Do not build features merely because they demonstrate AI.

Build features that demonstrate the ability to make a complex energy organization **more connected, more visible, and faster at turning information into decisions.**

---

# 3. Primary Problem

GridPortfolio simulates the operating environment of a large technology company with a rapidly expanding electricity footprint.

The fictional organization has:

```text
Data & Analytics
Asset Management
Energy Origination
Wholesale / Trading
Procurement
Sustainability
Finance
Leadership
```

Each function has specialized responsibilities.

### Data & Analytics

Owns:

* data
* forecasting
* analytics
* models
* reporting
* data quality

### Asset Management

Owns:

* physical assets
* data-center load
* generation
* storage
* availability
* operational performance

### Energy Origination

Owns:

* PPAs
* VPPAs
* renewable projects
* contract pipeline
* sourcing opportunities

### Wholesale

Owns:

* market exposure
* LMP
* congestion
* hedging
* wholesale purchases

### Procurement

Owns:

* procurement decisions
* commercial actions
* sourcing strategy
* contracting

### Sustainability

Owns:

* renewable coverage
* carbon intensity
* hourly matching
* sustainability targets

### Finance

Owns:

* financial exposure
* budgeting
* valuation
* financial risk

### Leadership

Needs to understand:

* what changed
* why it matters
* what risks are emerging
* what opportunities exist
* what decisions are required
* who owns the next action

The core problem is that **these teams must make decisions together even though their systems and workflows are separate.**

---

# 4. Product Goal

GridPortfolio should answer five questions continuously:

### 1. What is happening?

Portfolio state.

### 2. Why is it happening?

Drivers and evidence.

### 3. Who is affected?

Teams, assets, contracts, markets, and initiatives.

### 4. What should happen next?

Recommended action and decision.

### 5. Is the organization executing?

Ownership, dependencies, status, and outcomes.

The application should connect:

```text
OBSERVATION
    ↓
ANALYSIS
    ↓
CROSS-TEAM IMPACT
    ↓
RISK
    ↓
RECOMMENDATION
    ↓
DECISION
    ↓
OWNER
    ↓
EXECUTION
    ↓
OUTCOME
```

---

# 5. Core Product Concept

GridPortfolio is **not** primarily an AI chatbot.

It is an **Energy Integration Operating System**.

Its architecture should look like:

```text
                         ENERGY ORGANIZATION
                                │
       ┌────────────────────────┼────────────────────────┐
       │                        │                        │
       ▼                        ▼                        ▼
 DATA & ANALYTICS          ASSET MANAGEMENT         ORIGINATION
       │                        │                        │
       │                        │                        │
       └───────────────┬────────┴────────┬───────────────┘
                       │                 │
                       ▼                 ▼
                  WHOLESALE          SUSTAINABILITY
                       │                 │
                       └────────┬────────┘
                                │
                                ▼
                      SHARED PORTFOLIO TRUTH
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼
         PORTFOLIO          INITIATIVES       DECISIONS
          METRICS           & DEPENDENCIES    & ACTIONS
              │                 │                 │
              └─────────────────┼─────────────────┘
                                │
                                ▼
                        AI INTEGRATION LAYER
                                │
             ┌──────────────────┼──────────────────┐
             ▼                  ▼                  ▼
       MONITORING AGENT   INTEGRATION AGENT   DECISION AGENT
             │                  │                  │
             └──────────────────┼──────────────────┘
                                │
                                ▼
                       DECISION INTELLIGENCE
                                │
             ┌──────────────────┼──────────────────┐
             ▼                  ▼                  ▼
        DAILY PULSE        WEEKLY REVIEW      EXECUTIVE BRIEF
             │                  │                  │
             └──────────────────┼──────────────────┘
                                ▼
                       PROCUREMENT DECISION
                                │
                                ▼
                        EXECUTION TRACKER
                                │
                                ▼
                            OUTCOMES
                                │
                                └──────────► PORTFOLIO TRUTH
```

---

# 6. The Shared Portfolio Truth

The most important architectural concept is the **Shared Portfolio Truth**.

Different teams may have different systems.

GridPortfolio should create a shared semantic layer that reconciles those systems into common definitions.

For example:

```text
Data & Analytics
"Load = 1,284 MW"

Asset Management
"Physical demand = 1,301 MW"

Wholesale
"Market exposure = 1,298 MW"

GridPortfolio
"Portfolio Load"
Definition:
Canonical hourly electricity consumption
used for portfolio planning and exposure calculations.
```

The goal is not to pretend that all teams have identical data.

The goal is to make differences:

* explicit
* traceable
* reconcilable
* governed

---

# 7. Canonical Data Model

Build a canonical model connecting:

```text
Portfolio
│
├── Organizations
│   ├── Data & Analytics
│   ├── Asset Management
│   ├── Origination
│   ├── Wholesale
│   ├── Procurement
│   ├── Sustainability
│   ├── Finance
│   └── Leadership
│
├── Assets
│   ├── Data Centers
│   ├── Generation
│   └── Storage
│
├── Contracts
│   ├── PPAs
│   ├── VPPAs
│   └── Utility Contracts
│
├── Markets
│   ├── LMP
│   ├── Load
│   ├── Generation
│   └── Congestion
│
├── Forecasts
│   ├── Load
│   ├── Generation
│   └── Price
│
├── Risks
│   ├── Price
│   ├── Volume
│   ├── Basis
│   ├── Reliability
│   └── Contract
│
├── Initiatives
│   ├── Procurement
│   ├── Infrastructure
│   └── Strategic Programs
│
├── Decisions
│
└── Actions
```

Relationships are critical.

Examples:

```text
Asset
  ↓
has Load Forecast
  ↓
creates Market Exposure
  ↓
affects Procurement Requirement
  ↓
creates Initiative
  ↓
requires Origination + Wholesale + Finance
  ↓
requires Decision
  ↓
creates Action
  ↓
produces Outcome
```

---

# 8. Metric Governance

Create a **Metric Contract** system.

Every major metric should have:

```text
Metric Name
Definition
Owner
Contributing Teams
Source Systems
Calculation
Refresh Frequency
Consumers
Decision Uses
Data Quality Requirements
```

Example:

## Renewable Coverage

```text
Owner:
Sustainability

Contributing Teams:
Origination
Asset Management
Data & Analytics

Definition:
Eligible renewable MWh /
Total portfolio MWh

Sources:
PPA records
Generation telemetry
Portfolio load

Refresh:
Hourly

Consumers:
Leadership
Procurement
Sustainability

Decision Uses:
Procurement planning
Portfolio reporting
Sustainability strategy
```

This demonstrates that data integration means more than joining tables.

It means aligning:

**definitions + ownership + governance + decisions.**

---

# 9. Organizational Integration Map

The application must include a visual representation of how teams connect.

Example:

```text
                    DATA & ANALYTICS
                    Forecasts
                    Market Data
                    Data Quality
                           │
                           ▼
┌──────────────┐    ┌──────────────────┐    ┌───────────────┐
│ ASSET MGMT   │───►│                  │◄───│ ORIGINATION   │
│              │    │ SHARED PORTFOLIO │    │               │
│ Load         │    │      TRUTH       │    │ PPAs          │
│ Performance  │    │                  │    │ Contracts     │
│ Availability │    └────────┬─────────┘    │ Pipeline      │
└──────────────┘             │              └───────────────┘
                             │
                             ▼
                      ┌─────────────┐
                      │  WHOLESALE  │
                      │             │
                      │ Exposure    │
                      │ Hedging     │
                      │ Congestion  │
                      └──────┬──────┘
                             │
                             ▼
                      ┌─────────────┐
                      │ PROCUREMENT │
                      │             │
                      │ Decisions   │
                      │ Priorities  │
                      │ Actions     │
                      └──────┬──────┘
                             │
                             ▼
                         LEADERSHIP
```

This should be a first-class product view, not merely documentation.

---

# 10. Cross-Team Impact Analysis

One of the most important features is the ability to answer:

> **“If something changes, who needs to know?”**

Example:

```text
EVENT

TX-DC-02 load forecast increases 22%.

                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
   Asset Mgmt         Wholesale       Origination
   Validate load     Recalculate     Reassess
   assumptions       exposure         contracted
                                      coverage
        │                │                │
        └────────────────┼────────────────┘
                         │
                         ▼
                   Sustainability
                   Recalculate
                   renewable
                   coverage
                         │
                         ▼
                     Finance
                   Update financial
                     exposure
                         │
                         ▼
                   Procurement
                  Evaluate need
                  for additional
                    capacity
```

The system should identify affected teams automatically based on data relationships and business rules.

---

# 11. Initiative Management

GridPortfolio must include an **Initiative / Program Operating Layer**.

Track cross-functional initiatives such as:

* renewable procurement
* new data-center load onboarding
* storage deployment
* transmission projects
* contract renewals
* market strategy changes

Each initiative should contain:

```text
Initiative
Owner
Executive Sponsor
Participating Teams
Objective
Status
Priority
Decision Required
Dependencies
Risks
Milestones
Next Action
Due Date
```

Example:

```text
TEXAS RENEWABLE EXPANSION

Owner:
Energy Origination

Partners:
Asset Management
Wholesale
Sustainability
Finance

Status:
AT RISK

Objective:
Secure 500 MW renewable capacity.

Dependencies:

✓ Load forecast
✓ Market analysis
⚠ Transmission study
⚠ Contract structure
○ Finance approval

Next Decision:
Select procurement structure

Decision Owner:
Procurement

AI Summary:
Transmission uncertainty is currently
the primary schedule risk.
```

---

# 12. Dependency Graph

Build a dependency graph for initiatives.

Example:

```text
Load Forecast
      │
      ▼
Capacity Requirement
      │
 ┌────┴─────┐
 ▼          ▼
Market    Sustainability
Analysis    Target
 │          │
 └────┬─────┘
      ▼
Procurement Need
      │
      ▼
Origination
      │
      ▼
Contract Options
      │
 ┌────┴─────┐
 ▼          ▼
Wholesale  Finance
 │          │
 └────┬─────┘
      ▼
Procurement
      │
      ▼
Execution
```

Users should be able to ask:

> “What downstream decisions are affected if the load forecast changes?”

---

# 13. Portfolio Health

Create a transparent portfolio health system.

At minimum:

* Reliability
* Market Exposure
* Contract Coverage
* Renewable Coverage
* Price Risk
* Forecast Stability
* Execution Health

Example:

```text
PORTFOLIO HEALTH

82 / 100

Reliability          91
Market Exposure      73
Contract Coverage    87
Renewable Coverage   94
Price Risk           68
Forecast Stability   84
Execution Health     79
```

Every metric must include:

* definition
* source
* timestamp
* confidence
* contributing factors

---

# 14. Continuous Monitoring

Move the organization from periodic reporting to continuous monitoring.

The system should continuously detect:

* load anomalies
* price anomalies
* contract deviations
* renewable shortfalls
* forecast errors
* outages
* data-quality failures
* changes in portfolio exposure
* initiative delays

---

# 15. Anomaly Detection

Implement:

### Statistical

* z-score
* rolling statistics

### Seasonal

Account for:

* hour
* day
* month
* season

### Machine Learning

Use:

* Isolation Forest

### Forecast Residual

Compare:

```text
Actual - Forecast
```

### Change Point

Identify persistent shifts.

Every anomaly must have:

```text
ID
Category
Severity
Asset
Metric
Observed Value
Expected Value
Deviation
Timestamp
Confidence
Evidence
Recommended Action
Affected Teams
```

---

# 16. Risk Engine

Calculate:

### Price Risk

Exposure to market price movements.

### Volume Risk

Difference between expected and actual load/generation.

### Basis Risk

Location/settlement mismatch.

### Reliability Risk

Outages and insufficient capacity.

### Contract Risk

Deviation from contractual expectations.

Every risk should include:

```text
Risk
Exposure
Trend
Confidence
Drivers
Affected Teams
Recommended Investigation
```

---

# 17. Forecasting

Build baseline forecasting for:

* load
* renewable generation
* price

Horizons:

* 24 hours
* 7 days

Use simple, interpretable models where possible.

Potential technologies:

* seasonal baselines
* gradient boosting
* XGBoost

Measure:

* MAE
* RMSE
* MAPE where appropriate

The objective is decision usefulness, not model complexity.

---

# 18. AI Integration Layer

The AI layer should **connect specialist outputs**.

Do not use AI to replace the specialists.

Use AI to make them:

* faster
* more connected
* more visible
* easier for leadership to understand

---

# 19. AI Agents

Build specialized agents.

```text
                     ORCHESTRATOR
                          │
       ┌──────────────────┼──────────────────┐
       │                  │                  │
       ▼                  ▼                  ▼
 Market Agent        Asset Agent       Contract Agent
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
                          ▼
                     Risk Agent
                          │
                          ▼
                  Integration Agent
                          │
                          ▼
                   Decision Agent
                          │
                          ▼
                 Briefing Agent
```

---

# 20. Integration Agent

This is a core differentiator.

The Integration Agent should answer:

> **“Which teams, metrics, initiatives, and decisions are affected by this event?”**

Example:

```text
EVENT

TX load forecast increased 22%.

INTEGRATION AGENT

Affected teams:

Asset Management
→ Validate physical load assumptions

Wholesale
→ Recalculate market exposure

Origination
→ Reassess contracted coverage

Sustainability
→ Recalculate renewable coverage

Finance
→ Update financial exposure

Procurement
→ Evaluate incremental capacity requirement

Leadership
→ Review portfolio implications
```

The agent should use the canonical data model and dependency graph rather than guessing team relationships.

---

# 21. Market Agent

Analyze:

* LMP
* congestion
* wholesale exposure
* volatility
* hedging

Answer:

> What is happening in the market and how does it affect the portfolio?

---

# 22. Asset Agent

Analyze:

* physical load
* generation
* storage
* availability
* outages
* forecast deviation

Answer:

> Are our physical assets performing as expected?

---

# 23. Contract Agent

Analyze:

* PPAs
* VPPAs
* utility contracts
* contracted MW
* expected generation
* actual generation

Answer:

> Are our contractual positions performing as expected?

---

# 24. Risk Agent

Combine specialist outputs.

Determine:

* materiality
* exposure
* risk ranking
* confidence
* drivers

Do not allow the LLM to independently calculate deterministic financial or energy metrics.

---

# 25. Decision Agent

Translate analysis into recommended actions.

The agent should recommend actions for human review.

It should not autonomously execute procurement decisions.

---

# 26. Executive Brief Agent

Generate a cross-functional brief.

Example:

```text
DECISION REQUIRED

Texas Renewable Procurement

WHAT CHANGED

Load forecast increased 22%.

ASSET MANAGEMENT

Expected demand requires an additional 150 MW.

WHOLESALE

Current wholesale exposure increases by ~$8.4M/year.

ORIGINATION

Current PPA pipeline covers approximately 80 MW.

SUSTAINABILITY

Additional procurement is required to maintain
95% renewable coverage.

FINANCE

Estimated annual exposure:
$8.4M–$11.2M.

RECOMMENDED ACTION

Initiate procurement process for approximately
70 MW additional capacity.

DECISION OWNER

Procurement

REQUIRED PARTNERS

Asset Management
Origination
Wholesale
Finance
Sustainability

DEPENDENCIES

Transmission availability
Contract pricing
Load forecast validation

CONFIDENCE

84%
```

The purpose is to make the **cross-functional implications** explicit.

---

# 27. Decision Traceability

Every major decision must be traceable.

Backward:

```text
PROCUREMENT DECISION
        ↑
DECISION BRIEF
        ↑
RISK ANALYSIS
        ↑
PORTFOLIO EXPOSURE
        ↑
MARKET / ASSET ANALYSIS
        ↑
FORECAST
        ↑
SOURCE DATA
```

Forward:

```text
DECISION
   │
   ├── Owner
   ├── Teams Impacted
   ├── Expected Outcome
   ├── Financial Exposure
   ├── Dependencies
   ├── Actions
   └── Execution Status
```

This creates a complete:

> **Signal → Analysis → Decision → Action → Outcome**

chain.

---

# 28. Operating Cadence

GridPortfolio should demonstrate how leadership could actually run the portfolio.

## Daily Portfolio Pulse

Answers:

* What changed overnight?
* What risks emerged?
* What requires investigation?
* Which teams are affected?

## Weekly Energy Portfolio Review

Includes:

* portfolio health
* major exposures
* emerging risks
* procurement pipeline
* initiative status
* cross-team blockers
* decisions required

## Monthly Portfolio Strategy Review

Includes:

* portfolio trajectory
* procurement requirements
* contract performance
* market outlook
* strategic risks
* resource requirements
* long-term scenarios

The system should generate these views automatically.

---

# 29. Execution Tracker

Every decision should produce actionable work.

Example:

```text
DECISION
Acquire 300 MW renewable capacity

        ↓

ACTION 1
Origination
Identify candidate projects

ACTION 2
Wholesale
Model market exposure

ACTION 3
Sustainability
Validate renewable contribution

ACTION 4
Finance
Assess financial exposure

ACTION 5
Procurement
Prepare commercial strategy
```

Track:

* owner
* status
* due date
* dependency
* blocker
* outcome

This is critical.

GridPortfolio must not stop at **“here's an insight.”**

It must connect the insight to **execution**.

---

# 30. Audience Views

Users should be able to view the same portfolio through different organizational lenses.

## Executive

Focus:

* portfolio health
* material risks
* financial exposure
* major decisions
* cross-team blockers

## Asset Management

Focus:

* asset performance
* load
* availability
* outages
* forecast accuracy

## Origination

Focus:

* procurement requirements
* PPA pipeline
* contract coverage
* sourcing opportunities

## Wholesale

Focus:

* market exposure
* LMP
* congestion
* hedging
* volatility

## Sustainability

Focus:

* renewable coverage
* carbon intensity
* hourly matching

## Finance

Focus:

* financial exposure
* cost
* risk
* scenarios

The underlying portfolio truth remains shared.

Only the **decision lens** changes.

---

# 31. Synthetic Portfolio

Do not use proprietary employer data.

Generate a realistic fictional portfolio.

Example:

| Asset    | Type        | Region | Capacity |
| -------- | ----------- | ------ | -------: |
| TX-DC-01 | Data Center | ERCOT  |   500 MW |
| TX-DC-02 | Data Center | ERCOT  |   750 MW |
| AZ-DC-01 | Data Center | WECC   |   400 MW |
| IA-DC-01 | Data Center | MISO   |   300 MW |
| VA-DC-01 | Data Center | PJM    |   600 MW |

Include:

* data centers
* solar
* wind
* batteries
* PPAs
* VPPAs
* utility contracts
* wholesale purchases

Synthetic data should include:

* seasonality
* volatility
* forecast error
* outages
* contract deviations
* congestion
* market shocks
* load growth
* data-quality failures

Use a fixed random seed.

---

# 32. Data Layer

Preferred:

* Python
* DuckDB
* Parquet
* Polars/Pandas

Directory:

```text
data/
├── raw/
├── processed/
├── synthetic/
└── schemas/
```

Running:

```bash
python scripts/generate_data.py
```

must recreate the demo dataset.

---

# 33. Public Data

Optionally support:

* EIA
* Open Power System Data
* publicly available ISO/RTO datasets

Public APIs must not be required for the core demo.

The project should run locally.

---

# 34. Data Quality

Data quality is part of the product.

Detect:

* stale feeds
* missing observations
* schema changes
* duplicate records
* invalid values
* inconsistent definitions

Example:

```text
DATA QUALITY WARNING

ERCOT LMP feed has not updated for 42 minutes.

Affected:

Market Exposure
Price Risk
Executive Brief

Recommendation:

Validate data source before making decisions.
```

Never allow the AI layer to hide uncertainty caused by bad data.

---

# 35. Explainability

Every recommendation should provide:

```text
Why did the system flag this?

Risk Score: 87

Contributing factors:

+32% increase in load
+18% increase in LMP
+11% forecast error
+9% congestion exposure

Historical percentile:
97th

Confidence:
91%

Data freshness:
8 minutes
```

Clearly separate:

```text
Observed Fact
      ↓
Model Output
      ↓
AI Interpretation
      ↓
Recommendation
```

---

# 36. Human-in-the-Loop

GridPortfolio is a decision-support system.

It does not autonomously make procurement decisions.

The human remains responsible for:

* commercial decisions
* procurement
* contracting
* market actions
* strategic decisions

AI should surface:

* evidence
* implications
* risks
* dependencies
* recommendations

Humans make the final decision.

---

# 37. Technology Stack

## Backend

Python + FastAPI

## Data

DuckDB + Parquet + Polars/Pandas

## ML

scikit-learn + XGBoost

Optional PyTorch where justified.

## AI

Provider-agnostic LLM abstraction.

Support configurable:

```text
LLM_PROVIDER
LLM_MODEL
LLM_API_KEY
```

The application must work without an LLM.

## Frontend

Preferred:

* React
* Next.js
* TypeScript

Streamlit is acceptable for the initial MVP if it significantly accelerates development.

## Deployment

* Docker
* docker-compose
* GitHub Actions

---

# 38. Repository Structure

```text
gridportfolio/
│
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── .env.example
│
├── docs/
│   ├── architecture.md
│   ├── data-model.md
│   ├── metric-contracts.md
│   ├── organizational-model.md
│   ├── operating-cadence.md
│   ├── agent-design.md
│   ├── responsible-ai.md
│   └── evaluation.md
│
├── data/
│   ├── synthetic/
│   ├── schemas/
│   └── samples/
│
├── scripts/
│   └── generate_data.py
│
├── src/
│   ├── ingestion/
│   ├── data_model/
│   ├── metrics/
│   ├── analytics/
│   │   ├── forecasting/
│   │   ├── anomaly_detection/
│   │   ├── portfolio_health/
│   │   └── risk/
│   │
│   ├── organization/
│   │   ├── teams/
│   │   ├── dependencies/
│   │   ├── initiatives/
│   │   └── decisions/
│   │
│   ├── agents/
│   │   ├── orchestrator/
│   │   ├── market/
│   │   ├── asset/
│   │   ├── contract/
│   │   ├── risk/
│   │   ├── integration/
│   │   ├── decision/
│   │   └── briefing/
│   │
│   ├── api/
│   └── config/
│
├── frontend/
│
├── evaluation/
│   ├── agent_eval/
│   ├── model_eval/
│   ├── data_quality/
│   └── scenarios/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── agents/
│
└── examples/
    ├── daily_pulse/
    ├── weekly_review/
    ├── decision_briefs/
    └── scenarios/
```

---

# 39. API

Expose endpoints such as:

```text
GET /portfolio/health
GET /portfolio/risks
GET /portfolio/anomalies

GET /assets
GET /assets/{asset_id}

GET /contracts
GET /contracts/{contract_id}

GET /markets/exposure

GET /initiatives
GET /initiatives/{initiative_id}

GET /decisions
GET /decisions/{decision_id}

GET /dependencies/{entity_id}

GET /briefs/latest

POST /agents/investigate
POST /agents/impact-analysis
POST /agents/generate-brief
```

Use FastAPI/OpenAPI.

---

# 40. Example Scenarios

The application must include scenarios that demonstrate **cross-organizational integration**.

## Scenario 1 — Load Surge

TX-DC-02 load increases unexpectedly.

System behavior:

```text
Load anomaly
      ↓
Forecast deviation
      ↓
Asset impact
      ↓
Wholesale exposure
      ↓
Renewable coverage impact
      ↓
Financial exposure
      ↓
Affected teams
      ↓
Procurement implications
      ↓
Decision brief
      ↓
Actions
```

---

## Scenario 2 — Renewable Shortfall

Wind PPA underperforms.

System identifies:

```text
PPA deviation
      ↓
Origination
      ↓
Renewable coverage
      ↓
Wholesale replacement exposure
      ↓
Sustainability impact
      ↓
Finance impact
      ↓
Procurement requirement
```

---

## Scenario 3 — Market Price Spike

System identifies:

```text
Price spike
      ↓
Wholesale exposure
      ↓
Affected assets
      ↓
Financial risk
      ↓
Procurement/hedging implications
      ↓
Leadership alert
```

---

## Scenario 4 — Data Failure

Market data stops updating.

System should identify:

```text
Data Quality Failure
      ↓
Affected Metrics
      ↓
Affected Teams
      ↓
Affected Decisions
      ↓
Warning / Escalation
```

The system must **not** fabricate current market conditions.

---

## Scenario 5 — Procurement Initiative at Risk

Transmission study is delayed.

System identifies:

```text
Dependency Delay
      ↓
Origination schedule impact
      ↓
Procurement timeline impact
      ↓
Renewable target impact
      ↓
Leadership escalation
```

This scenario demonstrates program management and operating-model thinking.

---

# 41. Evaluation

Evaluate the system at four levels.

## Data

* completeness
* freshness
* validity
* consistency

## Models

* MAE
* RMSE
* anomaly precision
* anomaly recall
* false positives

## Agents

* tool selection
* factual accuracy
* evidence grounding
* hallucination rate
* recommendation quality

## Integration

Create evaluation scenarios that test whether the system correctly identifies:

* affected teams
* downstream metrics
* dependent initiatives
* required decisions
* decision owners
* recommended actions

This last category is critical.

The project should explicitly evaluate:

> **Can the system correctly connect an event in one part of the organization to the people, metrics, decisions, and actions affected elsewhere?**

---

# 42. Responsible AI

Document:

* human-in-the-loop controls
* hallucination risks
* model limitations
* data-quality risks
* confidence
* provenance
* evidence
* AI/model/fact separation
* decision boundaries

The AI should never imply certainty where the underlying data or models are uncertain.

---

# 43. Observability

Log:

* agent
* tool
* timestamp
* input
* output
* evidence
* confidence
* decision

Example:

```text
08:04:21
Integration Agent

Event:
TX load forecast increased 22%

Affected teams:
Asset Management
Wholesale
Origination
Sustainability
Finance
Procurement

Confidence:
94%
```

Never log secrets.

---

# 44. Local Developer Experience

A new developer should be able to run:

```bash
git clone <repository>

cd gridportfolio

pip install -e .

python scripts/generate_data.py

pytest

docker-compose up
```

The application should start locally with minimal configuration.

---

# 45. CLI

Provide commands such as:

```bash
gridportfolio generate-data

gridportfolio portfolio-health

gridportfolio detect-anomalies

gridportfolio analyze-impact

gridportfolio generate-brief

gridportfolio evaluate-agents

gridportfolio weekly-review
```

---

# 46. MVP

The MVP is complete when a user can:

1. Generate the synthetic portfolio.
2. Launch the application.
3. View the shared portfolio model.
4. View organizational teams.
5. View portfolio health.
6. View assets and contracts.
7. View market exposure.
8. View anomalies.
9. View risks.
10. Click an anomaly.
11. See affected teams.
12. See downstream metrics.
13. See affected initiatives.
14. Ask the Integration Agent to investigate.
15. Receive an evidence-grounded explanation.
16. Generate a cross-functional decision brief.
17. Assign an owner.
18. Create an action.
19. Track execution.
20. See the decision trace back to source data.
21. Run the entire system locally.

---

# 47. Phase 2

Add:

* public ISO/RTO datasets
* live ingestion
* richer forecasting
* scenario analysis
* procurement pipeline
* carbon optimization
* renewable matching
* contract valuation
* portfolio optimization
* scheduled reports
* richer agent evaluation

---

# 48. Phase 3 — Strategic Scenario Engine

Eventually support questions such as:

> “What happens if our Texas load increases 30% over the next three years?”

The system should produce:

```text
Load Scenario
      ↓
Capacity Requirement
      ↓
Market Exposure
      ↓
Contract Coverage
      ↓
Renewable Requirement
      ↓
Reliability Impact
      ↓
Financial Exposure
      ↓
Procurement Requirement
      ↓
Cross-Team Actions
```

Another example:

> “What happens if we need to achieve 95% hourly renewable matching?”

The system should determine:

* current position
* gap
* affected assets
* existing contracts
* procurement requirements
* market exposure
* storage requirements
* responsible teams
* decisions required

---

# 49. Optimization Layer

Eventually support:

> “What combination of PPAs, storage, and wholesale hedges minimizes expected cost while maintaining 95% renewable coverage and a defined reliability threshold?”

Use mathematical optimization for this layer.

Potential technologies:

* scipy.optimize
* Pyomo
* OR-Tools

The LLM should translate natural language into structured optimization parameters.

The optimization engine performs the actual calculation.

The LLM should explain the result.

---

# 50. Definition of Done

## Organizational Integration

* [ ] Teams represented explicitly
* [ ] Team ownership documented
* [ ] Shared semantic model implemented
* [ ] Metric contracts implemented
* [ ] Cross-team dependencies represented
* [ ] Integration map visible
* [ ] Affected-team analysis works
* [ ] Initiative tracking works
* [ ] Decision ownership works

## Portfolio Intelligence

* [ ] Portfolio health
* [ ] Risk engine
* [ ] Forecasting
* [ ] Anomaly detection
* [ ] Market exposure
* [ ] Contract performance
* [ ] Data quality

## AI

* [ ] Specialized agents
* [ ] Integration Agent
* [ ] Tool calling
* [ ] Evidence grounding
* [ ] Cross-functional impact analysis
* [ ] Decision briefs
* [ ] Executive summaries
* [ ] Confidence
* [ ] AI failure handling

## Operating Model

* [ ] Daily portfolio pulse
* [ ] Weekly portfolio review
* [ ] Monthly strategy review
* [ ] Initiative tracker
* [ ] Dependency graph
* [ ] Decision tracker
* [ ] Action tracker
* [ ] Outcome tracking

## Engineering

* [ ] Tests
* [ ] Docker
* [ ] CI
* [ ] API documentation
* [ ] Configuration
* [ ] Logging
* [ ] No secrets
* [ ] Reproducible synthetic data

## Responsible AI

* [ ] Human-in-the-loop
* [ ] Evidence provenance
* [ ] Confidence
* [ ] Data-quality warnings
* [ ] Fact/model/AI distinction
* [ ] Decision boundaries

---

# 51. Final Product Philosophy

The system should ultimately demonstrate:

```text
                     DATA
                      ↓
              SHARED DEFINITIONS
                      ↓
                PORTFOLIO TRUTH
                      ↓
                  ANALYTICS
                      ↓
             CONTINUOUS MONITORING
                      ↓
                RISK DETECTION
                      ↓
             CROSS-TEAM IMPACT
                      ↓
                     AI
                      ↓
              DECISION INTELLIGENCE
                      ↓
                   OWNERSHIP
                      ↓
                 PROCUREMENT
                      ↓
                  EXECUTION
                      ↓
                   OUTCOME
                      ↓
               PORTFOLIO TRUTH
```

The central product question is:

> **“What does the energy organization need to know, why does it matter, who needs to be involved, what decision does it create, who owns that decision, and did the organization actually execute?”**

GridPortfolio should not optimize for the number of AI features.

It should optimize for demonstrating that a technically sophisticated energy professional can connect:

**data + analytics + asset management + origination + wholesale + procurement + sustainability + finance + leadership + AI + execution**

into one coherent operating system.

---

# 52. What This Project Should Communicate

A person reviewing this project should come away with the following impression:

> **This person doesn't just build models.**

> **They understand how specialist teams operate, how their data and decisions intersect, where organizational seams create friction, how to establish a shared source of truth, how to turn fragmented signals into portfolio-level intelligence, and how to use AI to make the entire organization faster without replacing domain judgment.**

That is the core purpose of GridPortfolio.
