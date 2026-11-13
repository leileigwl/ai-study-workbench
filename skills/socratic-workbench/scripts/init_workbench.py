#!/usr/bin/env python3
"""Zero-dependency CLI scaffolder & validator for Socratic Study Workbenches."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TrackSpec:
    """Track-specific metadata and Part 4 template blocks."""

    label: str
    goal_hint: str
    part4_heading: str
    part4_body: str


TRACK_SPECS: dict[str, TrackSpec] = {
    "coding": TrackSpec(
        label="coding",
        goal_hint="System design ownership & deterministic test verification without memorizing raw syntax",
        part4_heading="Part 4: Active Production Drill — 4-Slot Pseudocode Compilation",
        part4_body="""### Drill 4.1: `<function_or_component_name>`

#### Input / Output Examples (Plain Data)
```json
{
  "input": {"example_param": "value"},
  "expected_output": {"status": "ok"}
}
```

#### Stripped Interface Contract
- Signature: `solve(arg) -> Result`
- Provided types / invariants: `<Document exact fields so the learner focuses 100% on logic>`

#### 4-Slot Native-Language Pseudocode (Do NOT write target-language boilerplate)
- **Slot 1 — State & Containers**: 
- **Slot 2 — Core Step / Transition**: 
- **Slot 3 — Boundary & Error Guards**: 
- **Slot 4 — Return / Side-Effect Contract**: 
""",
    ),
    "interview": TrackSpec(
        label="interview",
        goal_hint="Rapid interview/exam active recall + production failure diagnosis under stress",
        part4_heading="Part 4: Active Production Drill — Incident Root-Cause & Tradeoff Diagnosis",
        part4_body="""### Case 4.1: Production Incident / Exam Vignette
> **Scenario**: `<Describe a realistic failure symptom, latency spike, data anomaly, or exam vignette>`

- **Root Cause Hypothesis**: 
- **Immediate Mitigation vs Structural Fix**: 
- **Key Tradeoff Accepted**: 
""",
    ),
    "book": TrackSpec(
        label="book",
        goal_hint="Mental model extraction, intuition-trap immunity & real-world case transfer",
        part4_heading="Part 4: Active Production Drill — Cross-Context Case Transfer & Feynman Teach-Back",
        part4_body="""### Transfer 4.1: Apply the Core Model Outside the Author's Examples
> **Unfamiliar Scenario**: `<Describe a workplace, product, policy, or personal decision dilemma>`

1. **Structural Diagnosis (Name the mechanism / causal loop, not surface symptoms)**:
   - 
2. **Boundary / Second-Order Risk (Where could this framework backfire here?)**:
   - 
3. **60-Second Feynman Teach-Back (Explain cleanly to a peer with zero jargon)**:
   - 
""",
    ),
}


def render_workbench(title: str, track: str) -> str:
    """Render a spoiler-free 5-part workbench.md document for the given track."""
    spec = TRACK_SPECS[track]
    return f"""# {title} — Active Study Workbench

> **Track**: `{spec.label}`  
> **Goal**: {spec.goal_hint}  
> **Spoiler Rule**: Attempt every draft below *before* consulting `answer_key.md`.

---

## Part 1: Focus Guide & Macro Map

### 1.1 Priority Reading Guide
- **Core (High-Yield / Must Master)**:
  - `<Primary mechanism or chapter>`
- **Extended (Context Only)**:
  - `<Secondary implementation details>`

### 1.2 Macro Integration & Dependency Map
- **Upstream Inputs**: `<What triggers or feeds this unit?>`
- **Core Responsibility**: `<What invariant or decision does this unit own?>`
- **Downstream Consumers / Effects**: `<What breaks downstream if this unit fails?>`

```text
[Upstream] ---> [{title}] ---> [Downstream]
```

---

## Part 2: Categorized Blind Retrieval Q&A (Draft -> Scenario Probe -> Audit)

> Write concise keywords under `> **My Draft**:`. Send to your AI coach for point-count scoring and scenario follow-ups.

### Category A: Core Mechanisms & Invariants

#### Q1.1 `<Replace with core why/how question>` (`3` core points)
- > **My Draft**: 
- > **Follow-up & Audited Answer**: *(Locked until blind draft + scenario probe are completed)*

#### Q1.2 `<Replace with failure-boundary or tradeoff question>` (`3` core points)
- > **My Draft**: 
- > **Follow-up & Audited Answer**: *(Locked until blind draft + scenario probe are completed)*

---

## Part 3: Intuition Traps & Anti-Patterns

| Category | Intuition Trap | Real-World / Exam Failure Mode | Reliable Principle |
|---|---|---|---|
| Core Logic | `<What beginners intuitively guess>` | `<Exact symptom when it fails>` | `<Durable rule or architecture pattern>` |

---

## {spec.part4_heading}

{spec.part4_body.rstrip()}

---

## Part 5: Unit Sign-Off Checklist

- [ ] Can explain Part 1's macro map in 60 seconds without notes.
- [ ] Resolved all Part 2 blind Q&As including scenario follow-up probes.
- [ ] Can spot every Part 3 intuition trap when shown a flawed design.
- [ ] Passed Part 4 active drill verification.
"""


def render_answer_key(title: str, track: str) -> str:
    """Render a separated answer_key.md matched by Q-IDs to workbench.md."""
    return f"""# {title} — Separated Answer Key (AI Grading Rubric)

> **Track**: `{track}`  
> **Spoiler Guard**: Keep closed while drafting `workbench.md`. Use matched Q-IDs (`Q1.1`, `Q1.2`, ...) during grading.

---

### Q1.1 `<Repeat Q1.1 text>`
- **Core Scoring Points (`3`)**:
  1. **<Keyword Anchor 1>**: `<Explanation>`
  2. **<Keyword Anchor 2>**: `<Explanation>`
  3. **<Keyword Anchor 3>**: `<Explanation>`
- **Scenario Probes (Use if a point is missed — do NOT spoil directly)**:
  - *Missing Point 1*: `"<Concrete failure scenario forcing discovery of Point 1>"`
  - *Missing Point 2*: `"<Edge-case scenario forcing discovery of Point 2>"`

### Q1.2 `<Repeat Q1.2 text>`
- **Core Scoring Points (`3`)**:
  1. **<Keyword Anchor 1>**: `<Explanation>`
  2. **<Keyword Anchor 2>**: `<Explanation>`
  3. **<Keyword Anchor 3>**: `<Explanation>`
- **Scenario Probes (Use if a point is missed — do NOT spoil directly)**:
  - *Missing Point 1*: `"<Concrete tradeoff / incident prompt>"`
"""


def validate_pair(target_dir: Path) -> tuple[bool, list[str]]:
    """Validate structural integrity, Part 1-5 presence, and Q-ID parity without spoilers."""
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

    if "Core Scoring Points" in wb_text:
        errors.append("Spoiler leak detected: 'Core Scoring Points' found inside workbench.md")

    wb_qids = set(re.findall(r"^####\s+(Q\d+\.\d+)\b", wb_text, flags=re.MULTILINE))
    ak_qids = set(re.findall(r"^###\s+(Q\d+\.\d+)\b", ak_text, flags=re.MULTILINE))

    if not wb_qids:
        errors.append("No Q-IDs (e.g. '#### Q1.1 ...') found in workbench.md")
    missing_in_ak = sorted(wb_qids - ak_qids)
    extra_in_ak = sorted(ak_qids - wb_qids)
    if missing_in_ak:
        errors.append(f"Q-IDs present in workbench.md missing from answer_key.md: {missing_in_ak}")
    if extra_in_ak:
        errors.append(f"Extra Q-IDs in answer_key.md absent from workbench.md: {extra_in_ak}")

    return len(errors) == 0, errors


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Scaffold or validate a Socratic Workbench (workbench.md + answer_key.md)."
    )
    parser.add_argument("--dir", required=True, help="Target unit directory path.")
    parser.add_argument("--title", default="New Study Unit", help="Unit title.")
    parser.add_argument(
        "--track",
        choices=sorted(TRACK_SPECS.keys()),
        default="coding",
        help="Domain adapter track.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing workbench.md / answer_key.md if present.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate an existing workbench.md + answer_key.md pair instead of scaffolding.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Entry point for CLI execution."""
    args = parse_args(argv if argv is not None else sys.argv[1:])
    target_dir = Path(args.dir)

    if args.check:
        ok, errors = validate_pair(target_dir)
        if ok:
            print(f"OK: {target_dir} passed structure, anti-spoiler, and Q-ID parity checks.")
            return 0
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    target_dir.mkdir(parents=True, exist_ok=True)
    wb_path = target_dir / "workbench.md"
    ak_path = target_dir / "answer_key.md"

    if not args.force and (wb_path.exists() or ak_path.exists()):
        print(
            f"ERROR: Target already contains workbench.md or answer_key.md ({target_dir}). "
            "Pass --force to overwrite.",
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

    print(f"Scaffolded [{args.track}] workbench pair in {target_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
