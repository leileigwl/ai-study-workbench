#!/usr/bin/env python3
"""Zero-dependency CLI scaffolder & anti-spoiler checker for Socratic Study Workbenches."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TrackSpec:
    """Track metadata and Part 4 sparring/drill template."""

    label: str
    goal_hint: str
    part4_heading: str
    part4_body: str


TRACK_SPECS: dict[str, TrackSpec] = {
    "english": TrackSpec(
        label="english",
        goal_hint="Real-life speaking/writing sparring — produce first, get coached naturally, upgrade phrasing",
        part4_heading="Part 4: Live Roleplay Sparring",
        part4_body="""### Roleplay 4.1: Realistic Scenario
> **Setting**: `<Describe the real situation, e.g. client pushback, coffee chat, salary discussion>`
> **Your Role**: `<Who you are playing>` | **Coach Role**: `<Who pushes back>`

- **Coach Opening Line**: `"<Realistic question or pushback>"`
- **Your First Reply (Write naturally before looking anything up)**: 
- **Coach Follow-Up & Upgraded Phrasing**: *(Coach responds in character, probes gaps, then gives natural upgrades)*
""",
    ),
    "textbook": TrackSpec(
        label="textbook",
        goal_hint="Understand why a chapter works, catch naive intuition traps, and solve real cases without peeking",
        part4_heading="Part 4: Real-World Case & Problem Walkthrough",
        part4_body="""### Case 4.1: Everyday or Homework Scenario
> **Problem**: `<Describe a concrete real-life situation or textbook exercise before giving formulas>`

1. **Which core rule/mechanism applies here (in your own words)?**
   - 
2. **Walk through your prediction or calculation:**
   - 
3. **Coach Check & Edge Twist**: *(Completed during interactive review)*
""",
    ),
    "coding": TrackSpec(
        label="coding",
        goal_hint="Own 100% of the logic & edge cases in plain language; let AI compile syntax literally + run tests",
        part4_heading="Part 4: Plain-Language Code Drill (4-Step Logic -> Real Tests)",
        part4_body="""### Drill 4.1: `<function_or_component_name>`

#### Input / Output Examples
```json
{
  "input": {"example_param": "value"},
  "expected_output": {"status": "ok"}
}
```

#### Already Handled For You (Ignore Boilerplate)
- Signature: `solve(arg) -> Result`
- Available fields: `<List exact fields/types so you focus only on logic>`

#### Your 4 Plain-Language Steps (Chinese or English — NO need to write raw syntax)
1. **What to store**: 
2. **Main step / loop**: 
3. **Edge cases to guard**: 
4. **What to return**: 
""",
    ),
    "interview": TrackSpec(
        label="interview",
        goal_hint="Blind recall with point counts, scenario stress-testing, and concise keyword memory cards",
        part4_heading="Part 4: Realistic Failure / Exam Twist Case",
        part4_body="""### Case 4.1: Production Incident or Exam Vignette
> **Scenario**: `<Describe a tricky failure symptom, tradeoff dilemma, or multi-part exam question>`

- **Your Root-Cause Diagnosis**: 
- **Fix + One Tradeoff**: 
""",
    ),
}


def render_workbench(title: str, track: str) -> str:
    """Render a clean, spoiler-free 5-part workbench.md for the chosen track."""
    spec = TRACK_SPECS[track]
    return f"""# {title} — Active Study Workbench

> **Track**: `{spec.label}`  
> **What you'll master**: {spec.goal_hint}  
> **Rule**: Try every section below on your own *before* opening `answer_key.md`.

---

## Part 1: What Matters Most & Big Picture

### 1.1 Priority Guide
- **Must Master**:
  - `<Core idea or skill 1>`
- **Good Context (Don't over-memorize)**:
  - `<Supporting detail>`

### 1.2 How It All Connects
```text
[Trigger / Input] ---> [{title}] ---> [Outcome / Next Step]
```

---

## Part 2: Blind Check Questions (Try First -> Follow-Up -> Final Note)

> Jot rough keywords under `> **My Try**:` and send to your AI coach. Don't peek at `answer_key.md`.

### Topic A: Core Ideas

#### Q1.1 `<Question in plain language>` (`3` points)
- > **My Try**: 
- > **Coach Feedback & Final Note**: *(Unlocked after your try + follow-up)*

#### Q1.2 `<Boundary / "What happens if..." question>` (`3` points)
- > **My Try**: 
- > **Coach Feedback & Final Note**: *(Unlocked after your try + follow-up)*

---

## Part 3: Common Mistakes (Quick Trap Check)

| Area | Tempting Intuition | How It Backfires | Reliable Way |
|---|---|---|---|
| Basics | `<Common wrong guess>` | `<Real mistake or failure>` | `<What actually works>` |

---

## {spec.part4_heading}

{spec.part4_body.rstrip()}

---

## Part 5: Honest Sign-Off Checklist

- [ ] Can explain the Part 1 big picture in 60 seconds without notes.
- [ ] Answered all Part 2 questions blind and cleared coach follow-ups.
- [ ] Can spot every Part 3 common mistake immediately.
- [ ] Passed Part 4 active sparring / coding test drill.
"""


def render_answer_key(title: str, track: str) -> str:
    """Render a separated answer_key.md paired by Q-IDs to workbench.md."""
    return f"""# {title} — Separated Answer Key (For Your AI Coach)

> **Track**: `{track}`  
> Keep closed while practicing `workbench.md`. Q-IDs (`Q1.1`, `Q1.2`, ...) match 1:1.

---

### Q1.1 `<Repeat Q1.1 question>`
- **Key Points (`3`)**:
  1. **<Keyword 1>**: `<Plain explanation>`
  2. **<Keyword 2>**: `<Plain explanation>`
  3. **<Keyword 3>**: `<Plain explanation>`
- **Follow-Up Prompts if Missed (Do NOT spoil directly)**:
  - *If Point 1 is missing*: `"<Concrete scenario or question that nudges Point 1>"`
  - *If Point 2 is missing*: `"<Concrete edge twist that nudges Point 2>"`

### Q1.2 `<Repeat Q1.2 question>`
- **Key Points (`3`)**:
  1. **<Keyword 1>**: `<Plain explanation>`
  2. **<Keyword 2>**: `<Plain explanation>`
  3. **<Keyword 3>**: `<Plain explanation>`
- **Follow-Up Prompts if Missed (Do NOT spoil directly)**:
  - *If Point 1 is missing*: `"<Concrete twist>"`
"""


def validate_pair(target_dir: Path) -> tuple[bool, list[str]]:
    """Validate 5-part structure, zero spoiler leakage, and Q-ID parity."""
    wb_path = target_dir / "workbench.md"
    ak_path = target_dir / "answer_key.md"
    errors: list[str] = []

    if not wb_path.is_file():
        errors.append(f"Missing workbench.md in {target_dir}")
    if not ak_path.is_file():
        errors.append(f"Missing answer_key.md in {target_dir}")
    if errors:
        return False, errors

    wb_text = wb_path.read_text(encoding="utf-8")
    ak_text = ak_path.read_text(encoding="utf-8")

    for part in ("## Part 1:", "## Part 2:", "## Part 3:", "## Part 4:", "## Part 5:"):
        if part not in wb_text:
            errors.append(f"workbench.md missing required section: {part}")

    for spoiler_marker in ("Key Points (", "Core Scoring Points"):
        if spoiler_marker in wb_text:
            errors.append(f"Spoiler leak detected inside workbench.md: {spoiler_marker}")

    wb_qids = set(re.findall(r"^####\s+(Q\d+\.\d+)\b", wb_text, flags=re.MULTILINE))
    ak_qids = set(re.findall(r"^###\s+(Q\d+\.\d+)\b", ak_text, flags=re.MULTILINE))

    if not wb_qids:
        errors.append("No Q-IDs (e.g. '#### Q1.1 ...') found in workbench.md")
    missing_in_ak = sorted(wb_qids - ak_qids)
    extra_in_ak = sorted(ak_qids - wb_qids)
    if missing_in_ak:
        errors.append(f"Q-IDs in workbench.md missing from answer_key.md: {missing_in_ak}")
    if extra_in_ak:
        errors.append(f"Extra Q-IDs in answer_key.md missing from workbench.md: {extra_in_ak}")

    return len(errors) == 0, errors


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Scaffold or validate a Socratic Workbench (workbench.md + answer_key.md)."
    )
    parser.add_argument("--dir", required=True, help="Target study unit directory.")
    parser.add_argument("--title", default="New Study Unit", help="Unit title.")
    parser.add_argument(
        "--track",
        choices=sorted(TRACK_SPECS.keys()),
        default="coding",
        help="Learning track: english | textbook | coding | interview.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files if present.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate existing workbench.md + answer_key.md instead of creating files.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    args = parse_args(argv if argv is not None else sys.argv[1:])
    target_dir = Path(args.dir)

    if args.check:
        ok, errors = validate_pair(target_dir)
        if ok:
            print(f"OK: {target_dir} passed structure, anti-spoiler, and Q-ID checks.")
            return 0
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    target_dir.mkdir(parents=True, exist_ok=True)
    wb_path = target_dir / "workbench.md"
    ak_path = target_dir / "answer_key.md"

    if not args.force and (wb_path.exists() or ak_path.exists()):
        print(
            f"ERROR: {target_dir} already has workbench.md or answer_key.md. Use --force to overwrite.",
            file=sys.stderr,
        )
        return 2

    wb_path.write_text(render_workbench(args.title, args.track), encoding="utf-8")
    ak_path.write_text(render_answer_key(args.title, args.track), encoding="utf-8")
    ok, errors = validate_pair(target_dir)
    if not ok:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    print(f"Created [{args.track}] workbench in {target_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
