/**
 * This script defines an LLM-as-judge evaluator for the Langflow agent.
 */
import { openai_client } from "./config.js";
import type { Run, Example } from "langsmith";
import type { EvaluationResult } from "langsmith/evaluation";

/**
 * Check if the response is helpful compared to the reference answer.
 */
export async function helpfulness(
  run: Run,
  example?: Example,
): Promise<EvaluationResult> {
    const question = run.inputs.question ?? run.inputs.inputs?.question;
    const response = run.outputs?.response ?? run.outputs?.output;
    const answer = example?.outputs?.answer ?? example?.outputs?.outputs?.answer;

  const userContent = `
        You are grading the helpfulness of the following response on a scale of 1–5.
        Question:
        ${question}
        Reference answer:
        ${answer}
        Predicted answer:
        ${response}
        Respond with a single number from 1 (not helpful) to 5 (very helpful):
        Score:
    `;

  try {
    const completion = await openai_client.chat.completions.create({
      model: "gpt-4.1-mini",
      temperature: 0,
      messages: [{ role: "user", content: userContent }],
    });

    const responseScore = completion.choices[0].message.content?.trim();

    if (responseScore) {
      const score = parseFloat(responseScore);
      return {
        key: "helpfulness",
        score: isNaN(score) ? 0.0 : score,
        comment: `Helpfulness score: ${responseScore}`
      }
    }
    
    return {
        key: "helpfulness",
        score: 0.0,
        comment: "No score returned"
    };
  } catch (error) {
    console.error("Error getting helpfulness score:", error);
    return {
        key: "helpfulness",
        score: 0.0,
        comment: `Error getting helpfulness score: ${error}`
    };
  }
}

/**
 * Check if the response is concise compared to the reference answer.
 */
export function concision(
    run: Run,
    example?: Example,
): EvaluationResult {
    const response = run.outputs?.response ?? run.outputs?.output;
    const answer = example?.outputs?.answer ?? example?.outputs?.outputs?.answer;

  if (response == null || answer == null || typeof response !== 'string' || typeof answer !== 'string') {
    return {
        key: "concision",
        score: 0,
        comment: "Response or answer is not a string"
    }
  }

  const isConcise = response.length < 2 * answer.length;
  return {
    key: "concision",
    score: isConcise ? 1 : 0,
    comment: isConcise ? "Response is concise" : "Response is not concise"
  }
}

