// Windmill: Main TypeScript Function
// Path: /router/smart_router.ts
// Description: The central brain of the system. It takes a raw prompt,
// uses an LLM to classify its intent and extract parameters based on a YAML config,
// and returns a structured object to direct the next step in the workflow.

import { OpenAI } from "openai";
import yaml from "js-yaml";

// --- Type Definitions for strict output ---
interface EngineParams {
  [key: string]: any;
}

interface EngineRoute {
  engine: "image" | "video" | "caption" | "news_commentary" | "comment_reply" | "unknown";
  params: EngineParams;
  original_prompt: string;
}

// --- Main Function ---
export async function main(
  user_prompt: string,
  config_yaml_string: string, // The content of /config/model_routing.yaml
  openai_api_key: string // Injected as a secret
): Promise<EngineRoute> {
  console.log(`[Router] Received prompt: "${user_prompt}"`);

  // --- Step 1: Parse the YAML configuration ---
  let config: any;
  try {
    config = yaml.load(config_yaml_string);
    if (!config || !config.router || !config.router.system_prompt) {
      throw new Error("Invalid or missing router configuration in YAML.");
    }
  } catch (e) {
    console.error("[Router] Failed to parse YAML config:", e);
    return { engine: "unknown", params: {}, original_prompt: user_prompt };
  }
  
  const classification_model = config.router.classification_model || "gpt-4-turbo";
  const system_prompt = config.router.system_prompt;
  console.log(`[Router] Using model: ${classification_model}`);

  // --- Step 2: Call the classification model ---
  const openai = new OpenAI({ apiKey: openai_api_key });

  try {
    const response = await openai.chat.completions.create({
      model: classification_model,
      messages: [
        { role: "system", content: system_prompt },
        { role: "user", content: user_prompt },
      ],
      response_format: { type: "json_object" },
    });

    const messageContent = response.choices[0].message.content;
    if (!messageContent) {
        throw new Error("Received an empty response from the classification model.");
    }

    const result = JSON.parse(messageContent);
    console.log("[Router] Classification result:", result);

    // --- Step 3: Validate and format the output ---
    const { engine, params } = result;
    if (!engine || !params || typeof params !== 'object') {
        throw new Error("Invalid JSON structure from classification model.");
    }
    
    return {
      engine: engine,
      params: params,
      original_prompt: user_prompt
    };

  } catch (error) {
    console.error("[Router] Error during classification:", error);
    // On failure, return "unknown" to allow for manual intervention or a fallback path.
    return {
      engine: "unknown",
      params: {},
      original_prompt: user_prompt
    };
  }
}
