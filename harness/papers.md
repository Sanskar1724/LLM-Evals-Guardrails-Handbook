# Agent harness: reading list

Every item here was checked when this part was written (November 2026): the page exists, and the title, authors and year match. Summaries are in our own words.

Suggested first five, in order: *How to Build an Agent* (Thorsten Ball) → *Building effective AI agents* (Anthropic) → *Effective context engineering for AI agents* → *Writing effective tools for AI agents* → the ReAct paper.

## Start here: practical guides

| Title | Author, year | What it shows and why it matters |
|---|---|---|
| [How to Build an Agent](https://ampcode.com/how-to-build-an-agent) | Thorsten Ball, 2025 | Builds a working code-editing agent step by step in a few hundred lines. Shows that the core is a model, a loop and tools. |
| [Building effective AI agents](https://www.anthropic.com/research/building-effective-agents) | Anthropic | Separates workflows from agents, lists common patterns, and argues for the simplest design that works. |
| [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Anthropic, 2025 | Explains context as a limited resource and the main techniques: right-level prompts, just-in-time loading, compaction, notes, sub-agents. |
| [Writing effective tools for AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents) | Anthropic, 2025 | How to choose, name and describe tools, keep results small, and write helpful errors. |
| [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | Anthropic, 2025 | How to make an agent work across many context windows: a set-up session, a feature list, one feature per session, clean handovers, real testing. |
| [Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps) | Anthropic, 2026 | Planner, generator and evaluator roles; why a separate strict evaluator helps; and why harness parts should be removed as models improve. |
| [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) | Anthropic, 2025 | An orchestrator with parallel sub-agents. Gives honest numbers on the token cost and lessons on delegation. |
| [Don't Build Multi-Agents](https://cognition.ai/blog/dont-build-multi-agents) | Walden Yan (Cognition), 2025 | The opposing view: separate agents make conflicting hidden decisions. Share full context. |
| [Making Claude Code safer with sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing) | Anthropic, 2025 | Why file and network isolation are both needed, and how a sandbox reduces permission prompts. |
| [Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) | Anthropic, 2025 | With many tools, let the agent load definitions on demand and process data in code, to save context. |
| [Context Engineering for AI Agents: Lessons from Building Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) | Yichao "Peak" Ji, 2025 | Lessons from a production agent: stable prompt prefix for caching, files as memory, repeating the goal, keeping errors in context. |
| [12-factor agents](https://github.com/humanlayer/12-factor-agents) | HumanLayer | Twelve principles for building reliable LLM software. Own your prompts, context and control flow. |
| [I think "agent" may finally have a widely enough agreed upon definition...](https://simonwillison.net/2025/Sep/18/agents/) | Simon Willison, 2025 | Settles on a short definition: an agent runs tools in a loop to achieve a goal. |
| [Context engineering](https://simonwillison.net/2025/Jun/27/context-engineering/) | Simon Willison, 2025 | A short note on why the term "context engineering" is catching on. |
| [Context Engineering](https://blog.langchain.com/context-engineering-for-agents/) | LangChain | An overview that groups context techniques into writing, selecting, compressing and isolating context. |
| [Best practices for Claude Code](https://www.anthropic.com/engineering/claude-code-best-practices) | Anthropic | How to work well with a coding agent: give it checks, plan first, be specific, manage context. |
| [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Anthropic, 2026 | How to measure an agent. Needed to know whether a harness change helped. |

## The loop and reasoning

| Title | Authors, year | What it shows and why it matters |
|---|---|---|
| [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) | Yao, Zhao, Yu et al., 2022 | The thought, action, observation loop. The base pattern of nearly every agent. |
| [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903) | Wei, Wang, Schuurmans et al., 2022 | Writing out intermediate steps improves reasoning. The reason agents "think" before acting. |
| [Plan-and-Solve Prompting](https://arxiv.org/abs/2305.04091) | Wang, Xu, Lan et al., 2023 | Asking for a plan first, then solving, reduces missed steps. |
| [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601) | Yao, Yu, Zhao et al., 2023 | Explore several lines of reasoning, judge them, and go back when needed. |
| [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) | Shinn, Cassano, Berman et al., 2023 | After failing, the agent writes a lesson in words and uses it next time. Learning without retraining. |
| [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651) | Madaan, Tandon, Gupta et al., 2023 | A model improves its own output by giving itself feedback and trying again. |
| [Cognitive Architectures for Language Agents](https://arxiv.org/abs/2309.02427) | Sumers, Yao, Narasimhan, Griffiths, 2023 | A framework that organises agents by memory types, action space and decision process. A good map of the field. |

## Tools and interfaces

| Title | Authors, year | What it shows and why it matters |
|---|---|---|
| [MRKL Systems](https://arxiv.org/abs/2205.00445) | Karpas, Abend, Belinkov et al., 2022 | An early design that routes parts of a question to outside tools such as a calculator. |
| [Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761) | Schick, Dwivedi-Yu, Dessì et al., 2023 | A model learns when and how to call tools. |
| [SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering](https://arxiv.org/abs/2405.15793) | Yang, Jimenez, Wettig et al., 2024 | Designing commands and feedback for the model (the agent-computer interface) strongly raises success on real coding tasks. The key paper on why the harness matters. |
| [Executable Code Actions Elicit Better LLM Agents](https://arxiv.org/abs/2402.01030) | Wang, Chen, Yuan et al., 2024 | CodeAct: letting the agent act by writing Python can beat fixed JSON tool calls. |
| [OpenHands: An Open Platform for AI Software Developers as Generalist Agents](https://arxiv.org/abs/2407.16741) | Wang, Li, Song et al., 2024 | An open platform where agents write code, run commands and browse inside a sandbox. |

## Context and memory

| Title | Authors, year | What it shows and why it matters |
|---|---|---|
| [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) | Liu, Lin, Hewitt et al., 2023 | Models use the start and end of a long context best. Facts in the middle get missed. |
| [Context Rot: How Increasing Input Tokens Impacts LLM Performance](https://research.trychroma.com/context-rot) | Hong, Troynikov, Huber (Chroma), 2025 | Across 18 models, results get less reliable as input grows, even on simple tasks. |
| [MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560) | Packer, Wooders, Lin et al., 2023 | Treats context like computer memory: the model moves information between its window and outside storage. |
| [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442) | Park, O'Brien, Cai et al., 2023 | Simulated characters with a memory stream, retrieval and reflection. A well-known memory design. |
| [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291) | Wang, Xie, Jiang et al., 2023 | A Minecraft agent that saves working code as reusable skills. Memory as a growing skill library. |

## Multi-agent systems

| Title | Authors, year | What it shows and why it matters |
|---|---|---|
| [AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation](https://arxiv.org/abs/2308.08155) | Wu, Bansal, Zhang et al., 2023 | A framework for building apps from several agents that talk to each other. |
| [CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society](https://arxiv.org/abs/2303.17760) | Li, Hammoud, Itani et al., 2023 | Two agents in assigned roles cooperate on a task through conversation. |
| [MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework](https://arxiv.org/abs/2308.00352) | Hong, Zhuge, Chen et al., 2023 | Agents take roles from a software company and follow standard procedures. |

## Measuring agents and harnesses

| Title | Authors, year | What it shows and why it matters |
|---|---|---|
| [AI Agents That Matter](https://arxiv.org/abs/2407.01502) | Kapoor, Stroebl, Siegel et al., 2024 | Agent benchmarks often ignore cost. Simple agents can match complex ones once cost is counted. |
| [τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](https://arxiv.org/abs/2406.12045) | Yao, Shinn, Razavi, Narasimhan, 2024 | Introduces pass^k: does the agent succeed every time, not just once? |

More in the [evaluations reading list](../evaluations/papers.md).

## Documentation and code

- Tool calling: [Anthropic](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) · [OpenAI](https://developers.openai.com/api/docs/guides/function-calling) · [OpenRouter](https://openrouter.ai/docs/guides/features/tool-calling)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/docs/getting-started/intro)
- [Claude Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview) · [Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) · [Claude Code](https://github.com/anthropics/claude-code)
- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) · [LangGraph](https://github.com/langchain-ai/langgraph)
- [SWE-agent](https://github.com/SWE-agent/SWE-agent) · [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) · [OpenHands](https://github.com/All-Hands-AI/OpenHands)
- [AGENTS.md](https://agents.md/)

---
[Back to contents](../README.md)
