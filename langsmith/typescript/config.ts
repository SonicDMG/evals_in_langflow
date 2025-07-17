/**
 * This file contains the configuration for the LangSmith Typescript client.
 */
import { Client as LSClient } from "langsmith";
import { wrapOpenAI } from "langsmith/wrappers";
import OpenAI from "openai";
import { config } from "dotenv";
import path from "path";
import { fileURLToPath } from "url";

// ESM doesn't have __dirname, so we have to build it
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load environment variables from .env file in the project root
config({ path: path.resolve(__dirname, "../../.env") });

// Get the API key from the environment variables
const langchain_api_key = process.env.LANGCHAIN_API_KEY;
const langchain_project = process.env.LANGCHAIN_PROJECT;
const openai_api_key = process.env.OPENAI_API_KEY;
const langflow_api_key = process.env.LANGFLOW_API_KEY;

// Initialize clients
const ls_client = new LSClient({
    apiKey: langchain_api_key
});
const openai_client = wrapOpenAI(new OpenAI({apiKey: openai_api_key}));

export { 
    langchain_api_key,
    langchain_project,
    openai_api_key,
    langflow_api_key,
    ls_client,
    openai_client
};