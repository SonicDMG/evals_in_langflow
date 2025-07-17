/**
 * This script creates or fetches an eval dataset using LangSmith for the Langflow agent.
 */
import { ls_client } from "./config.js";
import type { Dataset } from "langsmith";

// Dataset name and description as they appear in LangSmith
const DATASET_NAME = "langflow-agent-evals"
const DATASET_DESC = "QA checks for our Langflow agent"

// Define the examples ONCE
const examples = [
    {
        inputs: { question: "How do you define a function in Python?" },
        outputs: {
            answer: (
                "In Python, you define a function using the 'def' keyword " +
                "followed by the function name," +
                "parameters in parentheses, and a colon. The function body is indented below."
            )
        },
    },
    {
        inputs: { question: "What is the difference between a list and a tuple in Python?" },
        outputs: {
            answer: (
                "Lists are mutable (can be changed after creation) while tuples are immutable " +
                "(cannot be changed after creation)." +
                "Lists use square brackets [] and tuples use parentheses ()."
            )
        },
    },
    {
        inputs: { question: "What does the 'self' parameter in Python class methods represent?" },
        outputs: {
            answer: (
                "The 'self' parameter in Python class methods refers to the instance of the class." +
                "It allows access to the attributes and methods of the class."
            )
        },
    },
    {
        inputs: { question: "What is a lambda function in Python?" },
        outputs: {
            answer: (
                "A lambda function is an anonymous function defined using the 'lambda' keyword." +
                "It can take any number of arguments but can only have one expression."
            )
        },
    }
];

// Check if dataset exists, and if so, use it.
const datasets = ls_client.listDatasets();
for await (const d of datasets) {
    console.log("LangSmith datasets found: %s", d.name)
}
console.log("Has dataset? %s", await ls_client.hasDataset({datasetName: DATASET_NAME}))

// Programmatically create a dataset in LangSmith
let dataset: Dataset;

if (await ls_client.hasDataset({datasetName: DATASET_NAME})) {
    dataset = await ls_client.readDataset({datasetName: DATASET_NAME})
    // Check if dataset is empty
    const examples_list = await Array.fromAsync(ls_client.listExamples({datasetId: dataset.id}));
    console.log("Number of examples: %s", examples_list.length)
    if (examples_list.length === 0) {
        console.log("Dataset is empty, populating examples...")
        for (const ex of examples) {
            await ls_client.createExamples({inputs: [ex.inputs], outputs: [ex.outputs], datasetId: dataset.id})
        }
    } else {
        console.log("Dataset exists and is not empty. No action needed.")
    }
} else {
    console.log("Dataset does not exist. Creating and populating examples...")
    dataset = await ls_client.createDataset(DATASET_NAME, { 
        description: DATASET_DESC
    });
    for (const ex of examples) {
        await ls_client.createExamples({inputs: [ex.inputs], outputs: [ex.outputs], datasetId: dataset.id})
    }
}

export { dataset }