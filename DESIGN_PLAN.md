# Presentation Design Plan
## CAS 2026 — AI for Medical Accelerators

---

## Design Contract

Six dimensions, each with a measurable target and a hard limit.

### D1 · Ideas per slide

| Parameter | Target | Hard limit |
|---|---|---|
| Content elements (boxes, numbered items, major bullets) | ≤ 3 | 4 |
| Key idea per slide | 1 dominant | — |
| "And also…" count in speaker notes | 0 | 1 |

**Rule:** If you need to say more than 3 things, split the slide or move to speaker notes.

---

### D2 · Attention guidance

| Parameter | Target | Hard limit |
|---|---|---|
| Pre-attentive anchor (chart, big number, icon) | 1 per slide | 0 = fail |
| Fragments on slides with ≥ 3 elements | ≥ 1 fragment | 0 = fail |
| Total fragments per slide | ≤ 5 | 6 |
| Symmetric columns (both ≥ 48% width) | forbidden | — |

**Rule:** One element must dominate. Fragments reveal one complete thought at a time — not half-sentences.  
**Column rule:** Always one dominant column (≥ 55%) and one secondary (≤ 42%).

---

### D3 · Color and contrast

| Parameter | Target | Hard limit |
|---|---|---|
| Cyan `#22d3ee` hot-spots per slide | 1 structural use | 3 |
| Semantic colors used | ≤ 3 (cyan/amber/orange) | 4 |
| Text on dark background contrast | WCAG AA minimum | — |

**Rule:** Cyan marks the single most important thing on the slide. Everything else recedes to `#94a3b8` or `#475569`.

---

### D4 · Visual anchoring

| Parameter | Target | Hard limit |
|---|---|---|
| Figure or chart present | every content slide | — |
| Icon/symbol as semantic shortcut | encouraged | — |
| Dominant column contains figure | ≥ 60% of two-column slides | — |

**Rule:** Every slide should have something the eye can rest on without reading. A chart, a big number, a diagram.

---

### D5 · Text density and empty space

| Parameter | Target | Hard limit |
|---|---|---|
| Words per content box | ≤ 18 | 28 |
| Total prose words per slide | ≤ 70 | 100 |
| Lines per content box | ≤ 3 | 4 |
| Inline font-size for content boxes | ≤ 0.80em | 0.85em |
| Empty space fraction (estimated) | ≥ 35% | < 25% = fail |

**Rule:** Boxes hold labels and one-line summaries — not paragraphs. Full explanations go in speaker notes.

---

### D6 · Cognitive load (Mayer / Sweller)

| Principle | Implementation |
|---|---|
| Coherence — remove extraneous material | No box unless it serves the slide's one key idea |
| Redundancy — don't write what you will say | ≤ 1 full sentence per slide; rest = labels |
| Signaling — mark structure explicitly | Bold key term + smaller supporting prose always |
| Segmenting — learner controls pace | Fragments for every multi-step build |
| Split-attention — no reading + listening simultaneously | Figure right / labels left so channels don't compete |
| Temporal contiguity — explain when shown | Fragment appears exactly when you speak it |

---

## Layout Templates

### Template A — Figure dominant (most content slides)
```
┌─────────────────────────────────────────────────────────┐
│ ## Slide title                                          │
│                                                         │
│  [Label 1]         │  ╔═══════════════════════╗        │
│                    │  ║                       ║        │
│  [Label 2]  ◄──────┼──║   Chart / Figure      ║        │
│   (fragment)       │  ║   (visual anchor)     ║        │
│  [Label 3]         │  ╚═══════════════════════╝        │
│   (fragment)       │                                   │
│   38%              │         60%                       │
└─────────────────────────────────────────────────────────┘
```

### Template B — Build slide (fragment-heavy, no figure)
```
┌─────────────────────────────────────────────────────────┐
│ ## Slide title                                          │
│                                                         │
│  ╔═══════════════════╗    ╔════════════════════╗        │
│  ║  Concept 1        ║    ║  Context / ref     ║        │
│  ╚═══════════════════╝    ╚════════════════════╝        │
│                                                         │
│  ╔═══════════════════╗ ◄── fragment                     │
│  ║  Concept 2        ║                                  │
│  ╚═══════════════════╝                                  │
│                                                         │
│       [≥ 35% empty space]                               │
└─────────────────────────────────────────────────────────┘
```

### Template C — Statement slide (low density, high impact)
```
┌─────────────────────────────────────────────────────────┐
│ ## Slide title                                          │
│                                                         │
│                                                         │
│        ┌─────────────────────────────┐                  │
│        │  ONE KEY RESULT / NUMBER   │                  │
│        └─────────────────────────────┘                  │
│                                                         │
│        Supporting sentence. One line.                   │
│                                                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Iteration Loop

```
READ slide content
    │
    ▼
RUN check_slides.py  ──► score per criterion per slide
    │
    ▼
TRIAGE by priority (HIGH → MEDIUM → LOW)
    │
    ▼
REDESIGN worst offenders (one slide at a time)
    │
    ▼
RE-RUN check_slides.py  ──► verify improvement
    │
    ▼
COMMIT when all slides pass hard limits
```

### Priority tiers
- **HIGH** (fix immediately): element count > 4, total words > 100, no pre-attentive anchor, no fragment on dense slide
- **MEDIUM** (fix before final): words per box > 20, font-size > 0.82em, symmetric columns
- **LOW** (polish): words per box 18–20, cyan overuse, minor spacing

---

## Acceptance Criteria

A slide **passes** when all of the following are true:
- [ ] D1: ≤ 3 content elements
- [ ] D2: ≥ 1 fragment if ≥ 3 elements; dominant column present
- [ ] D3: ≤ 2 structural cyan uses
- [ ] D4: chart or strong visual present (or slide is intentionally minimal)
- [ ] D5: ≤ 28 words per box, ≤ 100 total words, font-size ≤ 0.85em
- [ ] D6: no full paragraphs in boxes; key term bolded

The deck **ships** when all slides pass D5 hard limits and ≥ 90% pass D2.
