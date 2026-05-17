# 04 — Test Execution

Store execution logs and progress tracking here.

## What goes here:
- Live execution logs from `/06-execute` → `execution-log-[feature]-[date].md`
- Environment and build version records
- Blocker logs

## Naming convention:
`execution-log-[feature-name]-[YYYY-MM-DD].md`

## Track per execution session:
- Build version tested
- Environment (Staging / UAT / Prod)
- Pass / Fail / Blocked / Skipped counts
- Blockers raised

## Next step:
For each FAIL → run `/07-report-bug`
At end of cycle → produce Test Execution Summary → save to `06-reports/`
