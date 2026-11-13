<div align="center">

# AI Study Workbench (`socratic-workbench`)

**Learn English, textbooks, coding, or interview topics with AI—without it spoiling the answer or faking your confidence.**

[English](README.md) | [简体中文](README.zh-CN.md) | [Skill Spec](skills/socratic-workbench/SKILL.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![npx skills compatible](https://img.shields.io/badge/npx%20skills-Compatible-6f42c1.svg)](skills/socratic-workbench/SKILL.md)
[![4 Learning Tracks](https://img.shields.io/badge/Tracks-English%20%7C%20Textbook%20%7C%20Coding%20%7C%20Interview-0ea5e9.svg)](#what-you-can-learn)

</div>

---

## Why This Exists

Normal AI chat feels helpful while you read it—and fails you when it counts:
- Ask AI to practice **spoken English**, and it prints a polished essay you couldn't speak in a real meeting.
- Ask AI to quiz a **textbook chapter** or **interview topic**, and it dumps hints or full bullet lists right under the question.
- Ask AI to help you **practice coding** when your syntax is rusty, and it writes 50 lines with silent edge-case fixes so you learn nothing.

**AI Study Workbench (`socratic-workbench`)** fixes that with one simple change:
1. Your practice sheet (`workbench.md`) contains **zero answers**. Rubrics stay hidden in `answer_key.md`.
2. Your AI acts like a sharp human sparring partner—**never lecturing you about its prompt rules**—refusing to spoil what you missed until you try first and handle a real follow-up twist.

---

## What You Actually Get

Install this once and you get:
- **Anti-Spoiler Study Sheets**: Every unit splits questions (`workbench.md`) from answers (`answer_key.md`).
- **4 Ready-to-Use Coaching Tracks**:
  - **English & Languages**: Realistic roleplay where AI pushes back in character, flags awkward wording, and upgrades your phrasing *after* you retry.
  - **Textbooks & Any Subject**: Big-picture maps, common misconception traps, and real-life thought experiments before memorizing formulas.
  - **Coding Without Syntax Friction**: Write what you want in **4 plain-language steps** (what to store, main steps, edge cases, return). AI translates literally—no silent bug-fixing—so real unit tests catch what you forgot.
  - **Exams & Interviews**: Questions only show point counts like `(3 points)`. AI scores your rough try (`2/3`), throws a failure scenario for the missing piece, and builds clean review notes once you solve it.
- **Works Everywhere**: `npx skills` / Antigravity / Claude Code / Codex, Cursor (`.mdc`), or copy-paste into ChatGPT / Gemini / Claude web UI.

---

## What Real Coaching Feels Like

### Example 1: Practicing Spoken English
> **You**: *"No, I can't finish this by Friday, I have too much work."*  
> **Normal AI**: *"Sure! Here are 10 polite ways to say that: 1. I'm afraid..."* *(Passive reading)*  
> **`socratic-workbench` Coach**: *"Your teammate hears 'I don't care about the launch.' Keep your goal, drop 'too much work', and offer Tuesday for the second half. Try saying it again."*

### Example 2: Coding When Syntax Is Rusty
> **You write in plain English**: *"Keep tokens per user. On each call, refill based on elapsed seconds, subtract cost, return allowed."*  
> **`socratic-workbench` Coach**: Compiles those exact words into code, runs unit tests, and replies:  
> *"Passed 4 / 6 tests. When a user sits idle for 2 hours, `tokens` hit `14,405` (expected max `5.0`). What rule is missing in Step 3?"*

---

## Quick Install (Takes 30 Seconds)

### Option 1: Install as an Agent Skill (`npx skills` / Antigravity / Claude Code / Codex)

```bash
# Install directly via npx skills once hosted on GitHub:
npx skills add <your-github-username>/ai-study-workbench

# Or install locally from a cloned folder:
npx skills add ./ai-study-workbench
```

Manual copy also works with `~/.agents/skills/` or `~/.claude/skills/`:

```bash
cp -r ai-study-workbench/skills/socratic-workbench ~/.agents/skills/
```

Then tell your agent:
> *"Use `socratic-workbench` to help me practice [spoken English / microeconomics Ch.4 / rate limiters / system design interviews] without spoiling answers."*

### Option 2: Cursor

Drop [`adapters/cursor/socratic-workbench.mdc`](adapters/cursor/socratic-workbench.mdc) into `.cursor/rules/`.

### Option 3: Web Chat (ChatGPT / Claude / Gemini — Zero Setup)

Copy and paste [`adapters/web-llm/system-prompt.en.md`](adapters/web-llm/system-prompt.en.md) (or the [Chinese version](adapters/web-llm/system-prompt.zh-CN.md)) into Custom Instructions, a Project, or a new chat.

---

## Browse Built-In Examples (`examples/`)

| Track | Sample Topic | Try It |
|---|---|---|
| **English** | Politely pushing back on a Friday deadline | [`workbench.md`](examples/01-english-workplace-sparring/workbench.md) · [`answer_key.md`](examples/01-english-workplace-sparring/answer_key.md) |
| **Textbook** | Supply, Demand & Rent Control Shortages | [`workbench.md`](examples/02-textbook-supply-demand/workbench.md) · [`answer_key.md`](examples/02-textbook-supply-demand/answer_key.md) |
| **Coding** | Token Bucket Rate Limiter (4-step logic -> tests) | [`workbench.md`](examples/03-coding-token-bucket/workbench.md) · [`test_exercise.py`](examples/03-coding-token-bucket/test_exercise.py) |
| **Interview** | Database MVCC & Write Skew | [`workbench.md`](examples/04-interview-mvcc/workbench.md) · [`answer_key.md`](examples/04-interview-mvcc/answer_key.md) |

---

## Optional CLI Tool: Generate & Check Blank Study Sheets

```bash
# Create a new blind practice unit (english | textbook | coding | interview)
python3 skills/socratic-workbench/scripts/init_workbench.py \
  --dir ./my-unit --title "Negotiating Salary" --track english

# Verify no answers leaked into workbench.md
python3 skills/socratic-workbench/scripts/init_workbench.py --dir ./my-unit --check
```

---

## FAQ

**Can AI still cheat or leak answers when I switch to a cheaper/Flash model?**  
Because `answer_key.md` is a separate file, `workbench.md` stays empty of hints, and [coach-behavior.md](skills/socratic-workbench/references/coach-behavior.md) blocks premature spoilers and filler praise, even fast lightweight models stay on track.

**Will the AI annoy me by repeating "Rule 1 says I cannot tell you..."?**  
No. The skill explicitly tells the AI to keep its instructions invisible and respond naturally like a real tutor, interviewer, or conversation partner.

**Is this only for programmers?**  
No. Half of the built-in tracks and examples are non-technical (**English conversation sparring** and **textbook understanding**), and the same anti-spoiler loop works for any subject.

---

Licensed under [MIT](LICENSE). Search & AI discovery metadata: [`llms.txt`](llms.txt).
