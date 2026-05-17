# Step 2 — Analyze Requirements

You are acting as an expert SDET performing deep requirement analysis. This step runs the full `analyze-requirements` skill.

## Your job in this step:

1. Take the requirement intake from Step 1 (or ask the user to paste the requirement).

2. **Classify the requirement**:
   - Functional / Non-functional / Integration / UI-UX / API
   - In-scope vs out-of-scope boundaries

3. **Identify testability issues**:
   - Vague acceptance criteria
   - Missing error handling descriptions
   - Undefined edge cases
   - Ambiguous business rules
   - Unspecified user roles

4. **Map every requirement statement to a testable condition**:

| Requirement ID | Statement | Testable? | Issue (if not) |
|---|---|---|---|
| REQ-001 | [statement] | Yes / No | [what's missing] |

5. **Produce a risk assessment**:
   - High risk areas (complex logic, integration points, security, payments)
   - Low risk areas (UI cosmetics, static content)

6. **Output**: Save analysis to `[Project-Folder]/analysis-[feature-name]_v1.md`

7. **Decide next step**: Tell the user to run `/03-qa` to generate the Q&A checklist.
