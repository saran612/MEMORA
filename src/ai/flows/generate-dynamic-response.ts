'use server';

/**
 * @fileOverview This file defines a Genkit flow for generating dynamic chatbot responses.
 *
 * The flow uses an LLM to decide whether to incorporate additional data into its responses.
 *
 * - generateDynamicResponse -  A function that generates dynamic chatbot responses based on user input.
 * - DynamicResponseInput - The input type for the generateDynamicResponse function.
 * - DynamicResponseOutput - The output type for the generateDynamicResponse function.
 */

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

const DynamicResponseInputSchema = z.object({
  message: z.string().describe('The user message to respond to.'),
});
export type DynamicResponseInput = z.infer<typeof DynamicResponseInputSchema>;

const DynamicResponseOutputSchema = z.object({
  response: z.string().describe('The chatbot response.'),
});
export type DynamicResponseOutput = z.infer<typeof DynamicResponseOutputSchema>;

export async function generateDynamicResponse(input: DynamicResponseInput): Promise<DynamicResponseOutput> {
  return generateDynamicResponseFlow(input);
}

const shouldIncludeWeatherData = ai.defineTool({
  name: 'shouldIncludeWeatherData',
  description: 'Determines whether to include weather data in the response.',
  inputSchema: z.object({
    message: z.string().describe('The user message.'),
  }),
  outputSchema: z.boolean().describe('Whether to include weather data.'),
},
async (input) => {
  // In a real application, this would use an LLM or other logic to determine
  // whether to include weather data based on the user's message.
  // For this example, we just return true if the message contains the word "weather".
  return input.message.toLowerCase().includes('weather');
}
);

const getWeatherData = ai.defineTool({
    name: 'getWeatherData',
    description: 'Retrieves the current weather conditions.',
    inputSchema: z.object({
        location: z.string().describe('The location to get weather data for.'),
    }),
    outputSchema: z.string().describe('The current weather conditions.'),
},
async (input) => {
    // In a real application, this would call a weather API.
    // For this example, we just return a canned response.
    return `The current weather in ${input.location} is sunny with a temperature of 25 degrees Celsius.`
}
);

const dynamicResponsePrompt = ai.definePrompt({
  name: 'dynamicResponsePrompt',
  input: {schema: DynamicResponseInputSchema},
  output: {schema: DynamicResponseOutputSchema},
  tools: [shouldIncludeWeatherData, getWeatherData],
  prompt: `You are a helpful chatbot. Respond to the user message in a friendly and informative way.

  {% if shouldIncludeWeatherData(message=message) %}
  {{ getWeatherData(location='your location') }}
  {% endif %}

  User message: {{{message}}}

  Chatbot response:
  `,
  system: `You are a friendly and helpful chatbot.  You have access to tools that can provide additional information.
  Use the tools if the user's message indicates they would be useful.`
});

const generateDynamicResponseFlow = ai.defineFlow(
  {
    name: 'generateDynamicResponseFlow',
    inputSchema: DynamicResponseInputSchema,
    outputSchema: DynamicResponseOutputSchema,
  },
  async input => {
    const {output} = await dynamicResponsePrompt(input);
    return output!;
  }
);
