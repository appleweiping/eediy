## Summary / 摘要

<!-- Explain the learner-facing outcome and keep this pull request to one concern. -->

## Change type / 变更类型

- [ ] Course or resource data
- [ ] Route or prerequisite graph
- [ ] Project, tooling, or safety guidance
- [ ] Chinese/English content
- [ ] Generator, test, or deployment tooling
- [ ] Link or factual correction

## Evidence / 证据

- Primary sources:
- Verification date:
- Affected tracks, routes, and pages:
- Relationship to any provider or resource:

## Required checks / 必检项

- [ ] Chinese and English counterparts are both updated.
- [ ] Every resource records access, license, status, and last verification date.
- [ ] Workload has traceable provider evidence, or is labelled as a maintainer estimate with its basis and a two-week learner calibration requirement.
- [ ] Software, hardware, cost, safety, and completion evidence are present.
- [ ] Generated pages were regenerated and were not hand-edited.
- [ ] I did not add restricted answers, personal data, credentials, or unlicensed material.
- [ ] New physical work has conservative hazards, controls, and supervision requirements.

## Verification / 验证

```text
python -m pytest -q
python scripts/run_quality.py
```

Paste a concise result summary and explain any manual-review external links. Policy denials remain review items and must not be reported as healthy.
