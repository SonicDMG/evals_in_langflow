/**
 * This script runs a Langflow agent flow
 * and evaluates its performance using LangSmith.
 */
import { randomUUID } from "crypto";
import { langflow_api_key } from "./config.js";
import { dataset } from "./dataset.js";
import { helpfulness, concision } from "./judge.js";
import { evaluate } from "langsmith/evaluation";
import { traceable } from "langsmith/traceable";

const AGENT_ID = "Agent-20ggR";
const ENDPOINT_NAME = "evals_in_langflow";

// A list of models to test. You can add more models here.
// The `provider` should match the provider name in Langflow.
// The `model_name` should match the model name for that provider.
// The `api_key` should match the global variable for that provider in Langflow.
const MODELS_TO_TEST = [
    {
        "provider": "OpenAI",
        "model_name": "gpt-4.1",
        "api_key": "openai__API_KEY"
    },
    {
        "provider": "OpenAI",
        "model_name": "gpt-4.1-mini",
        "api_key": "openai__API_KEY"
    },
    {
        "provider": "OpenAI",
        "model_name": "gpt-4.1-nano",
        "api_key": "openai__API_KEY"
    },
];

/**
 * Calls the Langflow API to run the agent.
 * This function is traced by LangSmith.
 */
const callLangflowApi = traceable(async (props: Record<string, any>, model: Record<string, string>) => {
    const url = `http://127.0.0.1:7860/api/v1/run/${ENDPOINT_NAME}`;
    
    const payload = {
        "output_type": "chat",
        "input_type": "chat",
        "input_value": props.question,
        "session_id": randomUUID(),
        "tweaks": {
            [AGENT_ID]: {
                "agent_llm": model.provider,
                "model_name": model.model_name,
                "api_key": model.api_key
            }
        }
    };

    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "x-api-key": langflow_api_key!
        },
        body: JSON.stringify(payload)
    };

    const response = await fetch(url, options);
    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Langflow API request failed with status ${response.status}: ${errorText}`);
    }

    const result = (await response.json()) as { outputs?: any[] };
    // Safely navigate the nested JSON to get the desired text output
    const outputText = result?.outputs?.[0]?.outputs?.[0]?.results?.message?.data?.text;
    
    if (typeof outputText !== 'string') {
        console.warn("Could not find expected text in Langflow response. Full response:", JSON.stringify(result, null, 2));
        return "";
    }

    return outputText;
}, { name: "Langflow Agent Run", run_type: "chain" });

/**
 * Creates a target function for LangSmith evaluation.
 * @param model The model configuration to use.
 * @returns An async function that LangSmith can evaluate.
 */
function createLsTarget(model: Record<string, string>) {
    return async (props: Record<string, any>) => {
        const responseText = await callLangflowApi(props, model);
        return { response: responseText };
    };
}


// ===========================
// Main Evaluation Loop
// ===========================
async function main() {
    console.log("Starting LangSmith Evals...");

    for (const model of MODELS_TO_TEST) {
        console.log(`Running evaluation for ${model.provider} - ${model.model_name}`);
        
        const target = createLsTarget(model);

        // The `evaluate` function automatically uses the default LangSmith client,
        // which is configured via environment variables (LANGSMITH_API_KEY, etc.).
        await evaluate(
            target,
            {
                data: dataset.name,
                evaluators: [helpfulness, concision],
                metadata: {
                    "llm.provider": model.provider,
                    "llm.model": model.model_name,
                },
                experimentPrefix: `${ENDPOINT_NAME}-${model.provider}-${model.model_name}`,
            }
        );
    }
}

main();
