"""
Dataset Inspector
Review generated examples before fine-tuning.
Usage: python inspect_dataset.py
"""
import json
import random
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


def load_jsonl(path):
    if not path.exists():
        return []
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def print_separator():
    print("\n" + "─" * 60 + "\n")


def inspect_questions(data, n=5):
    print(f"=== QUESTION DATASET ({len(data)} examples) ===")
    samples = random.sample(data, min(n, len(data)))
    for i, ex in enumerate(samples, 1):
        print(f"\n[Example {i}]")
        print(f"Input:  {ex['input']}")
        print(f"Output: {ex['output']}")
        meta = ex.get("metadata", {})
        print(f"Meta:   difficulty={meta.get('difficulty')} | type={meta.get('type')}")


def inspect_evaluations(data, n=5):
    print(f"\n=== EVALUATION DATASET ({len(data)} examples) ===")
    samples = random.sample(data, min(n, len(data)))
    for i, ex in enumerate(samples, 1):
        print(f"\n[Example {i}]")
        lines = ex['input'].split('\n')
        print(f"Q: {lines[0].replace('Question: ', '')}")
        print(f"A: {lines[1].replace('Answer: ', '')[:120]}...")
        try:
            out = json.loads(ex['output'])
            print(f"Score: {out.get('score')}/10")
            print(f"Feedback: {out.get('feedback', '')[:100]}")
        except Exception:
            print(f"Output: {ex['output'][:100]}")
        meta = ex.get("metadata", {})
        print(f"Meta: topic={meta.get('topic')} | quality={meta.get('answer_quality')}")


def stats(data, label):
    if not data:
        print(f"\n{label}: No data found.")
        return
    print(f"\n{label} Stats:")
    print(f"  Total examples: {len(data)}")

    # Metadata breakdown
    meta_keys = set()
    for ex in data:
        meta_keys.update(ex.get("metadata", {}).keys())

    for key in meta_keys:
        values = [ex["metadata"].get(key) for ex in data if key in ex.get("metadata", {})]
        counts = {}
        for v in values:
            counts[v] = counts.get(v, 0) + 1
        print(f"  {key}:")
        for v, c in sorted(counts.items(), key=lambda x: -x[1]):
            print(f"    {v}: {c}")


def main():
    q_data = load_jsonl(DATA_DIR / "questions.jsonl")
    e_data = load_jsonl(DATA_DIR / "evaluations.jsonl")

    if not q_data and not e_data:
        print("No data found. Run generate_dataset.py first.")
        return

    stats(q_data, "Question Dataset")
    stats(e_data, "Evaluation Dataset")

    print_separator()

    if q_data:
        inspect_questions(q_data)

    print_separator()

    if e_data:
        inspect_evaluations(e_data)

    print_separator()
    print("To regenerate with more examples:")
    print("  python generate_dataset.py --questions 300 --evaluations 200 --resume")


if __name__ == "__main__":
    main()
