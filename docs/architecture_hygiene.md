# Architecture Hygiene

This document defines non-negotiable structural rules of the system.

## Layer Boundaries

- Retrieval must not know about prompting
- Prompting must not know about LLM implementations
- LLMs must not know about retrieval or prompting
- Orchestration happens only in run_rag

## Why This Matters

Violating these rules:
- Causes hidden coupling
- Makes testing unreliable
- Breaks grounding guarantees later (v0.2+)

## Tests Enforcing This

See:
- tests/architecture_hygiene/test_layer_boundaries.py
- tests/architecture_hygiene/test_public_contracts.py
