<div align="center">

# AI Study Workbench (`socratic-workbench`)

**别再让 AI 一上来就把答案糊你脸上。装上这个防剧透陪练技能，用 AI 学英语、啃课本、练编程、刷面试，都能像有个严格的真人教练在旁边带你练。**

[English](README.md) | [简体中文](README.zh-CN.md) | [Skill 核心规范](skills/socratic-workbench/SKILL.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![npx skills 兼容](https://img.shields.io/badge/npx%20skills-即装即用-6f42c1.svg)](skills/socratic-workbench/SKILL.md)
[![四大陪练赛道](https://img.shields.io/badge/赛道-学英语%20%7C%20学课本%20%7C%20写代码%20%7C%20刷面试-0ea5e9.svg)](#四大陪练赛道看实际效果)

</div>

---

## 为什么平时用 AI 学习总是“一看就会，一用就废”？

- **学英语**：让 AI 出场景练口语，它直接吐出一整篇地道范文，你看完觉得“太高级了”，转头开口还是憋不出一句。
- **学课本/背面试题**：刚问一句“为什么会这样”，AI 把 1、2、3、4 点全列在眼前，你顺着点点头以为自己会了，上考场脑子一片空白。
- **练代码/系统设计**：语法早就忘光，让 AI 带着写几行，它顺手把所有边界漏洞都帮你补齐了，跑通了你却根本不知道哪里最容易出 Bug。

**AI Study Workbench（`socratic-workbench`）就干一件事**：把 AI 从“直接吐答案的作弊器”，变成**先让你试、不提前剧透、抓你漏洞反问你**的真人陪练教练——而且**绝不把提示词规则念出来打断你**，全程自然对话。

---

## 装完你能拿到什么？能学到什么？

1. **物理防剧透的双文件练习本**：
   - 你看的文件叫 `workbench.md`：里面**只有重点导读、常见直觉坑、和只写着 `(共 3 个要点)` 的盲答空格**，怎么滑都不会不小心偷看到答案。
   - 答案和评分触发器独立放在 `answer_key.md` 里，专门给 AI 教练悄悄对照批改。
2. **四大实战陪练赛道（不限专业，学啥都能用）**：
   - **赛道 1 · 学英语 / 外语实战陪练**：把你扔进真实对话（如跟客户砍需求、老外同事聊天），必须你先硬着头皮写出来/说出来；哪里硬邦邦的像中式英语，教练先反问你怎么改得更委婉，改对再给地道平替。
   - **赛道 2 · 学课本 / 专业课通透理解**：先看“这一章到底解决啥问题”和大白话误区表，再做不带提示的概念题，用生活里的反例帮你把底层原理想通。
   - **赛道 3 · 学写代码 / 系统设计（不用硬背语法）**：只需用中文填清楚四句话——**存什么、主步骤怎么走、边界怎么防、返回什么**。AI **1:1 老实翻译**成代码跑真实测试（绝不偷偷替你补边界 Bug），哪条测试挂了就拿那条失败数据反问你，全绿后再教 1~2 个高手简洁写法。
   - **赛道 4 · 刷面试 / 考证突击**：只报“命中 2 / 3 个点”，绝对不直接告诉你漏了哪条；紧接着甩一个“线上真出事故了怎么兜底”的场景追问你，逼你自己想出来后再帮你收成黑体记忆卡。
3. **换便宜/轻量模型（比如 Flash）也不偷懒**：配套防偷懒护栏，切小模型一样老老实实只批改不剧透。

---

## 四大陪练赛道：看实际对话效果

### 1. 学英语陪练：不说“给你十种地道说法”，而是直接对话挑刺
> **场景**：国外老板周三突然要加两个功能，周五早上就要演示。  
> **你先试着回**：*"No, I can't finish this by Friday. I have too much work."*  
> **普通 AI**：*"很好！这里有 5 种更礼貌的说法：1. Actually, I'm afraid..."*（看两眼就忘）  
> **本教练**：*"对方听完会觉得你在甩锅。目标先留着，把 'too much work' 换成具体要保的质量，再给一个下周二的分批方案，重写一遍试试？"*

### 2. 学代码（忘光语法也能练设计）：写中文四步，AI 当编译器 + 测试裁判
> **你写中文逻辑**：`按用户存剩多少令牌；每次请求按过去几秒补令牌，够扣就扣掉返回成功。`  
> **本教练**：1:1 翻译进练习文件并跑单测，直接回复：  
> *`当前通过 4 / 6 个测试。有个用户 2 小时没发请求，再来请求时算出来令牌暴涨到 14,405（上限只有 5）。你第三步“边界怎么防”要补哪条规则？`*  
> *(全部通过后，才会拿出标准写法点拨一句：用 `min(capacity, ...)` 就行。)*

---

## 30 秒快速安装

### 方式 A：通过 `npx skills` 一键安装（推荐，支持 Antigravity / Claude Code / Codex）

```bash
# 托管到 GitHub 后，所有人可直接运行：
npx skills add <你的GitHub用户名>/ai-study-workbench

# 如果已经克隆到本地，可直接本地安装：
npx skills add ./ai-study-workbench
```

也可以直接复制到你的全局 Skills 目录：

```bash
cp -r ai-study-workbench/skills/socratic-workbench ~/.agents/skills/
# 如用 Claude Code，可同步到 ~/.claude/skills/
```

装好后直接对 AI 说一句就行：
> **“用 `socratic-workbench` 帮我防剧透陪练：我要练习 [职场英语拒绝需求 / 经济学供需关系 / 限流器代码设计 / 数据库面试题]。”**

### 方式 B：Cursor 用户
把 [`adapters/cursor/socratic-workbench.mdc`](adapters/cursor/socratic-workbench.mdc) 放进项目的 `.cursor/rules/` 即可自动生效。

### 方式 C：网页端 ChatGPT / Claude / Gemini / DeepSeek 用户（零配置）
直接把 [`adapters/web-llm/system-prompt.zh-CN.md`](adapters/web-llm/system-prompt.zh-CN.md) 里的整段文字复制粘贴到新对话开头，或放进 Custom Instructions / Gem 里就能用。

---

## 仓库内置样板文件（一眼看清格式）

| 赛道 | 示例主题 | 直接点开看 |
|---|---|---|
| **英语陪练** | 职场英文：委婉拒绝不合理排期 | [`workbench.md`](examples/01-english-workplace-sparring/workbench.md) · [`answer_key.md`](examples/01-english-workplace-sparring/answer_key.md) |
| **学课本** | 经济学：房租限价为什么反而更租不到房？ | [`workbench.md`](examples/02-textbook-supply-demand/workbench.md) · [`answer_key.md`](examples/02-textbook-supply-demand/answer_key.md) |
| **学写代码** | 令牌桶限流器（写中文逻辑 -> 跑真实单测） | [`workbench.md`](examples/03-coding-token-bucket/workbench.md) · [`test_exercise.py`](examples/03-coding-token-bucket/test_exercise.py) |
| **刷面试** | 数据库 MVCC 与 Write Skew 写偏斜 | [`workbench.md`](examples/04-interview-mvcc/workbench.md) · [`answer_key.md`](examples/04-interview-mvcc/answer_key.md) |

---

## 附带命令行小工具：一键生成新课程盲答本

```bash
# 支持 4 种赛道：english | textbook | coding | interview
python3 skills/socratic-workbench/scripts/init_workbench.py \
  --dir ./my-study-unit \
  --title "商务英语谈判" \
  --track english

# 自动检查是否把答案写漏进了 workbench.md
python3 skills/socratic-workbench/scripts/init_workbench.py --dir ./my-study-unit --check
```

---

## 常见问题

**1. 为什么专门加了 `answer_key.md` 分离文件？**  
因为只要答案在同一个文件里（哪怕折叠了），你自己也会忍不住点开，AI 读上下文时也更容易顺嘴剧透。拆成两个文件，彻底断掉作弊和剧透的可能。

**2. AI 会不会老把“根据规则一我不能告诉你”这种提示词念出来？**  
不会。技能内部已经规定教练必须把规则藏在后台，全程用真人家教/面试官/外国同事的口吻自然跟你互动。

**3. 开源协议？**  
[MIT License](LICENSE)，欢迎 Star、Fork 或改造成你自己的学科练习库。
