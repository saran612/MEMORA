"use server";

import { generateDynamicResponse } from "@/ai/flows/generate-dynamic-response";
import { z } from "zod";

const ResponseSchema = z.object({
  response: z.string(),
});

export async function getBotResponse(message: string): Promise<string> {
  try {
    const result = await generateDynamicResponse({ message });
    // The AI response might not be a simple string, so we need to validate it.
    const parsedResult = ResponseSchema.safeParse(result);
    if (!parsedResult.success) {
      console.error("AI response validation failed:", parsedResult.error);
      // Attempt to find a string in the response.
      if (typeof result === 'object' && result !== null && 'response' in result && typeof result.response === 'string') {
        return result.response;
      }
      return "I'm having trouble thinking right now. Please try again later.";
    }
    return parsedResult.data.response;
  } catch (error) {
    console.error("Error getting bot response:", error);
    return "Sorry, something went wrong on my end. Please try again.";
  }
}
