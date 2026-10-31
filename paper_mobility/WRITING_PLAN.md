# MOBILITY PAPER WRITING PLAN
# =============================
# Target: IEEE Transactions on Wireless Communications (TWC)
# Deadline: December 1, 2026 (SUBMIT)
# Time: 4 weeks (Nov 1 - Dec 1)

## PAPER METADATA

**Title**: Latency-Aware Phase Optimization for Reconfigurable Intelligent Surfaces in Mobile Scenarios

**Target Journal**: IEEE TWC (Impact Factor: 10.4, Tier 1)
**Page Limit**: 14-16 pages (double column)
**Current Status**: Template created, numbers collected

## TIMELINE (4 WEEKS)

### WEEK 1 (Nov 1-7): Introduction + Related Work + System Model
**Target**: 6 pages

| Day | Section | Content | Pages |
|-----|---------|---------|-------|
| Fri 1 | Introduction | Motivation, gap, contributions | 2 |
| Sat 2 | Introduction | Organization, polish | - |
| Sun 3 | Related Work | RIS optimization, mobility, latency | 2 |
| Mon 4 | System Model | Topology, channel, mobility | 1.5 |
| Tue 5 | System Model | Math details, equations | 0.5 |
| Wed 6 | Polish | Read-through, consistency | - |
| Thu 7 | Review | Week 1 deliverables complete | ✓ |

**Deliverable**: Sections I, II complete (6 pages)

### WEEK 2 (Nov 8-14): Main Results (Section III)
**Target**: 5 pages

| Day | Subsection | Content | Pages |
|-----|-----------|---------|-------|
| Fri 8 | Problem Formulation | Latency-aware objective | 1 |
| Sat 9 | Fresh vs Stale | 11.7-14.2× analysis | 1.5 |
| Sun 10 | Intrinsic Optimum | L=4 optimal, L=48 costs 14% | 1.5 |
| Mon 11 | Equal ms vs steps | Method ranking reversal | 1 |
| Tue 12 | Math proofs | Derivations, lemmas | - |
| Wed 13 | Figures | Fresh beam plot, optimum curve | - |
| Thu 14 | Review | Section III complete | ✓ |

**Deliverable**: Section III complete (5 pages)

### WEEK 3 (Nov 15-21): Methodology + Results
**Target**: 4 pages

| Day | Section | Content | Pages |
|-----|---------|---------|-------|
| Fri 15 | Methodology | Reproducibility, scripts, audit | 2 |
| Sat 16 | Methodology | Measurement traps, corrections | - |
| Sun 17 | Results | Tables, figures, discussion | 2 |
| Mon 18 | Results | Sensitivity analysis | - |
| Tue 19 | Conclusion | Summary, future work | 1 |
| Wed 20 | Abstract | Rewrite based on final paper | - |
| Thu 21 | Review | Week 3 deliverables complete | ✓ |

**Deliverable**: Sections IV, V, VI complete (4 pages)

### WEEK 4 (Nov 22-30): Polish + Submit
**Target**: Camera-ready

| Day | Task | Focus |
|-----|------|-------|
| Fri 22 | Full read-through | Flow, consistency |
| Sat 23 | References | Complete bibliography, check citations |
| Sun 24 | Figures | High-quality, consistent style |
| Mon 25 | Tables | Format, captions, alignment |
| Tue 26 | Proofreading | Grammar, typos, style |
| Wed 27 | Advisor review | Submit draft to advisor |
| Thu 28 | Revisions | Incorporate feedback |
| Fri 29 | Final check | Submission checklist |
| Sat 30 | **SUBMIT** | IEEE TWC submission |

**Deliverable**: Submitted manuscript


## SECTION BREAKDOWN (14 pages target)

| Section | Content | Pages |
|---------|---------|-------|
| I. Introduction | Motivation, gap, contributions | 2 |
| II. System Model | Topology, channel, mobility | 2 |
| III. Latency-Aware Analysis | Main theoretical results | 5 |
| IV. Measurement Methodology | Reproducibility framework | 2 |
| V. Numerical Results | Tables, figures, discussion | 2 |
| VI. Conclusion | Summary, future work | 1 |
| **Total** | | **14** |


## KEY FIGURES (8 total)

1. **System topology**: RIS-assisted MU-MISO downlink
2. **Fresh vs stale beam**: Bar chart (11.7-14.2×)
3. **Intrinsic optimum**: Rate vs L (showing L=4 peak)
4. **Convergence trap**: L=48 vs L=4 effective rate
5. **Equal steps**: Learned wins (table + bar chart)
6. **Equal milliseconds**: All 5 dominated (scatter plot)
7. **Aging correlation**: ρ(τ) vs delay
8. **Method ranking reversal**: Visualization

## KEY TABLES (5 total)

1. **Main results summary**: Fresh beam, L=4, ranking
2. **Fresh vs stale**: Three phase selections
3. **Equal steps comparison**: 5 budgets
4. **Equal ms comparison**: Domination analysis
5. **System parameters**: Configuration details


## WRITING RULES

### Content
- **Start each section with motivation**: Why does the reader care?
- **Lead with results**: State the finding, then derive it
- **Concrete before abstract**: Show example, then generalize
- **Numbers with context**: "11.7× faster" not just "faster"

### Style
- **Active voice**: "We show" not "It is shown"
- **Present tense for findings**: "The optimum is L=4"
- **Past tense for experiments**: "We measured 1200 scenarios"
- **Avoid hedging**: "This demonstrates" not "This may suggest"

### Math
- **Define all symbols**: Build symbol table first
- **Equations numbered**: Only if referenced later
- **Inline for simple**: Use inline math for single variables
- **Display for important**: Display equations for key results

### Figures
- **Vector format**: Use PDF/EPS, not PNG
- **Readable fonts**: 10-12pt in final size
- **Color + shape**: Don't rely on color alone
- **Captions complete**: Should be understandable alone

### References
- **Recent work**: Prioritize 2020-2024
- **Tier 1 journals**: IEEE TWC, TCOM, JSA, WCL
- **Top conferences**: ICC, Globecom, WCNC
- **Avoid arXiv**: Cite published version if available


## DAILY ROUTINE

### Morning (3 hours)
- Fresh writing on new content
- No email, no distractions
- Target: 1-2 pages of new text

### Afternoon (2 hours)
- Revise morning's work
- Create figures/tables
- Check references

### Evening (1 hour)
- Read related papers
- Plan next day
- Update this file


## CHECKLIST BEFORE SUBMIT

### Content
- [ ] All claims backed by numbers from KEY_NUMBERS.md
- [ ] All numbers traceable to scripts
- [ ] Contributions clearly stated (Section I)
- [ ] Results match abstract claims
- [ ] Future work section included

### Format
- [ ] IEEE TWC LaTeX template used
- [ ] Page limit: 14-16 pages
- [ ] Figures: Vector format (PDF/EPS)
- [ ] Tables: IEEE booktabs style
- [ ] References: IEEE format, complete

### Quality
- [ ] Spell check (US English)
- [ ] Grammar check (Grammarly/LanguageTool)
- [ ] Math symbols consistent
- [ ] Acronyms defined at first use
- [ ] Figure captions self-contained

### Reproducibility
- [ ] Scripts mentioned in text
- [ ] Data availability statement
- [ ] Code repository URL (if allowed)
- [ ] Conflict of interest statement

### Submission
- [ ] Copyright form signed
- [ ] Supplementary materials prepared
- [ ] Cover letter written
- [ ] Suggested reviewers list (3-5)
- [ ] Opposed reviewers list (optional)


## BACKUP PLAN

**If timeline slips:**
- Cut Section IV (Methodology) to 1.5 pages
- Reduce Related Work to 1.5 pages  
- Merge some figures → save 0.5 page
- **Still hit Dec 1 deadline**

**If advisor requests major changes:**
- Week 4 becomes revision week
- Submit Dec 7-8 (1 week slip acceptable)

**If TWC seems too ambitious:**
- Backup: IEEE Wireless Communications Letters (WCL)
- Page limit: 4 pages (much faster to write)
- Still Tier 1, faster review


## METRICS

Track daily progress:
```
Date       | Pages Written | Pages Total | Figures | Status
-----------|--------------|-------------|---------|--------
Nov 1      |              |             |         |
Nov 2      |              |             |         |
...        |              |             |         |
Nov 30     |              |      14     |    8    | SUBMIT
```

**Update this file DAILY**
