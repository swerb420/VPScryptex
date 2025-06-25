// Windmill: Main TypeScript Function
// Path: /inputs/manual_prompt_interface.ts
// Description: This script generates a simple HTML interface for manually
// submitting prompts to the AI content system. Windmill can serve this
// as a simple app.

import { express } from '@windmill-labs/wmill-types';

export async function main(app: express.Express) {
  // This serves a simple HTML page at the script's URL.
  app.get('/', (req, res) => {
    res.send(`
      <!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Content System | Manual Prompt</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <style>
          body { font-family: 'Inter', sans-serif; }
        </style>
      </head>
      <body class="bg-gray-100 text-gray-800 flex items-center justify-center h-screen">
        <div class="w-full max-w-2xl bg-white p-8 rounded-lg shadow-md">
          <h1 class="text-2xl font-bold mb-2">AI Content System</h1>
          <p class="mb-6 text-gray-600">Enter a prompt to start a generation task.</p>
          <form id="promptForm">
            <textarea
              id="prompt"
              class="w-full h-32 p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none"
              placeholder="e.g., 'Write a witty tweet about the future of AI' or 'Create a photorealistic image of a cat programming'"
            ></textarea>
            <button
              type="submit"
              id="submitBtn"
              class="mt-4 w-full bg-blue-600 text-white py-3 rounded-md font-semibold hover:bg-blue-700 transition-colors"
            >
              Start Generation
            </button>
          </form>
          <div id="result" class="mt-6 p-4 bg-gray-50 rounded-md border border-gray-200 hidden"></div>
        </div>
        <script>
          const form = document.getElementById('promptForm');
          const promptInput = document.getElementById('prompt');
          const resultDiv = document.getElementById('result');
          const submitBtn = document.getElementById('submitBtn');

          form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const prompt = promptInput.value;
            if (!prompt) return;

            submitBtn.disabled = true;
            submitBtn.textContent = 'Processing...';
            resultDiv.classList.add('hidden');
            
            // This would call the Windmill webhook for the 'webhook_trigger' script.
            // For demonstration, we simulate the call.
            // In a real setup, you'd fetch('/webhooks/u/your_user/webhook_trigger', ...)
            try {
                // Here you would call another Windmill script (the router) via its API.
                // This is a placeholder for that logic.
                console.log("Submitting prompt:", prompt);
                resultDiv.innerHTML = '<p class="text-green-700"><strong>Success!</strong> Workflow triggered with your prompt. Check the logs for progress.</p>';

            } catch (error) {
                resultDiv.innerHTML = '<p class="text-red-700"><strong>Error:</strong> Could not trigger workflow. ' + error.message + '</p>';
            } finally {
                resultDiv.classList.remove('hidden');
                submitBtn.disabled = false;
                submitBtn.textContent = 'Start Generation';
            }
          });
        </script>
      </body>
      </html>
    `);
  });
}
