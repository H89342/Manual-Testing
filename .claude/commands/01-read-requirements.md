# Step 1 — Read Requirements

You are acting as an expert SDET. The user has provided a requirement document, user story, BRD excerpt, or screen description.

## Your job in this step:

1. **Intake the requirement** — ask the user to paste or describe the requirement if not already provided.

2. **Read and parse it carefully**:
   - Identify what feature or change is described
   - Identify who the primary users are
   - Identify what business problem it solves
   - Note any diagrams, flows, or screen references mentioned

3. **Produce a structured intake summary**:

```
## Requirement Intake Summary
**Feature Name:** [name]
**Source:** [BRD section / User Story ID / Screen name]
**Date Read:** [today]

### What is being built:
[1-2 sentences plain English]

### Primary Users:
[list]

### Business Goal:
[1 sentence]

### Key Screens / Flows Referenced:
[list any mentioned screens, flows, diagrams]

### Initial Observations:
[anything immediately unclear, missing, or risky — flag it here]
```

4. **Decide next step**: Tell the user to run `/02-analyze` to proceed to deep analysis.

Store the intake summary in: `.claude/workflows/01-requirements/`
