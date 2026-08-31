# Meeting Minutes: AI Project Progress Review

- **Project:** Smart Assistant AI Platform (Codename: "Chunsik")
- **Date:** 2026-08-31 (Monday)
- **Time:** 10:00 - 11:15 KST
- **Location:** Conference Room B / Google Meet (hybrid)
- **Attendees:** Kim Min-jun (PM), Lee Ji-eun (AI/ML Lead), Park Sang-hoon (Backend Lead), Choi Ye-rin (Frontend Lead), Jung Hyun-woo (QA Lead), Han So-yeon (Data Engineer)
- **Absent:** none
- **Minutes taken by:** Kim Min-jun

## 1. Agenda

1. Review progress since last sprint
2. Model training and evaluation status
3. Backend/API integration status
4. Frontend UI progress
5. QA and testing plan
6. Risks and blockers
7. Action items and deadlines

## 2. Progress Summary

- Overall project is at **65% completion** against the Q3 roadmap.
- The core recommendation model (v2) training run finished with a 4.2% improvement in accuracy over v1, but latency increased by 180ms; the team agreed this needs optimization before release.
- Backend team completed the new `/v2/recommendations` API endpoint; load testing is pending.
- Frontend team finished the dashboard redesign mockups and started implementation of the new chat interface.
- QA identified 12 open bugs from the last testing cycle (3 critical, 5 major, 4 minor).

## 3. Discussion Highlights

- **Model latency:** Lee Ji-eun proposed switching to quantized inference (INT8) to reduce latency. Team agreed to prototype this before the next review.
- **Data pipeline:** Han So-yeon reported the nightly ETL job occasionally fails due to a schema mismatch from the upstream analytics source; a fix is in progress.
- **API rate limiting:** Park Sang-hoon raised concerns about rate-limit handling for external partner integrations; will coordinate with the platform team.
- **UI accessibility:** Choi Ye-rin noted the new chat interface needs accessibility (WCAG 2.1 AA) review before launch.
- **Critical bugs:** Jung Hyun-woo flagged that 2 of the 3 critical bugs are blocking the staging deployment and must be resolved first.

## 4. Risks / Blockers

| Risk / Blocker | Owner | Severity | Notes |
|---|---|---|---|
| Model inference latency (+180ms) | Lee Ji-eun | High | May delay release if not resolved by Sep 12 |
| ETL schema mismatch causing pipeline failures | Han So-yeon | Medium | Root cause identified, fix in progress |
| 2 critical bugs blocking staging deploy | Jung Hyun-woo | High | Must be fixed before staging release |
| Partner API rate-limit handling incomplete | Park Sang-hoon | Medium | Needs coordination with platform team |

## 5. Action Items

| # | Task | Owner | Deadline | Status |
|---|---|---|---|---|
| 1 | Prototype INT8 quantized inference to reduce model latency | Lee Ji-eun | 2026-09-05 | Not started |
| 2 | Fix ETL schema mismatch in nightly data pipeline | Han So-yeon | 2026-09-03 | In progress |
| 3 | Resolve 2 critical bugs blocking staging deployment | Jung Hyun-woo | 2026-09-04 | In progress |
| 4 | Complete load testing for `/v2/recommendations` API | Park Sang-hoon | 2026-09-08 | Not started |
| 5 | Coordinate partner API rate-limit design with platform team | Park Sang-hoon | 2026-09-10 | Not started |
| 6 | Finish chat interface implementation (frontend) | Choi Ye-rin | 2026-09-11 | In progress |
| 7 | Conduct WCAG 2.1 AA accessibility review on new UI | Choi Ye-rin | 2026-09-12 | Not started |
| 8 | Re-test all major/minor bugs from last QA cycle | Jung Hyun-woo | 2026-09-09 | Not started |
| 9 | Prepare staging deployment readiness report | Kim Min-jun | 2026-09-12 | Not started |

## 6. Decisions Made

- Staging deployment target date set to **2026-09-15**, contingent on resolving critical bugs and latency issue.
- Team agreed to hold a mid-week sync (Wednesday, 15 min standup) to track the two high-severity blockers.
- Final go/no-go decision for staging release will be made at the next full team meeting.

## 7. Next Meeting

- **Date:** 2026-09-07 (Monday)
- **Time:** 10:00 KST
- **Focus:** Review action item completion, staging deployment go/no-go readiness check
