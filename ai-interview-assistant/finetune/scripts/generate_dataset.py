"""
Dataset Generator for Interview AI Fine-tuning
================================================
Generates two datasets:
  1. questions.jsonl  — skills → interview question
  2. evaluations.jsonl — question + answer → score + feedback

Usage:
  python generate_dataset.py --questions 300 --evaluations 200

Runtime: ~2-3 hours on CPU with phi3:mini
"""

import json
import time
import random
import argparse
import re
from pathlib import Path
from openai import OpenAI
from skill_bank import SKILL_COMBINATIONS

OUTPUT_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR.mkdir(exist_ok=True)

client = OpenAI(
    api_key="ollama",
    base_url="http://localhost:11434/v1",
)
MODEL = "phi3:mini"

def extract_json(text: str):
    """Extract JSON from model output — handles raw, markdown, and embedded."""
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass
    match = re.search(r"```(?:json)?\s*([\s\S]+?)```", text)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass
    for pattern in (r"(\{[\s\S]+\})", r"(\[[\s\S]+\])"):
        match = re.search(pattern, text)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                continue
    return None


def call_model(prompt: str, max_tokens: int = 300) -> str:
    """Call Ollama with retry on failure."""
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"  Retry {attempt + 1}/3 — {e}")
            time.sleep(2)
    return ""


def save_jsonl(data: list, path: Path):
    with open(path, "w") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")
    print(f"Saved {len(data)} examples → {path}")


def load_jsonl(path: Path) -> list:
    if not path.exists():
        return []
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


# ─── Question Generation Dataset ─────────────────────────────────────────────

QUESTION_PROMPT = """You are a senior technical interviewer.

A candidate has these skills: {skills}

Write ONE specific, high-quality interview question for this candidate.
The question should test real understanding, not just definitions.
Be specific — mention their actual skills in the question if relevant.

Return ONLY the question, nothing else. No numbering, no explanation."""

DIFFICULTY_LEVELS = ["easy", "medium", "hard"]
QUESTION_TYPES = [
    "conceptual understanding",
    "practical implementation",
    "debugging scenario",
    "system design",
    "tradeoffs and decisions",
    "behavioural / past experience",
]


def generate_question_example(skills: list) -> dict | None:
    """Generate one question training example for a skill set."""
    difficulty = random.choice(DIFFICULTY_LEVELS)
    q_type = random.choice(QUESTION_TYPES)
    skills_str = ", ".join(skills)

    prompt = QUESTION_PROMPT.format(skills=skills_str)

    # Add variety by hinting at type
    if random.random() > 0.5:
        prompt += f"\n\nFocus: {q_type} ({difficulty} difficulty)"

    question = call_model(prompt, max_tokens=150)
    if not question or len(question) < 20:
        return None

    # Clean up — remove leading numbers or quotes
    question = re.sub(r"^[\d\.\"\'\-\*]+\s*", "", question).strip()

    return {
        "instruction": "Generate an interview question for a candidate with these skills.",
        "input": f"Skills: {skills_str}",
        "output": question,
        "metadata": {
            "skills": skills,
            "difficulty": difficulty,
            "type": q_type,
        }
    }


# ─── Answer Evaluation Dataset ───────────────────────────────────────────────

# Pre-written Q&A pairs at different quality levels
# We give model a question + a sample answer and ask it to evaluate
SAMPLE_ANSWERS = {
    "strong": [
        "I've worked extensively with this in production. For example, in my last project I {action} which resulted in {outcome}. The key thing to understand is {concept}, and the tradeoff between {a} and {b} depends on {condition}.",
        "The way I approach this is by first {step1}, then {step2}. I learned this the hard way when {scenario} happened and we had to {solution}.",
        "There are several important aspects here. First, {point1}. Second, {point2}. In practice, you also need to consider {point3} because {reason}.",
    ],
    "medium": [
        "Yes, I know about this. It works by {basic_explanation}. I've used it in projects before.",
        "This is basically about {concept}. You need to make sure you {action} and then {followup}.",
        "I've used this a few times. The main thing is {point}. There are some edge cases but generally it works well.",
    ],
    "weak": [
        "I'm not entirely sure but I think it's about {vague_concept}. I've heard of it but haven't used it much.",
        "Yes I know this. It's when you do something with {vague_term} to make things work better.",
        "I used it once in a project but don't remember the details exactly.",
    ]
}

EVAL_PROMPT = """You are evaluating a candidate's interview answer. Return ONLY valid JSON.

Question: {question}
Candidate Answer: {answer}

Evaluate and return:
{{
  "score": <0-10>,
  "feedback": "<2 sentence assessment>",
  "strengths": ["<strength>"],
  "improvements": ["<what to improve>"],
  "concepts_covered": ["<concept shown>"],
  "concepts_missing": ["<concept missed>"]
}}

Scoring guide: 9-10=expert, 7-8=strong, 5-6=adequate, 3-4=weak, 0-2=very poor.
JSON:"""

# Sample questions per domain for evaluation dataset
SAMPLE_QUESTIONS = {
    "Python": [
        "Explain the difference between a list and a generator in Python and when you'd use each.",
        "How does Python's GIL affect multithreading? When would you use multiprocessing instead?",
        "What are Python decorators and how would you use them in a FastAPI application?",
    ],
    "React": [
        "Explain the difference between useEffect and useLayoutEffect.",
        "How would you optimize a React app that's re-rendering too frequently?",
        "What is the difference between controlled and uncontrolled components?",
    ],
    "Docker": [
        "What is the difference between an image and a container in Docker?",
        "How would you reduce the size of a Docker image in production?",
        "Explain multi-stage builds in Docker and why they're useful.",
    ],
    "Machine Learning": [
        "What is the difference between overfitting and underfitting? How do you fix each?",
        "Explain the bias-variance tradeoff in simple terms.",
        "When would you use Random Forest over XGBoost?",
    ],
    "PostgreSQL": [
        "What is the difference between an index and a primary key?",
        "Explain ACID properties in databases.",
        "When would you use a JOIN vs a subquery?",
    ],
    "Kubernetes": [
        "What is the difference between a Deployment and a StatefulSet?",
        "How does Kubernetes handle service discovery?",
        "Explain how horizontal pod autoscaling works.",
    ],
    "AWS": [
        "What is the difference between EC2 and Lambda?",
        "Explain how S3 versioning works and when you'd use it.",
        "What is the difference between an SQS queue and SNS topic?",
    ],
    "Transformers": [
        "Explain how the attention mechanism works in transformers.",
        "What is the difference between BERT and GPT architectures?",
        "What is LoRA and why is it useful for fine-tuning?",
    ],
    "FastAPI": [
        "What makes FastAPI faster than Flask for building APIs?",
        "How do you handle background tasks in FastAPI?",
        "Explain dependency injection in FastAPI.",
    ],
    "SQL": [
        "What is the difference between INNER JOIN and LEFT JOIN?",
        "Explain what a window function is and give an example.",
        "What is database normalization and why does it matter?",
    ],
}


def make_sample_answer(quality: str) -> str:
    """Generate a plausible-sounding answer at a given quality level."""
    templates = SAMPLE_ANSWERS[quality]
    template = random.choice(templates)
    # Fill in placeholders with generic terms
    fillers = {
        "{action}": random.choice(["implemented caching", "refactored the pipeline", "optimized the query", "redesigned the architecture"]),
        "{outcome}": random.choice(["50% faster response times", "reduced memory usage by 40%", "eliminated the bottleneck"]),
        "{concept}": random.choice(["the underlying data structure", "how the runtime handles this", "the core principle here"]),
        "{a}": random.choice(["performance", "simplicity", "scalability"]),
        "{b}": random.choice(["memory usage", "complexity", "maintainability"]),
        "{condition}": random.choice(["your use case", "the scale you're operating at", "your team's expertise"]),
        "{step1}": random.choice(["understanding the requirements", "profiling the bottleneck", "reading the documentation"]),
        "{step2}": random.choice(["writing tests", "benchmarking", "reviewing with the team"]),
        "{scenario}": random.choice(["a production incident", "a performance regression", "a scaling issue"]),
        "{solution}": random.choice(["rollback and hotfix", "scale horizontally", "optimize the hot path"]),
        "{point1}": random.choice(["performance characteristics", "memory implications", "thread safety"]),
        "{point2}": random.choice(["error handling", "scalability", "maintainability"]),
        "{point3}": random.choice(["edge cases", "monitoring", "documentation"]),
        "{reason}": random.choice(["it affects production reliability", "it becomes critical at scale", "teams often overlook this"]),
        "{basic_explanation}": random.choice(["processing requests asynchronously", "storing data in memory", "managing connections"]),
        "{followup}": random.choice(["handle the errors", "monitor the results", "test thoroughly"]),
        "{point}": random.choice(["to configure it correctly", "to understand the defaults", "to test it properly"]),
        "{vague_concept}": random.choice(["handling data differently", "some kind of optimization", "a design pattern"]),
        "{vague_term}": random.choice(["the system", "the data", "the configuration"]),
    }
    for k, v in fillers.items():
        template = template.replace(k, v)
    return template


def generate_evaluation_example() -> dict | None:
    """Generate one evaluation training example."""
    topic = random.choice(list(SAMPLE_QUESTIONS.keys()))
    question = random.choice(SAMPLE_QUESTIONS[topic])
    quality = random.choice(["strong", "strong", "medium", "medium", "weak"])  # weighted
    answer = make_sample_answer(quality)

    prompt = EVAL_PROMPT.format(question=question, answer=answer)
    raw = call_model(prompt, max_tokens=400)
    if not raw:
        return None

    evaluation = extract_json(raw)
    if not evaluation or "score" not in evaluation:
        return None

    return {
        "instruction": "Evaluate this interview answer and return a JSON assessment.",
        "input": f"Question: {question}\nAnswer: {answer}",
        "output": json.dumps(evaluation),
        "metadata": {
            "topic": topic,
            "answer_quality": quality,
        }
    }


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", type=int, default=300, help="Number of question examples")
    parser.add_argument("--evaluations", type=int, default=200, help="Number of evaluation examples")
    parser.add_argument("--resume", action="store_true", help="Resume from existing progress")
    args = parser.parse_args()

    q_path = OUTPUT_DIR / "questions.jsonl"
    e_path = OUTPUT_DIR / "evaluations.jsonl"

    # ── Question Generation Dataset ──────────────────────────────────────────
    existing_q = load_jsonl(q_path) if args.resume else []
    needed_q = args.questions - len(existing_q)

    if needed_q > 0:
        print(f"\n=== Generating {needed_q} question examples ===")
        print(f"(Already have {len(existing_q)}, target: {args.questions})\n")

        # Expand skill combinations by shuffling and repeating
        skill_pool = SKILL_COMBINATIONS * (needed_q // len(SKILL_COMBINATIONS) + 2)
        random.shuffle(skill_pool)

        q_dataset = existing_q.copy()
        failed = 0

        for i, skills in enumerate(skill_pool[:needed_q + 20]):
            if len(q_dataset) - len(existing_q) >= needed_q:
                break

            example = generate_question_example(skills)
            if example:
                q_dataset.append(example)
                count = len(q_dataset) - len(existing_q)
                print(f"  [{count}/{needed_q}] Skills: {', '.join(skills[:3])}...")
                print(f"         Q: {example['output'][:80]}...")
            else:
                failed += 1

            # Save checkpoint every 25
            if (i + 1) % 25 == 0:
                save_jsonl(q_dataset, q_path)
                print(f"  ── Checkpoint saved ({len(q_dataset)} total) ──")

            time.sleep(0.3)  # small pause to not overwhelm CPU

        save_jsonl(q_dataset, q_path)
        print(f"\nQuestion dataset complete. Failed: {failed}")
    else:
        print(f"Question dataset already has {len(existing_q)} examples — skipping.")

    # ── Evaluation Dataset ───────────────────────────────────────────────────
    existing_e = load_jsonl(e_path) if args.resume else []
    needed_e = args.evaluations - len(existing_e)

    if needed_e > 0:
        print(f"\n=== Generating {needed_e} evaluation examples ===\n")

        e_dataset = existing_e.copy()
        failed = 0

        for i in range(needed_e + 20):
            if len(e_dataset) - len(existing_e) >= needed_e:
                break

            example = generate_evaluation_example()
            if example:
                e_dataset.append(example)
                count = len(e_dataset) - len(existing_e)
                data = json.loads(example["output"])
                print(f"  [{count}/{needed_e}] Topic: {example['metadata']['topic']} | Score: {data.get('score')}/10")
            else:
                failed += 1

            # Save checkpoint every 25
            if (i + 1) % 25 == 0:
                save_jsonl(e_dataset, e_path)
                print(f"  ── Checkpoint saved ({len(e_dataset)} total) ──")

            time.sleep(0.3)

        save_jsonl(e_dataset, e_path)
        print(f"\nEvaluation dataset complete. Failed: {failed}")
    else:
        print(f"Evaluation dataset already has {len(existing_e)} examples — skipping.")

    # ── Summary ──────────────────────────────────────────────────────────────
    print("\n=== Dataset Generation Complete ===")
    print(f"  Questions:   {OUTPUT_DIR / 'questions.jsonl'}")
    print(f"  Evaluations: {OUTPUT_DIR / 'evaluations.jsonl'}")
    print("\nNext step: run  python finetune.py")


if __name__ == "__main__":
    main()
