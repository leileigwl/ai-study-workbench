#!/usr/bin/env python3
"""Internal scaffolder & spoiler-lock validator for bilingual (EN / ZH-CN) Socratic Workbenches."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TrackSpec:
    """Domain metadata and Part 4 / Mock simulation templates."""

    label: str
    goal_en: str
    goal_zh: str
    part4_heading_en: str
    part4_body_en: str
    mock_en: str
    part4_heading_zh: str
    part4_body_zh: str
    mock_zh: str


TRACK_SPECS: dict[str, TrackSpec] = {
    "textbook": TrackSpec(
        label="textbook",
        goal_en="Extract core book mechanisms into answer_key.md, drill blind first, memorize verified answers, then pass oral mock checks",
        goal_zh="先从书本提炼标准答案，盲练抓出漏洞并解锁背诵，最后拿标准答案做脱稿模拟",
        part4_heading_en="Part 4: Applied Case Practice (From the Book)",
        part4_body_en="""### Case 4.1: Everyday or Chapter Scenario
> **Scenario**: `<Real-world situation or textbook exercise testing the chapter's core mechanism>`

1. **Core mechanism at work (in your own words before checking formulas):**
   - 
2. **Prediction or walkthrough:**
   - 
""",
        mock_en="Roleplay a skeptical peer or oral professor questioning why the chapter's rule holds—and where it breaks—strictly against `answer_key.md`.",
        part4_heading_zh="第四部分：应用案例推演（不看公式先判机制）",
        part4_body_zh="""### 案例 4.1：生活或课后场景题
> **场景**：`<贴近书本核心机制的真实场景或课后习题>`

1. **用自己的话讲清背后发生了什么机制（先别套公式）：**
   - 
2. **你的判断或推导结果：**
   - 
""",
        mock_zh="让 AI 扮演专业课口试考官或较真的同行，对照 `answer_key.zh-CN.md` 闭卷追问你书里的核心机制与失效边界。",
    ),
    "coding": TrackSpec(
        label="coding",
        goal_en="Own system logic & edge cases in 4 plain-language steps; compile 1:1 to real tests, memorize tradeoffs, then defend in design mock",
        goal_zh="忘光语法也能练：先写大白话四步让 AI 1:1 编译跑单测，全绿后学惯用法并做架构评审模拟",
        part4_heading_en="Part 4: 4-Step Plain-Language Code Drill",
        part4_body_en="""### Drill 4.1: `<function_or_component_name>`

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
        mock_en="Run a closed-book architecture review: ask 'what breaks under 10x load, clock skew, or invalid input?' graded against `answer_key.md`.",
        part4_heading_zh="第四部分：大白话四步编码闯关（AI 1:1 编译跑单测）",
        part4_body_zh="""### 题目 4.1：`<函数或模块名称>`

#### 输入 / 输出直观样例
```json
{
  "输入": {"example_param": "value"},
  "期望输出": {"status": "ok"}
}
```

#### 框架已经帮你包好的部分
- 函数签名：`solve(arg) -> Result`

#### 请填写你的中文四步逻辑（不用记语法）
1. **存什么容器/状态**：
2. **主步骤怎么算**：
3. **哪些边界要防住**：
4. **最后返回什么**：
""",
        mock_zh="让 AI 扮演高并发架构面试官，拿着 `answer_key.zh-CN.md` 闭卷追问并发、异常与边界故障处理。",
    ),
    "interview": TrackSpec(
        label="interview",
        goal_en="Extract rubric points into answer_key.md, practice blind recall, lock bold memory notes, and drill answer-grounded mock interviews",
        goal_zh="抽提面试/考证评分点，盲答追问补漏后解锁黑体记忆卡，再用标准答案当面试官考自己",
        part4_heading_en="Part 4: Incident / Exam Vignette Drill",
        part4_body_en="""### Case 4.1: Production Incident or Exam Case
> **Scenario**: `<Describe a realistic symptom, bottleneck, or multi-part exam vignette>`

- **Root-Cause Diagnosis**: 
- **Fix + One Tradeoff**: 
""",
        mock_en="Conduct a rapid-fire mock interview/oral exam strictly grounded in `answer_key.md` scoring points until every answer lands cold.",
        part4_heading_zh="第四部分：线上事故 / 考题情境推演",
        part4_body_zh="""### 案例 4.1：真实故障或考场案例
> **场景**：`<描述线上的真实报错现象、性能瓶颈或复合型考题>`

- **你的根因定位**：
- **修复方案与权衡代价**：
""",
        mock_zh="对照 `answer_key.zh-CN.md` 开启高压连环追问模拟面试/口试，直到脱口覆盖所有采分点。",
    ),
    "language": TrackSpec(
        label="language",
        goal_en="Extract target expressions & tone rules into answer_key.md, practice blind first, memorize upgrades, then run live roleplay simulation",
        goal_zh="提取教材表达与语气禁忌，先硬写改错再解锁地道句型去背，最后进行闭卷情景对话模拟",
        part4_heading_en="Part 4: Contextual Expression Drill",
        part4_body_en="""### Scenario 4.1: Real-World Situation From Material
> **Setting**: `<Describe the real communication context from the language book/unit>`

- **Prompt**: `"<Realistic opening line from the other speaker>"`
- **Your Reply (Write naturally before checking model sentences)**: 
""",
        mock_en="Run a multi-turn closed-book roleplay simulation checking whether memorized phrases from `answer_key.md` are used naturally under pressure.",
        part4_heading_zh="第四部分：教材真实情景实战初练",
        part4_body_zh="""### 场景 4.1：单元真实沟通场景
> **情景设定**：`<说明对话双方背景与沟通目标>`

- **对方原话**：`"<对方的开场催促或提问>"`
- **你的第一反应回复（先不查答案直接写）**：
""",
        mock_zh="严格对照 `answer_key.zh-CN.md` 开展两轮以上闭卷压力对练，检验刚背下的地道表达能否自然说出口。",
    ),
}

SPOILER_MARKERS = (
    "Standard Answer Key Points",
    "Core Scoring Points",
    "Key Points (",
    "标准答案要点（",
)


def render_workbench(title: str, track: str, lang: str) -> str:
    """Render a spoiler-free 5-part workbench in English or Simplified Chinese."""
    spec = TRACK_SPECS[track]
    if lang == "zh-CN":
        return f"""# {title} — 练习本

> **所属类型**：`{spec.label}`  
> **伴学流程**：{spec.goal_zh}  
> **防剧透说明**：请先在下面自己写思路，练完并过关后再解锁 `answer_key.zh-CN.md` 中的标准答案用于背诵。

---

## 第一部分：重点导读与核心脉络

### 1.1 看资料抓重点
- **必考核心**：
  - `<核心原理、机制或高频表达>`
- **了解即可**：
  - `<辅助细节>`

### 1.2 宏观脉络图
```text
[前提输入] ---> [{title}] ---> [核心结果/影响]
```

---

## 第二部分：盲答自测题（先想思路 -> 反问补漏 -> 解锁背诵）

> 请在 `> **我的思路**：` 下写简短关键词，先别翻看标准答案文件。

### 主题 A：核心理解

#### Q1.1 `<从原资料提炼的核心问题>`（共 `3` 个要点）
- > **我的思路**：
- > **解锁标准答案（背诵版）**：*（先提交思路并答完教练追问后，由 AI 解锁写入）*

#### Q1.2 `<失效边界、权衡或易混点问题>`（共 `3` 个要点）
- > **我的思路**：
- > **解锁标准答案（背诵版）**：*（先提交思路并答完教练追问后，由 AI 解锁写入）*

---

## 第三部分：常见直觉陷阱表（避坑速查）

| 类别 | 直觉误区 | 真实场景怎么翻车 | 原书正确结论 |
|---|---|---|---|
| 基础误区 | `<常见错误猜测>` | `<真实失效表现>` | `<可靠底层规律>` |

---

## {spec.part4_heading_zh}

{spec.part4_body_zh.rstrip()}

---

## 第五部分：标准答案脱稿模拟与通关清单

- **第四步模拟实战指令**：{spec.mock_zh}
- [ ] 不看笔记，60 秒讲清第一部分的宏观主线。
- [ ] 完成第二部分全部盲答与反问，并背诵解锁后的黑体标准答案。
- [ ] 完成第四部分实战练习。
- [ ] 通过对照 `answer_key.zh-CN.md` 的闭卷脱稿模拟。
"""

    return f"""# {title} — Practice Workbench

> **Domain**: `{spec.label}`  
> **Workflow**: {spec.goal_en}  
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

## {spec.part4_heading_en}

{spec.part4_body_en.rstrip()}

---

## Part 5: Answer-Grounded Mock Simulation & Sign-Off

- **Mock Simulation Brief**: {spec.mock_en}
- [ ] Explained Part 1's big picture in 60 seconds without notes.
- [ ] Unlocked and memorized all Part 2 verified standard answers.
- [ ] Passed Part 4 applied drill.
- [ ] Passed closed-book Mock Simulation using `answer_key.md` as the live rubric.
"""


def render_answer_key(title: str, track: str, lang: str) -> str:
    """Render a separated answer_key matched by Q-IDs in English or Simplified Chinese."""
    if lang == "zh-CN":
        return f"""# {title} — 提炼标准答案与模拟评分卡（AI 专用）

> **所属类型**：`{track}`  
> 从资料中提炼出的标准答案，专供 AI 教练批改 `workbench.zh-CN.md` 并开展第 4 步脱稿模拟。请勿提前偷看。

---

### Q1.1 `<重复 Q1.1 题目>`
- **标准答案要点（`3` 个）**：
  1. **<关键词 1>**：`<精炼准确解释>`
  2. **<关键词 2>**：`<精炼准确解释>`
  3. **<关键词 3>**：`<精炼准确解释>`
- **漏点追问话术（绝不直接剧透）**：
  - *若漏掉第 1 点*：`"<把第 1 点藏进故障/生活反例里的追问>"`
  - *若漏掉第 2 点*：`"<针对第 2 点的边界追问>"`

### Q1.2 `<重复 Q1.2 题目>`
- **标准答案要点（`3` 个）**：
  1. **<关键词 1>**：`<精炼准确解释>`
  2. **<关键词 2>**：`<精炼准确解释>`
  3. **<关键词 3>**：`<精炼准确解释>`
- **漏点追问话术（绝不直接剧透）**：
  - *若漏掉第 1 点*：`"<追问反例>"`
"""

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


def validate_single_pair(wb_path: Path, ak_path: Path, is_zh: bool) -> list[str]:
    """Validate structure, spoiler lock, and Q-ID parity for one workbench/answer_key pair."""
    errors: list[str] = []
    if not wb_path.is_file():
        errors.append(f"Missing {wb_path.name} in {wb_path.parent}")
    if not ak_path.is_file():
        errors.append(f"Missing {ak_path.name} in {wb_path.parent}")
    if errors:
        return errors

    wb_text = wb_path.read_text(encoding="utf-8")
    ak_text = ak_path.read_text(encoding="utf-8")

    required_parts = (
        ("## 第一部分：", "## 第二部分：", "## 第三部分：", "## 第四部分：", "## 第五部分：")
        if is_zh
        else ("## Part 1:", "## Part 2:", "## Part 3:", "## Part 4:", "## Part 5:")
    )
    for part in required_parts:
        if part not in wb_text:
            errors.append(f"{wb_path.name} missing required section: {part}")

    for marker in SPOILER_MARKERS:
        if marker in wb_text:
            errors.append(f"Spoiler leak detected inside {wb_path.name}: {marker}")

    wb_qids = set(re.findall(r"^####\s+(Q\d+\.\d+)\b", wb_text, flags=re.MULTILINE))
    ak_qids = set(re.findall(r"^###\s+(Q\d+\.\d+)\b", ak_text, flags=re.MULTILINE))

    if not wb_qids:
        errors.append(f"No Q-IDs (e.g. '#### Q1.1 ...') found in {wb_path.name}")
    missing_in_ak = sorted(wb_qids - ak_qids)
    extra_in_ak = sorted(ak_qids - wb_qids)
    if missing_in_ak:
        errors.append(f"Q-IDs in {wb_path.name} missing from {ak_path.name}: {missing_in_ak}")
    if extra_in_ak:
        errors.append(f"Extra Q-IDs in {ak_path.name} missing from {wb_path.name}: {extra_in_ak}")

    return errors


def validate_directory(target_dir: Path) -> tuple[bool, list[str]]:
    """Validate English pair and, if present (or alone), Simplified Chinese pair in target_dir."""
    en_wb = target_dir / "workbench.md"
    en_ak = target_dir / "answer_key.md"
    zh_wb = target_dir / "workbench.zh-CN.md"
    zh_ak = target_dir / "answer_key.zh-CN.md"

    has_en = en_wb.exists() or en_ak.exists()
    has_zh = zh_wb.exists() or zh_ak.exists()

    if not has_en and not has_zh:
        return False, [f"No workbench files found in {target_dir}"]

    errors: list[str] = []
    if has_en:
        errors.extend(validate_single_pair(en_wb, en_ak, is_zh=False))
    if has_zh:
        errors.extend(validate_single_pair(zh_wb, zh_ak, is_zh=True))
    return len(errors) == 0, errors


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Internal scaffolder & spoiler-check validator for EN / ZH-CN workbenches."
    )
    parser.add_argument("--dir", required=True, help="Target study unit directory.")
    parser.add_argument("--title", default="New Study Material", help="Material or chapter title.")
    parser.add_argument(
        "--track",
        choices=sorted(TRACK_SPECS.keys()),
        default="textbook",
        help="Material domain: textbook | coding | interview | language.",
    )
    parser.add_argument(
        "--lang",
        choices=("en", "zh-CN"),
        default="en",
        help="Output language for scaffolding: en | zh-CN.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing files if present.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate existing workbench/answer_key pairs instead of creating files.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    args = parse_args(argv if argv is not None else sys.argv[1:])
    target_dir = Path(args.dir)

    if args.check:
        ok, errors = validate_directory(target_dir)
        if ok:
            print(f"OK: {target_dir} passed structure, spoiler-lock, and Q-ID checks.")
            return 0
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    target_dir.mkdir(parents=True, exist_ok=True)
    suffix = ".zh-CN.md" if args.lang == "zh-CN" else ".md"
    wb_path = target_dir / f"workbench{suffix}"
    ak_path = target_dir / f"answer_key{suffix}"

    if not args.force and (wb_path.exists() or ak_path.exists()):
        print(
            f"ERROR: {target_dir} already has {wb_path.name} or {ak_path.name}. Use --force to overwrite.",
            file=sys.stderr,
        )
        return 2

    wb_path.write_text(render_workbench(args.title, args.track, args.lang), encoding="utf-8")
    ak_path.write_text(render_answer_key(args.title, args.track, args.lang), encoding="utf-8")
    errors = validate_single_pair(wb_path, ak_path, is_zh=(args.lang == "zh-CN"))
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    print(f"Created [{args.track} | {args.lang}] pair in {target_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
