# GridPortfolio

## What This Project Is

**GridPortfolio** is a demonstration of an AI-ready energy portfolio intelligence platform.

It brings together fragmented data from **Asset Management, Analytics, Wholesale, Origination, Procurement, and Initiatives** into a single cross-functional portfolio view.

The pipeline then:

* Validates source data quality
* Integrates disparate datasets
* Calculates portfolio health and risk metrics
* Detects cross-functional signals
* Identifies risks and business impacts
* Generates an executive-ready brief
* Evaluates the quality of the resulting signals and brief

The core idea is simple:

> **Don't just detect that something changed — understand what changed, who it affects, why it matters, and what decision should happen next.**

This repository currently uses synthetic data to demonstrate the architecture and workflow.

---

## Architecture

```text
Source Systems
     │
     ├── Asset Management
     ├── Analytics / Forecasting
     ├── Wholesale
     ├── Origination
     ├── Procurement
     └── Initiatives
              │
              ▼
       Data Quality Layer
              │
              ▼
      Integration Pipeline
              │
              ▼
    Cross-Functional View
              │
              ▼
       Portfolio Metrics
              │
              ▼
      Signal Detection
              │
              ▼
     Executive Decision Brief
              │
              ▼
        AI Evaluation
```

---

## Tech Stack

* Python
* pandas
* Pydantic
* uv
* Pytest
* Git / GitHub

The project is structured to support future integration with production data sources, ML models, and AI/agent workflows.

---

## Run the Project

From the repository root:

```bash
cd ~/Documents/GitHub/data-centers-energy
```

Install/sync the environment:

```bash
uv sync
```

Run the complete demonstration:

```bash
uv run python -m gridportfolio.pipeline
```

You should see:

* Source-system data quality
* Portfolio health
* Cross-functional signals
* Executive brief
* AI evaluation results

A successful run should finish with the evaluation passing.

---

## Run Validation

Compile the key modules:

```bash
uv run python -m py_compile src/gridportfolio/integration/pipeline.py
uv run python -m py_compile src/gridportfolio/portfolio/metrics.py
uv run python -m py_compile src/gridportfolio/signals/detector.py
uv run python -m py_compile src/gridportfolio/pipeline.py
```

Test imports:

```bash
uv run python -c "import gridportfolio; print('IMPORT OK')"
```

---

## Project Structure

```text
src/gridportfolio/
├── data/              # Synthetic source-system data and schemas
├── integration/       # Cross-system integration and data quality
├── portfolio/         # Portfolio health and risk metrics
├── signals/           # Cross-functional signal detection
├── models/             # Portfolio/domain models
└── pipeline.py         # End-to-end demonstration
```

---

## Current Status

**Working end-to-end demonstration.**

The current implementation demonstrates the complete flow from fragmented energy data → integrated portfolio intelligence → actionable signals → executive decision brief → automated evaluation.

The next step would be replacing synthetic data with real source-system interfaces and extending the intelligence layer with production ML/AI models.
