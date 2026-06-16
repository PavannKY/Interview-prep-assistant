"""
Question Generation Service
Generates personalized interview questions from parsed resume.
Optimised for small local models (phi3:mini, qwen2.5:1.5b, gemma2:2b).
"""
import uuid
from typing import List
from utils.llm_client import get_client, LLM_MODEL, extract_json
from models.schemas import ParsedResume, InterviewQuestion, DifficultyLevel


# Prompt is kept short and explicit — small models work better with tight prompts
QUESTION_PROMPT = """You are a technical interviewer. Generate {n} interview questions for this candidate.

Candidate skills: {skills}
Experience: {experience}
Projects: {projects}

Rules:
- Make questions specific to their actual skills and projects
- Mix: {easy} easy, {medium} medium, {hard} hard difficulty
- Include 2 behavioural questions
- Return ONLY a JSON array, nothing else

Format:
[
  {{"question": "...", "topic": "Python", "difficulty": "easy", "expected_concepts": ["concept1"]}},
  {{"question": "...", "topic": "System Design", "difficulty": "hard", "expected_concepts": ["concept1", "concept2"]}}
]

JSON array:"""


async def generate_questions(resume: ParsedResume, num_questions: int = 8) -> List[InterviewQuestion]:
    # Keep question count lower for small models (less tokens = faster + more reliable)
    num_questions = min(num_questions, 8)
    easy   = 2
    hard   = 2
    medium = num_questions - easy - hard

    exp = "; ".join(
        f"{e.get('title')} at {e.get('company')}" for e in resume.experience[:3]
    ) or "No experience listed"

    proj = "; ".join(
        f"{p.get('name')} ({', '.join(p.get('tech_stack', [])[:3])})"
        for p in resume.projects[:3]
    ) or "No projects listed"

    prompt = QUESTION_PROMPT.format(
        n=num_questions,
        skills=", ".join(resume.skills[:12]) or "General programming",
        experience=exp,
        projects=proj,
        easy=easy,
        medium=medium,
        hard=hard,
    )

    client = get_client()
    response = await client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1200,
    )

    raw = extract_json(response.choices[0].message.content)
    if isinstance(raw, dict):
        # Some models wrap in {"questions": [...]}
        raw = raw.get("questions", list(raw.values())[0])

    questions = []
    for item in raw[:num_questions]:
        try:
            questions.append(InterviewQuestion(
                id=str(uuid.uuid4()),
                question=item["question"],
                topic=item.get("topic", "General"),
                difficulty=DifficultyLevel(item.get("difficulty", "medium")),
                expected_concepts=item.get("expected_concepts", []),
            ))
        except Exception:
            continue

    return questions


async def generate_followup(original_question: str, candidate_answer: str) -> str:
    prompt = (
        f"Interviewer asked: {original_question}\n"
        f"Candidate answered: {candidate_answer}\n\n"
        f"Write ONE short follow-up question to probe deeper. Return only the question:"
    )
    client = get_client()
    response = await client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=80,
    )
    return response.choices[0].message.content.strip()
