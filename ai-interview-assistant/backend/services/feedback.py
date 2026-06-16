"""
Final Feedback Service
Aggregates evaluations → report, skill gaps, learning roadmap.
Optimised for small local models.
"""
from typing import List
from utils.llm_client import get_client, LLM_MODEL, extract_json
from models.schemas import ParsedResume, AnswerEvaluation, FinalFeedback, SkillGap


FEEDBACK_PROMPT = """You are a senior hiring manager. Write a final interview report. Return ONLY JSON.

Candidate skills: {skills}
Interview results (topic → score): {scores}
Overall score: {overall}/10

Return this exact JSON:
{{
  "performance_summary": "<3 sentence summary of overall performance>",
  "strongest_areas": ["<topic>", "<topic>"],
  "weakest_areas": ["<topic>", "<topic>"],
  "skill_gaps": [
    {{"skill": "<skill>", "current_level": "none|basic|intermediate", "required_level": "basic|intermediate|advanced", "resources": ["<free resource name>"]}}
  ],
  "resume_feedback": ["<specific resume improvement tip>"],
  "learning_roadmap": [
    {{"week": "Week 1-2", "focus": "<topic>", "resources": ["<resource>"]}}
  ],
  "interview_ready": true|false
}}

JSON:"""


async def generate_final_feedback(
    session_id: str,
    resume: ParsedResume,
    questions: list,
    evaluations: List[AnswerEvaluation],
) -> FinalFeedback:
    if not evaluations:
        raise ValueError("No evaluations to aggregate.")

    scores = [e.score for e in evaluations]
    overall = round(sum(scores) / len(scores), 1)

    score_summary = "; ".join(
        f"{q.topic}:{e.score}/10" for q, e in zip(questions, evaluations)
    )

    prompt = FEEDBACK_PROMPT.format(
        skills=", ".join(resume.skills[:10]) or "Not specified",
        scores=score_summary,
        overall=overall,
    )

    client = get_client()
    response = await client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1000,
    )

    data = extract_json(response.choices[0].message.content)

    skill_gaps = [
        SkillGap(
            skill=sg["skill"],
            current_level=sg.get("current_level", "none"),
            required_level=sg.get("required_level", "intermediate"),
            resources=sg.get("resources", []),
        )
        for sg in data.get("skill_gaps", [])
    ]

    return FinalFeedback(
        session_id=session_id,
        overall_score=overall,
        performance_summary=data.get("performance_summary", ""),
        strongest_areas=data.get("strongest_areas", []),
        weakest_areas=data.get("weakest_areas", []),
        skill_gaps=skill_gaps,
        resume_feedback=data.get("resume_feedback", []),
        learning_roadmap=data.get("learning_roadmap", []),
        interview_ready=data.get("interview_ready", False),
    )
