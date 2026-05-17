---
name: tester-intro
description: Introduces the core competencies, mindset, tools, and STLC knowledge expected of an expert QA/SDET engineer. Use when onboarding to a project, assessing skill gaps, or establishing testing standards for a team.
---

# Expert Tester / SDET — Introduction & Core Skills

## Instructions

When invoked, guide the user through the foundational knowledge and mindset of an expert tester. Assess context, then provide targeted guidance.

---

### Step 1: Establish Context

Ask (or infer from conversation):
- Are you a manual tester, automation engineer, or SDET?
- What domain/project are you working on (web, mobile, API, embedded)?
- What is your experience level (junior, mid, senior, expert)?

Tailor all subsequent guidance to this context.

---

### Step 2: Tester Mindset

Reinforce these core principles:
- **Assume nothing** — requirements are incomplete by default; probe for gaps.
- **Think like an adversary** — your job is to find what developers missed, requirement missed or unclear.
- **Risk-based thinking** — prioritize testing areas by business impact, not by ease.
- **Quality ownership** — quality is a team responsibility; advocate for it at every stage.
- **Shift-left** — engage in static testing of requirements, design, and PR reviews, not just after code is written.

---

### Step 3: Core Competencies

#### Manual Testing
- Exploratory testing techniques (session-based, charter-driven) which uncover hidden issues
- Equivalence partitioning, boundary value analysis, decision tables
- State transition testing, use case testing
- Usability and accessibility evaluation

#### Automation Engineering (SDET)
- Writing maintainable test code (Page Object Model, Screenplay pattern)
- Selecting the right automation layer (unit / integration / E2E)
- Test pyramid awareness — avoid over-reliance on UI tests
- CI/CD integration (tests as gates, not afterthoughts)

#### API & Backend Testing
- REST/GraphQL contract validation
- Authentication flows (OAuth, JWT, API keys)
- Schema validation, response time benchmarks

#### Non-Functional Testing
- Performance (load, stress, soak)
- Security (OWASP basics, injection, auth bypass)
- Accessibility (WCAG 2.x)
- Compatibility (browsers, OS, devices)

---

### Step 4: Tools Landscape

Present relevant tools based on the user's stack:

| Category | Tools |
|---|---|
| Web UI Automation | Selenium, Playwright, Cypress, WebdriverIO |
| Mobile | Appium, Espresso, XCTest |
| API Testing | Postman, RestAssured, Karate, Pact |
| Unit/Integration | JUnit 5, TestNG, pytest, Jest, Mocha |
| Performance | k6, JMeter, Gatling, Locust |
| BDD | Cucumber, SpecFlow, Behave |
| Test Management | JIRA + Zephyr/Xray, TestRail, qTest |
| CI/CD | GitHub Actions, Jenkins, GitLab CI, CircleCI |
| Reporting | Allure, ExtentReports, ReportPortal |

Recommend a minimal viable toolchain for their context — do not overwhelm with options.

---

### Step 5: SDLC / STLC Overview

Explain the Software Testing Life Cycle phases and the tester's role in each:

1. **Requirement Analysis** — Review specs, raise questions, identify testability issues
2. **Test Planning** — Scope, strategy, resources, timeline, risk assessment
3. **Test Design** — Write test cases, prepare test data, set up environments
4. **Environment Setup** — Verify test infra, configure test data, validate builds
5. **Test Execution** — Run tests, log defects, retest fixes, regression testing
6. **Test Closure** — Metrics, lessons learned, sign-off report

Emphasize: testers add the most value **before** execution (design and analysis phases).

---

### Step 6: Positioning as an Expert Tester

Advise on:
- Contributing to architecture and design reviews (testability lens)
- Writing test strategies, not just test cases
- Mentoring teams on quality practices
- Measuring and communicating quality metrics (defect density, coverage, escape rate)
- Participating in incident retrospectives to trace missed defects back to test gaps

### Keep in mind: being an expert tester is doing accuarately with a mindset of quality ownership, risk-based thinking, and continuous learning by giving clarify - logical test scenarios and asking questions to uncover hidden assumptions in requirements. Always following the given requirement and link strictly to the requirement and test case, and providing clear and concise feedback to developers and stakeholders.
