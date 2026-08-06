import api from "./api";
import { ChatRequest, ChatResponse } from "@/types/chat";

export async function askQuestion(
  question: string
): Promise<ChatResponse> {
  const payload: ChatRequest = {
    question,
  };

  const response = await api.post<ChatResponse>(
    "/chat",
    payload
  );

  return response.data;
}

/**
 * Stream an answer from the backend.
 */
export async function streamQuestion(
  question: string,
  onChunk: (chunk: string) => void
): Promise<void> {
  const response = await fetch(
    "http://127.0.0.1:8000/chat/stream",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question,
      }),
    }
  );

  if (!response.ok) {
    throw new Error("Streaming request failed.");
  }

  if (!response.body) {
    throw new Error("No response body.");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();

    if (done) {
      break;
    }

    const chunk = decoder.decode(value);

    onChunk(chunk);
  }
}