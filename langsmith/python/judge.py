"""
This script defines an LLM-as-judge evaluator for the Langflow agent.
"""
from config import openai_client # OpenAI client

def helpfulness(inputs: dict, outputs: dict, reference_outputs: dict) -> float:
    """Check if the response is helpful compared to the reference answer."""
    # Extract question
    question = inputs.get("question")
    if question is None and "inputs" in inputs:
        question = inputs["inputs"].get("question")
    # Extract response
    response = outputs.get("response")
    if response is None and "output" in outputs:
        response = outputs.get("output")
    # Extract answer
    answer = reference_outputs.get("answer")
    if answer is None and "outputs" in reference_outputs:
        answer = reference_outputs["outputs"].get("answer")
    user_content = f"""
        You are grading the helpfulness of the following response on a scale of 1–5.
        Question:
        {question}
        Reference answer:
        {answer}
        Predicted answer:
        {response}
        Respond with a single number from 1 (not helpful) to 5 (very helpful):
        Score:
    """
    response_score = openai_client.chat.completions.create(
        model="gpt-4.1",
        temperature=0,
        messages=[
            {"role": "user", "content": user_content},
        ],
    ).choices[0].message.content.strip()
    try:
        return float(response_score)
    except ValueError:
        return 0.0


def concision(outputs: dict, reference_outputs: dict) -> bool:
    """Check if the response is concise compared to the reference answer."""
    # Extract response
    response = outputs.get("response")
    if response is None and "output" in outputs:
        response = outputs.get("output")
    # Extract answer
    answer = reference_outputs.get("answer")
    if answer is None and "outputs" in reference_outputs:
        answer = reference_outputs["outputs"].get("answer")
    if response is None or answer is None:
        return False
    return int(len(response) < 2 * len(answer))
