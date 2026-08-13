import api from "./api";

import {
  ChatRequest,
  ChatResponse,
} from "@/types/chat";


// =======================================================
// Normal Chat
// =======================================================

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


// =======================================================
// Streaming Chat
// =======================================================

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


  // Check HTTP response
  if (!response.ok) {
    throw new Error(
      `Streaming request failed: ${response.status}`
    );
  }


  // Check streaming body
  if (!response.body) {
    throw new Error(
      "No response body received from server."
    );
  }


  const reader =
    response.body.getReader();

  const decoder =
    new TextDecoder();


  try {

    while (true) {

      const {
        done,
        value,
      } = await reader.read();


      if (done) {
        break;
      }


      if (value) {

        const chunk =
          decoder.decode(
            value,
            {
              stream: true,
            }
          );

        onChunk(chunk);
      }
    }


    // Flush remaining decoder data
    const finalChunk =
      decoder.decode();

    if (finalChunk) {
      onChunk(finalChunk);
    }

  } finally {

    reader.releaseLock();

  }
}