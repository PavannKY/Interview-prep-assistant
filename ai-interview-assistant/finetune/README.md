# Fine-tuning Pipeline

## Overview

```
Step 1: Generate dataset   → generate_dataset.py   (~2-3 hrs)
Step 2: Inspect dataset    → inspect_dataset.py     (5 min)
Step 3: Fine-tune model    → finetune.py            (overnight)
Step 4: Use fine-tuned model in the app
```

## Step 1 — Generate Dataset

Make sure Ollama is running with phi3:mini, then:

```bash
cd finetune/scripts
pip install openai
python generate_dataset.py --questions 300 --evaluations 200
```

If it crashes mid-way, resume without losing progress:
```bash
python generate_dataset.py --questions 300 --evaluations 200 --resume
```

Output files:
- `finetune/data/questions.jsonl`   — 300 skill → question examples
- `finetune/data/evaluations.jsonl` — 200 question+answer → score examples

## Step 2 — Inspect Dataset

Review random samples before training:
```bash
python inspect_dataset.py
```

Check that:
- Questions are specific and relevant to the skills
- Scores make sense (strong answers = 7-10, weak = 0-4)
- No garbage / empty outputs

## Step 3 — Fine-tune (coming next)

We'll use **LoRA + PEFT** to fine-tune phi3:mini on your dataset.
Works on CPU, runs overnight (~6-8 hours for 500 examples).

## Dataset Format

### questions.jsonl
```json
{
  "instruction": "Generate an interview question for a candidate with these skills.",
  "input": "Skills: Python, FastAPI, PostgreSQL",
  "output": "How would you handle connection pooling in FastAPI with PostgreSQL?",
  "metadata": {"skills": ["Python", "FastAPI", "PostgreSQL"], "difficulty": "medium"}
}
```

### evaluations.jsonl
```json
{
  "instruction": "Evaluate this interview answer and return a JSON assessment.",
  "input": "Question: What is connection pooling?\nAnswer: It reuses database connections...",
  "output": "{\"score\": 7, \"feedback\": \"Good explanation...\", ...}",
  "metadata": {"topic": "PostgreSQL", "answer_quality": "medium"}
}
```
