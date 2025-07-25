"""
This script defines an LLM-as-judge evaluator for the Langflow agent.
"""
from typing import Any, Dict
import openai
from config import openai_client
from phoenix.experiments.evaluators import (
    create_evaluator,
    #HelpfulnessEvaluator,
    ConcisenessEvaluator,
    CoherenceEvaluator
)
from phoenix.evals import OpenAIModel
openai_model = OpenAIModel(model="gpt-4.1-mini")

#helpfulness = HelpfulnessEvaluator(model=openai_model)
conciseness = ConcisenessEvaluator(model=openai_model)
coherence = CoherenceEvaluator(model=openai_model)

# the decorator can be used to set display properties
# `name` corresponds to the metric name shown in the UI
# `kind` indicates if the eval was made with a "CODE" or "LLM" evaluator
@create_evaluator(name="Shorter than reference?", kind="code")
def wordiness(output: str, reference: Dict[str, Any]) -> float:
    """Evaluates if the output is shorter than the reference text."""
    reference_length = len(reference["answer"].split())
    output_length = len(output.split())
    return float(output_length < reference_length)


@create_evaluator(kind="llm")
def helpfulness(input: Dict[str, Any], output: str, expected: Dict[str, Any]) -> float:
    """Evaluates if the model's response is helpful."""
    user_content = f"""
        You are grading the helpfulness of the following response on a scale of 0.0-1.0.
        Question:
        {input["question"]}
        Reference answer:
        {expected["answer"]}
        Predicted answer:
        {output}
        Respond with a single number from 0.0 (not helpful) to 1.0 (very helpful):
        Score:
    """
    try:
        response_score = openai_client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0,
            messages=[
                {"role": "user", "content": user_content},
            ],
        ).choices[0].message.content.strip()
        return float(response_score)
    except openai.APIConnectionError as e:
        print(f"Caught APIConnectionError: {e}")
        return 0.0
    except ValueError:
        return 0.0
