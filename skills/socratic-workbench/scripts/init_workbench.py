#!/usr/bin/env python3
"""Internal template & anti-spoiler parity checker for Socratic Study Workbenches."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TrackSpec:
    """Domain metadata and Part 4/Mock simulation blocks."""

    label: str
    goal_hint: str
    part4_heading: str
    part4_body: str
    mock_prompt: str


TRACK_SPECS: dict[str, TrackSpec] = {
    "textbook": TrackSpec(
        label="textbook",
        goal_hint="Extract core book mechanisms into answer_key.md, drill blind first, memorize verified answers, then pass oral mock checks",
        part4_heading="Part 4: Applied Case Practice (From the Book)",
        part4_body="""### Case 4.1: Everyday or Chapter Scenario
> **Scenario**: `<Real-world situation or textbook exercise testing the chapter's core mechanism>`

1. **Core mechanism at work (in your own words before checking formulas):**
   - 
2. **Prediction or walkthrough:**
   - 
""",
        mock_prompt="Roleplay a skeptical peer or oral professor questioning why the chapter's rule holds—and where it breaks—strictly against `answer_key.md`.",
    ),
    "coding": TrackSpec(
        label="coding",
        goal_hint="Own system logic & edge cases in 4 plain-language steps; compile 1:1 to real tests, memorize tradeoffs, then defend in design mock",
        part4_heading="Part 4: 4-Step Plain-Language Code Drill",
        part4_body="""### Drill 4.1: `<function_or_component_name>`

#### Input / Output Examples
```json
{
  "input": {"example_param": "value"},
  "expected_output": {"status": "ok"}
}
```

#### Already Handled For You
- Signature: `solve(arg) -> Result`

#### Your 4 Plain-Language Steps (No raw syntax needed)
1. **What to store**: 
2. **Main step / loop**: 
3. **Edge cases to guard**: 
4. **What to return**: 
""",
        mock_prompt="Run a closed-book architecture review: ask 'what breaks under 10x load, clock skew, or invalid input?' graded against `answer_key.md`.",
    ),
    "interview": TrackSpec(
        label="interview",
        goal_hint="Extract rubric points into answer_key.md, practice blind recall, lock bold memory notes, and drill answer-grounded mock interviews",
        part4_heading="Part 4: Incident / Exam Vignette Drill",
        part4_body="""### Case 4.1: Production Incident or Exam Case
> **Scenario**: `<Describe a realistic symptom, bottleneck, or multi-part exam vignette>`

- **Root-Cause Diagnosis**: 
- **Fix + One Tradeoff**: 
""",
        mock_prompt="Conduct a rapid-fire mock interview/oral exam strictly grounded in `answer_key.md` scoring points until every answer lands cold.",
    ),
    "language": TrackSpec(
        label="language",
        goal_hint="Extract target expressions & tone rules into answer_key.md, practice blind first, memorize upgrades, then run live roleplay simulation",
        part4_heading="Part 4: Contextual Expression Drill",
        part4_body="""### Scenario 4.1: Real-World Situation From Material
> **Setting**: `<Describe the real communication context from the language book/unit>`

- **Prompt**: `"<Realistic opening line from the other speaker>"`
- **Your Reply (Write naturally before checking model sentences)**: 
""",
        mock_prompt="Run a multi-turn closed-book roleplay simulation checking whether memorized phrases from `answer_key.md` are used naturally under pressure.",
    ),
}


def render_workbench(title: str, track: str) -> str:
    """Render a spoiler-free 5-part workbench.md for the chosen material track."""
    spec = TRACK_SPECS[track]
    return f"""# {title} — Practice Workbench

> **Domain**: `{spec.label}`  
> **Workflow**: {spec.goal_hint}  
> **Spoiler Lock**: Practice here *before* unlocking standard answers from `answer_key.md`.

---

## Part 1: High-Yield Guide & Big Picture

### 1.1 Priority Reading Focus
- **Must Master**:
  - `<Core thesis, mechanism, or pattern>`
- **Good Context**:
  - `<Supporting details>`

### 1.2 Big-Picture Map
```text
[Source Input / Premise] ---> [{title}] ---> [Result / Impact]
```

---

## Part 2: Blind Check Questions (Practice -> Follow-Up -> Unlock to Memorize)

> Write rough keywords under `> **My Try**:` first. Once cleared, your coach unlocks concise bold answers under `> **Verified Answer to Memorize**:`.

### Topic A: Core Understanding

#### Q1.1 `<Question extracted from the source material>` (`3` points)
- > **My Try**: 
- > **Verified Answer to Memorize**: *(Locked until blind try + follow-up probe are completed)*

#### Q1.2 `<Boundary / tradeoff / misconception question>` (`3` points)
- > **My Try**: 
- > **Verified Answer to Memorize**: *(Locked until blind try + follow-up probe are completed)*

---

## Part 3: Common Misconception Traps

| Area | Tempting Mistake | How It Fails in Practice | Grounded Truth |
|---|---|---|---|
| Basics | `<Common intuition trap>` | `<Real breakdown / misconception>` | `<Reliable principle from source>` |

---

## {spec.part4_heading}

{spec.part4_body.rstrip()}

---

## Part 5: Answer-Grounded Mock Simulation & Sign-Off

- **Mock Simulation Brief**: {spec.mock_prompt}
- [ ] Explained Part 1's big picture in 60 seconds without notes.
- [ ] Unlocked and memorized all Part 2 verified standard answers.
- [ ] Passed Part 4 applied drill.
- [ ] Passed closed-book Mock Simulation using `answer_key.md` as the live rubric.
"""


def render_answer_key(title: str, track: str) -> str:
    """Render a separated answer_key.md paired by Q-IDs to workbench.md."""
    return f"""# {title} — Extracted Standard Answers & Mock Rubric

> **Domain**: `{track}`  
> Extracted from source material. Used by the AI coach to grade `workbench.md` and run Step 4 Mock Simulations.

---

### Q1.1 `<Repeat Q1.1 question>`
- **Standard Answer Key Points (`3`)**:
  1. **<Keyword 1>**: `<Concise grounded explanation>`
  2. **<Keyword 2>**: `<Concise grounded explanation>`
  3. **<Keyword 3>**: `<Concise grounded explanation>`
- **Follow-Up Probes if Missed (Never spoil directly)**:
  - *If Point 1 is missing*: `"<Scenario twist nudging Point 1>"`
  - *If Point 2 is missing*: `"<Counterexample nudging Point 2>"`

### Q1.2 `<Repeat Q1.2 question>`
- **Standard Answer Key Points (`3`)**:
  1. **<Keyword 1>**: `<Concise grounded explanation>`
  2. **<Keyword 2>**: `<Concise grounded explanation>`
  3. **<Keyword 3>**: `<Concise grounded explanation>`
- **Follow-Up Probes if Missed (Never spoil directly)**:
  - *If Point 1 is missing*: `"<Scenario twist>"`
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

    for spoiler_marker in ("Standard Answer Key Points", "Core Scoring Points", "Key Points ("):
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
        description="Internal scaffolder & spoiler-check validator for workbench.md + answer_key.md."
    )
    parser.add_argument("--dir", required=True, help="Target study unit directory.")
    parser.add_argument("--title", default="New Study Material", help="Material or chapter title.")
    parser.add_argument(
        "--track",
        choices=sorted(TRACK_SPECS.keys()),
        default="textbook",
        help="Material domain: textbook | coding | interview | language.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing files if present.")
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
            print(f"OK: {target_dir} passed structure, spoiler-lock, and Q-ID checks.")
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
