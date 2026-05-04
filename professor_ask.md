# professor_ask.md — Lab Resource Request and Access Translation

**Date:** 2026-03-30  
**Role:** Lab Manager / PI Lens  
**Evidence standard:** Per AGENT_MISSION.md  

---

## 1. The Ask

### Equipment needed

| Resource | Specification | Duration needed |
|---------|--------------|-----------------|
| Closed-loop liquid cooling bench | Small pump (gear or peristaltic, < 5 LPM), reservoir, temperature-controlled bath (25 °C ± 1 °C) | 2–3 days |
| Data acquisition system | 4-channel thermocouple input + 1 analog voltage (pressure) + 1 flow signal, 1 Hz logging | 2–3 days |
| Differential pressure transducer | 0–10 kPa range, ±0.5% FS (or better) | Borrow for test period |
| Flow meter | 0.01–5 LPM, ±2% (Coriolis or small turbine) | Borrow for test period |
| Thermocouples (3×) | Type-T, ±0.5 °C, thin-gauge for surface mounting | Own or purchase ($30–50) |
| Heater | Cartridge heater, 0–50 W controllable via DC supply | Borrow |
| µCT scanner (optional) | Verify internal geometry pre-test | 1 session (~2 hours) |

### Estimated facility hours
- **Setup:** 4–6 hours (first day)
- **Testing:** 3–4 hours (second day)
- **Teardown + cleanup:** 2 hours
- **Total:** ~10–12 hours over 2–3 days

### Staff / student help needed
- None required — the requester performs all test operations
- Optional: lab safety orientation if required by facility policy
- Optional: brief consultation with lab manager on flow loop setup

### Consumables
- Deionized water (~2 L)
- Thermal paste (~1 g)
- O-rings for port sealing (standard sizes, bring own)
- Teflon tape for fittings

### Safety / setup needs
- Leak containment tray under test section
- Low voltage DC heater (< 50 V) — no high-voltage hazard
- Water only, room temperature — no chemical hazard
- Over-temperature shutoff on heater controller (set to 150 °C)
- No pressure vessel hazard (< 50 kPa operating)

---

## 2. The Offer

### Value exchange

**For the lab / professor:**
- A **well-prepared, self-contained test** — specimen, test plan, pass/fail criteria, data analysis all handled by the requester
- **Short duration** (2–3 days) — minimal disruption to lab schedule
- **Publishable result regardless of outcome:**
  - Positive match → demonstrates simplified pipeline captures correct physics (novel for AM TPMS cold plates)
  - Negative match → identifies specific model limitations with clear failure mode analysis (useful for thermal modeling community)
- **Co-authorship** on any publication using the data
- **Acknowledgment** of lab facility in all publications and presentations
- **Open-source pipeline** — lab can reuse the design tool for their own research
- **Student mentorship opportunity** — if lab has students interested in thermal management or AM

**For the requester:**
- First experimental data point for pipeline validation
- Go/no-go on pipeline direction
- Evidence for thesis / project advancement

---

## 3. Why a PI Might Say No

| Reason | Likelihood | Mitigation |
|--------|-----------|------------|
| No suitable flow loop at this scale (most labs have larger rigs) | **MEDIUM** | Ask about any small-scale test capability; a syringe pump + graduated cylinder could work |
| No time / schedule conflict | **MEDIUM** | Offer flexible scheduling; 2–3 days over any 2-week window |
| Unclear scope — "how do I know this won't take weeks?" | **LOW** | Test plan is fully defined; show this package. Total bench time < 4 hours |
| Safety review needed for new test article | **LOW** | Prepare safety summary in advance; no unusual hazards |
| Specimen is too small (5 mm cube) — hard to instrument | **MEDIUM** | Acknowledged. Surface-mount thermocouples work; show attachment plan |
| No value proposition — "what do I get out of this?" | **LOW** | Co-authorship, interesting result, open-source tool access |
| Geometry maturity unclear | **MEDIUM** | Show Stage 6 screening results, STL manifest, watertight check |

---

## 4. One-Paragraph Email Ask

> I'm working on an open-source cold-plate design pipeline that generates diamond TPMS internal geometries for direct-to-chip liquid cooling. I have a 5 mm aluminum test specimen ready for AM fabrication, with locked simulation predictions, pre-defined pass/fail thresholds, and a complete test plan. I'm looking for 2–3 days of access to a small-scale liquid cooling test bench (< 5 LPM pump, DAQ with thermocouples, differential pressure transducer) to run a directional validation — is the pipeline's thermal resistance prediction within an order of magnitude of reality? I'll prepare the specimen, fixture, and all documentation; I'd just need bench access, flow loop, and instrumentation. The result is publishable regardless of outcome, and I'd be happy to offer co-authorship. Would you have 15 minutes to discuss feasibility?

---

## 5. Meeting Checklist — What Must Be Ready Before Contacting Lab

- [ ] **Fabrication STL file on disk and verified watertight** (currently: NOT on disk — blocker)
- [ ] **Locked simulation reference** (currently: EXISTS — SIMREF-C02-001)
- [ ] **Test plan document** (currently: EXISTS — 22 documents in docs/stage7_validation/)
- [ ] **Pass/fail thresholds** (currently: EXISTS — see bench_pass_fail.md)
- [ ] **Specimen procurement plan** — vendor, cost estimate, lead time (currently: NOT prepared)
- [ ] **Fixture design concept** — how the 5 mm cube is mounted, sealed, and heated (currently: NOT designed)
- [ ] **Instrumentation list with correct specifications** (currently: EXISTS but flow meter range is wrong — needs correction from 0–200 LPM to 0.01–5 LPM)
- [ ] **Safety summary** — one page covering hazards and controls (currently: NOT prepared)
- [ ] **Budget summary** — who pays for specimen, consumables, facility time (currently: NOT prepared)

### Items that BLOCK the lab ask:
1. ❌ Regenerate and verify geometry files (volume.npy + STL) — cannot show a specimen without them
2. ❌ Correct flow meter specification — showing a 200 LPM spec for a 5 mm cold plate destroys credibility
3. ❌ Design the mounting fixture — a PI wants to see that you've thought through how this actually mounts

### Items that should be ready but don't block:
4. ⚠ Fixture fabrication — can discuss timeline during meeting
5. ⚠ AM vendor quote — can procure after lab access is confirmed
6. ⚠ Safety summary — straightforward, can prepare overnight

---

## 6. Realistic Timeline

| Week | Activity | Owner |
|------|---------|-------|
| 1 | Re-run pipeline, regenerate geometry, correct flow meter specs, design fixture | User |
| 1–2 | Contact professor, schedule meeting | User |
| 2 | Meeting with professor / lab manager | User + Lab |
| 2–3 | Submit specimen to AM vendor ($500–2,000) | User |
| 3–5 | Vendor fabrication (2–3 week lead time typical for small Al LPBF) | Vendor |
| 5 | Receive specimen, mass check, optional µCT | User |
| 5–6 | Fabricate fixture, prepare instrumentation | User |
| 6 | Execute test (2–3 days lab access) | User at lab |
| 7 | Process data, write verdict | User |

**Total: 6–7 weeks, dominated by AM lead time.**
