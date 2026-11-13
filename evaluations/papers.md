# Evaluations: reading list

Every item here was checked when this handbook was written (November 2026): the page exists, and the title, authors and year match. Summaries are in our own words.

**How to read a paper as a student:** read the abstract, look at the figures and tables, read the introduction and conclusion. Read the middle only if you need the method.

Suggested first five, in order: Anthropic's agent-eval guide → Hamel Husain's two posts → the LLM-as-judge paper (Zheng et al.) → Ragas → *Adding Error Bars to Evals*.

## Start here: practical guides

| Title | Author, year | What it shows and why it matters |
|---|---|---|
| [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Anthropic, 2026 | Clear definitions (task, trial, grader, transcript, outcome), the three grader types, and a step-by-step plan for building evals. The best single starting point. |
| [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) | Hamel Husain, 2024 | A practical case study. Explains three levels: unit tests, human and model review, A/B tests. Pushes you to look at your data. |
| [Using LLM-as-a-Judge For Evaluation: A Complete Guide](https://hamel.dev/blog/posts/llm-judge/) | Hamel Husain, 2024 | How to build a judge and check it against a domain expert, using pass/fail labels with written critiques. |
| [Patterns for Building LLM-based Systems & Products](https://eugeneyan.com/writing/llm-patterns/) | Eugene Yan, 2023 | A long overview with sections on evals and on guardrails. Good for seeing how the pieces fit in a product. |
| [Evaluating the Effectiveness of LLM-Evaluators](https://eugeneyan.com/writing/llm-evaluators/) | Eugene Yan | A survey-style post about when LLM judges work and how to measure them. |
| [Challenges in evaluating AI systems](https://www.anthropic.com/research/evaluating-ai-systems) | Anthropic, 2023 | An honest list of what goes wrong in practice: prompt format changes scores, benchmarks are hard to run, human evals are costly. |
| [Define success criteria and build evaluations](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests) | Anthropic docs | Short official guide on writing success criteria and test cases. |

## Classic metrics

| Title | Authors, year | What it shows and why it matters |
|---|---|---|
| [BLEU: a Method for Automatic Evaluation of Machine Translation](https://aclanthology.org/P02-1040/) | Papineni, Roukos, Ward, Zhu, 2002 | Introduced BLEU: clipped n-gram precision with a brevity penalty. It made automatic evaluation of translation normal. |
| [ROUGE: A Package for Automatic Evaluation of Summaries](https://aclanthology.org/W04-1013/) | Lin, 2004 | Introduced ROUGE-N and ROUGE-L, recall-based overlap metrics that became the standard for summarisation. |
| [METEOR: An Automatic Metric for MT Evaluation with Improved Correlation with Human Judgments](https://aclanthology.org/W05-0909/) | Banerjee, Lavie, 2005 | An overlap metric that also matches word stems and synonyms. Shows an early attempt to fix BLEU's weak points. |
| [BERTScore: Evaluating Text Generation with BERT](https://arxiv.org/abs/1904.09675) | Zhang, Kishore, Wu, Weinberger, Artzi, 2019 | Compares texts by the similarity of their contextual embeddings, so different words with the same meaning can match. |
| [Speech and Language Processing](https://web.stanford.edu/~jurafsky/slp3/) | Jurafsky, Martin (free online textbook) | The standard textbook. The chapter on n-gram language models explains perplexity from the ground up. |

## LLM-as-judge

| Title | Authors, year | What it shows and why it matters |
|---|---|---|
| [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685) | Zheng, Chiang, Sheng et al., 2023 | Studies judge biases (position, verbosity, self-enhancement) and shows a strong judge can match human agreement levels of over 80%. The key paper on this topic. |
| [G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment](https://arxiv.org/abs/2303.16634) | Liu, Iter, Xu et al., 2023 | A judge method using chain-of-thought and form-filling. It agreed with humans better than BLEU and ROUGE on summarisation. |
| [Who Validates the Validators? Aligning LLM-Assisted Evaluation of LLM Outputs with Human Preferences](https://arxiv.org/abs/2404.12272) | Shankar, Zamfirescu-Pereira, Hartmann et al., 2024 | Shows that people change their grading criteria while grading ("criteria drift"). Judges need human checks. |
| [A Survey on LLM-as-a-Judge](https://arxiv.org/abs/2411.15594) | Gu, Jiang, Shi et al., 2024 | A broad survey on how to build reliable judge systems. |
| [From Generation to Judgment: Opportunities and Challenges of LLM-as-a-judge](https://arxiv.org/abs/2411.16594) | Li, Jiang, Huang et al., 2024 | Another survey, organised by what to judge, how to judge, and how to benchmark judges. |
| [LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods](https://arxiv.org/abs/2412.05579) | Li, Dong, Chen et al., 2024 | A third survey. Useful as a map of the research area. |
| [ChatEval: Towards Better LLM-based Evaluators through Multi-Agent Debate](https://arxiv.org/abs/2308.07201) | Chan et al., 2023 | Uses several LLM "referees" that discuss before grading. An example of multi-judge designs. |

## RAG evaluation

| Title | Authors, year | What it shows and why it matters |
|---|---|---|
| [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) | Lewis, Perez, Piktus et al., 2020 | The paper that named RAG: combine a retriever with a generator so answers come from fetched documents. |
| [Ragas: Automated Evaluation of Retrieval Augmented Generation](https://arxiv.org/abs/2309.15217) | Es, James, Espinosa-Anke, Schockaert, 2023 | Reference-free RAG metrics: faithfulness, answer relevance, context relevance. The basis of the Ragas library. |
| [ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems](https://arxiv.org/abs/2311.09476) | Saad-Falcon, Khattab, Potts, Zaharia, 2023 | Trains small judge models and corrects them with a few human labels, giving scores with confidence intervals. |
| [FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation](https://arxiv.org/abs/2305.14251) | Min, Krishna, Lyu et al., 2023 | Splits long text into atomic facts and checks each against a knowledge source. The "split into claims, verify each" idea used everywhere now. |
| [SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models](https://arxiv.org/abs/2303.08896) | Manakul, Liusie, Gales, 2023 | Detects hallucinations with no documents at all: sample several answers and see if they agree. |

## Agents

| Title | Authors, year | What it shows and why it matters |
|---|---|---|
| [SWE-bench: Can Language Models Resolve Real-World GitHub Issues?](https://arxiv.org/abs/2310.06770) | Jimenez, Yang, Wettig et al., 2023 | Tasks are real software issues, graded by real tests. A model of outcome-based grading. |
| [τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](https://arxiv.org/abs/2406.12045) | Yao, Shinn, Razavi, Narasimhan, 2024 | Agents talk to a simulated user and must follow policy. Introduces pass^k to measure reliability over repeated trials. |
| [WebArena: A Realistic Web Environment for Building Autonomous Agents](https://arxiv.org/abs/2307.13854) | Zhou, Xu, Zhu et al., 2023 | Realistic websites for agents to operate, with checks on functional correctness. |
| [GAIA: a benchmark for General AI Assistants](https://arxiv.org/abs/2311.12983) | Mialon, Fourrier, Swift et al., 2023 | Questions that are simple for people but need tools, browsing and reasoning for an AI. |
| [AgentBench: Evaluating LLMs as Agents](https://arxiv.org/abs/2308.03688) | Liu, Yu, Zhang et al., 2023 | Tests agents in eight different environments. |
| [Building effective AI agents](https://www.anthropic.com/research/building-effective-agents) | Anthropic | Design patterns for agents. Useful background before you evaluate one. |

## Benchmarks

| Title | Authors, year | What it shows and why it matters |
|---|---|---|
| [GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding](https://arxiv.org/abs/1804.07461) | Wang, Singh, Michael et al., 2018 | An early multi-task benchmark with a leaderboard. Shaped how the field compares models. |
| [SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems](https://arxiv.org/abs/1905.00537) | Wang, Pruksachatkun, Nangia et al., 2019 | The harder follow-up, made because GLUE was nearly solved. A clear example of saturation. |
| [Measuring Massive Multitask Language Understanding](https://arxiv.org/abs/2009.03300) | Hendrycks, Burns, Basart et al., 2020 | MMLU: multiple-choice questions over 57 subjects. Still widely quoted. |
| [Evaluating Large Language Models Trained on Code](https://arxiv.org/abs/2107.03374) | Chen, Tworek, Jun et al., 2021 | Introduced HumanEval: code is graded by running unit tests, not by text overlap. |
| [Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models](https://arxiv.org/abs/2206.04615) | Srivastava, Rastogi, Rao et al., 2022 | BIG-bench: over 200 tasks written by a very large group of authors. |
| [Holistic Evaluation of Language Models](https://arxiv.org/abs/2211.09110) | Liang, Bommasani, Lee et al., 2022 | HELM: measure many things (accuracy, calibration, robustness, fairness, bias, toxicity, efficiency), not accuracy alone. |
| [TruthfulQA: Measuring How Models Mimic Human Falsehoods](https://arxiv.org/abs/2109.07958) | Lin, Hilton, Evans, 2021 | 817 questions where many people believe a false answer. Tests if models repeat myths. |
| [Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference](https://arxiv.org/abs/2403.04132) | Chiang, Zheng, Sheng et al., 2024 | Ranks models from votes by real users comparing two anonymous models. |
| [LiveBench: A Challenging, Contamination-Limited LLM Benchmark](https://arxiv.org/abs/2406.19314) | White, Dooley, Roberts et al., 2024 | Refreshes its questions often so that models cannot have seen them in training. |
| [Dynabench: Rethinking Benchmarking in NLP](https://arxiv.org/abs/2104.14337) | Kiela, Bartolo, Nie et al., 2021 | People write examples that fool current models, so the benchmark keeps moving. |

## Limits of benchmarks and good method

| Title | Authors, year | What it shows and why it matters |
|---|---|---|
| [Time Travel in LLMs: Tracing Data Contamination in Large Language Models](https://arxiv.org/abs/2308.08493) | Golchin, Surdeanu, 2023 | A method to detect contamination: ask the model to complete benchmark items word for word. |
| [GSM-Symbolic: Understanding the Limitations of Mathematical Reasoning in Large Language Models](https://arxiv.org/abs/2410.05229) | Mirzadeh, Alizadeh, Shahrokhi et al., 2024 | Changing only numbers and names in maths problems lowers scores. A sign that benchmark scores overstate reasoning. |
| [Rethinking Benchmark and Contamination for Language Models with Rephrased Samples](https://arxiv.org/abs/2311.04850) | Yang, Chiang, Zheng et al., 2023 | Reworded or translated test data slips past simple filters and still inflates scores. |
| [Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations](https://arxiv.org/abs/2411.00640) | Miller, 2024 | Treats evals as experiments. Shows how to report confidence intervals and compare models properly. |
| [Lessons from the Trenches on Reproducible Evaluation of Language Models](https://arxiv.org/abs/2405.14782) | Biderman, Schoelkopf, Sutawika et al., 2024 | Why the same benchmark gives different numbers in different papers, and how to make results repeatable. |
| [Beyond Accuracy: Behavioral Testing of NLP Models with CheckList](https://arxiv.org/abs/2005.04118) | Ribeiro, Wu, Guestrin, Singh, 2020 | Brings software-testing ideas to NLP: minimum functionality, invariance and directional tests. |

## Safety evals

| Title | Authors, year | What it shows and why it matters |
|---|---|---|
| [HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal](https://arxiv.org/abs/2402.04249) | Mazeika, Phan, Yin et al., 2024 | A standard way to compare red-teaming methods and how well models refuse. |
| [JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models](https://arxiv.org/abs/2404.01318) | Chao, Debenedetti, Robey et al., 2024 | An open benchmark and leaderboard for jailbreak attacks and defences, with fixed scoring rules. |
| [XSTest: A Test Suite for Identifying Exaggerated Safety Behaviours in Large Language Models](https://arxiv.org/abs/2308.01263) | Röttger, Kirk, Vidgen et al., 2023 | Safe prompts that look unsafe. Measures over-refusal, the other side of safety. |
| [RealToxicityPrompts: Evaluating Neural Toxic Degeneration in Language Models](https://arxiv.org/abs/2009.11462) | Gehman, Gururangan, Sap, Choi, Smith, 2020 | Shows that harmless-looking sentence starts can lead models into toxic text. |

More safety and attack papers are in the [guardrails reading list](../guardrails/papers.md).

## Tools (documentation)

- [Inspect](https://inspect.aisi.org.uk/) · [code](https://github.com/UKGovernmentBEIS/inspect_ai)
- [promptfoo](https://www.promptfoo.dev/docs/intro/) · [code](https://github.com/promptfoo/promptfoo)
- [DeepEval](https://deepeval.com/docs/getting-started) · [code](https://github.com/confident-ai/deepeval)
- [Ragas](https://docs.ragas.io/en/stable/)
- [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)
- [HELM](https://crfm.stanford.edu/helm/)
- [OpenAI Evals (open source)](https://github.com/openai/evals)
- [Hugging Face Evaluate](https://github.com/huggingface/evaluate)
- [Langfuse](https://langfuse.com/docs)
- [SWE-bench leaderboards](https://www.swebench.com/)

---
[Back to contents](../README.md)
