---
name: canary-token-prompt-guard
description: Analyze and instrument poc-gmmc-agent prompt text with a canary token. Use when reviewing prompt cards, Java prompt builders, renderer logic, GigaChat/GigaChat Ultra prompts, few-shot examples, or canary-token placement rules.
priority: 20
---

# Canary Token Prompt Guard

Use this skill when adding, reviewing, or validating canary-token insertion in
`poc-gmmc-agent` prompts. It is especially relevant to PRs that touch
`docs/prompts/`, `docs/plans/*prompt*`, `src/main/java/**/llm/prompts/`, prompt
renderers, or prompt examples such as `ANSWER_GENERATOR_GIGACHAT_ULTRA@v1.0`.

## Contract

Definitions:

- Trigger symbols: `.`, `!`, `?`, and newline.
- Sentence: text between trigger symbols with length greater than 3 characters
  and more than 2 unique characters after trimming outer whitespace.
- Canary rendering: wrap the raw canary token in angle brackets as `<TOKEN>`.

Insertion rules:

1. Insert the wrapped canary token immediately after the first trigger symbol.
2. Then insert after every 5 sentences.
3. Also insert after every 10 trigger symbols, even if fewer than 5 sentences
   were seen.
4. Reset both trigger and sentence counters after every insertion.
5. Do not include a canary token in few-shot examples, request/response
   examples, JSON fixtures, schema examples, or evaluation matrices.

## Workflow

1. Inventory prompt-bearing files and separate runtime prompt text from examples.
   For PR #62, review:
   - `docs/prompts/answer-generation-gigachat-ultra.ru.md`
   - `docs/plans/2026-07-25-answer-generation-gigachat-ultra-prompt-artifact-design.md`
   - `docs/plans/2026-07-25-answer-generation-gigachat-ultra-prompt-artifact.md`
2. Identify actual prompt payloads: `SYSTEM`, `USER TEMPLATE`, `REPAIR TEMPLATE`,
   and Java renderer strings. Treat JSON request fixtures, few-shot examples,
   schemas, and eval matrices as forbidden zones for canary tokens.
3. Use `scripts/canary_prompt.py` on the exact prompt text or string literal body,
   not blindly on the whole Markdown file.
4. Re-check that forbidden zones contain no wrapped canary token.
5. For code changes, require focused tests around the renderer or prompt builder.

## Helper Script

Run from this skill directory or pass the script path explicitly.

Insert into a prompt text file:

```bash
python3 scripts/canary_prompt.py insert --token "$CANARY_TOKEN" prompt.txt > prompt.canary.txt
```

Check already instrumented prompt text:

```bash
python3 scripts/canary_prompt.py check --token "$CANARY_TOKEN" prompt.canary.txt
```

Run built-in deterministic checks:

```bash
python3 scripts/canary_prompt.py self-test
```

Pass the raw token without angle brackets. The script wraps it as `<TOKEN>` and
preserves an already wrapped value as-is.

## PR #62 Review Notes

- The production card has runtime sections named `### SYSTEM`,
  `### USER TEMPLATE`, and `### REPAIR TEMPLATE`.
- JSON request examples, schema blocks, fixture requests, and the adversarial
  evaluation matrix are examples/eval material. They must not contain the canary.
- If future Java integration adds canary insertion, place it after sanitization
  and prompt rendering of the target runtime payload, before the provider call.
- Do not insert canaries into `response_format`, JSON Schema, validation fixtures,
  rejected drafts used as examples, or few-shot demonstrations.

## Common Mistakes

| Mistake | Correction |
|---|---|
| Inserting into the whole Markdown prompt card | Extract the actual runtime prompt text first. |
| Counting every trigger as a sentence | A sentence must pass the length and unique-character thresholds. |
| Continuing counters after insertion | Reset both counters after every insertion. |
| Adding the token to few-shot examples | Keep examples and fixtures token-free. |
| Hardcoding the real token in docs or tests | Use placeholders in docs; pass the real token via environment/secret config. |

