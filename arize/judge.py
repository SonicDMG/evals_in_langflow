"""
This script defines an LLM-as-judge evaluator for the Langflow agent.
"""
from typing import Any, Dict

from config import openai_client  # OpenAI client
from phoenix.experiments.evaluators import create_evaluator

@create_evaluator(kind="llm")
def helpfulness(input: Dict[str, Any], output: str, expected: Dict[str, Any]) -> float:
    """Evaluates if the model's response is helpful."""
    user_content = f"""
        You are grading the helpfulness of the following response on a scale of 1–5.
        Question:
        {input["question"]}
        Reference answer:
        {expected["answer"]}
        Predicted answer:
        {output}
        Respond with a single number from 1 (not helpful) to 5 (very helpful):
        Score:
    """
    response_score = openai_client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[
            {"role": "user", "content": user_content},
        ],
    ).choices[0].message.content.strip()
    try:
        return float(response_score)
    except ValueError:
        return 0.0

@create_evaluator(kind="code")
def concision(output: str, expected: Dict[str, Any]) -> float:
    """Check if the response is concise compared to the reference answer."""
    if not output or not expected or "answer" not in expected:
        return 0.0
    return float(len(output) < 2 * len(expected["answer"]))
