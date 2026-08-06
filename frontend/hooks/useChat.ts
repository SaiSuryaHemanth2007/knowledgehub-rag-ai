"use client";

import { useState } from "react";
import { askQuestion } from "@/services/chat";
import { ChatResponse } from "@/types/chat";

export function useChat() {
  const [loading, setLoading] = useState(false);

  const [response, setResponse] =
    useState<ChatResponse | null>(null);

  const [error, setError] =
    useState<string | null>(null);

  async function sendMessage(question: string) {
    try {
      setLoading(true);
      setError(null);

      const result = await askQuestion(question);

      setResponse(result);
    } catch {
      setError("Failed to contact server.");
    } finally {
      setLoading(false);
    }
  }

  return {
    loading,
    response,
    error,
    sendMessage,
  };
}