"""
Answer Evaluation Service — LLM-as-Judge
Optimised for small local models (phi3:mini, qwen2.5, gemma2).
"""
from utils.llm_client import get_client, LLM_MODEL, extract_json
from models.schemas import AnswerEvaluation


EVAL_PROMPT = """You are a technical interviewer evaluating a candidate's answer. Return ONLY JSON.

Question: {question}
Key concepts expected: {concepts}
Candidate's answer: {answer}

Score the answer and return this exact JSON (no extra text):
{{
  "score": <0-10>,
  "feedback": "<2 sentence assessment>",
  "strengths": ["<strength>"],
  "improvements": ["<improvement needed>"],
  "concepts_covered": ["<concept they showed>"],
  "concepts_missing": ["<concept they missed>"]
}}

Scoring: 9-10=expert, 7-8=strong, 5-6=adequate, 3-4=weak, 0-2=very poor or no answer.

JSON:"""


async def evaluate_answer(
    question_id: str,
    question_text: str,
    answer: str,
    expected_concepts: list[str],
) -> AnswerEvaluation:
    if not answer or len(answer.strip()) < 5:
        return AnswerEvaluation(
            question_id=question_id,
            score=0,
            feedback="No answer was provided.",
            strengths=[],
            improvements=["Always attempt an answer — explain your thinking even if unsure."],
            concepts_covered=[],
            concepts_missing=expected_concepts,
        )

    prompt = EVAL_PROMPT.format(
        question=question_text,
        concepts=", ".join(expected_concepts) if expected_concepts else "general understanding",
        answer=answer[:1500],   # cap for small model context
    )

    client = get_client()
    response = await client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=600,
    )

    data = extract_json(response.choices[0].message.content)

    return AnswerEvaluation(
        question_id=question_id,
        score=max(0, min(10, int(data.get("score", 5)))),
        feedback=data.get("feedback", ""),
        strengths=data.get("strengths", []),
        improvements=data.get("improvements", []),
        concepts_covered=data.get("concepts_covered", []),
        concepts_missing=data.get("concepts_missing", []),
    )
