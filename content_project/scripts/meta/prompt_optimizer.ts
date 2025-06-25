// Windmill: Main TypeScript Function
// Path: /meta/prompt_optimizer.ts
// Description: The "AI Switcher." Takes a single prompt, runs it against
// multiple LLMs, and uses a "judge" LLM to score the outputs and find the best one.

import { OpenAI } from "openai";
import { Anthropic } from "@anthropic-ai/sdk";
// Assume a Google Gemini SDK would be available as well.

interface ModelResponse {
  model: string;
  response: string;
}

interface Evaluation {
  scores: { [key: string]: number };
  winning_model: string;
  winning_response: string;
}

// --- Main Function ---
export async function main(
  base_prompt: string,
  models_to_test: string[], // e.g., ["gpt-4-turbo", "claude-3-opus-20240229"]
  evaluation_criteria: string = "Evaluate for clarity, creativity, and adherence to the prompt.",
  judge_model: string = "gpt-4-turbo",
  openai_api_key: string,   // Secret
  anthropic_api_key: string // Secret
): Promise<Evaluation> {
  console.log(`[Optimizer] Starting optimization for prompt: "${base_prompt}"`);

  // --- Step 1: Generate responses from all configured models ---
  const responsePromises = models_to_test.map(model => 
    getLLMResponse(model, base_prompt, openai_api_key, anthropic_api_key)
  );
  const responses = await Promise.all(responsePromises);
  console.log("[Optimizer] Generated responses from all models.");

  // --- Step 2: Prepare the evaluation prompt for the judge model ---
  let evaluationPrompt = `You are an expert AI evaluator. Your task is to analyze responses from several AI models for a given prompt and select the best one based on specific criteria.

**Original Prompt:**
"${base_prompt}"

**Evaluation Criteria:**
"${evaluation_criteria}"

**AI Model Responses:**
`;
  responses.forEach((res, index) => {
    evaluationPrompt += `
---
Response from Model #${index + 1} (${res.model}):
\`\`\`
${res.response}
\`\`\`
`;
  });

  evaluationPrompt += `
---
**Your Task:**
1.  Carefully review each response.
2.  For each response, provide a score from 1-100 based on the evaluation criteria.
3.  Identify the winning model.
4.  Provide the winning response.

Please format your output as a single, valid JSON object with the following keys: "scores", "winning_model", "winning_response".
The "scores" key should be an object where keys are the model names and values are the integer scores.
`;

  // --- Step 3: Use the judge model to score the responses ---
  const openai = new OpenAI({ apiKey: openai_api_key });
  console.log("[Optimizer] Asking judge model to score responses...");

  const evaluationResult = await openai.chat.completions.create({
    model: judge_model,
    messages: [{ role: "user", content: evaluationPrompt }],
    response_format: { type: "json_object" },
  });
  
  const final_evaluation = JSON.parse(evaluationResult.choices[0].message.content || "{}") as Evaluation;
  console.log("[Optimizer] Evaluation complete:", final_evaluation);

  return final_evaluation;
}

// --- Helper function to call different LLM providers ---
async function getLLMResponse(
  modelName: string,
  prompt: string,
  oaiKey: string,
  anthKey: string
): Promise<ModelResponse> {
  try {
    if (modelName.startsWith("gpt")) {
      const openai = new OpenAI({ apiKey: oaiKey });
      const completion = await openai.chat.completions.create({
        model: modelName,
        messages: [{ role: "user", content: prompt }],
      });
      return { model: modelName, response: completion.choices[0].message.content || "" };
    } else if (modelName.startsWith("claude")) {
      const anthropic = new Anthropic({ apiKey: anthKey });
      const msg = await anthropic.messages.create({
        model: modelName,
        max_tokens: 2048,
        messages: [{ role: "user", content: prompt }],
      });
      return { model: modelName, response: msg.content[0].text };
    } 
    // Add other providers like Google Gemini here
    else {
      return { model: modelName, response: `Model provider for ${modelName} not implemented.` };
    }
  } catch (error) {
    console.error(`[Optimizer] Error fetching response from ${modelName}:`, error);
    return { model: modelName, response: "Error fetching response." };
  }
}
