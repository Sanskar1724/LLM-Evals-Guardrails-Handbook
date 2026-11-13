# Guardrails: reading list

Every item here was checked when this handbook was written (November 2026): the page exists, and the title, authors and year match. Summaries are in our own words.

Suggested first five, in order: the OWASP Top 10 → Simon Willison's "lethal trifecta" post → *Not what you've signed up for* (Greshake et al.) → *Building Guardrails for Large Language Models* (Dong et al.) → *The Attacker Moves Second*.

## Start here: standards and practical guides

| Title | Author, year | What it shows and why it matters |
|---|---|---|
| [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/) | OWASP Gen AI Security Project, 2025 | The standard checklist of ten security risks for LLM apps. Each risk page has examples and fixes. |
| [LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) | OWASP Cheat Sheet Series | A short, practical list of defences against prompt injection. |
| [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | OWASP Gen AI Security Project, December 2025 | A separate list for systems where LLMs plan and act with tools. |
| [The lethal trifecta for AI agents](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) | Simon Willison, 2025 | Private data + untrusted content + a way to send data out = data theft. The most useful single rule for agent design. |
| [Prompt injection attacks against GPT-3](https://simonwillison.net/2022/Sep/12/prompt-injection/) | Simon Willison, 2022 | The blog post that gave prompt injection its name. Short and clear. |
| [The Dual LLM pattern for building AI assistants that can resist prompt injection](https://simonwillison.net/2023/Apr/25/dual-llm-pattern/) | Simon Willison, 2023 | A design where the LLM that reads untrusted text has no tools, and the LLM with tools never reads untrusted text. |
| [Prompt injection is not SQL injection (it may be worse)](https://www.ncsc.gov.uk/blog-post/prompt-injection-is-not-sql-injection) | UK National Cyber Security Centre | Explains why prompt injection has no simple technical fix and must be managed as a risk. |
| [Mitigate jailbreaks and prompt injections](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks) | Anthropic docs | Official advice: screen inputs, mark untrusted content, least privilege, chain several safeguards. |
| [Reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations) | Anthropic docs | Practical prompt techniques for fewer made-up answers. |
| [Building effective AI agents](https://www.anthropic.com/research/building-effective-agents) | Anthropic | Design patterns for agents. Simple designs are easier to guard. |
| [Patterns for Building LLM-based Systems & Products](https://eugeneyan.com/writing/llm-patterns/) | Eugene Yan, 2023 | Has a section on guardrails for output quality, next to evals, RAG and more. |
| [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) | NIST | A government framework listing risks of generative AI and actions to manage them. Broader than security. |
| [MITRE ATLAS](https://atlas.mitre.org/) | MITRE | A knowledge base of real attack techniques against AI systems. |

## Guardrails in general

| Title | Authors, year | What it shows and why it matters |
|---|---|---|
| [Building Guardrails for Large Language Models](https://arxiv.org/abs/2402.01822) | Dong, Mu, Jin et al., 2024 | An overview of what guardrails are, how current tools work, and what a careful design process needs. |
| [NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications with Programmable Rails](https://arxiv.org/abs/2310.10501) | Rebedea, Dinu, Sreedhar, Parisien, Cohen, 2023 | Describes programmable "rails" and the Colang language for controlling conversations. |
| [Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations](https://arxiv.org/abs/2312.06674) | Inan, Upasani, Chi et al., 2023 | An LLM trained to classify prompts and responses as safe or unsafe against a policy you can change. |
| [Constitutional Classifiers: Defending against Universal Jailbreaks across Thousands of Hours of Red Teaming](https://arxiv.org/abs/2501.18837) | Sharma, Tong, Mu et al., 2025 | Classifiers trained on synthetic data made from written rules. Held up in over 3,000 hours of red teaming, with a small rise in refusals and some extra compute cost. |

## Prompt injection

| Title | Authors, year | What it shows and why it matters |
|---|---|---|
| [Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173) | Greshake, Abdelnabi, Mishra et al., 2023 | Introduced indirect prompt injection: instructions hidden in data the app reads. Showed it against real products. |
| [Ignore Previous Prompt: Attack Techniques For Language Models](https://arxiv.org/abs/2211.09527) | Perez, Ribeiro, 2022 | An early study of two attacks: hijacking the model's goal and leaking its prompt. |
| [Defending Against Indirect Prompt Injection Attacks With Spotlighting](https://arxiv.org/abs/2403.14720) | Hines, Lopez, Hall et al., 2024 | Mark or transform untrusted text so the model can tell it from instructions. Cut attack success from over 50% to under 2% in their tests. |
| [StruQ: Defending Against Prompt Injection with Structured Queries](https://arxiv.org/abs/2402.06363) | Chen, Piet, Sitawarin, Wagner, 2024 | Separates the prompt and the data into two channels, and trains the model to follow instructions only from the prompt channel. |
| [The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions](https://arxiv.org/abs/2404.13208) | Wallace, Xiao, Leike et al., 2024 | Trains models to rank instructions: system prompt above user, user above third-party content. |
| [Design Patterns for Securing LLM Agents against Prompt Injections](https://arxiv.org/abs/2506.08837) | Beurer-Kellner, Buesser, Creţu et al., 2025 | Agent designs that limit what untrusted text can influence. Security from structure, not from detection. |
| [Defeating Prompt Injections by Design](https://arxiv.org/abs/2503.18813) | Debenedetti, Shumailov, Fan et al., 2025 | CaMeL: take the control flow from the trusted user request, so that retrieved data can never change which actions run. |
| [The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections](https://arxiv.org/abs/2510.09023) | Nasr, Carlini, Sitawarin et al., 2025 | Broke 12 published defences with attacks adapted to each one. Read this before you trust any filter. |

## Jailbreaks

| Title | Authors, year | What it shows and why it matters |
|---|---|---|
| [Jailbroken: How Does LLM Safety Training Fail?](https://arxiv.org/abs/2307.02483) | Wei, Haghtalab, Steinhardt, 2023 | Explains *why* jailbreaks work: the model's goals compete, and safety training does not cover everything the model can do. |
| ["Do Anything Now": Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models](https://arxiv.org/abs/2308.03825) | Shen, Chen, Backes, Shen, Zhang, 2023 | Collected and studied over a thousand real jailbreak prompts shared online. |
| [Universal and Transferable Adversarial Attacks on Aligned Language Models](https://arxiv.org/abs/2307.15043) | Zou, Wang, Carlini et al., 2023 | The GCG attack: a program finds a strange suffix that makes models comply, and it often works on other models too. |
| [Jailbreaking Black Box Large Language Models in Twenty Queries](https://arxiv.org/abs/2310.08419) | Chao, Robey, Dobriban et al., 2023 | PAIR: one LLM rewrites attacks against another until one works, often in few tries. |
| [Many-shot jailbreaking](https://www.anthropic.com/research/many-shot-jailbreaking) | Anthropic, 2024 | A very long prompt with many fake dialogues can override safety training. Works better with more examples. |
| [SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks](https://arxiv.org/abs/2310.03684) | Robey, Wong, Hassani, Pappas, 2023 | A defence: make several slightly changed copies of the prompt and combine the results, because machine-made attack strings break under small changes. |
| [Baseline Defenses for Adversarial Attacks Against Aligned Language Models](https://arxiv.org/abs/2309.00614) | Jain, Schwarzschild, Wen et al., 2023 | Tests simple defences: perplexity filters, paraphrasing the input, and adversarial training. |

## Content moderation

| Title | Authors, year | What it shows and why it matters |
|---|---|---|
| [A Holistic Approach to Undesired Content Detection in the Real World](https://arxiv.org/abs/2208.03274) | Markov, Zhang, Agarwal et al., 2022 | How a production moderation system is built: category design, labelling, and handling rare cases. |
| [ToxicChat: Unveiling Hidden Challenges of Toxicity Detection in Real-World User-AI Conversation](https://arxiv.org/abs/2310.17389) | Lin, Wang, Tong et al., 2023 | Real chatbot conversations are unlike social media. Older toxicity models do poorly on them. |
| [RealToxicityPrompts: Evaluating Neural Toxic Degeneration in Language Models](https://arxiv.org/abs/2009.11462) | Gehman, Gururangan, Sap, Choi, Smith, 2020 | Models can produce toxic text even from harmless-looking prompts. A reason for output moderation. |
| [ShieldGemma: Generative AI Content Moderation Based on Gemma](https://arxiv.org/abs/2407.21772) | Zeng, Liu, Mullins et al., 2024 | Open safety classifier models from Google for several harm types. |
| [WildGuard: Open One-Stop Moderation Tools for Safety Risks, Jailbreaks, and Refusals of LLMs](https://arxiv.org/abs/2406.18495) | Han, Rao, Ettinger et al., 2024 | One open model that detects harmful prompts, harmful responses, and whether the model refused. |

## Privacy

| Title | Authors, year | What it shows and why it matters |
|---|---|---|
| [Extracting Training Data from Large Language Models](https://arxiv.org/abs/2012.07805) | Carlini, Tramèr, Wallace et al., 2020 | Showed that language models memorise pieces of their training data and that attackers can pull them out, including personal details. |

## Hallucination and grounding

| Title | Authors, year | What it shows and why it matters |
|---|---|---|
| [Survey of Hallucination in Natural Language Generation](https://arxiv.org/abs/2202.03629) | Ji, Lee, Frieske et al., 2022 | Defines the terms (intrinsic, extrinsic) and reviews causes and fixes across tasks. |
| [SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models](https://arxiv.org/abs/2303.08896) | Manakul, Liusie, Gales, 2023 | Detects hallucination by sampling several answers and checking if they agree. No documents needed. |
| [FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation](https://arxiv.org/abs/2305.14251) | Min, Krishna, Lyu et al., 2023 | Split text into atomic facts and verify each against a source. |
| [Chain-of-Verification Reduces Hallucination in Large Language Models](https://arxiv.org/abs/2309.11495) | Dhuliawala, Komeili, Xu et al., 2023 | The model drafts, writes checking questions, answers them separately, then corrects its draft. |
| [MiniCheck: Efficient Fact-Checking of LLMs on Grounding Documents](https://arxiv.org/abs/2404.10774) | Tang, Laban, Durrett, 2024 | Small, cheap models can check claims against documents nearly as well as large LLMs. |
| [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) | Lewis, Perez, Piktus et al., 2020 | The RAG paper. Grounding answers in fetched documents is the main way to reduce hallucination. |

## Structured output

| Title | Authors, year | What it shows and why it matters |
|---|---|---|
| [Efficient Guided Generation for Large Language Models](https://arxiv.org/abs/2307.09702) | Willard, Louf, 2023 | How to force a model's output to match a pattern or grammar efficiently. The basis of the Outlines library. |

## Evaluating guardrails

| Title | Authors, year | What it shows and why it matters |
|---|---|---|
| [AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents](https://arxiv.org/abs/2406.13352) | Debenedetti, Zhang, Balunović et al., 2024 | Tests agents under injection attacks and reports both utility (task done?) and security (attack failed?). |
| [InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents](https://arxiv.org/abs/2403.02691) | Zhan, Liang, Ying, Kang, 2024 | A benchmark of indirect injection attacks against agents that use tools. |
| [Benchmarking and Defending Against Indirect Prompt Injection Attacks on Large Language Models](https://arxiv.org/abs/2312.14197) | Yi, Xie, Zhu et al., 2023 | BIPIA: a benchmark for indirect injection through external content, plus simple defences. |
| [JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models](https://arxiv.org/abs/2404.01318) | Chao, Debenedetti, Robey et al., 2024 | A standard, open way to compare jailbreak attacks and defences. |
| [HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal](https://arxiv.org/abs/2402.04249) | Mazeika, Phan, Yin et al., 2024 | A common framework for comparing red-teaming methods and model robustness. |
| [XSTest: A Test Suite for Identifying Exaggerated Safety Behaviours in Large Language Models](https://arxiv.org/abs/2308.01263) | Röttger, Kirk, Vidgen et al., 2023 | Safe prompts that look unsafe. Measures false alarms. |
| [OR-Bench: An Over-Refusal Benchmark for Large Language Models](https://arxiv.org/abs/2405.20947) | Cui, Chiang, Stoica, Hsieh, 2024 | A large benchmark for over-refusal. Shows that safer models often refuse more harmless requests. |
| [garak: A Framework for Security Probing Large Language Models](https://arxiv.org/abs/2406.11036) | Derczynski, Galinkin, Martin, Majumdar, Inie, 2024 | An open-source scanner that runs many known attack probes against a model. |
| [PyRIT: A Framework for Security Risk Identification and Red Teaming in Generative AI System](https://arxiv.org/abs/2410.02828) | Munoz, Minnich, Lutz et al., 2024 | Microsoft's open-source toolkit for red teaming generative AI. |

## Tools (documentation and code)

Frameworks:

- [NeMo Guardrails docs](https://docs.nvidia.com/nemo/guardrails/latest/index.html) · [code](https://github.com/NVIDIA-NeMo/Guardrails)
- [Guardrails AI](https://github.com/guardrails-ai/guardrails)
- [LLM Guard](https://github.com/protectai/llm-guard)
- [OpenAI Agents SDK: Guardrails](https://openai.github.io/openai-agents-python/guardrails/)

Detectors:

- [Purple Llama](https://github.com/meta-llama/PurpleLlama) (Llama Guard, Prompt Guard) · [Llama Guard 4 model card](https://www.llama.com/docs/model-cards-and-prompt-formats/llama-guard-4/) · [Prompt Guard 2](https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M)
- [ShieldGemma docs](https://ai.google.dev/gemma/docs/shieldgemma)
- [OpenAI Moderation guide](https://developers.openai.com/api/docs/guides/moderation)
- [Presidio](https://presidio.dataprivacystack.org/) · [code](https://github.com/data-privacy-stack/presidio)
- [Detoxify](https://github.com/unitaryai/detoxify)
- [Vectara hallucination leaderboard](https://github.com/vectara/hallucination-leaderboard)

Structured output:

- [Pydantic](https://docs.pydantic.dev/latest/) · [JSON Schema](https://json-schema.org/) · [Instructor](https://python.useinstructor.com/) · [Outlines](https://github.com/dottxt-ai/outlines) · [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs)

Red-team tools:

- [garak](https://github.com/NVIDIA/garak) · [PyRIT](https://github.com/Azure/PyRIT) · [promptfoo red teaming](https://www.promptfoo.dev/docs/red-team/)

Cloud services (paid, not used in this handbook):

- [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) · [Azure AI Content Safety](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview) · [Azure Prompt Shields](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection)

---
[Back to contents](../README.md)
