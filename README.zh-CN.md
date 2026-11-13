<div align="center">

# AI Study Workbench (`socratic-workbench`)

**把任何书本、课本、代码库或备考资料喂给 AI：先提炼标准答案、生成无剧透练习本带你盲练；练完解锁精炼答案去背诵；最后用这套标准答案直接做脱稿模拟实战。**

[English](README.md) | [简体中文](README.zh-CN.md) | [Skill 核心规范](skills/socratic-workbench/SKILL.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![npx skills 兼容](https://img.shields.io/badge/npx%20skills-即装即用-6f42c1.svg)](skills/socratic-workbench/SKILL.md)
[![资料驱动防剧透伴学](https://img.shields.io/badge/核心理念-资料驱动型防剧透伴学-0ea5e9.svg)](#怎么用四步资料驱动闭环)

</div>

---

## 这是什么？解决什么痛点？

平时直接把课本、专业书或代码丢给 AI 总结，看着顺畅无比，结果一关掉文档全忘光。**AI Study Workbench（`socratic-workbench`）** 是一套**资料驱动型防剧透伴学（Source-Driven Active Learning）**技能：
- **双文件防剧透锁（Dual-File Spoiler Lock）**：练习本 `workbench.md` 绝对不放答案；从你资料里抽出来的标准答案单独存进 `answer_key.md`。
- **盲练先导闭环（Blind-First Loop）**：先让你写出关键词或四格大白话逻辑再批改，不提前剧透，漏点只用反例/故障追问。
- **标准答案脱稿模拟（Answer-Grounded Mock）**：练完解锁精炼标准答案让你背完后，AI 直接拿着这批标准答案当“评分卡”，变身严格考官/面试官/现实对手做脱稿模拟。

**平时怎么上手？不用记命令行参数！** 装好 Skill 后，直接把你想学的**书本章节、PDF/笔记、代码仓库、考纲或外语教材**发进对话里，跟 AI 正常聊天就行。

---

## 怎么用？（四步资料驱动闭环）

1. **第一步：把真实资料喂给 AI，先抽出《标准答案库》(`answer_key.md`)**  
   你发来一章专业课本、一本商业好书、一段工程代码或考试大纲。AI 先吃透资料，把核心考点、常见直觉误区和精炼**标准答案**抽出来存进 `answer_key.md`（先不给你看）。
2. **第二步：在零剧透《练习本》(`workbench.md`) 里先盲练，漏点只反问**  
   AI 按你的学科自动切换措辞生成 `workbench.md`：每道题只留 `(共 N 个要点)` 和空白 `My Try:`；编程设计题只需你填“存什么、主步骤、边界怎么防、返回什么”四句大白话。你答完后，AI 只报命中数（比如 `命中 2 / 3`），针对漏掉的点甩一个现实反例或失败测试输入逼你自己补齐——**全程绝不把内部规则念出来破坏沉浸感**。
3. **第三步：练过关后解锁《标准答案》，直接拿去背诵**  
   等你把追问想通、或代码单测全绿后，AI 才把精炼成**黑体关键词的标准答案**（代码题附带 1~2 个高手好写法）解锁写入练习本，让你清晰对照、快速背牢。
4. **第四步：用这套标准答案做脱稿模拟实战（Mock Simulation）**  
   背完后对 AI 说一句“开始第四步模拟实战”。AI 立刻拿刚才的 `answer_key.md` 当唯一评判标准，扮演严格的专业课口试考官、技术面试官或实战对话对象对你连续追问，直到你不看笔记也能脱口而出。

---

## 学什么都能用（按你的资料自动换一套行话）

| 你喂给 AI 的资料 | 练习方式与陪练重点 | 最后的“解锁背诵 + 模拟实战” | 示例样板 |
|---|---|---|---|
| **课本 / 专业书 / 非虚构好书** | 抽核心机理、因果链与日常直觉误区；先用生活反例考你 | 解锁精炼核心论点去背诵 -> 模拟“抬杠评审/口试辩论” | [`01-textbook-supply-demand`](examples/01-textbook-supply-demand/workbench.md) |
| **代码库 / 系统架构 / 算法题** | 忘光语法也能练：**写 4 句大白话** -> AI 1:1 死板翻译（绝不偷改 Bug）-> 跑真实单测暴露漏洞 | 全绿后学习 1~2 个地道写法 -> 模拟“高并发/故障架构评审” | [`02-coding-token-bucket`](examples/02-coding-token-bucket/workbench.md) |
| **考证大纲 / 面试八股手册** | 按考点归类盲答（只写着 `共 N 个点`）+ 事故排查题 | 补齐漏洞后锁成黑体关键词记忆卡 -> 模拟“高压面试官连环追问” | [`03-interview-mvcc`](examples/03-interview-mvcc/workbench.md) |
| **外语教材 / 商务沟通资料** | 不先给地道例句，先把你扔进书中场景让你硬着头皮写/说 | 自己改通后解锁地道表达去背诵 -> 模拟“连续多轮外语实战对话” | [`04-language-workplace-pushback`](examples/04-language-workplace-pushback/workbench.md) |

---

## 真实互动效果长什么样？

### 场景 A：喂给 AI 一章《微观经济学》课本
> **你试着答 Q1.1（限价为什么反而更租不到房）**：*“房租便宜了，穷人就都租得起了。”*  
> **AI 教练**：*“命中了需求侧这 1 点（`1 / 3`）。换位想一下：如果你是开发商，政府规定房租砍掉 40%，你是继续盖出租房还是改盖写字楼？另外 1,000 个人抢 100 套便宜房时，房东怎么挑租客？”*  
> *(等你想通补齐 -> AI 解锁 3 条黑体关键词标准答案让你背 -> 背完模拟“市政听证会辩论”。)*

### 场景 B：忘光语法时用中文练代码设计（令牌桶限流）
> **你用大白话写四步**：*“按用户存剩多少令牌；每次请求按过去几秒补令牌，够扣就减掉返回允许。”*  
> **AI 教练**：1:1 老实翻译成代码跑测试，绝不替你补漏，直接返回：  
> *`通过 4 / 6 个测试。输入 now=9999.0 时剩余令牌算成了 19980.0（上限只能是 5.0）。你第三步“边界怎么防”要补哪条规则？`*  
> *(单测 100% 全绿后，解锁参考写法并模拟架构师压力追问。)*

---

## 30 秒装好，直接把资料发给 AI 开始练

### 方式 1：Antigravity / Claude Code / Codex（标准 Skill，`npx skills` 兼容）

```bash
# 推上 GitHub 后，任何人可直接一行安装：
npx skills add <你的GitHub用户名>/ai-study-workbench

# 本地克隆后也可直接安装：
npx skills add ./ai-study-workbench
```

也可以直接复制技能文件夹到全局目录：

```bash
cp -r ai-study-workbench/skills/socratic-workbench ~/.agents/skills/
```

装好后无需任何额外命令，直接对 AI 说：
> **“用 `socratic-workbench` 帮我学这份资料（课本/文档/代码库/考纲）：先抽标准答案、出防剧透练习本带我练，练完解锁标准答案给我背，最后用标准答案跟我脱稿模拟。”**

### 方式 2：Cursor 用户
把 [`adapters/cursor/socratic-workbench.mdc`](adapters/cursor/socratic-workbench.mdc) 放进项目的 `.cursor/rules/` 即可。

### 方式 3：只用 ChatGPT / Claude / Gemini 网页聊天？
把 [`adapters/web-llm/system-prompt.zh-CN.md`](adapters/web-llm/system-prompt.zh-CN.md) 复制到新对话开头（或放进 Custom Instructions / Gem），再贴入你的课本或资料就能直接进入四步伴学。

---

## 自带防剧透校验小工具（可选）

如果你改写了某个练习本，可以顺手跑一下内置脚本检查是否把答案误写进了 `workbench.md`：

```bash
python3 skills/socratic-workbench/scripts/init_workbench.py --dir examples/01-textbook-supply-demand --check
```

---

## 常见问题

**1. 题目和标准答案是 AI 瞎编的，还是严格基于我的书/资料？**  
严格基于你提供的资料。第一步会先把书本/代码/考纲里的核心原理和标准答案抽出来锁进 `answer_key.md`，后面的批改、背诵和第四步模拟考全部以它为准。

**2. 换用便宜的小模型（比如 Flash 模型）会直接泄题吗？**  
通过把答案物理隔离在 `answer_key.md`，加上 [`coach-behavior.md`](skills/socratic-workbench/references/coach-behavior.md) 里的硬性计数与禁夸赞约束，轻量模型也能稳稳执行先练后背、不提前剧透。

**3. 开源协议？**  
[MIT License](LICENSE)。大模型索引地图：[`llms.txt`](llms.txt)。
