import api from "./api";

import {
  ChatRequest,
  ChatResponse,
} from "@/types/chat";

// =======================================================
// SSE Event Types
// =======================================================

interface StreamTokenEvent {
  type: "token";
  text: string;
}

interface StreamDoneEvent {
  type: "done";
  sources: ChatResponse["sources"];
  conversation_id?: number;
}

interface StreamErrorEvent {
  type: "error";
  message?: string;
}

type StreamEvent =
  | StreamTokenEvent
  | StreamDoneEvent
  | StreamErrorEvent;


// =======================================================
// Normal Chat
// =======================================================

export async function askQuestion(
  question: string,
  conversationId?: number
): Promise<ChatResponse> {

  const payload: ChatRequest = {
    question,
    conversation_id: conversationId,
  };

  const response =
    await api.post<ChatResponse>(
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
  conversationId: number | undefined,
  onChunk: (chunk: string) => void,
  onComplete?: (
    sources: ChatResponse["sources"],
    conversationId?: number
  ) => void
): Promise<void> {

  const response = await fetch(
    "http://127.0.0.1:8000/chat/stream",
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
      },

      body: JSON.stringify({
        question,
        conversation_id: conversationId,
      }),
    }
  );


  // =====================================================
  // HTTP Error
  // =====================================================

  if (!response.ok) {

    throw new Error(
      `Streaming request failed: ${response.status}`
    );

  }


  // =====================================================
  // Streaming Body
  // =====================================================

  if (!response.body) {

    throw new Error(
      "No response body received from server."
    );

  }


  const reader =
    response.body.getReader();

  const decoder =
    new TextDecoder();

  let buffer = "";


  // =====================================================
  // Process SSE Event
  // =====================================================

  const processEvent = (
    event: string
  ) => {

    const line =
      event
        .split("\n")
        .find((line) =>
          line.startsWith("data:")
        );


    if (!line) {
      return;
    }


    const data =
      line
        .replace(/^data:\s*/, "")
        .trim();


    if (!data) {
      return;
    }


    // ===================================================
    // Parse JSON
    // ===================================================

    let parsed: StreamEvent;

    try {

      parsed =
        JSON.parse(data) as StreamEvent;

    } catch (error) {

      console.error(
        "Failed to parse SSE event:",
        data,
        error
      );

      return;

    }


    // ===================================================
    // Token Event
    // ===================================================

    if (
      parsed.type === "token" &&
      typeof parsed.text === "string"
    ) {

      onChunk(
        parsed.text
      );

      return;

    }


    // ===================================================
    // Done Event
    // ===================================================

    if (
      parsed.type === "done"
    ) {

      if (
        onComplete &&
        Array.isArray(parsed.sources)
      ) {

        onComplete(
          parsed.sources,
          parsed.conversation_id
        );

      }

      return;

    }


    // ===================================================
    // Error Event
    // ===================================================

    if (
      parsed.type === "error"
    ) {

      throw new Error(
        parsed.message ||
        "Streaming request failed."
      );

    }

  };


  // =====================================================
  // Read Stream
  // =====================================================

  try {

    while (true) {

      const {
        done,
        value,
      } = await reader.read();


      if (done) {
        break;
      }


      // =================================================
      // Decode Incoming Bytes
      // =================================================

      buffer += decoder.decode(
        value,
        {
          stream: true,
        }
      );


      // =================================================
      // Split SSE Events
      // =================================================

      const events =
        buffer.split("\n\n");


      // Keep incomplete event
      buffer =
        events.pop() || "";


      // =================================================
      // Process Complete Events
      // =================================================

      for (
        const event of events
      ) {

        if (!event.trim()) {
          continue;
        }

        processEvent(
          event
        );

      }

    }


    // ===================================================
    // Flush TextDecoder
    // ===================================================

    buffer += decoder.decode();


    // ===================================================
    // Process Final Event
    // ===================================================

    if (
      buffer.trim()
    ) {

      processEvent(
        buffer
      );

    }

  } finally {

    reader.releaseLock();

  }

}