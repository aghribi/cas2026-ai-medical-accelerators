#!/usr/bin/env python3
"""
Slide design checker — CAS 2026 presentation.
Parses index.qmd, scores each slide against the design contract,
and prints a prioritised report.

Usage:  python check_slides.py [index.qmd]
"""

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ── Thresholds (from DESIGN_PLAN.md) ─────────────────────────────────────────
LIMIT_ELEMENTS      = 4      # hard: > this → HIGH
TARGET_ELEMENTS     = 3      # soft
LIMIT_WORDS_BOX     = 28     # hard
TARGET_WORDS_BOX    = 18     # soft
LIMIT_WORDS_SLIDE   = 100    # hard
TARGET_WORDS_SLIDE  = 70     # soft
LIMIT_FONTSIZE      = 0.85   # hard (em)
TARGET_FONTSIZE     = 0.80   # soft (em)
LIMIT_FRAGMENTS     = 6      # hard: > this → noise
TARGET_FRAGMENTS    = 5      # soft
MIN_DOMINANT_COL    = 52     # dominant column must be ≥ this %

# ── Helpers ───────────────────────────────────────────────────────────────────

def strip_code_blocks(text: str) -> str:
    """Remove fenced code blocks (```...```) and speaker notes."""
    # Quarto fenced code blocks: ```{python} ... ``` or ``` ... ```
    text = re.sub(r"```[^\n]*\n.*?```", "", text, flags=re.DOTALL)
    # Speaker notes: ::: notes ... :::
    text = re.sub(r":::\s*notes\b.*?:::", "", text, flags=re.DOTALL)
    # Fragment overlay divs (concept callout / callout box) — intentional design elements
    text = re.sub(r'<div class="fragment slide-callout-overlay">.*?</div>\s*</div>\s*</div>',
                  "", text, flags=re.DOTALL)
    return text

def strip_html_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", " ", text)

def strip_markdown(text: str) -> str:
    text = re.sub(r"\*+([^*]+)\*+", r"\1", text)   # bold/italic
    text = re.sub(r"`[^`]+`", "", text)              # inline code
    text = re.sub(r"\$[^$]+\$", "", text)            # inline math
    text = re.sub(r"^\s*[#\-\*>|]\s*", "", text, flags=re.MULTILINE)
    return text

def word_count(text: str) -> int:
    text = strip_code_blocks(text)
    text = strip_html_tags(text)
    text = strip_markdown(text)
    return len(text.split())

def extract_font_sizes(text: str) -> list[float]:
    """Find all inline font-size:Xem values."""
    hits = re.findall(r"font-size:\s*([\d.]+)em", text)
    return [float(h) for h in hits]

def count_content_elements(text: str) -> int:
    """
    Count discrete content boxes / items:
    - .highlight-box  .key-result  .warning-box  .callout-box  .concept-callout-box
    - top-level ordered/unordered list items (lines starting with - or digit.)
    """
    boxes = len(re.findall(
        r'class="(?:highlight-box|key-result|warning-box|callout-box|concept-callout-box)',
        text))
    # also count ::: {.highlight-box ...}  style dividers
    boxes += len(re.findall(r":::\s*\{[^}]*(?:highlight-box|key-result|warning-box)[^}]*\}", text))
    # deduplicate: the HTML and markdown forms shouldn't both appear for the same box
    # just take the max approach: use the larger of the two patterns
    list_items = len(re.findall(r"^\s*[-*]\s+\S", text, flags=re.MULTILINE))
    list_items += len(re.findall(r"^\s*\d+\.\s+\S", text, flags=re.MULTILINE))
    # treat list items only if no boxes found (avoid double-counting)
    return boxes if boxes > 0 else min(list_items, 8)

def count_fragments(text: str) -> int:
    return len(re.findall(r"\.fragment", text))

def has_figure(text: str) -> bool:
    return bool(re.search(
        r"go\.Figure|plotly|js-plotly|<iframe|!\[|\.svg|\.png|\.jpg|metric\b",
        text, re.IGNORECASE))

def extract_box_word_counts(text: str) -> list[int]:
    """Return word count for each content box found."""
    counts = []
    # HTML-style divs
    for m in re.finditer(
        r'<div class="(?:highlight-box|key-result|warning-box|callout-box|concept-callout-box)[^"]*">(.*?)</div>',
        text, re.DOTALL):
        counts.append(word_count(m.group(1)))
    # Markdown-fenced boxes  ::: {.highlight-box ...} ... :::
    chunks = re.split(r":::", text)
    for i, chunk in enumerate(chunks):
        if re.match(r"\s*\{[^}]*(?:highlight-box|key-result|warning-box)[^}]*\}", chunk):
            content = chunks[i + 1] if i + 1 < len(chunks) else ""
            counts.append(word_count(content))
    return counts

def check_column_balance(text: str) -> list[str]:
    issues = []
    widths = [int(m) for m in re.findall(r'width="(\d+)%"', text)]
    if len(widths) >= 2:
        dominant = max(widths)
        if dominant < MIN_DOMINANT_COL:
            issues.append(
                f"Symmetric columns ({widths}) — dominant must be ≥{MIN_DOMINANT_COL}%")
    col_left = len(re.findall(r'col-left', text))
    col_right = len(re.findall(r'col-right', text))
    if col_left and col_right and not has_figure(text):
        issues.append("Two float columns but no figure — risk of symmetric text overload")
    return issues

def extract_cyan_count(text: str) -> int:
    structural = re.findall(r"#22d3ee", text)
    # discount uses inside python code blocks
    in_code = re.findall(r"```.*?#22d3ee.*?```", text, re.DOTALL)
    return max(0, len(structural) - len(in_code) * 3)

# ── Slide parser ──────────────────────────────────────────────────────────────

@dataclass
class Slide:
    number: int
    title: str
    line_start: int
    raw: str
    issues: list[str] = field(default_factory=list)
    stats: dict = field(default_factory=dict)
    priority: str = "OK"


def parse_slides(qmd: str) -> list[Slide]:
    # Remove YAML front-matter (between first two --- at file top)
    qmd = re.sub(r"^---\n.*?---\n", "", qmd, count=1, flags=re.DOTALL)

    # Split on hard slide separators, keeping line numbers approximate
    raw_slides = re.split(r"\n---\n", qmd)

    slides = []
    slide_num = 0
    for raw in raw_slides:
        # find title
        title_m = re.search(r"^##\s+(.+)$", raw, re.MULTILINE)
        if not title_m:
            title_m = re.search(r"^#\s+(.+)$", raw, re.MULTILINE)
        if not title_m:
            continue  # skip non-slide chunks

        slide_num += 1
        title = title_m.group(1).strip()
        # strip section-divider / title slides from scoring (they're intentionally sparse)
        is_structural = bool(re.search(
            r"\.section-divider|\.title-slide|\.plain|\.no-footer\s+background-iframe|background-iframe",
            raw))

        slides.append(Slide(
            number=slide_num,
            title=title[:60],
            line_start=0,
            raw=raw,
            stats={"structural": is_structural},
        ))

    return slides


def score_slide(slide: Slide) -> None:
    if slide.stats.get("structural"):
        slide.stats["skipped"] = True
        return

    raw = slide.raw
    clean = strip_code_blocks(raw)

    # ── D1: element count ────────────────────────────────────────────────────
    n_elements = count_content_elements(clean)
    slide.stats["elements"] = n_elements
    if n_elements > LIMIT_ELEMENTS:
        slide.issues.append(
            f"D1 ❌ {n_elements} content elements (hard limit {LIMIT_ELEMENTS})")
    elif n_elements > TARGET_ELEMENTS:
        slide.issues.append(
            f"D1 ⚠  {n_elements} content elements (target {TARGET_ELEMENTS})")

    # ── D2: fragments ────────────────────────────────────────────────────────
    n_frags = count_fragments(raw)
    slide.stats["fragments"] = n_frags
    if n_elements >= 3 and n_frags == 0:
        slide.issues.append(
            f"D2 ❌ {n_elements} elements but 0 fragments — dense slide with no pacing")
    if n_frags > LIMIT_FRAGMENTS:
        slide.issues.append(
            f"D2 ⚠  {n_frags} fragments (limit {LIMIT_FRAGMENTS}) — may feel noisy")

    # column balance
    for col_issue in check_column_balance(raw):
        slide.issues.append(f"D2 ⚠  {col_issue}")

    # ── D3: cyan overuse ─────────────────────────────────────────────────────
    cyan = extract_cyan_count(raw)
    slide.stats["cyan_count"] = cyan
    if cyan > 5:
        slide.issues.append(
            f"D3 ⚠  {cyan} uses of #22d3ee structural color — dilutes accent")

    # ── D4: visual anchor ────────────────────────────────────────────────────
    fig = has_figure(raw)
    slide.stats["has_figure"] = fig
    if not fig and n_elements >= 3:
        slide.issues.append(
            "D4 ⚠  No figure/chart on a dense slide — missing visual anchor")

    # ── D5: text density ─────────────────────────────────────────────────────
    box_counts = extract_box_word_counts(raw)
    total_words = word_count(clean)
    slide.stats["total_words"] = total_words
    slide.stats["box_word_counts"] = box_counts

    if total_words > LIMIT_WORDS_SLIDE:
        slide.issues.append(
            f"D5 ❌ {total_words} total words (hard limit {LIMIT_WORDS_SLIDE})")
    elif total_words > TARGET_WORDS_SLIDE:
        slide.issues.append(
            f"D5 ⚠  {total_words} total words (target {TARGET_WORDS_SLIDE})")

    for i, wc in enumerate(box_counts, 1):
        if wc > LIMIT_WORDS_BOX:
            slide.issues.append(
                f"D5 ❌ Box {i}: {wc} words (hard limit {LIMIT_WORDS_BOX})")
        elif wc > TARGET_WORDS_BOX:
            slide.issues.append(
                f"D5 ⚠  Box {i}: {wc} words (target {TARGET_WORDS_BOX})")

    font_sizes = extract_font_sizes(raw)
    for fs in font_sizes:
        if fs > LIMIT_FONTSIZE:
            slide.issues.append(
                f"D5 ❌ font-size {fs}em found (limit {LIMIT_FONTSIZE}em)")
        elif fs > TARGET_FONTSIZE:
            slide.issues.append(
                f"D5 ⚠  font-size {fs}em found (target {TARGET_FONTSIZE}em)")

    # ── Priority ─────────────────────────────────────────────────────────────
    hard_fails = [i for i in slide.issues if "❌" in i]
    soft_warns = [i for i in slide.issues if "⚠" in i]
    if hard_fails:
        slide.priority = "HIGH"
    elif soft_warns:
        slide.priority = "MEDIUM"
    else:
        slide.priority = "OK"


# ── Report ────────────────────────────────────────────────────────────────────

PRIORITY_ORDER = {"HIGH": 0, "MEDIUM": 1, "OK": 2}
PRIORITY_ICON  = {"HIGH": "🔴", "MEDIUM": "🟡", "OK": "🟢"}

def print_report(slides: list[Slide]) -> None:
    scored = [s for s in slides if not s.stats.get("skipped")]
    scored_sorted = sorted(scored, key=lambda s: (PRIORITY_ORDER[s.priority], s.number))

    high   = [s for s in scored if s.priority == "HIGH"]
    medium = [s for s in scored if s.priority == "MEDIUM"]
    ok     = [s for s in scored if s.priority == "OK"]

    print("=" * 70)
    print("SLIDE DESIGN AUDIT — CAS 2026")
    print("=" * 70)
    print(f"  Slides scored : {len(scored)}")
    print(f"  🔴 HIGH       : {len(high)}")
    print(f"  🟡 MEDIUM     : {len(medium)}")
    print(f"  🟢 OK         : {len(ok)}")
    print()

    current_priority = None
    for slide in scored_sorted:
        if slide.priority != current_priority:
            current_priority = slide.priority
            print(f"{'─'*70}")
            print(f"  {PRIORITY_ICON[slide.priority]}  {slide.priority} PRIORITY")
            print(f"{'─'*70}")

        if slide.priority == "OK":
            print(f"  #{slide.number:02d}  {slide.title}")
            continue

        print(f"\n  #{slide.number:02d}  {slide.title}")
        stats = slide.stats
        print(f"        elements={stats.get('elements','?')}  "
              f"words={stats.get('total_words','?')}  "
              f"fragments={stats.get('fragments','?')}  "
              f"figure={'yes' if stats.get('has_figure') else 'no'}")
        for issue in slide.issues:
            print(f"        {issue}")

    print()
    print("=" * 70)
    print("VISUAL INSPECTION CHECKLIST (manual — run in browser)")
    print("=" * 70)
    for slide in [s for s in slides if not s.stats.get("skipped") and s.priority != "OK"]:
        print(f"  #{slide.number:02d}  {slide.title[:55]}")
        print(f"        □ One pre-attentive anchor (chart / big number / icon)")
        print(f"        □ ≥35% empty space at full reveal")
        print(f"        □ Single cyan 'hot spot' visible")
        print(f"        □ Typography hierarchy: title > bold key term > prose")
        print()


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("index.qmd")
    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(1)

    qmd = path.read_text()
    slides = parse_slides(qmd)
    for slide in slides:
        score_slide(slide)
    print_report(slides)


if __name__ == "__main__":
    main()
